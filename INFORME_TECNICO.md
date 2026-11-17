# Informe técnico / Technical report

**Proyecto / Project:** AutoDecide Habana (antes / formerly *ICD Automotive Market Project*)  
**Autor / Author:** responsable del proyecto / project owner  
**Fecha / Date:** 17 de noviembre de 2026  
**Ubicación / Location:** `~/Proyectos/ICD Automotive Market Project`  
**Estado / Status:** Fase 6 — scraping y captura de catálogos y anuncios, en curso / Phase 6 — scraping and capture, in progress  
**Idioma / Language:** español e inglés / Spanish and English

---

# Parte I — Español

## 1. Objetivo

El proyecto se llama **AutoDecide Habana**. Su objetivo actual es realizar un **análisis del mercado automotor de La Habana**: caracterizar estructura, precios, oferta, segmentos, tendencias, asequibilidad y condiciones de rentabilidad. La definición de un producto interactivo que recomiende la compra más rentable según las preocupaciones del usuario queda diferida a una especialización posterior. El análisis se apoya en dos pilares: la base de datos del mercado cubano y un pipeline de scraping reutilizable que se actualiza para adaptarse al momento en que se revise.

Se conserva el nombre anterior, *ICD Automotive Market Project*, para mantener la trazabilidad de la documentación ya producida.

## 2. Estado y fases

Las fases se redefinieron para que la fase activa sea la sexta. Estado a 17/11/2026:

| Fase | Nombre | Estado |
|---|---|---|
| 1 | Marco normativo y regulatorio | Completada |
| 2 | Descubrimiento y verificación de fuentes | Completada |
| 3 | Infraestructura técnica y herramientas | Completada |
| 4 | Corpus documental y trabajos investigativos | Completada |
| 5 | Diseño del esquema de datos y del pipeline | Completada |
| 6 | **Scraping y captura de catálogos y anuncios** | **En curso** |
| 7 | Unificación, limpieza y control de calidad | Pendiente |
| 8 | Análisis de mercado, comparables y rentabilidad | Pendiente |
| 9 | Documentación final, informe PDF y entrega | Pendiente |

La creación de este informe y del `README.md` es soporte transversal y no cambia la fase activa.

## 3. Organización de carpetas

```text
ICD Automotive Market Project/
├── README.md
├── INFORME_TECNICO.md / INFORME_TECNICO.pdf
├── .gitignore
├── Anexos/                  # corpus legal y documentos de apoyo
├── Auxiliares/              # .venv, cache, herramientas, Repositorios, Referencias
├── Copias/                  # 4 repos de referencia (excluidos de este informe)
├── Data/                    # investigaciones, verificaciones y SQLite por tienda
└── Hombros/                 # PDFs, HTML, repos y derivadas
```

Decisiones de diseño: todo el material auxiliar vive dentro de `Auxiliares/`; los clones se hicieron con `--depth 1` y se registraron en `Auxiliares/Repositorios/_clone_log.tsv`; la descubrimiento se separó de la verificación; `Copias/` no se registra en este informe por decisión explícita.

## 4. Fase 1 — Marco normativo y regulatorio

Se documentaron **17 empresas autorizadas** a importar y comercializar vehículos, distribuidores privados (BDC One, Dongfeng, MCV, Finauto, Changan, Chinautos, Envision, ATR Export), precios de referencia (BDC One 14.849–31.478 EUR; Dongfeng desde 21.900 EUR; Finauto desde 15.500 EUR; ATR Export con 46 modelos), aranceles y parque automotor. La norma marco es el **Decreto 163/2026** (Gaceta Oficial No. 65 Ordinaria, 04/08/2026, vigente desde el 11/08/2026), que deroga el Decreto 119/2024. Se cotejaron las resoluciones 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171–175/2026 (MFP), 312/2026 (Aduana) y 102/2026 (BCC). Resultado: `Data/investigacion-mercado-automotor-cuba.md` y `Data/verificacion-marketplaces-tiendas-organismos-2026-11-16.md`.

## 5. Fase 2 — Descubrimiento y verificación de fuentes

Dos búsquedas iniciales en DuckDuckGo, 30 páginas cada una, con bloqueo por CAPTCHA: se cambió a Yahoo y visitas directas. Se consolidaron **409 resultados, 400 únicos**. Se inventariaron **35 sitios** de compraventa en `Data/mercados-compraventa-cuba.md` y repositorios útiles en `Data/github-scraping-repos.md`.

Se verificaron **40 sitios/URLs**. Marketplaces con sección activa: Autocubana (667 vehículos), iTENCEL (951), VentaCuba (801 carros/camionetas), Timbirichi (281 carros), Revolico (112 enlaces en la primera página), Cogetucarro (5.225 anuncios), Cubisima (155 fichas), Apululu y Carros.com Cuba. Se corrigieron clasificaciones: Mercadoba y Fagales Market sin sección real; TuCuevita, Mercubano, Mercandil, Revoltillo, QvaVentas, Casinuevo, Publicid, WAnuncios y AnunciosCuba con categoría vacía; BizneCubano, Katapulk, A la Venta, Pymes Bulevar, MeroliCU y Rico Cuba son de piezas, motos o servicios.

Se documentaron **14 organismos** con competencia sobre el mercado: Consejo de Ministros/Estado, MINCEX, MINCIN, MITRANS, CEMA, MFP, ONAT, Aduana General, BCC, MININT, MINJUS, MEP, MINREX y MINSAP.

## 6. Fase 3 — Infraestructura técnica y herramientas

Se clonaron **61 repositorios** en `Auxiliares/Repositorios` con `--depth 1` (2,2 GB, 61 entradas `OK`). El conjunto cubre scraping general (Firecrawl, browser-use, Scrapling, crawl4ai, Scrapy, SeleniumBase, trafilatura, curl_cffi, Patchright, Playwright), Facebook, WhatsApp, Telegram y CAPTCHA. Se clasificaron **92 proyectos** de CAPTCHA en `Data/github-captcha-repos.md` y se seleccionaron 9.

Se creó `Auxiliares/.venv` con patchright 1.64.4, PyPasser 1.1.0, Scrapling 0.5.1, ddddocr 1.6.1, playwright 1.65.2, curl_cffi 0.17.0, trafilatura, pandas, numpy, onnxruntime 1.32.0, ddgs 9.16.1 y tenacity 9.2.1. Se usa el Chromium del sistema y FlareSolverr 3.5.2 en Docker (`http://127.0.0.1:8191/`).

Herramientas creadas: `ddg_research.py`, `buscar_fallback.py`, `descargar_hombros.py`, `scrape_concesionarios.py`, `resumen_catalogos.py` y `actualizar_informe.py`.

## 7. Fase 4 — Corpus documental y trabajos investigativos

Tres búsquedas con la regla de parar tras 10 páginas sin enlaces útiles (útil = primera aparición de un trabajo investigativo automotriz):

| Búsqueda | Páginas | Resultados | Útiles | Parada |
|---|---:|---:|---:|---|
| `mercado automovilistico trabajos investigativos` | 112 | 1.086 | 11 | página 19 |
| `rentabilidad del precio de automoviles trabajos investigativos` | 24 | 226 | 2 | página 11 |
| `calidad precio mercado automotriz trabajo investigativo` | 23 | 230 | 10 | página 22 |

El material se guardó en `Hombros/`: descarga inicial **93 OK / 17 fallos**, rentabilidad **23 OK / 10 fallos**, calidad/precio **78 OK / 36 fallos**, con `manifest.jsonl` e `indice.md`.

## 8. Fase 5 — Diseño del esquema de datos y del pipeline

Se diseñó una base SQLite por tienda con una tabla `vehiculos`: identificación (`url`, `shop`, `title`, `status`, `scraped_at`), metadatos y 30 campos estructurados (`marca`, `modelo`, `anio`, `precio`, `moneda`, `km`, `combustible`, `transmision`, `potencia`, etc.), además de campos sin normalizar (`tables_json`, `jsonld_json`, `raw_html`, ...). El scraper `scrape_concesionarios.py` usa adaptadores por dominio y renderizado opcional con Playwright.

