#!/usr/bin/env python3
"""Pipeline de 3 etapas con colas persistentes para Revolico.

Etapas (se ejecutan en paralelo):
  1. Descubrimiento: recorre página por página y guarda el enlace de cada anuncio
     en `url_queue`.
  2. Descarga: workers toman URLs pendientes, descargan la página con curl_cffi
     y guardan TODOS los datos parseados en `download_queue`.
  3. Procesamiento: workers clasifican cada anuncio (4+ ruedas + datos necesarios)
     y dejan la decisión en `process_queue`.

Cada 25 anuncios **procesados** (aceptados o rechazados) se hace un commit por
lotes en la BD principal: aceptados -> `anuncios` + `autos` (+ imágenes y teléfonos),
rechazados -> `revision`. Nada se descarta sin registro.

Uso:
  python scrape_revolico_pipeline.py --max-pages 5 --downloaders 8 --processors 4
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import scrape_revolico as sr
import limpiar_revolico as lr

OUT = sr.OUT
MAIN_DB = sr.DB
QUEUE_DB = OUT / "pipeline.sqlite"
BATCH = 25


def conn_queue() -> sqlite3.Connection:
    c = sqlite3.connect(QUEUE_DB, timeout=30, check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=30000")
    return c


def init_queues() -> None:
    c = conn_queue()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS url_queue (
            path TEXT PRIMARY KEY, status TEXT DEFAULT 'pending',
            discovered_at TEXT, error TEXT
        );
        CREATE TABLE IF NOT EXISTS download_queue (
            id TEXT PRIMARY KEY, payload TEXT, status TEXT DEFAULT 'pending',
            downloaded_at TEXT, error TEXT
        );
        CREATE TABLE IF NOT EXISTS process_queue (
            id TEXT PRIMARY KEY, decision TEXT, motivo TEXT,
            status TEXT DEFAULT 'pending', processed_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_url_status ON url_queue(status);
        CREATE INDEX IF NOT EXISTS idx_dl_status ON download_queue(status);
        CREATE INDEX IF NOT EXISTS idx_pr_status ON process_queue(status);
        """
    )
    c.commit()
    c.close()


