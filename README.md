# AutoDecide Habana / AutoDecide Habana

> **ES** — Inteligencia del mercado automotor habanero, un producto interactivo que recomienda la opción de compra más rentable según las preocupaciones y dificultades del usuario, y un pipeline de scraping reutilizable que se adapta al momento en que se revise.
>
> **EN** — Intelligence on the Havana automotive market, an interactive product that recommends the most profitable purchase option based on the user's concerns and constraints, and a reusable scraping pipeline that adapts to the moment of review.

**Nombre del proyecto / Project name:** AutoDecide Habana  
**Nombre anterior / Former name:** ICD Automotive Market Project  
**Ubicación / Location:** `~/Proyectos/ICD Automotive Market Project`  
**Sugerencia de repositorio / Suggested repository:** `autodecide-habana`  
**Idioma / Language:** español e inglés / Spanish and English  
**Última actualización / Last update:** 17 de noviembre de 2026

---

## 1. Objetivo / Objective

**ES.** Construir un producto interactivo capaz de responder: *«dado mi presupuesto y mis preocupaciones (fiabilidad, consumo, mantenimiento, reventa, disponibilidad de piezas, etc.), cuál es la opción de compra más rentable en La Habana hoy?»*. Para ello se combinan tres líneas de trabajo:

1. **Análisis del mercado automotor cubano**, con foco exclusivo en **La Habana**, tanto en el canal formal (concesionarios e importadores autorizados) como en el informal (marketplaces y anuncios de compraventa).
2. **Producto interactivo de decisión**, que traduzca las preferencias del usuario en una recomendación de compra rentable.
3. **Pipeline de scraping reutilizable y adaptable**, capaz de actualizarse cuando cambian los sitios, los bloqueos o el contexto regulatorio.

**EN.** Build an interactive product able to answer: *"given my budget and my concerns (reliability, fuel use, maintenance, resale, spare parts availability, etc.), which purchase option is the most profitable in Havana today?"*. Three workstreams support it:

1. **Analysis of the Cuban automotive market**, focused only on **Havana**, covering both the formal channel (dealers and authorized importers) and the informal one (marketplaces and classified ads).
2. **Interactive decision product**, translating user preferences into a profitable purchase recommendation.
3. **Reusable, adaptive scraping pipeline**, able to update itself when sites, blocks or the regulatory context change.

---

## 2. Estado actual / Current status

| | Estado |
|---|---|
| **ES** | **Fase 6 — Scraping y captura de catálogos y anuncios**, en curso. Las fases 1-5 están completadas; las fases 7-9 están pendientes. |
| **EN** | **Phase 6 — Scraping and capture of catalogues and listings**, in progress. Phases 1-5 are complete; phases 7-9 are pending. |

La documentación (este `README.md` y el informe técnico) se ha creado como soporte transversal; **no cambia la fase activa del proyecto** / Documentation (this `README.md` and the technical report) was created as cross-cutting support and **does not change the active phase**.

---

## 3. Fases del proyecto / Project phases

| Fase / Phase | Nombre / Name | Estado / Status |
|---|---|---|
| 1 | Marco normativo y regulatorio / Regulatory framework | Completada / Complete |
| 2 | Descubrimiento y verificación de fuentes / Source discovery and verification | Completada / Complete |
| 3 | Infraestructura técnica y herramientas / Technical infrastructure and tools | Completada / Complete |
| 4 | Corpus documental y trabajos investigativos / Document corpus and research | Completada / Complete |
| 5 | Diseño del esquema de datos y del pipeline / Data schema and pipeline design | Completada / Complete |
| 6 | **Scraping y captura de catálogos y anuncios / Scraping and capture** | **En curso / In progress** |
| 7 | Unificación, limpieza y control de calidad / Unification, cleaning and QA | Pendiente / Pending |
| 8 | Análisis, modelo de rentabilidad y producto interactivo / Analysis, profitability model and interactive product | Pendiente / Pending |
| 9 | Documentación final, informe PDF y entrega / Final documentation, PDF report and delivery | Pendiente / Pending |

---

## 4. Estructura / Structure

```text
ICD Automotive Market Project/          # AutoDecide Habana
├── README.md                           # este archivo / this file
├── INFORME_TECNICO.md                  # informe bilingüe / bilingual report
├── INFORME_TECNICO.pdf                 # PDF generado desde el MD / PDF generated from MD
├── .gitignore                          # reglas para GitHub / GitHub rules
├── Anexos/                             # corpus legal y documentos de apoyo / legal corpus
├── Auxiliares/                         # entorno, herramientas y repositorios / env, tools, repos
│   ├── .venv/
│   ├── cache/
│   ├── herramientas/
│   │   ├── actualizar_informe.py       # actualiza MD + PDF / updates MD + PDF
│   │   ├── ddg_research.py
│   │   ├── buscar_fallback.py
│   │   ├── descargar_hombros.py
│   │   ├── scrape_concesionarios.py
│   │   ├── resumen_catalogos.py
│   │   └── README.md
│   ├── Repositorios/
│   └── Repositorios Referencias/
├── Copias/                             # 4 repos de referencia / 4 reference repos
│   ├── AutosxCuba/
│   ├── analisis-del-mercado-de-motos-bicicletas-patinetes/
│   ├── taso-api/
│   └── guani-saimc/
├── Data/                               # investigaciones, verificación y SQLite / research and data
│   └── catalogos_concesionarios/
└── Hombros/                            # PDFs, HTML, repos y derivadas / downloads
```