## 9. Fase 6 — Scraping y captura (en curso)

Se prepararon 11 bases y se obtuvieron **256 filas**:

| Tienda | Filas | Con precio |
|---|---:|---:|
| AGN Motors | 60 | 45 |
| ATR Export | 6 | 5 |
| BDC One | 19 | 3 |
| Changan | 2 | 2 |
| Chinautos Cuba | 70 | 0 |
| ConnectingCuba | 1 | 1 |
| Dongfeng Cuba | 45 | 16 |
| Envision Autos | 1 | 0 |
| Finauto | 45 | 34 |
| MCV Commercial | 4 | 0 |
| La Subasta Cubana | 3 | 3 |

Excluidas por bloqueo técnico: carrosw (HTTP 403 con Bot Verification), LlamaCuba (timeout) y SASA/DIVEP (sin catálogo). Mejor densidad: AGN Motors, Chinautos Cuba, Dongfeng Cuba y Finauto. Esta fase sigue abierta: quedan por ampliar fuentes y completar campos.

## 10. Marco legal para la recolección y el análisis de datos

Solo se incluyen las normas y fuentes relevantes para el contexto del proyecto:

- **Decreto 163/2026**, Gaceta Oficial No. 65 Ordinaria (04/08/2026): regula la importación y comercialización de vehículos; define el marco sobre el que debe trabajar el análisis de precios y oferta.
- **Resolución 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171–175/2026 (MFP), 312/2026 (Aduana) y 102/2026 (BCC)**: desarrollos sectoriales, fiscales y cambiarios que condicionan el mercado.
- **Condiciones de uso de cada portal**: criterio operativo para la recolección. No se eluden mecanismos anti-automatización; los HTTP 403/429 se registran como limitación.
- **Protección de datos personales, ciberseguridad y derechos de autor**: antes de publicar resultados deben verificarse las normas cubanas vigentes y aplicar solo datos agregados, sin nombres, teléfonos ni información personal de anunciantes.
- `Anexos/Leyes/gaceta_catalog.json` es el índice de referencia; el corpus completo de gacetas no se registra entrada por entrada en este informe, solo se citan las normas anteriores.

## 11. Problemas y soluciones

| Problema | Solución |
|---|---|
| CAPTCHA en paginación DDG | Yahoo + visitas directas; después sesión con `vqd`. |
| HTTP 202 y página “anomaly” | Pausa 7–10 s con jitter, backoff exponencial y cooldown. |
| Falso “anomaly” en HTTP 200 | Detector ajustado para exigir texto real de anomalía. |
| carrosw anti-bot | Registrado como limitación; no se falsificó su contenido. |
| Sitios JS-heavy | Renderizado con Chromium del sistema desde Playwright. |
| Repetidos y mirrors | Deduplicación por título normalizado, prefijo y dominio. |

## 12. Conclusiones

1. El mercado habanero tiene nueve marketplaces con inventario real y una docena con categorías vacías o solo piezas.
2. El marco regulatorio vigente es el Decreto 163/2026 y el paquete de resoluciones citado.
3. El scraping sostenible depende del ritmo, la sesión y la reanudación, no principalmente del fingerprint TLS.
4. La regla de las 10 páginas evitó consumir resultados repetidos.
5. El análisis de mercado y el modelo de rentabilidad (fase 8) aún no están implementados; el producto interactivo se difiere a una especialización futura.

---

# Part II — English

## 1. Objective

The project is named **AutoDecide Habana**. Its goal is to define an interactive product able to recommend the most profitable car purchase in the **Havana** automotive market, based on the user's values, concerns and constraints (budget, reliability, fuel use, maintenance, resale value, spare-part availability, etc.). The product rests on two pillars: an analysis of the Cuban automotive market and a reusable scraping pipeline that updates itself to adapt to the moment of review.

The former name, *ICD Automotive Market Project*, is kept for traceability of existing documentation.

## 2. Status and phases

Phases were redefined so that the active phase is the sixth. Status as of 17 Nov 2026:

| Phase | Name | Status |
|---|---|---|
| 1 | Regulatory framework | Complete |
| 2 | Source discovery and verification | Complete |
| 3 | Technical infrastructure and tools | Complete |
| 4 | Document corpus and research | Complete |
| 5 | Data schema and pipeline design | Complete |
| 6 | **Scraping and capture of catalogues and listings** | **In progress** |
| 7 | Unification, cleaning and QA | Pending |
| 8 | Analysis, profitability model and interactive product | Pending |
| 9 | Final documentation, PDF report and delivery | Pending |

Creating this report and the `README.md` is cross-cutting support and does not change the active phase.

## 3. Folder structure

```text
ICD Automotive Market Project/
├── README.md
├── INFORME_TECNICO.md / INFORME_TECNICO.pdf
├── .gitignore
├── Anexos/                  # legal corpus and supporting documents
├── Auxiliares/              # .venv, cache, tools, cloned repos
├── Copias/                  # 4 reference repos (excluded from this report)
├── Data/                    # research, verification and per-store SQLite
└── Hombros/                 # PDFs, HTML, repos and derivatives
```

Design decisions: all auxiliary material lives under `Auxiliares/`; clones used `--depth 1` and are logged in `Auxiliares/Repositorios/_clone_log.tsv`; discovery was separated from verification; `Copias/` is excluded from this report by explicit decision.

## 4. Phase 1 — Regulatory framework

**17 authorized companies** were documented, along with private distributors (BDC One, Dongfeng, MCV, Finauto, Changan, Chinautos, Envision, ATR Export), reference prices (BDC One 14,849–31,478 EUR; Dongfeng from 21,900 EUR; Finauto from 15,500 EUR; ATR Export with 46 models), tariffs and the vehicle fleet. The framework is **Decree 163/2026** (Official Gazette No. 65, 04/08/2026, in force since 11/08/2026), which repeals Decree 119/2024. Resolutions 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171-175/2026 (MFP), 312/2026 (Customs) and 102/2026 (BCC) were cross-checked. Results: `Data/investigacion-mercado-automotor-cuba.md` and `Data/verificacion-marketplaces-tiendas-organismos-2026-11-16.md`.

## 5. Phase 2 — Source discovery and verification

Two initial DuckDuckGo searches, 30 pages each, blocked by CAPTCHA: switched to Yahoo and direct visits. **409 results, 400 unique**. A **35-site** inventory was produced in `Data/mercados-compraventa-cuba.md` and useful repos in `Data/github-scraping-repos.md`.

**40 sites/URLs** were verified. Active marketplaces: Autocubana (667 vehicles), iTENCEL (951), VentaCuba (801 cars/pickups), Timbirichi (281 cars), Revolico (112 links on page 1), Cogetucarro (5,225 ads), Cubisima (155 listings), Apululu and Carros.com Cuba. Corrections: Mercadoba and Fagales Market have no real section; several sites have empty categories; others only sell parts or motorcycles.

**14 organizations** with market competence were documented: Council of Ministers/State, MINCEX, MINCIN, MITRANS, CEMA, MFP, ONAT, General Customs, BCC, MININT, MINJUS, MEP, MINREX and MINSAP.

## 6. Phase 3 — Technical infrastructure and tools

**61 repositories** were cloned into `Auxiliares/Repositorios` with `--depth 1` (2.2 GB, 61 `OK` entries), covering general scraping, Facebook, WhatsApp, Telegram and CAPTCHA. **92 CAPTCHA projects** were classified in `Data/github-captcha-repos.md`; 9 were selected.

`Auxiliares/.venv` was created with patchright 1.64.4, PyPasser 1.1.0, Scrapling 0.5.1, ddddocr 1.6.1, playwright 1.65.2, curl_cffi 0.17.0, trafilatura, pandas, numpy, onnxruntime 1.32.0, ddgs 9.16.1 and tenacity 9.2.1. System Chromium and FlareSolverr 3.5.2 in Docker are used.

Tools created: `ddg_research.py`, `buscar_fallback.py`, `descargar_hombros.py`, `scrape_concesionarios.py`, `resumen_catalogos.py` and `actualizar_informe.py`.

## 7. Phase 4 — Document corpus and research

