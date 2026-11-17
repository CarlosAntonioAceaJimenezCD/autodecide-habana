# Análisis descriptivo inicial — mercado de autos usados en La Habana

**Fecha:** 18/11/2026  
**Fuente:** `Data/Revolico/revolico.sqlite`, tablas `autos` + `anuncios`  
**Nivel de confianza:** anuncios (precio pedido, no transacción)  
**Moneda del análisis:** USD (322 de 323 autos; 1 en CUP se excluye del precio)
**Precios descartados por inválidos (<500 USD):** 74 (se conservan en la BD, no se usan en estadísticos)

## 1. Cobertura de datos

| campo             |   disponibles |   total |   cobertura_% |
|:------------------|--------------:|--------:|--------------:|
| price             |           323 |     323 |         100   |
| currency          |           323 |     323 |         100   |
| municipality_name |           323 |     323 |         100   |
| marca_est         |           221 |     323 |          68.4 |
| anio_est          |           205 |     323 |          63.5 |
| km_est            |            20 |     323 |           6.2 |

## 2. Estadísticos generales (USD)

| estadístico   |   valor |
|:--------------|--------:|
| n             |   248   |
| media         | 24416.6 |
| mediana       | 22000   |
| p25           | 11375   |
| p75           | 35000   |
| min           |   600   |
| max           | 95000   |
| desviacion    | 16649.3 |

## 3. Precios por marca estimada (n ≥ 3)

| marca_est   |   n |   mediana |   p25 |   p75 |   minimo |   maximo |
|:------------|----:|----------:|------:|------:|---------:|---------:|
| hyundai     |  55 |     28000 | 20250 | 35000 |     5000 |    83000 |
| kia         |  20 |     21500 | 18500 | 33925 |    15500 |    34000 |
| toyota      |  18 |     14000 | 11500 | 33000 |     3800 |    42000 |
| chevrolet   |  11 |     18000 | 13750 | 22000 |     7000 |    28000 |
| honda       |  11 |     27000 | 24675 | 29500 |    12000 |    38000 |
| audi        |  10 |     41000 | 17500 | 45000 |     8000 |    95000 |
| peugeot     |  10 |      7500 |  5000 | 15000 |     5000 |    16000 |
| nissan      |   8 |     25500 | 16000 | 30250 |     7800 |    40000 |
| fiat        |   6 |      4750 |  2625 |  8750 |     1800 |    28000 |
| mercedes    |   5 |     52000 | 25000 | 60000 |    25000 |    80000 |
| mg          |   5 |     15000 | 15000 | 15000 |    15000 |    26500 |
| bmw         |   4 |     33500 | 28625 | 47500 |    18500 |    85000 |
| dongfeng    |   4 |     31500 | 28000 | 35000 |    28000 |    35000 |
| geely       |   4 |     10250 |  8825 | 11250 |     6800 |    12000 |
| ford        |   3 |     10000 |  7250 | 22500 |     4500 |    35000 |
| vw          |   3 |     36000 | 19750 | 37500 |     3500 |    39000 |

## 4. Precios por municipio (n ≥ 3)

| municipality_name     |   n |   mediana |   p25 |     p75 |   minimo |   maximo |
|:----------------------|----:|----------:|------:|--------:|---------:|---------:|
| Playa                 |  46 |     23750 | 18875 | 36000   |      650 |    85000 |
| Cerro                 |  33 |     24000 | 11500 | 34000   |     1100 |    95000 |
| Arroyo Naranjo        |  29 |     28000 | 11000 | 37000   |     2000 |    45000 |
| Centro Habana         |  26 |     27000 | 18500 | 34000   |      600 |    65000 |
| Plaza                 |  24 |     17750 |  9500 | 22000   |     1600 |    43000 |
| Habana del Este       |  21 |     34000 | 16000 | 45000   |     2000 |    75000 |
| Diez de Octubre       |  16 |     15000 |  8375 | 26506.2 |     4000 |    48300 |
| Boyeros               |  12 |     14000 |  5000 | 23625   |     5000 |    40000 |
| La Lisa               |   8 |     13500 | 10000 | 31250   |     3800 |    35000 |
| Marianao              |   7 |     15000 | 15000 | 20250   |     9500 |    45000 |
| Habana Vieja          |   4 |     16750 |  7000 | 29375   |     7000 |    38000 |
| San Miguel del Padrón |   4 |     11250 |  8375 | 13000   |     3500 |    14500 |
| Pinar del Río         |   3 |     30000 | 21500 | 34000   |    13000 |    38000 |

## 5. Precios por año estimado (n ≥ 3)

|   anio_est |   n |   mediana |   p25 |   p75 |   minimo |   maximo |
|-----------:|----:|----------:|------:|------:|---------:|---------:|
|       2022 |  28 |     33450 | 30250 | 35250 |    14000 |    80000 |
|       2019 |  20 |     19000 | 15575 | 25750 |    15000 |    53000 |
|       2021 |  18 |     28750 | 25750 | 40750 |     8000 |    60000 |
|       2017 |  17 |     24675 | 21000 | 42000 |    18000 |    45000 |
|       2023 |  16 |     32000 | 20375 | 41250 |    12000 |    95000 |
|       2024 |  16 |     35350 | 30000 | 38000 |     3800 |    42000 |
|       2020 |  11 |     21000 | 18500 | 41000 |    10000 |    85000 |
|       2026 |   9 |     35000 | 27000 | 35000 |    25500 |    83000 |
|       2005 |   6 |     11500 | 11500 | 11875 |     6000 |    12000 |
|       2018 |   6 |     18000 | 16000 | 21500 |    15000 |    65000 |
|       1957 |   5 |     22000 | 22000 | 22000 |     7800 |    22000 |
|       2025 |   5 |     28000 | 26500 | 60000 |    24000 |    75000 |
|       2009 |   3 |     10000 |  9750 | 11000 |     9500 |    12000 |
|       2016 |   3 |     17000 | 17000 | 28500 |    17000 |    40000 |

## 6. Outliers por IQR (precio USD)

Límites: [-24,062, 70,438] USD. Total: **5**.

|       id | title                                                  |   price | marca_est   |   anio_est |
|---------:|:-------------------------------------------------------|--------:|:------------|-----------:|
| 52651826 | Mercedes Benz C300e 2022 híbrido gasolina y electrico. |   80000 | mercedes    |       2022 |
| 57875714 | Audi e-tron GT performance  2023 con 23 mil millas     |   95000 | audi        |       2023 |
| 58348032 | HYUNDAI PALISADE CALLIGRAPHY 2026                      |   83000 | hyundai     |       2026 |
| 56412195 | 🔥 INFINITI QX60 2025 – 7 PLAZAS 🔥                      |   75000 | nan         |       2025 |
| 58733654 | BMW X6 M50i 2020                                       |   85000 | bmw         |       2020 |

## 7. Limitaciones

- `marca_est`, `anio_est` y `km_est` son **heurísticos** (regex sobre título/descripción/ad_json).
- `km_est` tiene baja cobertura y puede contener errores; no se usa para precio/km aún.
- Los precios son **anunciados**, no precios de transacción.
- No se dispone aún de combustible/transmisión estructurados ni de costos ocultos.
- Los precios <500 USD se marcan como inválidos y se excluyen de los estadísticos, pero no se borran.
- 1 anuncio en CUP queda fuera del análisis de precios para no mezclar monedas.