`Copias/` está presente en el proyecto pero **no se registra en el informe técnico** por decisión explícita / `Copias/` exists in the project but is **excluded from the technical report** by explicit decision.

---

## 5. Documentos y registro de altas / Documents and change log

- **Informe técnico:** `INFORME_TECNICO.md` (fuente) y `INFORME_TECNICO.pdf` (entregable).
- **Registro de altas:** sección `Registro de altas / Change log` del informe. Todo lo nuevo que se añada a la carpeta del proyecto se registra con fecha, ruta, tipo, origen, tamaño, fase, descripción y estado.
- **Actualización:** ejecutar:

```bash
cd "~/Proyectos/ICD Automotive Market Project"
Auxiliares/.venv/bin/python Auxiliares/herramientas/actualizar_informe.py
```

El script detecta archivos y carpetas nuevos, añade las entradas y regenera el PDF con LibreOffice. Si no existe el archivo de estado, lo crea como línea base sin registros / The script detects new files and folders, appends entries and regenerates the PDF with LibreOffice. If no state file exists, it creates a baseline without entries.

---

## 6. Uso rápido / Quick start

```bash
cd "~/Proyectos/ICD Automotive Market Project/Auxiliares"
.venv/bin/pip install curl_cffi ddgs tenacity trafilatura pandas playwright

.venv/bin/python herramientas/ddg_research.py search "consulta" --pages 30 --delay 7
.venv/bin/python herramientas/ddg_research.py analyze "consulta" --out ../Data/analisis.md
.venv/bin/python herramientas/descargar_hombros.py --query "consulta" --out ../Hombros/mi_busqueda
.venv/bin/python herramientas/scrape_concesionarios.py
.venv/bin/python herramientas/resumen_catalogos.py
```

---

## 7. Marco legal / Legal framework

El proyecto respeta los términos de uso de cada portal: no elude mecanismos anti-automatización, no recopila datos personales de anunciantes y conserva la procedencia de cada dato. El marco del mercado automotor está constituido por el **Decreto 163/2026** (Gaceta Oficial No. 65 Ordinaria, 04/08/2026, vigente desde el 11/08/2026) y las resoluciones 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171-175/2026 (MFP), 312/2026 (Aduana) y 102/2026 (BCC). Antes de publicar cualquier resultado deben verificarse además las normas vigentes cubanas sobre protección de datos personales, ciberseguridad y derechos de autor. Detalle en el informe técnico.

The project respects each site's terms of use: it does not bypass anti-automation mechanisms, does not collect personal data from advertisers, and preserves the provenance of every datum. The automotive market framework is **Decree 163/2026** (Official Gazette No. 65, 04/08/2026, in force since 11/08/2026) plus resolutions 104/2026 (MINCEX), 17/2026 (MINCIN), 52/2026 (MITRANS), 171-175/2026 (MFP), 312/2026 (Customs) and 102/2026 (BCC). Before publishing results, current Cuban rules on personal data protection, cybersecurity and copyright must also be verified. See the technical report.

---

## 8. Subida a GitHub / Publishing to GitHub

El repositorio local ya está inicializado pero **no tiene commits**. Antes de subir:

1. **No subir los repositorios auxiliares usados.** Quedan excluidos en `.gitignore`: `Auxiliares/Repositorios/`, `Auxiliares/Repositorios Referencias/`, `Hombros/03_Repositorios/` y `Copias/`. Solo se listan como referencia al final de este README.
2. Tampoco se versionan `Auxiliares/.venv/`, `Auxiliares/cache/`, `Anexos/Leyes/` completo ni las `.sqlite` grandes sin Git LFS.
3. Verificar que no haya secretos (tokens de API, claves de Telegram, etc.).
4. Crear el repositorio remoto `autodecide-habana` y ejecutar:

```bash
git add README.md INFORME_TECNICO.md INFORME_TECNICO.pdf .gitignore Auxiliares/herramientas Data Hombros
git commit -m "docs: nombre del proyecto, fases, informe bilingüe y script de altas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/autodecide-habana.git
git push -u origin main
```

Para corpus grandes, usar Git LFS o almacenamiento externo y dejar en el repositorio solo manifiestos y scripts de descarga.

**EN — Publishing framework:** the local repo has no commits yet. Do **not** upload auxiliary repositories; they are ignored and listed only at the end of this README. Check `.gitignore`, remove secrets, then commit the documentation, tools, `Data/` and `Hombros/` (not ignored), create the remote `autodecide-habana` and push. Use Git LFS or external storage for large corpora and databases.

---

## 9. Limitaciones / Limitations

