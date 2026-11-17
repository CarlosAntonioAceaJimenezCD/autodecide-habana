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

El proyecto se llama **AutoDecide Habana**. Su objetivo es definir un producto interactivo capaz de recomendar la opción de compra más rentable en el mercado automotor de **La Habana**, a partir de los valores, preocupaciones y dificultades que el usuario introduzca (presupuesto, fiabilidad, consumo, mantenimiento, reventa, disponibilidad de piezas, etc.). Ese producto se apoya en dos pilares: un análisis del mercado automotor cubano y un pipeline de scraping reutilizable que se actualiza para adaptarse al momento en que se revise.

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
| 8 | Análisis, modelo de rentabilidad y producto interactivo | Pendiente |
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
5. El producto interactivo y el modelo de rentabilidad (fase 8) aún no están implementados.

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
| pendiente / pending | — | — | — | Ejecutar `reconstruir_revolico.py` / run it |

## 15. Eficiencia de Telegram, WhatsApp y Facebook / Efficiency of Telegram, WhatsApp and Facebook

**ES.** Para obtener más datos del mercado habanero, la ruta más eficiente es Telegram MTProto (`telethon`, ya integrado): sin navegador, con cursor incremental `min_id`/`offset_id`, búsqueda server-side y manejo de `FloodWaitError`. Le sigue Facebook GQL (`facebook_gql_scraper`): llamadas GraphQL con sesión autenticada y normalización con `price-parser`/`iso4217parse`, más rápido que Selenium. Para grupos de WhatsApp no existe API pública personal; la opción operativa es un servidor WAHA auto-hospedado y su REST (`/api/sessions`, `/api/{session}/chats`, `/api/{session}/chats/{chatId}/messages`) con deduplicación por id, que es lo que hace `whatsapp/waha_client.py`. Playwright/Selenium quedan como último recurso para páginas JS. La salida de las tres fuentes debe convergir en un esquema común (`fuente`, `id`, `chat/página`, `timestamp`, `texto`, `precio`, `moneda`, `url`) con dedup por `hash(fuente,id)` y sin datos personales.

**EN.** For more Havana market data, the most efficient route is Telegram MTProto (`telethon`, already integrated): no browser, incremental cursor, server-side search and `FloodWaitError` handling. Next is Facebook GQL: authenticated GraphQL calls with `price-parser`/`iso4217parse`, faster than Selenium. WhatsApp has no public personal API; the practical option is self-hosted WAHA REST with id deduplication, implemented in `waha_client.py`. Playwright/Selenium remain a last resort. All three should converge into a common schema with source-based deduplication and no personal data.

---

**Firma / Signature:** responsable del proyecto / project owner.  
**Última actualización / Last update:** 17/11/2026.
