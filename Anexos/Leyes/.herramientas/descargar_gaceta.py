#!/usr/bin/env python3
"""Descargador reanudable de la Gaceta Oficial de Cuba.

- Persiste todo dentro de la carpeta del proyecto (sobrevive reinicios del entorno).
- Omite archivos ya descargados y válidos; nunca descarga dos veces la misma URL.
- Sesión HTTP nueva tras cada error de red (evita conexiones muertas en el pool).
- Ritmo suave (2 conexiones + pausa) para no disparar el límite de ráfaga del servidor.
"""
import csv, json, os, shutil, subprocess, threading, time
from pathlib import Path
import requests

ROOT = Path('/home/thony70807/Proyectos/ICD Automotive Market Project/Anexos/Leyes')
HERE = ROOT / '.herramientas'
CATALOG = ROOT / 'gaceta_catalog.json'
ESTADO = ROOT / 'estado_descarga.json'
LOG = ROOT / 'descarga.log'
REPORTE = ROOT / 'reporte_progreso.log'
FALTANTES = ROOT / 'faltantes.csv'
INDICE = ROOT / 'indice_ediciones.csv'
NORMAS = ROOT / 'indice_normas.csv'
VERIF = ROOT / 'verificacion_final.txt'

_print_lock = threading.Lock()
_local = threading.local()


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with _print_lock:
        print(line, flush=True)
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


def report(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with _print_lock:
        with open(REPORTE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


def session():
    s = getattr(_local, 's', None)
    if s is None:
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
            'Accept': 'application/pdf,application/octet-stream,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
        })
        _local.s = s
    return s


def reset_session():
    s = getattr(_local, 's', None)
    if s is None:
        return
    try:
        s.close()
    except Exception:
        pass
    try:
        del _local.s
    except Exception:
        pass


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


def build_items():
    cat = json.load(open(CATALOG, encoding='utf-8'))
    items = []
    for r in cat:
        base = Path(str(r.get('year'))) / _tipo_slug(r.get('type', ''))
        if r.get('ext') == 'rar':
            base = base / '_originales'
        rel = base / Path(r['file_name']).name
        items.append({
            'year': r.get('year'), 'number': r.get('number'), 'type': r.get('type'),
            'date': r.get('date'), 'node': r.get('node'), 'file_url': r.get('file_url'),
            'file_name': r.get('file_name'), 'ext': r.get('ext', ''),
            'norms': r.get('norms', []), 'local_path': str(ROOT / rel),
            'status': 'pendiente', 'bytes': 0,
        })
    return items


def _tipo_slug(t):
    return {
        'Ordinaria': 'Ordinaria', 'Extraordinaria': 'Extraordinaria',
        'Extraordinaria Especial': 'Extraordinaria-Especial',
        'Edición Especial': 'Edicion-Especial',
        'Ordinaria Especial': 'Ordinaria-Especial', 'Exclusiva': 'Exclusiva',
    }.get(t, 'Otros')