Three searches with a stop rule after 10 pages without useful links (useful = first appearance of an automotive research work):

| Search | Pages | Results | Useful | Stopped at |
|---|---:|---:|---:|---|
| `mercado automovilistico trabajos investigativos` | 112 | 1,086 | 11 | page 19 |
| `rentabilidad del precio de automoviles trabajos investigativos` | 24 | 226 | 2 | page 11 |
| `calidad precio mercado automotriz trabajo investigativo` | 23 | 230 | 10 | page 22 |

Material was saved under `Hombros/`: initial download **93 OK / 17 failures**, profitability **23 OK / 10 failures**, quality/price **78 OK / 36 failures**, with `manifest.jsonl` and `indice.md`.

## 8. Phase 5 — Data schema and pipeline design

A SQLite database per store was designed with a `vehiculos` table: identification (`url`, `shop`, `title`, `status`, `scraped_at`), metadata, 30 structured fields (`brand`, `model`, `year`, `price`, `currency`, `km`, `fuel`, `transmission`, `power`, etc.) and unstructured fields (`tables_json`, `jsonld_json`, `raw_html`, ...). `scrape_concesionarios.py` uses per-domain adapters and optional Playwright rendering.

## 9. Phase 6 — Scraping and capture (in progress)

11 databases were prepared and **256 rows** obtained:

| Store | Rows | With price |
|---|---:|---:|
| AGN Motors | 60 | 45 |
| ATR Export | 6 | 5 |
| BDC One | 19 | 3 |
| Changan | 2 | 2 |
| Chinautos Cuba | 70 | 0 |
| ConnectingCuba | 1 | 1 |
| Dongfeng Cuba | 45 | 16 |
| Envision Autos | 1 | 0 |
| Finauto | 45 | 34 |
| MCV Commercial | 4 | 0 |
| La Subasta Cubana | 3 | 3 |

Excluded due to technical blocks: carrosw (HTTP 403 Bot Verification), LlamaCuba (timeout) and SASA/DIVEP (no catalogue). Best density: AGN Motors, Chinautos Cuba, Dongfeng Cuba and Finauto. This phase is still open: more sources and fields are pending.

## 10. Legal framework for data collection and analysis

Only relevant norms and sources are included:

- **Decree 163/2026**, Official Gazette No. 65 (04/08/2026): regulates vehicle import and sales; defines the framework for price and supply analysis.
- **Resolution 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171-175/2026 (MFP), 312/2026 (Customs), 102/2026 (BCC)**: sectoral, fiscal and exchange-rate conditions.
- **Terms of use of each site**: operational rule for collection. Anti-automation mechanisms are not bypassed; HTTP 403/429 are recorded as limitations.
- **Personal data protection, cybersecurity and copyright**: before publishing results, current Cuban rules must be verified and only aggregated data used, with no names, phone numbers or personal information from advertisers.
- `Anexos/Leyes/gaceta_catalog.json` is the reference index; the full gazette corpus is not logged entry by entry here.

## 11. Problems and solutions

| Problem | Solution |
|---|---|
| CAPTCHA on DDG pagination | Yahoo + direct visits; later a `vqd` session. |
| HTTP 202 and "anomaly" page | 7-10 s pause with jitter, exponential backoff and cooldown. |
| False "anomaly" on HTTP 200 | Detector adjusted to require actual anomaly text. |
| carrosw anti-bot | Recorded as a limitation; content was not faked. |
| JS-heavy sites | Rendering with system Chromium via Playwright. |
| Duplicates and mirrors | Deduplication by normalized title, prefix and domain. |

## 12. Conclusions

1. The Havana market has nine marketplaces with real inventory and a dozen with empty categories or parts only.
2. The current regulatory framework is Decree 163/2026 and the cited resolutions.
3. Sustainable scraping depends on pace, session and resumability, not mainly on TLS fingerprinting.
4. The 10-page rule prevented consuming repeated results.
5. The interactive product and profitability model (phase 8) are not implemented yet.

---

# 13. Registro de altas / Change log

Registro automático de todo lo que se añade a la carpeta del proyecto. El script `Auxiliares/herramientas/actualizar_informe.py` añade filas debajo del marcador y regenera el PDF. `Copias/` queda excluido por decisión explícita.

Automatic record of everything added to the project folder. The script appends rows below the marker and regenerates the PDF. `Copias/` is excluded by explicit decision.

