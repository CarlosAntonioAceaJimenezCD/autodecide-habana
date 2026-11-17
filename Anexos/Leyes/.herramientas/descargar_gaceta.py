#!/usr/bin/env python3
"""Descargador reanudable de la Gaceta Oficial de Cuba.

Reglas:
- Omite todo archivo ya descargado y válido: nunca se vuelve a bajar.
- Una sola intentativa por archivo y por pasada; sin reintentos.
- Los 404 reales se guardan en fallidos.json y no se reintentan.
- Cortacircuitos: si el servidor corta 5 archivos seguidos, aborta la pasada
  SIN marcar esos archivos como fallidos (vuelven a quedar pendientes).
- Una conexión y pausa de 3 s para no disparar el límite de ráfaga del servidor.
"""
import csv, json, os, re, shutil, subprocess, sys, threading, time
from pathlib import Path
import requests

ROOT = Path('/home/thony70807/Proyectos/ICD Automotive Market Project/Anexos/Leyes')
HERE = ROOT / '.herramientas'
CATALOG = ROOT / 'gaceta_catalog.json'
ESTADO = ROOT / 'estado_descarga.json'
LOG = ROOT / 'descarga.log'
REPORTE = ROOT / 'reporte_progreso.log'
FALTANTES = ROOT / 'faltantes.csv'
FALLIDOS = ROOT / 'fallidos.json'
FALLOS_RED = ROOT / 'fallos_red.json'
INDICE = ROOT / 'indice_ediciones.csv'
NORMAS = ROOT / 'indice_normas.csv'
VERIF = ROOT / 'verificacion_final.txt'

PAUSA_OK = 3.0
PAUSA_ERROR = 10.0
MAX_FALLOS_SEGUIDOS = 5

_lock = threading.Lock()


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with _lock:
        print(line, flush=True)
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


