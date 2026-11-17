#!/usr/bin/env python3
"""Vigilante de salud del servidor de la Gaceta.

- Sondea PDFs (uno de referencia y uno pendiente real) sin descargarlos completos.
- Solo lanza descargar_gaceta.py cuando hay 2 sondas sanas consecutivas.
- Si el descargador aborta por cortacircuitos, espera con retroceso exponencial
  y vuelve a probar. No marca nada como fallido.
"""
import json, random, subprocess, sys, time
from pathlib import Path
import requests

ROOT = Path('/home/thony70807/Proyectos/ICD Automotive Market Project/Anexos/Leyes')
HERE = ROOT / '.herramientas'
CATALOG = ROOT / 'gaceta_catalog.json'
FALLIDOS = ROOT / 'fallidos.json'
DESCARGADOR = HERE / 'descargar_gaceta.py'
ESTADO_TXT = ROOT / 'vigilante_estado.txt'
LOG = ROOT / 'vigilante.log'

REF = 'https://www.gacetaoficial.gob.cu/sites/default/files/goc-2024-ex10_0.pdf'
UA = 'Mozilla/5.0'


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def estado(msg):
    ESTADO_TXT.write_text(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n", encoding='utf-8')


def tipo_slug(t):
    return {
        'Ordinaria': 'Ordinaria', 'Extraordinaria': 'Extraordinaria',
        'Extraordinaria Especial': 'Extraordinaria-Especial',
        'Edición Especial': 'Edicion-Especial',
        'Ordinaria Especial': 'Ordinaria-Especial', 'Exclusiva': 'Exclusiva',
    }.get(t, 'Otros')


def pendientes_pdf():
    fallidos = set()
    if FALLIDOS.exists():
        try:
            fallidos = set(json.load(open(FALLIDOS, encoding='utf-8')))
        except Exception:
            pass
    out = []
    for r in json.load(open(CATALOG, encoding='utf-8')):
        if r.get('ext') != 'pdf' or not r.get('file_url'):
            continue
        name = Path(r['file_name']).name
        if name in fallidos:
            continue
        p = ROOT / str(r['year']) / tipo_slug(r.get('type', '')) / name
        if not p.exists():
            out.append(r['file_url'])
    return out


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


def sonda(url, session):
    try:
        with session.get(url, stream=True, timeout=(15, 25), allow_redirects=True) as r:
            if r.status_code != 200:
                return False, f'HTTP {r.status_code}'
            data = b''
            for chunk in r.iter_content(1024):
                data += chunk
                if len(data) >= 1024:
                    break
        ok = len(data) >= 512 and (b'%PDF' in data[:1024])
        return ok, f'{r.status_code} {len(data)}B'
    except Exception as e:
        return False, str(e)[:80]


def sanidad(pend):
    s = requests.Session()
    s.headers.update({'User-Agent': UA, 'Connection': 'close',
                      'Referer': 'https://www.gacetaoficial.gob.cu/es/inicio'})
    urls = [REF]
    if pend:
        urls.append(random.choice(pend))
    resultados = []
    for i, u in enumerate(urls):
        ok, det = sonda(u, s)
        resultados.append((ok, det, u.rsplit('/', 1)[-1]))
        if i == 0 and not ok:
            break
    return all(x[0] for x in resultados), resultados


def main():
    log('Vigilante iniciado')
    espera = 60
    while True:
        pend = pendientes_pdf()
        if not pend:
            log('No quedan PDF pendientes. Vigilante termina.')
            estado('Sin PDF pendientes: nada que descargar.')
            return 0
        if descargador_activo():
            estado('Descargador activo: esperando a que termine.')
            time.sleep(30)
            continue

        ok1, r1 = sanidad(pend)
        if not ok1:
            estado(f'Servidor no sano: {r1[0][1]} ({r1[0][2]}). Reintento en {espera}s.')
            log(f'Sonda fallida: {r1}. Espera {espera}s')
            time.sleep(espera)
            espera = min(600, int(espera * 1.5))
            continue

        time.sleep(20)
        ok2, r2 = sanidad(pend)
        if not ok2:
            estado(f'Segunda sonda fallida: {r2[0][1]} ({r2[0][2]}). Reintento en {espera}s.')
            log(f'Segunda sonda fallida: {r2}. Espera {espera}s')
            time.sleep(espera)
            espera = min(600, int(espera * 1.5))
            continue

        detalle = ' | '.join(f'{x[2]}: {x[1]}' for x in r2)
        log(f'Servidor sano ({detalle}). Lanzando descargador.')
        estado(f'Servidor sano. Iniciando descarga. {detalle}')
        t0 = time.time()
        with open(HERE / 'descargador_stdout.log', 'a', encoding='utf-8') as f:
            proc = subprocess.Popen([sys.executable, '-u', str(DESCARGADOR)],
                                    stdout=f, stderr=subprocess.STDOUT)
            (HERE / 'descargador.pid').write_text(str(proc.pid), encoding='utf-8')
            rc = proc.wait()
        dur = int(time.time() - t0)
        if rc == 0:
            log('Descarga completa: el descargador termino sin pendientes.')
            estado('Descarga completa: sin pendientes.')
            return 0
        log(f'Descargador termino con codigo {rc} tras {dur}s. Reinicio con espera.')
        estado(f'Descarga interrumpida (codigo {rc}). Nueva sonda en {espera}s.')
        espera = 60
        time.sleep(espera)
        espera = min(600, int(espera * 1.5))


if __name__ == '__main__':
    sys.exit(main())