| Fecha / Date | Ruta / Path | Tipo / Type | Origen / Source | Tamaño / Size | Fase / Phase | Descripción / Description | Estado / Status |
|---|---|---|---|---|---|---|---|
<!-- REGISTRO_ALTAS -->
| 2026-11-17 | `Auxiliares/herramientas/actualizar_revolico.py` | script / script | — | 6 532 B | 3 / 3 | Actualización incremental de la BD de Revolico y subida por partes a Git. | Actualizado / Updated |
| 2026-11-17 | `Data/Revolico` | carpeta / folder | — | carpeta / folder (11 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Data/Revolico/partes` | carpeta / folder | — | carpeta / folder (47 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Data/Revolico/pipeline.sqlite` | base de datos / database | — | 10 625 024 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/Revolico/resumen.md` | documento / document | — | 412 B | 2 / 2 | Revolico — base de datos completa de la categoría Vehículos | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt` | carpeta / folder | — | carpeta / folder (28 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part001` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part002` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part003` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part004` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part005` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part006` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part007` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part008` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part009` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part010` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part011` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part012` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part013` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part014` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part015` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part016` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part017` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part018` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part019` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part020` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part021` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part022` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part023` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part024` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part025` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part026` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part027` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/revolico_parts_9qprzigt/revolico.sqlite.part028` | archivo / file | — | 16 777 216 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 77 264 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas/analisis_mercado.py` | script / script | — | 13 794 B | 3 / 3 | Análisis descriptivo inicial del mercado de autos usados en La Habana. | Actualizado / Updated |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 76 824 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 75 373 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (19 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/analisis_mercado.py` | script / script | — | 12 282 B | 3 / 3 | Análisis descriptivo inicial del mercado de autos usados en La Habana. | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/graficos_mercado.py` | script / script | — | 9 312 B | 3 / 3 | Funciones para generar todas las gráficas del análisis de mercado. | Añadido / Added |
| 2026-11-17 | `Data/analisis` | carpeta / folder | — | carpeta / folder (11 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/cobertura.csv` | datos / data | — | 174 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/dashboard.html` | HTML / HTML | — | 16 086 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/graficos` | carpeta / folder | — | carpeta / folder (9 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/01_histograma_precios.png` | archivo / file | — | 59 758 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/02_boxplot_marcas.png` | archivo / file | — | 64 227 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/03_barras_municipios.png` | archivo / file | — | 68 628 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/04_precios_por_anio.png` | archivo / file | — | 90 044 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/05_serie_precio_vs_tasa.png` | archivo / file | — | 99 874 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/06_variaciones_tasa_precio.png` | archivo / file | — | 94 796 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/07_outliers.png` | archivo / file | — | 53 770 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/08_cobertura.png` | archivo / file | — | 36 886 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/graficos/dashboard_interactivo.html` | HTML / HTML | — | 24 245 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/informe_descriptivo.md` | documento / document | — | 9 592 B | 2 / 2 | Análisis descriptivo inicial — mercado de autos usados en La Habana | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/outliers.csv` | datos / data | — | 768 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/precios_por_anio.csv` | datos / data | — | 879 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/precios_por_marca.csv` | datos / data | — | 803 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/precios_por_municipio.csv` | datos / data | — | 741 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/resumen_general.csv` | datos / data | — | 102 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Data/analisis/serie_precio_vs_tasa.csv` | datos / data | — | 544 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/serie_precio_vs_tasa_mensual.csv` | datos / data | — | 152 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 68 735 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (18 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/analisis_mercado.py` | script / script | — | 8 816 B | 3 / 3 | Análisis descriptivo inicial del mercado de autos usados en La Habana. | Añadido / Added |
| 2026-11-17 | `Data` | carpeta / folder | — | carpeta / folder (11 entradas) | 7 / 7 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Data/analisis` | carpeta / folder | — | carpeta / folder (8 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Data/analisis/cobertura.csv` | datos / data | — | 174 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/dashboard.html` | HTML / HTML | — | 14 753 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/informe_descriptivo.md` | documento / document | — | 6 498 B | 2 / 2 | Análisis descriptivo inicial — mercado de autos usados en La Habana | Añadido / Added |
| 2026-11-17 | `Data/analisis/outliers.csv` | datos / data | — | 768 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/precios_por_anio.csv` | datos / data | — | 728 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/precios_por_marca.csv` | datos / data | — | 803 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/precios_por_municipio.csv` | datos / data | — | 741 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/analisis/resumen_general.csv` | datos / data | — | 102 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 65 081 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 63 764 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |
| 2026-11-17 | `README.md` | documento / document | — | 16 116 B | 9 / 9 | AutoDecide Habana / AutoDecide Habana | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 62 338 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 59 613 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 56 770 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 53 268 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (17 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/scrape_revolico_pipeline.py` | script / script | — | 14 401 B | 3 / 3 | Pipeline de 3 etapas con colas persistentes para Revolico. | Añadido / Added |
| 2026-11-17 | `Data/Revolico` | carpeta / folder | — | carpeta / folder (7 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Data/Revolico/pipeline.sqlite` | base de datos / database | — | 10 625 024 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Data/Revolico/snapshots` | carpeta / folder | — | carpeta / folder (1 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Data/Revolico/snapshots/ultimo.json` | datos / data | — | 101 344 B | 2 / 2 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 48 537 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas/limpiar_revolico.py` | script / script | — | 7 655 B | 3 / 3 | Limpieza de la BD de Revolico: solo vehículos de 4+ ruedas con datos útiles. | Actualizado / Updated |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 46 466 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 45 634 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Data/Revolico` | carpeta / folder | — | carpeta / folder (5 entradas) | 2 / 2 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 44 625 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas/sincronizar_github.py` | script / script | — | 2 193 B | 3 / 3 | Sincroniza con GitHub SOLO los archivos del proyecto ya definidos. | Actualizado / Updated |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 43 591 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (16 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/actualizar_revolico.py` | script / script | — | 6 406 B | 3 / 3 | Actualización incremental de la BD de Revolico y subida por partes a Git. | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/limpiar_revolico.py` | script / script | — | 7 610 B | 3 / 3 | Limpieza de la BD de Revolico: solo vehículos de 4+ ruedas con datos útiles. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/sincronizar_github.py` | script / script | — | 2 038 B | 3 / 3 | Sincroniza con GitHub SOLO los archivos del proyecto ya definidos. | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 42 639 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 42 490 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 42 341 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (14 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/integraciones` | carpeta / folder | — | carpeta / folder (7 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/README.md` | documento / document | — | 2 827 B | 3 / 3 | Integraciones / Integrations | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook` | carpeta / folder | — | carpeta / folder (8 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper` | carpeta / folder | — | carpeta / folder (10 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/__init__.py` | script / script | — | 1 316 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/exceptions.py` | script / script | — | 3 042 B | 3 / 3 | Base for all errors raised by this library. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/facebookConsolidater.py` | script / script | — | 4 012 B | 3 / 3 | Recursively merge dictionaries, extend lists. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/facebookGraphql.py` | script / script | — | 45 585 B | 3 / 3 | Facebook request context. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/facebookNoiseRemoval.py` | script / script | — | 5 090 B | 3 / 3 | Recursively remove UI/React/Relay garbage from data | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/facebookOperationDiscovery.py` | script / script | — | 22 550 B | 3 / 3 | var __registry = {}; | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/parserModels.py` | script / script | — | 14 357 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/structures.py` | script / script | — | 122 555 B | 3 / 3 | Facebook photo. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_gql_scraper/unifiedFacebookParser.py` | script / script | — | 72 729 B | 3 / 3 | Wrap a ParserMedia in a ParserMediaPost. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper` | carpeta / folder | — | carpeta / folder (7 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/__init__.py` | script / script | — | 314 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/driver_initialization.py` | script / script | — | 3 798 B | 3 / 3 | adds capabilities to the driver | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/driver_utilities.py` | script / script | — | 7 902 B | 3 / 3 | expects driver's instance, closes the driver | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/element_finder.py` | script / script | — | 22 200 B | 3 / 3 | Holds the collections of methods that finds element of the facebook's posts using selenium's webdriver's methods | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/scraper.py` | script / script | — | 17 678 B | 3 / 3 | changes the class member __driver value to driver on call | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_page_scraper/scraping_utilities.py` | script / script | — | 5 450 B | 3 / 3 | expects string and returns numbers from them as integer type, | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper` | carpeta / folder | — | carpeta / folder (10 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/__init__.py` | script / script | — | 20 243 B | 3 / 3 | Get a Facebook user's profile information | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/__main__.py` | script / script | — | 6 624 B | 3 / 3 | facebook-scraper entry point when used as a script | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/constants.py` | script / script | — | 285 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/exceptions.py` | script / script | — | 636 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/extractors.py` | script / script | — | 62 499 B | 3 / 3 | Class for Extracting fields from a FacebookPost | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/facebook_scraper.py` | script / script | — | 51 259 B | 3 / 3 | Class for creating FacebookScraper Iterators | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/fb_types.py` | script / script | — | 340 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/page_iterators.py` | script / script | — | 10 774 B | 3 / 3 | Class for Parsing a single page on a Page | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/facebook_scraper/utils.py` | script / script | — | 14 155 B | 3 / 3 | Strip invalid XML characters that `lxml` cannot parse. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/marketplace_gui.py` | script / script | — | 1 982 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/marketplace_scraper.py` | script / script | — | 9 640 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper` | carpeta / folder | — | carpeta / folder (17 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/__init__.py` | script / script | — | 637 B | 3 / 3 | Facebook scraper package. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/auth.py` | script / script | — | 1 263 B | 3 / 3 | Authentication helpers: cookie parsing and cURL parsing. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/comments.py` | script / script | — | 14 175 B | 3 / 3 | Comment and reply scraping with full metadata (author, IDs, reactions). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/config.py` | script / script | — | 2 694 B | 3 / 3 | Central runtime configuration shared by all scraper modules. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/extractors.py` | script / script | — | 8 202 B | 3 / 3 | Field extractors for Facebook Story nodes (counts, names, media checks). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/group_posts.py` | script / script | — | 7 869 B | 3 / 3 | Group post scraping (posts + media, batched via callback). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/http.py` | script / script | — | 4 202 B | 3 / 3 | HTTP helpers: retry logic with proxy rotation and Facebook response parsing. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/logging_utils.py` | script / script | — | 726 B | 3 / 3 | Thread-aware logging for scrapers. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/media.py` | script / script | — | 7 634 B | 3 / 3 | Media extraction and image downloading (with optional album traversal). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/page_posts.py` | script / script | — | 11 528 B | 3 / 3 | Page/profile post scraping (posts + media, batched via callback). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/proxy_utils.py` | script / script | — | 4 048 B | 3 / 3 | Lazy import to avoid a circular dependency (config imports this module). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/resolvers.py` | script / script | — | 3 685 B | 3 / 3 | Resolve Facebook URLs into the IDs the scrapers need. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/run.py` | script / script | — | 1 668 B | 3 / 3 | Facebook Scraper — Flask web GUI. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/single_post.py` | script / script | — | 1 847 B | 3 / 3 | Single post scraping: comments + optional album image download. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/storage.py` | script / script | — | 9 826 B | 3 / 3 | Storage layer: everything under the project's data/ directory. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/post_comment_scraper/tasks.py` | script / script | — | 5 973 B | 3 / 3 | High-level scrape operations used by the web app (and usable from CLI). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/facebook/selenium_car_scraper.py` | script / script | — | 28 921 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas` | carpeta / folder | — | carpeta / folder (8 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scrape_autocubana.py` | script / script | — | 22 277 B | 3 / 3 | Script de Web Scraping para extraer el catálogo de vehículos en venta | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraper_cubamerica.py` | script / script | — | 12 187 B | 3 / 3 | Scraper de CubAmerica (envioscubamerica.com). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraper_itencel.py` | script / script | — | 15 220 B | 3 / 3 | Scraper de iTENCEL (itencel.com). | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraper_revolico.py` | script / script | — | 26 644 B | 3 / 3 | scraper_revolico.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraper_telegram.py` | script / script | — | 3 344 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraper_vedca.py` | script / script | — | 12 563 B | 3 / 3 | Scraper de la tienda VEDCA dentro de Islagrande. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/fuentes_cubanas/scraping_dongfeng.py` | script / script | — | 16 155 B | 3 / 3 | Scraping del catalogo de vehiculos de https://dongfengqba.com/ | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/requirements-integraciones.txt` | texto / text | — | 258 B | 3 / 3 | Dependencias de los scripts integrados (instalar solo las que se vayan a usar) | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny` | carpeta / folder | — | carpeta / folder (10 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/captcha_solver.py` | script / script | — | 33 515 B | 3 / 3 | captcha_solver.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/diff_runs.py` | script / script | — | 19 098 B | 3 / 3 | diff_runs.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/env_config.py` | script / script | — | 8 828 B | 3 / 3 | env_config.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/fingerprint_client.py` | script / script | — | 18 748 B | 3 / 3 | fingerprint_client.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/output_writer.py` | script / script | — | 38 158 B | 3 / 3 | output_writer.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/page_flow.py` | script / script | — | 38 393 B | 3 / 3 | page_flow.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/playwright_scraper.py` | script / script | — | 89 998 B | 3 / 3 | spinny-scraper — Playwright edition (primary engine) | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/product_parser.py` | script / script | — | 90 678 B | 3 / 3 | product_parser.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/spinny/proxy_pool.py` | script / script | — | 13 938 B | 3 / 3 | proxy_pool.py | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram` | carpeta / folder | — | carpeta / folder (1 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite` | carpeta / folder | — | carpeta / folder (10 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/__init__.py` | script / script | — | 105 B | 3 / 3 | TeleGraphite - A tool to fetch and save posts from public Telegram channels. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/cli.py` | script / script | — | 11 392 B | 3 / 3 | Command-line interface for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/client.py` | script / script | — | 3 090 B | 3 / 3 | Client module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/config.py` | script / script | — | 4 552 B | 3 / 3 | Configuration module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/contact_extractor.py` | script / script | — | 735 B | 3 / 3 | Contact Extractor module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/errors.py` | script / script | — | 2 170 B | 3 / 3 | Error handling module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/fetcher.py` | script / script | — | 9 093 B | 3 / 3 | Fetcher module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/logging_config.py` | script / script | — | 4 598 B | 3 / 3 | Logging configuration module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/telegram/telegraphite/store.py` | script / script | — | 11 976 B | 3 / 3 | Store module for TeleGraphite. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/whatsapp` | carpeta / folder | — | carpeta / folder (4 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/whatsapp/waha_client.py` | script / script | — | 4 212 B | 3 / 3 | Cliente Python para WAHA (WhatsApp HTTP API) orientado a AutoDecide Habana. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/whatsapp/whatsapp_mcp_reader.py` | script / script | — | 24 712 B | 3 / 3 | Determine if chat is a group based on JID pattern. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/integraciones/whatsapp/whatsapp_web_example.js` | archivo / file | — | 30 417 B | 3 / 3 | Añadido al proyecto; pendiente de descripción / Added; description pending | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 22 664 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |

| 2026-11-17 | `.gitignore` | archivo / file | — | 1 107 B | 9 / 9 | Añadido al proyecto; pendiente de descripción / Added; description pending | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas` | carpeta / folder | — | carpeta / folder (13 entradas) | 3 / 3 | Carpeta añadida al proyecto / Folder added to the project | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/actualizar_informe.py` | script / script | — | 14 283 B | 3 / 3 | Registra altas nuevas del proyecto en INFORME_TECNICO.md y regenera el PDF. | Actualizado / Updated |
| 2026-11-17 | `Auxiliares/herramientas/actualizar_revolico.py` | script / script | — | 6 408 B | 3 / 3 | Actualización incremental de la BD de Revolico y subida por partes a Git. | Añadido / Added |
| 2026-11-17 | `Auxiliares/herramientas/reconstruir_revolico.py` | script / script | — | 1 812 B | 3 / 3 | Reconstruye revolico.sqlite a partir de las partes versionadas en Git. | Añadido / Added |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | 21 391 B | 9 / 9 | Informe técnico / Technical report | Actualizado / Updated |
| 2026-11-17 | `README.md` | documento / document | — | 15 804 B | 9 / 9 | AutoDecide Habana / AutoDecide Habana | Actualizado / Updated |

| 2026-11-17 | `README.md` | documento / document | — | 7,6 KB | 9 | Nombre del proyecto, estado, fases y marco para GitHub / Project name, status, phases and GitHub framework | Creado / Created |
| 2026-11-17 | `INFORME_TECNICO.md` | documento / document | — | — | 9 | Informe técnico redefinido en 9 fases, bilingüe y con marco legal / Technical report redefined into 9 phases, bilingual, with legal framework | Actualizado / Updated |
| 2026-11-17 | `INFORME_TECNICO.pdf` | PDF / PDF | generado desde MD / generated from MD | — | 9 | Entregable en PDF / PDF deliverable | Generado / Generated |
| 2026-11-17 | `Auxiliares/herramientas/actualizar_informe.py` | script / script | — | — | 3 | Registro automático de altas y regeneración del PDF / Automatic change log and PDF regeneration | Creado / Created |
| 2026-11-17 | `.gitignore` | configuración / config | — | — | 3 | Exclusiones para GitHub / GitHub exclusions | Creado / Created |

## 14. Sincronización automática de Revolico / Automatic Revolico sync

La BD `Data/Revolico/revolico.sqlite` **no se versiona como archivo único**. Cada 10 minutos un timer de systemd ejecuta `Auxiliares/herramientas/actualizar_revolico.py`: corre el scraper incremental, divide la BD en partes de 16 MiB dentro de `Data/Revolico/partes/`, sube solo las partes que cambiaron y actualiza esta fila. Para recuperar el archivo completo se usa `Auxiliares/herramientas/reconstruir_revolico.py`, que verifica el hash.

The database is **not versioned as a single file**. Every 10 minutes a systemd timer runs `actualizar_revolico.py`: it runs the incremental scraper, splits the DB into 16 MiB chunks under `Data/Revolico/partes/`, uploads only changed chunks and updates this row. Use `reconstruir_revolico.py` to rebuild the full file and verify its hash.

| Última ejecución / Last run | Tamaño / Size | Partes / Chunks | SHA-256 (inicio) | Reconstrucción / Rebuild |
|---|---|---|---|---|
<!-- SYNC_REVOLICO -->
| 2026-11-17T15:29:31+00:00 | 795373568 B | 48 partes de 16 MiB | `dadd2bffba615d8a…` | Reconstruir con `reconstruir_revolico.py` / Rebuild with `reconstruir_revolico.py` |

## 15. Eficiencia de Telegram, WhatsApp y Facebook / Efficiency of Telegram, WhatsApp and Facebook

**ES.** Para obtener más datos del mercado habanero, la ruta más eficiente es Telegram MTProto (`telethon`, ya integrado): sin navegador, con cursor incremental `min_id`/`offset_id`, búsqueda server-side y manejo de `FloodWaitError`. Le sigue Facebook GQL (`facebook_gql_scraper`): llamadas GraphQL con sesión autenticada y normalización con `price-parser`/`iso4217parse`, más rápido que Selenium. Para grupos de WhatsApp no existe API pública personal; la opción operativa es un servidor WAHA auto-hospedado y su REST (`/api/sessions`, `/api/{session}/chats`, `/api/{session}/chats/{chatId}/messages`) con deduplicación por id, que es lo que hace `whatsapp/waha_client.py`. Playwright/Selenium quedan como último recurso para páginas JS. La salida de las tres fuentes debe convergir en un esquema común (`fuente`, `id`, `chat/página`, `timestamp`, `texto`, `precio`, `moneda`, `url`) con dedup por `hash(fuente,id)` y sin datos personales.

**EN.** For more Havana market data, the most efficient route is Telegram MTProto (`telethon`, already integrated): no browser, incremental cursor, server-side search and `FloodWaitError` handling. Next is Facebook GQL: authenticated GraphQL calls with `price-parser`/`iso4217parse`, faster than Selenium. WhatsApp has no public personal API; the practical option is self-hosted WAHA REST with id deduplication, implemented in `waha_client.py`. Playwright/Selenium remain a last resort. All three should converge into a common schema with source-based deduplication and no personal data.

**Nota / Note (17/11/2026):** se detuvo manualmente `revolico-scrape.timer` y su servicio a petición del usuario. El scraper había ampliado la BD de 3.682 a **6.332 anuncios** (520,6 MB) antes de detenerse; no se generaron partes (`estado.json` ausente) porque se detuvo antes de la fase de división. `revolico-git.timer` sigue activo para no perder cambios ya versionados. / The scrape timer and its service were stopped manually at the user's request. The scraper had grown the DB from 3,682 to **6,332 ads** (520.6 MB) before stopping; no chunks were produced because it was stopped before the split phase. `revolico-git.timer` remains active so versioned changes are not lost.

**Limpieza ejecutada / Cleaning run (17/11/2026):** sobre los 6.332 anuncios actuales, `limpiar_revolico.py` conservó **304 autos** en la tabla `autos` y registró **6.028 exclusiones** en `revision` (5.983 no vehículo 4+ ruedas, 45 sin datos necesarios, 0 páginas sin datos suficientes). No se borraron filas originales: `anuncios` conserva las columnas de auditoría `es_auto`, `motivo_exclusion`, `pagina_revisada` y `datos_necesarios`. Se añadieron `microbús/guagua/ómnibus/bus` a los patrones de inclusión. / On the current 6,332 ads, 304 cars were kept and 6,028 exclusions logged; no original rows were deleted and microbus terms were added to the inclusion patterns.

**Permanencia / Retention:** las Condiciones de Uso de Revolico (23/09/2026) no fijan un plazo de caducidad de los anuncios. Empíricamente, un anuncio con `updated_on_by_user=2024-12-17` seguía en HTTP 200 el 17/11/2026 (~699 días), por lo que no puede asumirse una expiración de 30 días. El 99,3 % de los anuncios tiene `updated_on_by_user` en los últimos 7 días (mediana 1 día en los 189 autos), lo que indica renovación frecuente por parte del vendedor. Revolico's Terms (23/09/2026) set no fixed expiry; an ad last updated 2024-12-17 was still HTTP 200 on 2026-11-17 (~699 days), while 99.3% of ads were updated within 7 days, suggesting frequent seller renewal.

## 16. Pipeline de colas / Queue-based pipeline (18/11/2026)

`Auxiliares/herramientas/scrape_revolico_pipeline.py` separa el trabajo en tres etapas simultáneas con colas persistentes en `Data/Revolico/pipeline.sqlite`:

1. **Descubrimiento**: recorre página por página y guarda enlace, `ad_id` y firma de listado en `url_queue`.
2. **Descarga**: workers toman URLs pendientes y guardan **todos** los campos parseados (`raw_html`, `apollo_full`, `meta_json`, imágenes, teléfonos, etc.) en `download_queue`.
3. **Procesamiento**: workers clasifican cada anuncio con `limpiar_revolico.clasificar` y escriben la decisión en `process_queue`. Cada **25 anuncios procesados** (aceptados o rechazados) se hace un commit por lotes en `anuncios`/`autos`/`imagenes`/`telefonos` o en `revision`.

Se adaptó el patrón `output_writer.py` + `diff_runs.py` de `spinny-scraper` como snapshot `Data/Revolico/snapshots/ultimo.json` (`{id: firma}`). El campo `updatedOnToOrder` del listado resultó ser un marcador de ranking y no de edición, así que el salto de descarga queda desactivado por defecto (`--skip-unchanged`); el snapshot se conserva como registro de diferencias.

Prueba con 1 página: **119 enlaces** descubiertos y procesados, 7 lotes de 25, BD principal de 6.332 a **6.334 anuncios** y de 304 a **317 autos**. Todo queda auditado; no se descarta información.

**EN.** The new pipeline runs three concurrent stages with persistent queues, committing every 25 processed ads. The spinny diff pattern was adapted as a snapshot, but skipping downloads is disabled by default because the listing timestamp is a ranking signal, not an edit signal. Test run: 119 links, 6,334 ads and 317 cars in the main DB.

## 17. Guía de análisis de mercado / Market-analysis guide (18/11/2026)

Fuentes académicas y repositorios revisados para definir los requerimientos del análisis (Fases 7-8):

| Fuente | Aporte metodológico | Requerimiento para AutoDecide |
|---|---|---|
| `Hombros/01_PDFs/Análisis del mercado de vehículos usados y su comercialización en el__73e1773e.pdf` (PUCE) | Asimetría de información (Akerlof); clasificación de calidad por antigüedad (≤5 años alta, >5 años con defectos); encuesta a 130 comerciantes; medición de costos ocultos y margen de reventa | Capturar año/antigüedad, estado, costos de reacondicionamiento y margen; comparar precio por calidad |
| `Hombros/RESUMEN_NUEVAS_BUSQUEDAS.md` (variaciones de precio, 2 trabajos útiles) | Variación de precios en seminuevos | Serie temporal de precio y depreciación por año |
| `Hombros/01_PDFs/PDF Informe de competencia del mercado automotriz ...` / `Mercado automotriz chileno: un análisis empírico` | Estructura y concentración del mercado | Cuota por marca/segmento, comparables |
| `Hombros/02_HTML/Inteligencia De Negocios Aplicada Al Sector Automovilístico__5e5a32a5.html` | ETL + dashboard | Pipeline, métricas y visualización |
| Informes ANFAC / EY / INEGI / BBVA / COIIM en `Hombros/01_PDFs/` | Indicadores macro: matriculaciones, parque, electrificación, combustible | Contexto: tipo de combustible, años, normativa |
| `Copias/AutosxCuba/code/{unir_todo_final,modelo_predictivo,generar_graficos}.py` | Unificación multi-fuente, predicción de precios, gráficos | Unificar fuentes, modelo de precio, visualizaciones |
| `Copias/guani-saimc/src/saimc/*` | Precio por producto/provincia con trazabilidad | Procedencia y geografía (provincia/municipio) |
| `Copias/taso-api/src/*` | Tasas de cambio múltiples | Normalizar CUP/USD/MLC/EUR |
| `Auxiliares/Repositorios Referencias/IDSE-DATA-SCIENCE-PROJECT-/{car_features,predict,server}.py` | Feature engineering, XGBoost, SHAP, Flask | Explicabilidad de la recomendación |
| `Auxiliares/Repositorios Referencias/used-cars-price-prediction/app.py` | Producto interactivo con Gradio | Interfaz de "preocupaciones del usuario" |
| `Auxiliares/Repositorios Referencias/Iran-Car-Market-Intelligence/src/icmi/analytics/*` | Comparables, estadística y dashboard | Metodología de comparables y rentabilidad |
| `Auxiliares/Repositorios Referencias/{uk-automotive-transition,vahan-india,nz-vehicle-market-tracker,zimbabwe-used-vehicle-market-analysis}` | Series por período, EDA, viabilidad | Tendencias y segmentación |

**Requerimientos derivados:** (1) esquema común con precio+moneda normalizada, año/km/combustible/transmisión/marca/modelo/provincia/tipo de vendedor y procedencia; (2) clasificación de calidad y estimación de costos ocultos; (3) comparables por marca-modelo-año-provincia; (4) modelo de rentabilidad = precio de reventa esperado − precio de compra − costos − impuestos; (5) serie temporal con snapshots; (6) dashboard de mercado; (7) validación, dedup y sin datos personales. La ponderación de preferencias del usuario y el producto interactivo quedan para la especialización futura.

**EN.** Academic sources and integrated repositories were reviewed to define the Fase 7-8 requirements: common schema with normalized currency, quality classification and hidden costs, comparables, profitability model, user-preference weighting, time series, interactive product, and validation/provenance.

## 18. Auditoría de procedencia / Source audit (18/11/2026)

| Fuente | Naturaleza | Verificación | Uso en el análisis |
|---|---|---|---|
| DfT / DVLA (UK), `gov.uk/government/statistical-data-sets/vehicle-licensing-statistics-data-files` | **Oficial gubernamental** | Verificado en vivo: publicado por Department for Transport + DVLA, actualizado 23/09/2026, Open Government Licence | Repos `uk-automotive-transition`: erste Registrierungen por marca/combustible/trimestre |
| VAHAN (India), declarado por `vahan-india-automotive-market-2025` | **Oficial gubernamental** (MoRTH) | No accesible desde este entorno (error de transporte); el repo documenta 12 exportaciones mensuales 2025 y manifiesto de verificacion | Registros por fabricante/combustible |
| BCC (Banco Central de Cuba) | **Oficial gubernamental** | No accesible en vivo desde este entorno; citado en `Data/investigacion-mercado-automotor-cuba.md` y Resolución 102/2026 | Tasa oficial |
| Gaceta Oficial / MINCEX / MITRANS / MININT | **Oficial gubernamental** | Verificado en investigacion previa (Gaceta 65/2026, Decreto 163/2026) | Marco legal y normativo |
| ANFAC (España) | **Gremial** (asociación de fabricantes) | Verificado en vivo: anfac.com, cifras de matriculaciones y parque, informe anual | Contexto sectorial, no precio de Cuba |
| AEADE (Ecuador) | **Gremial** | Verificado en vivo: aeade.net, anuarios y boletines de ventas | Fuente declarada por el estudio PUCE de vehículos usados |
| INEGI (México), EY, BBVA Research, COIIM, OICA | **Oficial / consultoría / gremio internacional** | Citados en los informes descargados en `Hombros/01_PDFs/`; no todos re-verificados en vivo | Contexto macro y tendencias |
| Universidades (PUCE, UPS, UPV, UChile, UNAL, etc.) | **Académico** | Repositorios institucionales (.edu / repositorios oficiales) en `Hombros/indice.md` | Metodología, encuestas, EDA |
| CarDekho (Kaggle), Spinny, OLX, Revolico, Autocubana, Dongfeng | **Marketplace / anuncios** | No son estadísticas oficiales; son precios **pedidos**, no transaccionados | Señal de precios; requiere dedup, verificación y sesgo declarado |
| WhatsApp / Telegram / Facebook groups | **Redes sociales** | No verificables como fuente estadística; requieren consentimiento y sin datos personales | Precios reportados por usuarios |
| elTOQUE, QvaPay, Binance (en `taso-api`) | **No oficial** (medios/P2P/crypto) | No verificados en vivo; elTOQUE es medio independiente, no BCC | Tasa informal/P2P, separada de la oficial |
| UCI Automobile, datasets sintéticos (Zimbabwe/Nigeria) | **Académico/sintético** | Declarado en los propios README | Solo referencia metodológica, nunca precio real de Cuba |

**Conclusión:** las fuentes oficiales y gremiales sirven de **contexto y validación**; los anuncios y redes son la **señal de precio** pero no sustituyen estadísticas oficiales. El análisis debe etiquetar cada métrica con su procedencia y nivel de confianza, y no mezclar tasas oficiales e informales ni precios anunciados con precios de transacción.

**EN.** Official/governmental and industry sources are used for context and validation; marketplaces and social platforms provide advertised-price signals only. Every metric must carry provenance and confidence level, keeping official vs informal rates and asking vs transaction prices separate.

## 19. Marco de análisis de mercado y su adaptación / Market-analysis framework and adaptation (18/11/2026)

### Marco general (8 pasos, derivado de los trabajos revisados)

1. **Pregunta y decisión**: qué se decide, para quién y en qué horizonte (PUCE: funcionamiento del mercado de usados; Chile: variables que influyen en tener automóvil).
2. **Delimitación**: geografía, producto, canal y unidad de análisis.
3. **Marco teórico y normativo**: asimetría de información (Akerlof), selección adversa, riesgo moral, regulación vigente.
4. **Diseño de datos**: fuentes primarias (encuestas/entrevistas) y secundarias (registros, anuncios), esquema común, muestreo y sesgos.
5. **Recolección y curación**: captura, deduplicación, validación y trazabilidad (ETL + BI).
6. **Descriptivo y segmentación**: distribución de precios, participación por marca/segmento, series temporales.
7. **Analítico**: comparables, depreciación, costos ocultos, margen de reventa, modelos explicables.
8. **Entrega y monitoreo**: dashboard de mercado, limitaciones y actualización periódica.

### Adaptación a Cuba / La Habana

- **Delimitación**: La Habana; autos de 4+ ruedas; canales formal e informal; precios anunciados en CUP/USD/MLC/EUR **sin mezclar**.
- **Fuentes**: Revolico (BD propia, 6.334 anuncios / 317 autos), concesionarios (Autocubana, Dongfeng, BDC One…), Gaceta/Decreto 163/2026, BCC (oficial) y elTOQUE (informal), salarios de la Resolución 14, y señales de Telegram/WhatsApp/Facebook sin datos personales.
- **Variables**: precio+moneda, año/antigüedad, km, combustible, transmisión, marca/modelo, provincia/municipio, tipo de vendedor, imágenes, estado y palabras de defecto en el texto (para estimar costos ocultos).
- **Métodos adaptados**: descriptivo por marca-modelo-año; clases de calidad (≤5 años alta, >5 años con defectos, según PUCE); bandera de asimetría por ocultamiento; comparables por modelo ±2 años y municipio; rentabilidad = reventa esperada − compra − reacondicionamiento − impuestos (Decreto 163/2026); asequibilidad = precio / salario; series con snapshots.
- **Entregables**: tabla `autos` + `revision`, dashboard de mercado, informe técnico. El recomendador interactivo se difiere a la especialización futura.
- **Límites**: precios pedidos no transaccionados, sesgo de supervivencia de anuncios, sin datos personales, vigencia normativa a verificar.

**EN.** An eight-step generic framework was adapted to Havana: scope, regulatory/theoretical frame, data design, curation, descriptive analysis, comparables and profitability, affordability, and an explainable interactive recommender, with explicit provenance and limitations.

## 20. Marco analítico detallado / Detailed analytical framework (18/11/2026)

**ES.** El marco operativo completo consta de nueve bloques:

1. **Objetivo del análisis**: caracterizar el mercado de autos usados en La Habana (estructura, precios, oferta, segmentos, tendencias, asequibilidad y rentabilidad), sin recomendar aún una compra concreta.
2. **Alcance**: La Habana, autos 4+ ruedas, canales formal e informal, precios anunciados separados por moneda.
3. **Marco teórico**: asimetría de información, selección adversa, riesgo moral, diferenciación de precios y calidad por antigüedad.
4. **Marco normativo**: Decreto 163/2026, resoluciones 104/17/52/171-175/312/102 de 2026, Gaceta 65/2026; impedimentos legales para recolección y uso de datos.
5. **Arquitectura de datos**: fuentes (Revolico, concesionarios, tasas BCC/elTOQUE, salarios Resolución 14, redes), esquema común con IDs, precio+moneda, geografía, timestamps y procedencia; pipeline de 3 colas con commit cada 25 procesados; limpieza a `autos`/`revision`.
6. **Descriptivo**: distribuciones (mediana, IQR, outliers), segmentación por marca-modelo-año, precio/km, geografía municipal, series con snapshots.
7. **Analítico**: comparables por modelo ±2 años y municipio, depreciación, clasificación de calidad y costos ocultos, regresión hedónica, margen de rentabilidad, asequibilidad precio/salario, ponderación de preferencias, explicabilidad tipo SHAP.
8. **Entregables del análisis**: tablas limpias, dashboard de mercado, informe bilingüe y trazabilidad de cada cifra. El producto interactivo de recomendación se difiere a una especialización posterior.
9. **Validación y entrega**: dedup, manejo de missing, sensibilidad a moneda y supuestos, pruebas con datos conocidos, informe bilingüe, limitaciones y monitoreo continuo.

**Lo que ya existe:** BD de 6.334 anuncios / 317 autos, esquema con 30 campos + auditoría, imágenes/teléfonos, snapshots de precios, normativa documentada, tasas y salarios referenciados, repositorios de modelos y dashboards.

**Lo que falta por conseguir:** extracción estructurada de año/km/marca/modelo/combustible/transmisión desde `ad_json`/`apollo_full`; montos de costos ocultos; precios de transacción reales; estadísticas oficiales cubanas de parque y matriculaciones; encuestas a compradores habaneros; series históricas de tasas y salarios digitalizadas; geocodificación de ubicaciones; validación en vivo de anuncios.

**EN.** The detailed framework covers nine blocks: decision, scope, theory, regulation, data architecture, descriptive analytics, causal/comparable analytics, interactive product, and validation/delivery. Existing assets and missing data needs are listed explicitly.

## 21. Cambio de objetivo / Objective change (18/11/2026)

A petición del usuario, el objetivo inmediato deja de ser la recomendación interactiva de compra y pasa a ser **un análisis de mercado**. En consecuencia:

- La fase 8 pasa a llamarse **Análisis de mercado, comparables y rentabilidad**.
- Se eliminan del alcance actual la ponderación de preferencias del usuario y el recomendador interactivo.
- Quedan como **especialización futura**: el producto que traduzca preocupaciones del usuario en una recomendación explicada.
- El marco detallado de la sección 20 se mantiene, pero sus bloques 1 y 8 se interpretan ahora como *objetivo del análisis* y *entregables del análisis*, respectivamente.

**EN.** At the user's request, the immediate objective becomes market analysis instead of interactive purchase recommendation. Phase 8 is renamed; user-preference weighting and the recommender are deferred to a later specialization.

## 22. Análisis descriptivo inicial / Initial descriptive analysis (18/11/2026)

Se creó `Auxiliares/herramientas/analisis_mercado.py`, que genera en `Data/analisis/`: `resumen_general.csv`, `precios_por_marca.csv`, `precios_por_municipio.csv`, `precios_por_anio.csv`, `outliers.csv`, `cobertura.csv`, `informe_descriptivo.md` y `dashboard.html`.

Resultados sobre 323 autos: 248 precios USD válidos (≥500 USD); 74 precios <500 USD marcados como inválidos y 1 en CUP excluidos. Precio mediano **22.000 USD**, media 24.416,59 USD, IQR 11.375–35.000 USD, rango 600–95.000 USD. Marca más frecuente: Hyundai (n=75); municipio con más oferta: Playa (n=53). Cobertura de campos derivados: marca 68,4 %, año 63,5 %, km 6,2 % (heurísticos, extraídos solo de título/descripción). Detectados 5 outliers por IQR.

**EN.** Initial descriptive analysis: 323 cars, 248 valid USD prices, median 22,000 USD, IQR 11,375–35,000, Hyundai and Playa leading, 5 IQR outliers. Derived year/km fields remain partial and heuristic.

## 23. Conversión elTOQUE, serie temporal y gráficas (18/11/2026)

Se amplió `analisis_mercado.py`:

- **Por año del vehículo**: `precios_por_anio.csv` con n, mediana USD, mediana CUP y tasa promedio; la conversión usa `precio_USD × TRMI elTOQUE` del día del anuncio (columna `Mediana` de `Anexos/Investigacion Cambios/trmi_USD.csv`).
- **Supuesto de anuncio activo**: todos los registros tienen `status=PUBLISHED` y página verificada en la captura, por lo que se asume que son comprables; no se comprueba disponibilidad en tiempo real.
- **Serie precio vs tasa**: `serie_precio_vs_tasa.csv` y `serie_precio_vs_tasa_mensual.csv`, con variación % diaria de la TRMI, del precio CUP y del precio USD. Ejemplo: la TRMI pasó de 680 CUP/USD (09/07/2026) a 920 (16-17/11/2026); la mediana mensual CUP subió de 12,58 M (julio) a 20,7 M (noviembre).
- **Gráficas**: `Auxiliares/herramientas/graficos_mercado.py` usa matplotlib, seaborn y plotly (instalados) y genera 8 PNG + `dashboard_interactivo.html` en `Data/analisis/graficos/`.

**EN.** Prices converted to CUP with elTOQUE daily TRMI, divided by vehicle year, with a daily/monthly price-vs-rate series and a full plotting module (matplotlib/seaborn/plotly). Active ads are assumed purchasable.

## 24. Estado del scrapeo y procesamiento de diccionarios (18/11/2026)

**Diccionarios/JSON guardados** (6.334/6.334 anuncios): `meta_json`, `ad_json` y `apollo_full`. En `ad_json` hay 21 claves, entre ellas `price`, `currency`, `status`, `updatedOnByUser`, `province`, `municipality`, `subcategory`, `imagesCount`, `viewCount`, `permalink`. En `apollo_full` hay cinco tipos: `ImageType`, `CategoryType`, `ProvinceType`, `MunicipalityType`, `AdType` y `ROOT_QUERY`. **No hay claves estructuradas de año, kilometraje, marca, modelo, combustible ni transmisión**: por eso `anio_est`, `marca_est` y `km_est` se derivan con regex del texto visible (cobertura 63,5 %, 68,4 % y 6,2 %). Los diccionarios se usan hoy para precio/moneda/estado/fecha/geografía y como respaldo de trazabilidad; `autos` no guarda esas columnas y se hace `JOIN` con `anuncios` para el análisis.

**Reporte de scrapeo:** `anuncios` 6.334 · `autos` 323 · `revision` 6.085 · `imagenes` 13.932 · `telefonos` 7.699 · BD 520,6 MB. Colas: `url_queue` 141 (125 done, 3 downloading, 13 pending); `download_queue` 125 (123 processed, 1 processing, 1 pending); `process_queue` 123 (107 committed, 16 pending). Los pendientes quedaron de una corrida interrumpida por reinicio del servidor. Snapshot `ultimo.json` de 17/11 04:44 (6.334 entradas); partes generadas: 0. `revolico-git.timer` activo (última ejecución 10:12). El análisis descriptivo y las 8 gráficas + dashboard ya están en `Data/analisis/`.

**EN.** JSON dictionaries hold price/currency/status/date/geography but no structured year/km/brand; those remain heuristic. Scrape report: 6,334 ads, 323 cars, 6,085 rejections, queues with pending items from an interrupted run, no DB chunks uploaded yet.

## 25. Reanudación, resiliencia y supuesto de catálogos (18/11/2026)

- **Librerías de mapas instaladas:** `geopandas 1.2.0`, `shapely 2.2.0`, `pyproj`, `folium 1.0.0`, `mapclassify`, `geopy` (además de matplotlib/seaborn/plotly ya instaladas).
- **Reinicio automático:** `revolico-scrape.service` ahora tiene `Restart=on-failure`, `RestartSec=30`, `StartLimitIntervalSec=300` y `StartLimitBurst=20`, de modo que una pérdida de conexión que detenga el proceso provoca su relanzamiento.
- **Supuesto de catálogos:** en `analisis_mercado.py` se añadió `add_publication_assumption()`. Para concesionarios y páginas similares (`CATALOGOS`) se asume que todo el catálogo está disponible salvo que la página indique lo contrario y que se publicó el día de la captura (`fecha_publicacion = scraped_at`); el año del vehículo no es clave. Para clasificados se mantiene el supuesto de anuncio activo = comprable, con `fecha_publicacion = updated_on_by_user`.
- **Reanudación:** se reanuda el pipeline desde las colas pendientes (13 URLs, 1 descarga y 16 decisiones pendientes) con `revolico-scrape.timer` activo e indefinido.

**EN.** Map libraries installed, systemd auto-restart added, catalog availability/publication-date assumption encoded, and the pipeline resumed from pending queues.

---

**Firma / Signature:** responsable del proyecto / project owner.  
**Última actualización / Last update:** 17/11/2026.