def download(item):
    path = Path(item['local_path'])
    ext = item.get('ext', '')
    url = item.get('file_url')
    if not url:
        return 'sin_archivo', 0
    if path.exists() and path.stat().st_size > 64 and magic_ok(path, ext):
        return 'existente', path.stat().st_size
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_name(path.name + '.part')
    last_err = ''
    for attempt in range(6):
        try:
            headers = {}
            resume = part.exists() and part.stat().st_size > 0
            if resume:
                headers['Range'] = f'bytes={part.stat().st_size}-'
            with session().get(url, headers=headers, stream=True, timeout=(20, 120), allow_redirects=True) as r:
                if r.status_code == 416 and resume:
                    part.replace(path)
                    return 'ok', path.stat().st_size
                if r.status_code == 404:
                    log(f'ERROR 404 {path.name} <- {url}')
                    return 'error_404', 0
                if r.status_code not in (200, 206):
                    raise RuntimeError(f'HTTP {r.status_code}')
                if resume and r.status_code == 200:
                    part.unlink(missing_ok=True)
                    resume = False
                expected = None
                if r.headers.get('Content-Length'):
                    try:
                        expected = (part.stat().st_size if resume else 0) + int(r.headers['Content-Length'])
                    except Exception:
                        pass
                with open(part, 'ab' if resume else 'wb') as f:
                    for chunk in r.iter_content(1024 * 256):
                        if chunk:
                            f.write(chunk)
                size = part.stat().st_size
                if expected is not None and size != expected:
                    raise RuntimeError(f'tamaño incompleto {size}/{expected}')
                if size < 64 or not magic_ok(part, ext):
                    part.unlink(missing_ok=True)
                    raise RuntimeError('archivo inválido')
                part.replace(path)
                return 'ok', path.stat().st_size
        except Exception as e:
            last_err = str(e)
            reset_session()
            if '404' in last_err:
                log(f'ERROR 404 {path.name} <- {url}')
                return 'error_404', 0
            if attempt < 5:
                log(f'Reintento {attempt+1}/5 {path.name}: {last_err[:100]}')
            time.sleep(min(45, 2.5 ** attempt))
    log(f'ERROR DEFINITIVO {path.name} <- {url}: {last_err[:120]}')
    return f'error: {last_err[:110]}', 0