- El análisis se limita a **La Habana** / Analysis is limited to **Havana**.
- `carrosw` sigue protegido por verificación de bot / `carrosw` remains behind bot verification.
- Los catálogos actuales contienen 256 filas en 11 tiendas; BDC One y Changan publican parte de su catálogo en PDF / Current catalogues contain 256 rows across 11 stores.
- La fase 8 (modelo de rentabilidad y producto interactivo) aún no está implementada / Phase 8 (profitability model and interactive product) is not implemented yet.

---

## 10. Repositorios auxiliares usados (solo referencia) / Auxiliary repositories used (reference only)

**ES.** Estos repositorios se usaron como herramientas o referencia, pero **no se suben a GitHub**: están excluidos en `.gitignore` y solo se enumeran aquí.

**EN.** These repositories were used as tools or references, but they are **not uploaded to GitHub**: they are excluded in `.gitignore` and listed here only.

### Infraestructura, scraping y evasión de bloqueos / Infrastructure, scraping and anti-block tooling (61)

```text
AZeC4/TelegramGroup · AstrBotDevs/AstrBot · CloakHQ/CloakBrowser · D4Vinci/Scrapling · DIYgod/RSSHub · DrKLO/Telegram · FlareSolverr/FlareSolverr · JustSxm/Deals-Scraper · Kaliiiiiiiiii-Vinyzu/patchright · Kaliiiiiiiiii-Vinyzu/patchright-python · LonamiWebs/Telethon · MasuRii/FBScrapeIdeas · ScrapeGraphAI/Scrapegraph-ai · WhiskeySockets/Baileys · XD-MHLOO/facebook-gql-scraper · abhishekjnvk/telegram-channel-downloader · adbar/trafilatura · apify/crawlee · apify/crawlee-python · apurvmishra99/facebook-scraper-selenium · browser-use/browser-use · browserbase/stagehand · chris124567/cfsolve · dessant/buster · devlikeapro/waha · dgtlmoon/changedetection.io · eternnoir/pyTelegramBotAPI · evolution-foundation/evolution-api · firecrawl/firecrawl · getmaxun/maxun · gosom/google-maps-scraper · hamodywe/telegram-scraper-TeleGraphite · iyear/tdl · jhy/jsoup · jo-inc/camofox-browser · kevinzg/facebook-scraper · lexiforest/curl_cffi · lharries/whatsapp-mcp · lorien/awesome-web-scraping · mohdtalal3/facebook_post_comment_scraper · passivebot/facebook-marketplace-scraper · paulpierre/informer · pyrogram/pyrogram · python-telegram-bot/python-telegram-bot · rmyndharis/OpenWA · sarperavci/CloudflareBypassForScraping · scrapfly/Antibot-Detector · scrapy/scrapy · seleniumbase/SeleniumBase · shaikhsajid1111/facebook_page_scraper · sml2h3/ddddocr · tdlib/td · telegraf/telegraf · telegramdesktop/tdesktop · tulir/whatsmeow · ultrafunkamsterdam/nodriver · unclecode/crawl4ai · vespertiliamvir/FacebookMarketplaceScraper · wwebjs/whatsapp-web.js · xHossein/PyPasser · yagop/node-telegram-bot-api
```

### Referencias de mercado automotriz / Automotive market references (28 + 4)

```text
KoushikRao123/Automotive-Feature-and-Price-Analysis-using-Regex · JKomskis/Car-Inventory-Scraper · Mahmoud-Elsokary/Cars-Market-Listings-Analysis-Python-Pandas-Matplotlib-Seaborn · yoskev/Data-Analysis-Project-Sales-Marketing-Automotive-Car-Analysis · abdlrhmnmo/Dongfeng-Al-Ahram-Report-Market-Dashboard · moatasimyakoub92-dot/Egyptian-Used-Cars · AdwaithKalathil/IDSE-DATA-SCIENCE-PROJECT- · KiarashShayegani/Iran-Car-Market-Intelligence · MADZIVI/TradeSmart-AI · anshh-py/Vehicle-IQ · AnalistaDanielLlado/analisis-mercado-automotriz-espana · kaje94/auto-marketplace · Danail-A/automotive-market-intelligence · api-evangelist/carsxe · dmitriibilecki/automotive-market-intelligence · axiom-stat/econometric-market-valuation · luminati-io/facebook-marketplace-dataset-samples · Sama256/japan-auto-intelligence · michaelocez/nz-vehicle-market-tracker · nickholttt/nzta-analytics-dashboard · 2scraper/spinny-scraper · Busayosage/uk-automotive-transition · atushi1841/upgarage-parts-scraper · AvinabhDutta-Dev/used-cars-price-prediction · Bhavya-rajyaguru/vahan-india-automotive-market-2025 · tatendagonzo/zimbabwe-used-vehicle-market-analysis
```

### Copias locales en `Copias/` / Local copies in `Copias/` (4, excluidas también del informe técnico)

```text
anapaula65/AutosxCuba · AdrianaAmadorVerdecia/analisis-del-mercado-de-motos-bicicletas-patinetes · arielhechavaria/guani-saimc · TASALO-TEAM/taso-api
```

### Otros / Other

```text
jmev1/TFG-2026
```
