#!/usr/bin/env python3
"""Reporte de progreso actualizado cada 10 segundos.

Escribe progreso_10s.txt (legible) y progreso_10s.json (datos).
Se ejecuta hasta que lo maten; no termina aunque el descargador esté en espera.
"""
import json, subprocess, time
from pathlib import Path

ROOT = Path('/home/thony70807/Proyectos/ICD Automotive Market Project/Anexos/Leyes')
ESTADO = ROOT / 'estado_descarga.json'
VIGILANTE = ROOT / 'vigilante_estado.txt'
TXT = ROOT / 'progreso_10s.txt'
JSON = ROOT / 'progreso_10s.json'
LOG = ROOT / 'descarga.log'


def leer_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def actividad():
    try:
        lineas = LOG.read_text(encoding='utf-8', errors='replace').splitlines()[-300:]
        for ln in reversed(lineas):
            if 'Progreso' in ln or 'FALLO' in ln or '404' in ln:
                return ln[11:].strip() if len(ln) > 11 else ln
    except Exception:
        pass
    return 'sin actividad reciente'


def descargador_activo():
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():
            continue
        try:
            partes = (p / 'cmdline').read_bytes().rstrip(b'\0').split(b'\0')
        except Exception:
            continue
        if len(partes) >= 2 and b'python' in partes[0] and \
                any(a.endswith(b'descargar_gaceta.py') for a in partes[1:]):
            return True
    return False


def main():
    while True:
        s = leer_json(ESTADO)
        total = s.get('total', 4748)
        proc = s.get('procesados', 0)
        pct = 100 * proc / total if total else 0
        ses = s.get('sesion', {})
        lineas = [
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Descarga Gaceta Oficial de Cuba",
            f"  Progreso total: {proc}/{total} ({pct:.1f}%)",
            f"  Descargadas validas: {s.get('ok', 0)} | Pendientes: {s.get('pendientes', 0)}",
            f"  Fallidas definitivas: {s.get('errores', 0)} | Sin archivo: {s.get('sin_archivo', 0)}",
            f"  En disco: {s.get('GB', 0)} GB | Esta sesion: {ses.get('descargados', 0)} archivos, {ses.get('GB', 0)} GB",
            f"  Velocidad: {s.get('velocidad_KBps', 0)} KB/s | Actualizado: {s.get('actualizado', '?')}",
            f"  Descargador: {'ACTIVO' if descargador_activo() else 'en espera'}",
        ]
        try:
            lineas.append('  Vigilante: ' + VIGILANTE.read_text(encoding='utf-8').strip())
        except Exception:
            lineas.append('  Vigilante: sin estado')
        lineas.append(f"  Ultima actividad: {actividad()[:160]}")
        TXT.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
        JSON.write_text(json.dumps({'estado': s, 'descargador_activo': descargador_activo(),
                                    'reporte': time.strftime('%Y-%m-%d %H:%M:%S')},
                                   ensure_ascii=False, indent=1), encoding='utf-8')
        time.sleep(10)


if __name__ == '__main__':
    main()