def conn_main() -> sqlite3.Connection:
    c = sqlite3.connect(MAIN_DB, timeout=60, check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=60000")
    return c


AD_COLS = [
    "id", "url", "title", "short_description", "description", "price", "currency",
    "status", "seller_name", "contact_info", "updated_on_by_user", "updated_on_to_order",
    "is_promoted", "is_sold", "views", "images_count", "province_id", "province_name",
    "municipality_id", "municipality_name", "category_id", "category_name",
    "subcategory_id", "subcategory_name", "meta_json", "ad_json", "apollo_full",
    "text", "raw_html", "scraped_at",
]
AUDIT_COLS = ["es_auto", "motivo_exclusion", "pagina_revisada", "datos_necesarios"]


def ensure_main_tables(c: sqlite3.Connection) -> None:
    c.execute(
        """CREATE TABLE IF NOT EXISTS revision (
            id TEXT PRIMARY KEY, url TEXT, categoria TEXT, motivo TEXT, revisado_utc TEXT)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS autos AS SELECT
            id,url,title,short_description,description,price,currency,status,
            province_name,municipality_name,category_id,subcategory_id,
            images_count,scraped_at,raw_html,text FROM anuncios WHERE 0"""
    )
    c.commit()


STOP = threading.Event()
lock_commit = threading.Lock()
processed_counter = {"n": 0}


def discover(max_pages: int) -> None:
    """Página por página, anuncio por anuncio: guarda el enlace en la cola."""
    c = conn_queue()
    written = 0
    for page in range(max_pages, 0, -1):
        if STOP.is_set():
            break
        html = sr.get_html(sr.SEARCH.format(page=page))
        st = sr.state_from(html)
        found = []
        for k, v in st.items():
            if k.startswith("AdType:") and isinstance(v, dict) and v.get("permalink"):
                found.append(v["permalink"])
        found = list(dict.fromkeys(found))
        now = sr.now()
        for path in found:
            c.execute(
                "INSERT OR IGNORE INTO url_queue (path,status,discovered_at) VALUES (?,?,?)",
                (path, "pending", now),
            )
            written += 1
        c.commit()
        print(f"[descubridor] página {page}: {len(found)} enlaces (cola {written})", flush=True)
        time.sleep(0.35)
    c.close()


def download_loop() -> None:
    c = conn_queue()
    while not STOP.is_set():
        row = c.execute("SELECT path FROM url_queue WHERE status='pending' LIMIT 1").fetchone()
        if not row:
            time.sleep(0.5)
            continue
        path = row[0]
        c.execute("UPDATE url_queue SET status='downloading' WHERE path=?", (path,))
        c.commit()
        try:
            d = sr.fetch_one(path)
            if d:
                payload = dict(d)
                payload["meta_json"] = json.dumps(d.get("meta", {}), ensure_ascii=False)
                payload["scraped_at"] = sr.now()
                c.execute(
                    "INSERT OR IGNORE INTO download_queue (id,payload,status,downloaded_at) VALUES (?,?,?,?)",
                    (str(d["id"]), json.dumps(payload, ensure_ascii=False), "pending", sr.now()),
                )
                c.execute("UPDATE url_queue SET status='done' WHERE path=?", (path,))
            else:
                c.execute("UPDATE url_queue SET status='failed', error='fetch_one=None' WHERE path=?", (path,))
        except Exception as e:
            c.execute("UPDATE url_queue SET status='failed', error=? WHERE path=?", (str(e)[:300], path))
        c.commit()
    c.close()


def commit_batch() -> None:
    """Vuelca los procesados pendientes a la BD principal."""
    q = conn_queue()
    m = conn_main()
    ensure_main_tables(m)
    rows = q.execute(
        "SELECT id,decision,motivo FROM process_queue WHERE status='pending' LIMIT ?", (BATCH,)
    ).fetchall()
    if not rows:
        q.close(); m.close(); return

    accepted = rejected = 0
    now = sr.now()
    for pid, decision, motivo in rows:
        dl = q.execute("SELECT payload FROM download_queue WHERE id=?", (pid,)).fetchone()
        if not dl:
            continue
        d = json.loads(dl[0])
        if decision == "accept":
            values = []
            for col in AD_COLS:
                if col == "meta_json":
                    values.append(d.get("meta_json", "{}"))
                else:
                    values.append(d.get(col, ""))
            values += [1, motivo or "", 1, 1]  # es_auto, motivo, pagina_revisada, datos_necesarios
            all_cols = AD_COLS + AUDIT_COLS
            m.execute(
                f"INSERT OR IGNORE INTO anuncios ({','.join(all_cols)}) VALUES ({','.join('?'*len(all_cols))})",
                values,
            )
            auto_cols = [c for c in all_cols if c in
                         {"id","url","title","short_description","description","price","currency",
                          "status","province_name","municipality_name","category_id","subcategory_id",
                          "images_count","scraped_at","raw_html","text"}]
            m.execute(
                f"INSERT OR IGNORE INTO autos ({','.join(auto_cols)}) VALUES ({','.join('?'*len(auto_cols))})",
                [values[all_cols.index(c)] for c in auto_cols],
            )
            for im in d.get("images", []):
                m.execute(
                    "INSERT OR IGNORE INTO imagenes (ad_id,image_id,gcs_key,url) VALUES (?,?,?,?)",
                    (pid, str(im.get("id", "")), im.get("key", ""), im.get("url", "")),
                )
            for ph in d.get("phones", []):
                m.execute(
                    "INSERT OR IGNORE INTO telefonos (ad_id,number,prefix,type,is_whatsapp) VALUES (?,?,?,?,?)",
                    (pid, str(ph.get("number", "")), ph.get("prefix", ""), ph.get("type", ""),
                     int(ph.get("is_whatsapp", 0))),
                )
            accepted += 1
        else:
            m.execute(
                "INSERT OR IGNORE INTO revision VALUES (?,?,?,?,?)",
                (pid, d.get("url", ""), lr.categoria(d.get("text", "")), motivo or "", now),
            )
            rejected += 1
        q.execute("UPDATE process_queue SET status='committed' WHERE id=?", (pid,))
    m.commit()
    q.commit()
    q.close(); m.close()
    print(f"[commit] lote de {len(rows)}: {accepted} aceptados, {rejected} rechazados", flush=True)


def process_loop() -> None:
    q = conn_queue()
    while not STOP.is_set():
        row = q.execute("SELECT id,payload FROM download_queue WHERE status='pending' LIMIT 1").fetchone()
        if not row:
            time.sleep(0.5)
            continue
        pid, payload = row
        q.execute("UPDATE download_queue SET status='processing' WHERE id=?", (pid,))
        q.commit()
        try:
            d = json.loads(payload)
            guardar, motivo, pagina_ok, datos_ok = lr.clasificar(d)
            if guardar and pagina_ok and datos_ok:
                decision, motivo_final = "accept", ""
            else:
                decision = "reject"
                motivo_final = motivo or "sin motivo"
                if not pagina_ok:
                    motivo_final += "; página sin datos suficientes"
            q.execute(
                "INSERT OR REPLACE INTO process_queue (id,decision,motivo,status,processed_at) VALUES (?,?,?,?,?)",
                (pid, decision, motivo_final, "pending", sr.now()),
            )
            q.execute("UPDATE download_queue SET status='processed' WHERE id=?", (pid,))
            q.commit()
            with lock_commit:
                processed_counter["n"] += 1
                if processed_counter["n"] % BATCH == 0:
                    commit_batch()
        except Exception as e:
            q.execute(
                "INSERT OR REPLACE INTO process_queue (id,decision,motivo,status,processed_at) VALUES (?,?,?,?,?)",
                (pid, "reject", f"error de procesamiento: {e}", "pending", sr.now()),
            )
            q.execute("UPDATE download_queue SET status='failed' WHERE id=?", (pid,))
            q.commit()
    q.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-pages", type=int, default=100)
    ap.add_argument("--downloaders", type=int, default=8)
    ap.add_argument("--processors", type=int, default=4)
    ap.add_argument("--batch-size", type=int, default=25)
    args = ap.parse_args()
    global BATCH
    BATCH = args.batch_size

    OUT.mkdir(parents=True, exist_ok=True)
    init_queues()
    m = conn_main()
    ensure_main_tables(m)
    m.close()

    threads = []
    t = threading.Thread(target=discover, args=(args.max_pages,), daemon=True)
    t.start(); threads.append(t)
    for _ in range(args.downloaders):
        t = threading.Thread(target=download_loop, daemon=True); t.start(); threads.append(t)
    for _ in range(args.processors):
        t = threading.Thread(target=process_loop, daemon=True); t.start(); threads.append(t)

    try:
        while True:
            time.sleep(2)
            q = conn_queue()
            pending = q.execute(
                """SELECT
                   (SELECT count(*) FROM url_queue WHERE status IN ('pending','downloading')),
                   (SELECT count(*) FROM download_queue WHERE status IN ('pending','processing')),
                   (SELECT count(*) FROM process_queue WHERE status='pending')"""
            ).fetchone()
            q.close()
            if sum(pending) == 0:
                print("Colas vacías; cerrando pipeline.", flush=True)
                break
    except KeyboardInterrupt:
        print("Interrumpido por el usuario", flush=True)
    finally:
        STOP.set()
        commit_batch()
        for t in threads:
            t.join(timeout=5)
    print(f"Procesados en total: {processed_counter['n']}", flush=True)


if __name__ == "__main__":
    main()
