#!/usr/bin/env python3
"""Descubre canales de Telegram referentes al mercado cubano hasta 100.

Fuentes: tgden.com (búsquedas por término y tipo). Cada candidato se valida
con la vista pública t.me/s/<usuario> para obtener título, miembros, mensajes
y una muestra. Salida: Data/integraciones/telegram/canales_referencia.jsonl
"""

from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from curl_cffi import requests as creq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Data/integraciones/telegram"
SALIDA = OUT / "canales_referencia.jsonl"
OBJETIVO = 100

CONSULTAS = [
    ("cuba", "channel"), ("cuba", "chat"),
    ("habana", "channel"), ("habana", "chat"),
    ("revolico", "channel"), ("revolico", "chat"),
    ("carros cuba", "channel"), ("carros cuba", "chat"),
    ("autos cuba", "channel"), ("autos cuba", "chat"),
    ("venta cuba", "channel"), ("venta cuba", "chat"),
    ("mercado cuba", "channel"), ("mercado cuba", "chat"),
    ("cubano", "channel"), ("compra venta cuba", "chat"),
]

RELEVANTE = re.compile(
    r"cuba|habana|revolico|carro|auto|venta|mercado|compra|tasa|eltoque|"
    r"cuban|cubano|isla|emprend", re.I
)
AUTO = re.compile(r"carro|auto|coche|camioneta|veh[ií]culo|moto|repuesto", re.I)


def get(url: str, params: dict | None = None) -> str:
    r = creq.get(url, params=params, impersonate="chrome", timeout=25,
                 headers={"Accept-Language": "es-ES,es;q=0.9"})
    r.raise_for_status()
    return r.text


def candidatos() -> list[str]:
    vistos: set[str] = set()
    for q, tipo in CONSULTAS:
        try:
            html = get("https://tgden.com/en/search", {"q": q, "type": tipo})
        except Exception as exc:
            print(f"[busqueda] {q}/{tipo}: {exc}", flush=True)
            continue
        s = BeautifulSoup(html, "lxml")
        encontrados = []
        for a in s.select(f'a[href^="/en/{tipo}/"]'):
            user = a.get("href", "").rsplit("/", 1)[-1]
            if not user or "-" in user or len(user) > 40:
                continue
            if user not in vistos:
                vistos.add(user)
                encontrados.append(user)
        print(f"[busqueda] {q}/{tipo}: {len(encontrados)} nuevos", flush=True)
        time.sleep(0.3)
    return sorted(vistos)


def validar(usuario: str) -> dict:
    fila = {
        "usuario": usuario,
        "url": f"https://t.me/{usuario}",
        "validado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    try:
        html = get(f"https://t.me/s/{usuario}")
        s = BeautifulSoup(html, "lxml")
        titulo = s.select_one(".tgme_page_title")
        extra = s.select_one(".tgme_page_extra")
        mensajes = s.select("div.tgme_widget_message")
        textos = [
            m.select_one(".tgme_widget_message_text").get_text(" ", strip=True)
            for m in mensajes if m.select_one(".tgme_widget_message_text")
        ]
        fila.update({
            "titulo": titulo.get_text(" ", strip=True) if titulo else "",
            "audiencia": extra.get_text(" ", strip=True) if extra else "",
            "mensajes_publicos": len(mensajes),
            "muestra": (textos[0][:200] if textos else ""),
            "es_automotriz": bool(AUTO.search(" ".join(textos) + " " + fila["titulo"])),
            "es_relevante": bool(RELEVANTE.search(fila["titulo"] + " " + " ".join(textos))),
            "publico": len(mensajes) > 0,
        })
    except Exception as exc:
        fila.update({"titulo": "", "audiencia": "", "mensajes_publicos": 0,
                     "muestra": "", "es_automotriz": False, "es_relevante": False,
                     "publico": False, "error": str(exc)[:160]})
    return fila


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    usuarios = candidatos()
    print(f"Candidatos totales: {len(usuarios)}", flush=True)

    resultados: list[dict] = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futuros = {ex.submit(validar, u): u for u in usuarios}
        for i, fut in enumerate(as_completed(futuros), 1):
            fila = fut.result()
            resultados.append(fila)
            if i % 25 == 0:
                print(f"  validados {i}/{len(usuarios)}", flush=True)

    utiles = [f for f in resultados if f["publico"] or f["es_relevante"]]
    utiles.sort(key=lambda f: (f["es_automotriz"], f["mensajes_publicos"]), reverse=True)
    resultados = utiles[:max(OBJETIVO, len(utiles))]

    with SALIDA.open("w", encoding="utf-8") as fh:
        for fila in resultados:
            fh.write(json.dumps(fila, ensure_ascii=False) + "\n")

    print(f"Referencias guardadas: {len(resultados)} (objetivo {OBJETIVO})", flush=True)
    print(f"Automotrices: {sum(1 for f in resultados if f['es_automotriz'])}", flush=True)
    print(f"Con mensajes públicos: {sum(1 for f in resultados if f['publico'])}", flush=True)


if __name__ == "__main__":
    main()