def report(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with _lock:
        with open(REPORTE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


def magic_ok(path, ext):
    try:
        with open(path, 'rb') as f:
            head = f.read(2048)
    except Exception:
        return False
    if ext == 'pdf':
        return b'%PDF' in head[:1024]
    if ext == 'rar':
        return head.startswith(b'Rar!')
    return True


def tipo_slug(t):
    return {
        'Ordinaria': 'Ordinaria', 'Extraordinaria': 'Extraordinaria',
        'Extraordinaria Especial': 'Extraordinaria-Especial',
        'Edición Especial': 'Edicion-Especial',
        'Ordinaria Especial': 'Ordinaria-Especial', 'Exclusiva': 'Exclusiva',
    }.get(t, 'Otros')


def cargar_lista(path):
    if path.exists():
        try:
            return set(json.load(open(path, encoding='utf-8')))
        except Exception:
            return set()
    return set()


def build_items():
    cat = json.load(open(CATALOG, encoding='utf-8'))
    fallidos = cargar_lista(FALLIDOS)
    items = []
    for r in cat:
        base = Path(str(r.get('year'))) / tipo_slug(r.get('type', ''))
        if r.get('ext') == 'rar':
            base = base / '_originales'
        name = Path(r['file_name']).name
        path = ROOT / base / name
        if path.exists() and path.stat().st_size > 64 and magic_ok(path, r.get('ext', '')):
            status, size = 'existente', path.stat().st_size
        elif name in fallidos:
            status, size = 'error_permanente', 0
        elif not r.get('file_url'):
            status, size = 'sin_archivo', 0
        else:
            status, size = 'pendiente', 0
        items.append({
            'year': r.get('year'), 'number': r.get('number'), 'type': r.get('type'),
            'date': r.get('date'), 'node': r.get('node'), 'file_url': r.get('file_url'),
            'file_name': name, 'ext': r.get('ext', ''), 'norms': r.get('norms', []),
            'local_path': str(path), 'status': status, 'bytes': size,
        })
    desc = sum(1 for x in items if x['status'] == 'existente')
    fall = sum(1 for x in items if x['status'] == 'error_permanente')
    sina = sum(1 for x in items if x['status'] == 'sin_archivo')
    pend = sum(1 for x in items if x['status'] == 'pendiente')
    log(f'Inventario: {desc} ya descargados, {fall} fallidos omitidos, '
        f'{sina} sin archivo, {pend} pendientes')
    return items


def nueva_sesion():
    s = requests.Session()
    s.headers.update({
        # UA corto: el WAF del servidor corta la conexión con el UA largo de Chrome.
        'User-Agent': 'Mozilla/5.0',
        'Connection': 'close',
        'Accept': 'application/pdf,application/octet-stream,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www.gacetaoficial.gob.cu/es/inicio',
    })
    return s


def clasificar_error(txt):
    t = txt.lower()
    if '404' in t:
        return 'error_404'
    if 'inválido' in t or 'incompleto' in t:
        return 'error_archivo'
    return 'error_red'


def descargar(item, sesion):
    """Una sola intentativa. Devuelve (estado, bytes)."""
    path = Path(item['local_path'])
    ext = item.get('ext', '')
    url = item.get('file_url')
    if path.exists() and path.stat().st_size > 64 and magic_ok(path, ext):
        return 'existente', path.stat().st_size
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_name(path.name + '.part')
    try:
        # Sin Range: el servidor corta algunas peticiones parciales y no hace falta reanudar.
        with sesion.get(url, stream=True, timeout=(20, 120), allow_redirects=True) as r:
            if r.status_code == 404:
                log(f'404 REAL {path.name}')
                return 'error_404', 0
            if r.status_code != 200:
                return clasificar_error(f'HTTP {r.status_code}'), 0
            esperado = None
            if r.headers.get('Content-Length'):
                try:
                    esperado = int(r.headers['Content-Length'])
                except Exception:
                    esperado = None
            with open(part, 'wb') as f:
                for chunk in r.iter_content(1024 * 256):
                    if chunk:
                        f.write(chunk)
            size = part.stat().st_size
            if esperado is not None and size != esperado:
                part.unlink(missing_ok=True)
                return 'error_red', 0
            if size < 64 or not magic_ok(part, ext):
                part.unlink(missing_ok=True)
                return 'error_archivo', 0
            part.replace(path)
            log(f'OK {path.name} {path.stat().st_size} bytes')
            return 'ok', path.stat().st_size
    except Exception as e:
        part.unlink(missing_ok=True)
        msg = str(e)[:110]
        if '404' in msg:
            log(f'404 REAL {path.name}')
            return 'error_404', 0
        return clasificar_error(msg), 0


def escribir_estado(items, inicio, sesion_bytes, sesion_ok, cortado):
    total = len(items)
    cuenta = lambda *ss: sum(1 for x in items if x['status'] in ss)
    ok = cuenta('ok', 'existente', 'copia')
    errores = cuenta('error_permanente', 'error_404', 'error_archivo')
    sin_archivo = cuenta('sin_archivo')
    pendientes = cuenta('pendiente')
    resueltos = total - pendientes
    byt = sum(x['bytes'] for x in items)
    elapsed = max(1, time.time() - inicio)
    st = {
        'inicio': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inicio)),
        'actualizado': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total': total,
        'procesados': resueltos,
        'ok': ok,
        'errores': errores,
        'sin_archivo': sin_archivo,
        'pendientes': pendientes,
        'bytes': byt,
        'GB': round(byt / 1073741824, 3),
        'velocidad_KBps': round(sesion_bytes / 1024 / elapsed, 1),
        'sesion': {'descargados': sesion_ok, 'bytes': sesion_bytes,
                   'GB': round(sesion_bytes / 1073741824, 3)},
        'interrumpido': cortado,
    }
    tmp = ESTADO.with_suffix('.tmp')
    json.dump(st, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tmp.replace(ESTADO)
    return st


def escribir_aux(items):
    try:
        falt = [x for x in items if x['status'] == 'sin_archivo' or str(x['status']).startswith('error')]
        with open(FALTANTES.with_suffix('.tmp'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['anio', 'numero', 'tipo', 'fecha', 'edicion_url', 'archivo_url', 'estado'])
            for x in falt:
                w.writerow([x['year'], x['number'], x['type'], x['date'], x['node'], x['file_url'], x['status']])
        FALTANTES.with_suffix('.tmp').replace(FALTANTES)
        with open(INDICE.with_suffix('.tmp'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['anio', 'numero', 'tipo', 'fecha', 'edicion_url', 'archivo_url',
                        'ruta_local', 'bytes', 'estado', 'normas'])
            for x in items:
                w.writerow([x['year'], x['number'], x['type'], x['date'], x['node'],
                            x['file_url'], x['local_path'], x['bytes'], x['status'],
                            len(x.get('norms', []))])
        INDICE.with_suffix('.tmp').replace(INDICE)
        with open(NORMAS.with_suffix('.tmp'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['anio', 'numero', 'tipo', 'fecha', 'norma', 'url'])
            for x in items:
                for n in x.get('norms', []):
                    w.writerow([x['year'], x['number'], x['type'], x['date'],
                                n.get('title', ''), n.get('url', '')])
        NORMAS.with_suffix('.tmp').replace(NORMAS)
    except Exception as e:
        log(f'No se pudieron escribir indices: {e}')


def extraer_rars():
    rars = sorted(ROOT.rglob('*.rar'))
    if not rars:
        return
    log(f'Extrayendo {len(rars)} RAR')
    ok = errs = 0
    for rar in rars:
        dest = rar.parent.parent if rar.parent.name == '_originales' else rar.parent
        try:
            names = subprocess.run(['unrar', 'lb', str(rar)], capture_output=True,
                                   text=True, timeout=30).stdout.splitlines()
            names = [n for n in names if n.strip() and not n.endswith('/')]
            if not names or all((dest / n).exists() for n in names):
                continue
            subprocess.run(['unrar', 'x', '-o+', '-inul', str(rar), str(dest) + os.sep],
                           check=True, timeout=120, capture_output=True)
            ok += 1
        except Exception as e:
            errs += 1
            log(f'ERROR extraccion {rar.name}: {str(e)[:90]}')
    log(f'Fin extraccion: ok={ok} errores={errs}')


def verificar(items):
    cat = json.load(open(CATALOG, encoding='utf-8'))
    exp_pdf = sum(1 for x in cat if x.get('ext') == 'pdf')
    exp_rar = sum(1 for x in cat if x.get('ext') == 'rar')
    act_pdf = sum(1 for x in items if x.get('ext') == 'pdf' and Path(x['local_path']).exists())
    act_rar = sum(1 for x in items if x.get('ext') == 'rar' and Path(x['local_path']).exists())
    cuenta = lambda *ss: sum(1 for x in items if x['status'] in ss)
    ok = cuenta('ok', 'existente', 'copia')
    fall = cuenta('error_permanente', 'error_404', 'error_archivo')
    pend = cuenta('pendiente')
    sina = cuenta('sin_archivo')
    falt = list(csv.DictReader(open(FALTANTES, encoding='utf-8'))) if FALTANTES.exists() else []
    lines = [
        f'Ediciones en catalogo: {len(cat)}',
        f'Validadas en disco: {ok} (PDF {act_pdf}/{exp_pdf}, RAR {act_rar}/{exp_rar})',
        f'Pendientes: {pend}',
        f'Fallidos definitivos: {fall}',
        f'Sin archivo en el servidor: {sina}',
        f'Registros en faltantes.csv: {len(falt)}',
    ]
    for f in falt[:30]:
        lines.append(f"  {f['anio']} {f['numero']} {f['tipo']}: {f['estado']}")
    VERIF.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    log('VERIFICACION:\n' + '\n'.join(lines))


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    items = build_items()
    inicio = time.time()
    sesion = nueva_sesion()
    sesion_bytes = sesion_ok = hechos = 0
    ultimo_guardado = 0.0
    cola = [x for x in items if x['status'] == 'pendiente']
    log(f'Inicio: {len(cola)} pendientes, 1 conexion, {PAUSA_OK:.0f} s entre archivos')

    seguidos = []
    cortado = False
    for it in cola:
        st, size = descargar(it, sesion)
        it['status'], it['bytes'] = st, size
        hechos += 1
        if st in ('ok', 'copia'):
            sesion_ok += 1
            sesion_bytes += size
        if st == 'error_red':
            seguidos.append(it)
            log(f'FALLO RED {it["file_name"]} ({len(seguidos)}/{MAX_FALLOS_SEGUIDOS} seguidos)')
        else:
            if st.startswith('error') and st != 'error_red':
                log(f'FALLO {it["file_name"]}: {st}')
            seguidos.clear()

        ahora = time.time()
        if hechos % 5 == 0 or ahora - ultimo_guardado >= 10:
            escribir_estado(items, inicio, sesion_bytes, sesion_ok, False)
            ultimo_guardado = ahora
        if hechos % 25 == 0:
            escribir_aux(items)

        if len(seguidos) >= MAX_FALLOS_SEGUIDOS:
            cortado = True
            log(f'CORTACIRCUITOS: {len(seguidos)} fallos de red seguidos. '
                f'Se aborta sin marcar estos archivos como fallidos.')
            for x in seguidos:
                x['status'], x['bytes'] = 'pendiente', 0
            break

        time.sleep(PAUSA_OK if st in ('ok', 'existente', 'copia', 'error_404', 'error_archivo') else PAUSA_ERROR)

    for x in items:
        if x['status'] == 'error_red':
            x['status'], x['bytes'] = 'pendiente', 0

    escribir_aux(items)
    st = escribir_estado(items, inicio, sesion_bytes, sesion_ok, cortado)

    if cortado:
        # Registrar los fallos de red de esta pasada solo como informativos.
        prev = {}
        if FALLOS_RED.exists():
            try:
                prev = json.load(open(FALLOS_RED, encoding='utf-8'))
            except Exception:
                prev = {}
        for x in items:
            if x['file_name'] in {y['file_name'] for y in seguidos}:
                prev[x['file_name']] = prev.get(x['file_name'], 0) + 1
        json.dump(prev, open(FALLOS_RED, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        report(f'DESCARGA INTERRUMPIDA POR EL SERVIDOR: {st["ok"]}/{st["total"]} OK, '
               f'{st["pendientes"]} pendientes. Se reanudara automaticamente.')
        log('Pasada abortada por salud del servidor; los pendientes siguen pendientes.')
        return 2

    # Solo los errores definitivos pasan a fallidos.json
    fallidos = cargar_lista(FALLIDOS)
    for x in items:
        if x['status'] in ('error_404', 'error_archivo'):
            fallidos.add(x['file_name'])
    json.dump(sorted(fallidos), open(FALLIDOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f'Fallidos definitivos acumulados: {len(fallidos)}')

    if st['pendientes'] == 0:
        extraer_rars()
    verificar(items)
    report(f'PASADA TERMINADA: {st["ok"]}/{st["total"]} OK, {st["errores"]} fallidos, '
           f'{st["pendientes"]} pendientes')
    return 0 if st['pendientes'] == 0 else 2


if __name__ == '__main__':
    sys.exit(main())