def write_state(items, started, errors, done):
    total = len(items)
    byt = sum(x['bytes'] for x in items)
    elapsed = max(1, time.time() - started)
    st = {
        'inicio': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(started)),
        'actualizado': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total': total, 'procesados': done,
        'ok': sum(1 for x in items if x['status'] in ('ok', 'existente', 'copia')),
        'errores': errors, 'bytes': byt, 'GB': round(byt / 1073741824, 3),
        'velocidad_KBps': round(byt / 1024 / elapsed, 1),
        'pendientes': total - done,
    }
    tmp = ESTADO.with_suffix('.tmp')
    json.dump(st, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tmp.replace(ESTADO)
    return st


def write_aux(items):
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
            w.writerow(['anio', 'numero', 'tipo', 'fecha', 'edicion_url', 'archivo_url', 'ruta_local', 'bytes', 'estado', 'normas'])
            for x in items:
                w.writerow([x['year'], x['number'], x['type'], x['date'], x['node'], x['file_url'],
                            x['local_path'], x['bytes'], x['status'], len(x.get('norms', []))])
        INDICE.with_suffix('.tmp').replace(INDICE)
        with open(NORMAS.with_suffix('.tmp'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['anio', 'numero', 'tipo', 'fecha', 'norma', 'url'])
            for x in items:
                for n in x.get('norms', []):
                    w.writerow([x['year'], x['number'], x['type'], x['date'], n.get('title', ''), n.get('url', '')])
        NORMAS.with_suffix('.tmp').replace(NORMAS)
    except Exception as e:
        log(f'No se pudieron escribir indices: {e}')


def extract_rars():
    log('Extrayendo RAR')
    ok = errs = 0
    for rar in sorted(ROOT.rglob('*.rar')):
        dest = rar.parent.parent if rar.parent.name == '_originales' else rar.parent
        try:
            names = subprocess.run(['unrar', 'lb', str(rar)], capture_output=True, text=True, timeout=30).stdout.splitlines()
            names = [n for n in names if n.strip() and not n.endswith('/')]
            if not names:
                continue
            if all((dest / n).exists() for n in names):
                continue
            subprocess.run(['unrar', 'x', '-o+', '-inul', str(rar), str(dest) + os.sep],
                           check=True, timeout=120, capture_output=True)
            ok += 1
        except Exception as e:
            errs += 1
            log(f'ERROR extraccion {rar.name}: {e}')
    log(f'Fin extraccion: ok={ok} errores={errs}')


def verify(items):
    cat = json.load(open(CATALOG, encoding='utf-8'))
    exp_pdf = sum(1 for x in cat if x.get('ext') == 'pdf')
    exp_rar = sum(1 for x in cat if x.get('ext') == 'rar')
    act_pdf = len(list(ROOT.rglob('*.pdf')))
    act_rar = len(list(ROOT.rglob('*.rar')))
    falt = list(csv.DictReader(open(FALTANTES, encoding='utf-8'))) if FALTANTES.exists() else []
    lines = [f'Ediciones en catalogo: {len(cat)}',
             f'PDF esperados/descargados: {exp_pdf}/{act_pdf}',
             f'RAR esperados/descargados: {exp_rar}/{act_rar}',
             f'Faltantes registrados: {len(falt)}']
    for f in falt[:20]:
        lines.append(f"  {f['anio']} {f['numero']} {f['tipo']}: {f['estado']}")
    VERIF.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    log('VERIFICACION:\n' + '\n'.join(lines))


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    items = build_items()
    started = time.time()
    log(f'Inicio: {len(items)} ediciones, 2 conexiones')
    lock = threading.Lock()
    seen_urls = {}
    done = errors = 0
    last_report = time.time()

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def work(it):
        url = it.get('file_url') or ''
        target = Path(it['local_path'])
        with lock:
            fuente = seen_urls.get(url)
        if fuente and fuente != target and not (target.exists() and target.stat().st_size > 64 and magic_ok(target, it.get('ext', ''))):
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fuente, target)
                st, size = 'copia', target.stat().st_size
                log(f'DUPLICADO EVITADO {target.name} <- {fuente.name}')
            except Exception as e:
                st, size = f'error copia: {str(e)[:100]}', 0
        else:
            try:
                st, size = download(it)
            except Exception as e:
                st, size = f'error: {str(e)[:110]}', 0
                log(f'ERROR NO CONTROLADO {target.name}: {e}')
        with lock:
            it['status'], it['bytes'] = st, size
            if st in ('ok', 'existente', 'copia') and url and target.exists() and magic_ok(target, it.get('ext', '')):
                seen_urls.setdefault(url, target)
        return st

    try:
        with ThreadPoolExecutor(max_workers=2) as ex:
            futs = [ex.submit(work, it) for it in items]
            for fut in as_completed(futs):
                st = fut.result()
                time.sleep(0.4 if st in ('ok', 'existente', 'copia', 'sin_archivo') else 2.0)
                with lock:
                    done += 1
                    if str(st).startswith('error'):
                        errors += 1
                    n = done
                if n % 20 == 0 or n == len(items):
                    write_aux(items)
                    stt = write_state(items, started, errors, n)
                    log(f"Progreso {n}/{len(items)} | OK {stt['ok']} | errores {errors} | {stt['GB']} GB | {stt['velocidad_KBps']} KB/s")
                if time.time() - last_report >= 60:
                    last_report = time.time()
                    s = write_state(items, started, errors, n)
                    report(f"{n}/{len(items)} ({100*n/len(items):.1f}%) | {s['GB']} GB | {errors} errores | {s['pendientes']} pendientes")
    finally:
        write_aux(items)
        write_state(items, started, errors, done)
        log(f'Fin: {done} procesados, {errors} errores')

    # Segunda pasada solo para los fallos (sin tocar los ya descargados)
    pendientes = [x for x in items if str(x['status']).startswith('error') or x['status'] == 'sin_archivo']
    if pendientes:
        log(f'Segunda pasada: {len(pendientes)} archivos')
        for it in pendientes:
            st, size = download(it)
            it['status'], it['bytes'] = st, size
            time.sleep(1.0)
        write_aux(items)
        write_state(items, started, sum(1 for x in items if str(x['status']).startswith('error')), len(items))

    extract_rars()
    verify(items)
    report(f'DESCARGA Y VERIFICACION TERMINADAS: {sum(1 for x in items if x["status"] in ("ok","existente","copia"))}/{len(items)} OK')


if __name__ == '__main__':
    main()
