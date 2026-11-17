#!/usr/bin/env python3
"""Aviso de progreso del scraper de Revolico cada 10 minutos.

- Escribe Data/Revolico/progreso.md con el estado actual.
- Envía una notificación de escritorio con notify-send (si está disponible).
- Imprime el resumen en stdout para el journal de systemd.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "Data/Revolico/revolico.sqlite"
QUEUE_DB = ROOT / "Data/Revolico/pipeline.sqlite"
ESTADO = ROOT / "Data/Revolico/estado.json"
PARTES = ROOT / "Data/Revolico/partes"
SALIDA = ROOT / "Data/Revolico/progreso.md"


def count(path: Path, query: str) -> int:
    con = sqlite3.connect(path)
    try:
        return int(con.execute(query).fetchone()[0])
    finally:
        con.close()


def service_state() -> str:
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "revolico-scrape.service"],
            text=True, capture_output=True,
        )
        estado = result.stdout.strip()
        if result.returncode == 0 or estado in {"inactive", "activating", "deactivating", "failed", "unknown"}:
            return estado or "desconocido"
        return "desconocido"
    except Exception:
        return "desconocido"


def main() -> None:
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    anuncios = count(DB, "SELECT count(*) FROM anuncios")
    autos = count(DB, "SELECT count(*) FROM autos")
    revision = count(DB, "SELECT count(*) FROM revision")
    sin_revisar = count(DB, "SELECT count(*) FROM anuncios WHERE pagina_revisada=0")
    ultimo = subprocess.check_output(
        ["python3", "-c", f"import sqlite3;c=sqlite3.connect('{DB}');print(c.execute('select max(scraped_at) from anuncios').fetchone()[0])"],
        text=True,
    ).strip()

    colas = {}
    if QUEUE_DB.exists():
        for tabla in ["url_queue", "download_queue", "process_queue"]:
            colas[tabla] = count(QUEUE_DB, f"SELECT count(*) FROM {tabla} WHERE status IN ('pending','downloading','processing')")

    partes = len(list(PARTES.glob("revolico.sqlite.part*"))) if PARTES.exists() else 0
    estado_ts = "—"
    if ESTADO.exists():
        try:
            estado_ts = json.loads(ESTADO.read_text(encoding="utf-8")).get("actualizado_utc", "—")
        except Exception:
            pass

    lineas = [
        f"# Progreso Revolico — {ahora}",
        "",
        f"- Servicio scrapeo: **{service_state()}**",
        f"- Anuncios: **{anuncios:,}** | Autos: **{autos}** | Revisiones: **{revision:,}**",
        f"- Sin revisar: **{sin_revisar:,}**",
        f"- Última captura: {ultimo}",
        f"- Colas pendientes: " + (", ".join(f"{k}={v}" for k, v in colas.items()) or "sin colas"),
        f"- Partes en repo local: {partes} | estado.json: {estado_ts}",
    ]
    texto = "\n".join(lineas) + "\n"
    SALIDA.write_text(texto, encoding="utf-8")
    print(texto, flush=True)

    if shutil.which("notify-send"):
        resumen = f"Revolico: {anuncios} anuncios | {autos} autos | {sin_revisar} sin revisar | colas {sum(colas.values())}"
        subprocess.run(["notify-send", "-u", "normal", "-t", "10000", "AutoDecide Habana", resumen],
                       check=False, capture_output=True)


if __name__ == "__main__":
    main()
