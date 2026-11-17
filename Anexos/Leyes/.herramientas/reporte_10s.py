#!/usr/bin/env python3
"""Reporte de progreso de la descarga actualizado cada 10 segundos."""
import json, os, time
from pathlib import Path

ROOT = Path('/home/thony70807/Proyectos/ICD Automotive Market Project/Anexos/Leyes')
HERE = ROOT / '.herramientas'
ESTADO = ROOT / 'estado_descarga.json'
LOG = ROOT / 'descarga.log'
PIDFILE = HERE / 'descargador.pid'
TXT = ROOT / 'progreso_10s.txt'
JSON = ROOT / 'progreso_10s.json'


def leer():
    try:
        return json.loads(ESTADO.read_text(encoding='utf-8'))
    except Exception:
        return {}


def actividad():
    try:
        lineas = LOG.read_text(encoding='utf-8', errors='replace').splitlines()[-200:]
        for ln in reversed(lineas):
            if '-> ok' in ln or 'Progreso' in ln:
                return ln[11:] if len(ln) > 11 else ln
    except Exception:
        pass
    return ''


def main():
    pid = None
    try:
        pid = int(PIDFILE.read_text().strip())
    except Exception:
        pass
    while True:
        s = leer()
        total = s.get('total', 0)
        proc = s.get('procesados', 0)
        pct = 100 * proc / total if total else 0
        gb = s.get('GB', 0)
        vel = s.get('velocidad_KBps', 0)
        pend = s.get('pendientes', 0)
        err = s.get('errores', 0)
        lineas = [
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Descarga Gaceta Oficial",
            f"  Progreso: {proc}/{total} ({pct:.1f}%)",
            f"  Descargado: {gb} GB | Velocidad media: {vel} KB/s",
            f"  Errores: {err} | Pendientes: {pend}",
            f"  Última actividad: {actividad()[:120]}",
            f"  Archivo: {ROOT / 'estado_descarga.json'}",
        ]
        TXT.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
        JSON.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding='utf-8')
        if pid and not os.path.exists(f'/proc/{pid}'):
            TXT.write_text('\n'.join(lineas + ['  PROCESO TERMINADO']) + '\n', encoding='utf-8')
            break
        time.sleep(10)


if __name__ == '__main__':
    main()
