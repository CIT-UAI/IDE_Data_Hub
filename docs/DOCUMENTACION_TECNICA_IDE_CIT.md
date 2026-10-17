# 🌐 Infraestructura de Datos Espaciales (IDE CIT) — Documentación Técnica, Estándares de Arquitectura y Registro Algorítmico

> **Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez**  
> **Ecosistema**: MBHT (Matriz de Bienestar Humano Territorial) · IDE 4.0 Cloud-Native Geospatial  
> **Versión de la IDE**: 2026.1 · **Dataset Canónico**: v1.0.3 (Octubre 2026)  
> **Contacto y Custodia Institucional**: `contactocit@uai.cl` / `https://ide.cit.uai.cl`  

---

## 🏛️ 1. Arquitectura General y Propósito

La **IDE CIT** es la infraestructura de datos espaciales institucional, de acceso abierto y reproducible del Centro de Inteligencia Territorial de la Universidad Adolfo Ibáñez. Su diseño representa un cambio paradigmático respecto a los geoportales tradicionales: combina el acceso abierto universal a microdatos territoriales, especificaciones **Cloud-Native Geospatial (GeoParquet 1.1, STAC 1.0.0, Mapbox Vector Tiles)**, trazabilidad de código con verificación criptográfica SHA-256, y **preparación semántica para Inteligencia Artificial (AI-Readiness)** mediante catálogos legibles por máquinas (`DCAT-AP 2.0`, `Schema.org JSON-LD` y endpoints estructurados).

### 1.1 Coberturas Territoriales Maestras

1. **MBHT 2017 (Línea Base Censal Oficial)**:
   - **204.906 manzanas censales** en las 16 regiones de Chile, abarcando **345 comunas amanzanadas** (de las 346 comunas nacionales; la Comuna de Antártica no posee manzanas censales habitadas y es administrada por Cabo de Hornos).
   - **55.035 equipamientos esenciales** georreferenciados (salud primaria y hospitalaria, educación parvularia/básica/media, áreas verdes públicas, deporte, cultura y servicios comunitarios).
   - **1.589.595 tramos viales caminables** con topología validada y ruteo peatonal.
   - **18 indicadores elementales** en 4 macro-dimensiones, sintetizados mediante el **Axioma de Neutralidad Elemental** ($W(D) = n_D / N_{\text{total}}$).
   - Cuadratura exacta ($\Delta = 0$) entre el consolidado nacional y los 16 paquetes regionales descargables.
2. **PEM / SBAP (Planificación Espacial Marina)**:
   - Maritorio continental e insular chileno, Zona Económica Exclusiva (ZEE) de 200 millas náuticas y Áreas Marinas Protegidas (AMCP-MU) bajo la Ley N° 21.600 (SBAP).
3. **Censo 2024 (Imputaciones Demográficas Sprague)**:
   - Geometrías de polígonos oficiales del Instituto Nacional de Estadísticas (INE).
   - Desagregación etaria y por sexo en 42 cohortes mediante el algoritmo osculatorio de 5.º orden de Sprague acoplado al método de mayor resto (Hamilton-Hare), conservando con rigor matemático los totales comunales censales oficiales y salvaguardando el secreto estadístico (Ley N° 17.374).
4. **INSE (Estratificación Socioeconómica Territorial)**:
   - Índice de Nivel Socioeconómico a nivel de manzanas y entidades rurales para todo Chile, clasificado en 5 quintiles metodológicos.
5. **SII (Áreas Homogéneas y Avalúos Fiscales)**:
   - Catastro nacional de 14.157 polígonos de valor guía de terreno (VGT) y avalúos bajo la Ley N° 17.235.
6. **MBHT 2024 (Nueva Línea Base Nacional)**:
   - En proceso de calibración institucional final con ministerios y organismos públicos. Publicada con pre-aviso metodológico en el catálogo STAC (`stac/mbht_2024.json`).

---

## ⚙️ 2. Pipeline de Compilación y Certificación en 10 Etapas (`compilar_ecosistema.py`)

Toda la infraestructura se compila, valida y audita de manera 100% determinista mediante el orquestador central `compilar_ecosistema.py` (ejecutable desde la raíz del proyecto), el cual coordina 10 etapas algorítmicas secuenciales en `src/`:

```
07_Aplicaciones_y_Visualizadores_Web/IDE_Data_Hub/
├── compilar_ecosistema.py                    # Orquestador maestro de certificación y compilación
├── version.json                              # Manifiesto de compilación y control de caché
├── data/
│   ├── catalogo_ide_cit.json                 # Fuente única de verdad (Single Source of Truth)
│   ├── dcat.json                             # Catálogo semántico W3C DCAT-AP 2.0
│   ├── connection_examples.json              # Ejemplos ejecutables Python / DuckDB / QGIS
│   ├── iso_xml/                              # Metadatos normalizados XML ISO 19139 (Perfil SNIT)
│   └── stac/                                 # Colección y catálogo STAC 1.0.0
├── src/
│   ├── validador_metadatos_iso.py            # [Etapa 1] Auditoría ISO 19115 y exportador XML/STAC
│   ├── generar_connection_examples.py        # [Etapa 2] Generador de recetas de consumo multilingüe
│   ├── generador_ficha_dataset.py            # [Etapa 3] Ficha técnica metodológica exhaustiva 17D
│   ├── generador_descargas_2017.py           # [Etapa 4] Centro de descargas y verificador SHA-256
│   ├── generador_guia_tecnica.py             # [Etapa 5] Guía técnica de interoperabilidad y geodésica
│   ├── generador_red_ides.py                 # [Etapa 6] Directorio de 19 geoportales SNIT Chile
│   ├── generador_portal_ide_cit.py           # [Etapa 7] Portal web, buscador y Copiloto IA CIT
│   ├── generar_recursos_qgis_y_stac.py       # [Etapa 8] STAC 1.0.0, QGIS (.qlr) y Clean URLs
│   ├── auditor_calidad_html.py               # [Etapa 9] Auditoría integral de accesibilidad y hashes
│   └── auditor_adversarial_ide.py            # [Etapa 10] Auditoría adversarial continua (sonda HTTP)
├── public/                                   # Artefactos web compilados listos para distribución
└── docs/
    └── DOCUMENTACION_TECNICA_IDE_CIT.md      # (Este archivo) Registro maestro de arquitectura
```

### 📋 Detalle de las 10 Etapas del Pipeline

1. **Etapa 1: `validador_metadatos_iso.py`**:
   - Audita el 100% de los metadatos contra el perfil nacional SNIT (ISO 19115-1:2014) y genera los archivos XML ISO 19139 para cosecha por Geonetwork/CKAN.
   - Exporta la colección base STAC 1.0.0 (`data/stac/collection.json`) con extensión de proyección (`proj:epsg: 4326`), proveedores institucionales y enlaces formales.
2. **Etapa 2: `generar_connection_examples.py`**:
   - Genera `connection_examples.json` con snippets verificados para DuckDB, Python (`geopandas`, `pyarrow`), R (`sf`), cURL y QGIS.
3. **Etapa 3: `generador_ficha_dataset.py`**:
   - Compila la ficha técnica exhaustiva (`ficha-mbht-2017.html`), con linaje detallado, inventarios de equipamientos, formulaciones matemáticas completas (Tobler, E2SFCA) y KaTeX integrado.
4. **Etapa 4: `generador_descargas_2017.py`**:
   - Ensambla el centro de descargas (`descargas-2017.html` / `descargas.html`) con los 208 paquetes regionales y nacionales (GeoParquet, GPKG, Shapefile, CSV), integrando un verificador criptográfico SHA-256 en el navegador con Web Crypto API.
5. **Etapa 5: `generador_guia_tecnica.py`**:
   - Compila la guía metodológica y de interoperabilidad (`guia-tecnica.html`), documentando el marco normativo chileno, marco geodésico (SIRGAS-Chile / WGS 84), especificaciones OGC y el ejemplo reproducible end-to-end con script de prueba R15.
6. **Etapa 6: `generador_red_ides.py`**:
   - Genera el geoportal de articulación institucional (`red-ides.html`) con 19 nodos oficiales del SNIT Chile (IDE Chile, MINVU, MMA, MOP, CIREN, INE, CONAF, etc.).
7. **Etapa 7: `generador_portal_ide_cit.py`**:
   - Ensambla el portal principal (`index.html` / `inicio.html`), la suite semántica (`data/catalogo_ide_cit.csv`, `data/dcat.json`), metadatos Schema.org JSON-LD para motores de búsqueda, `sitemap.xml`, `robots.txt` y el Copiloto IA Territorial con síntesis de voz (TTS) y memoria episódica.
8. **Etapa 8: `generar_recursos_qgis_y_stac.py`**:
   - Construye el catálogo STAC 1.0.0 estático de alta disponibilidad (`stac/catalog.json` y 5 colecciones temáticas con proyección `proj:epsg: 4326`, enlaces `describedby`, `about`, `license` y activos de metadatos).
   - Genera archivos de definición de capas de QGIS (`.qlr`) y estructura las Clean URLs amigables en `public/`.
9. **Etapa 9: `auditor_calidad_html.py`**:
   - Inspecciona la validez semántica HTML5, atributos ARIA de accesibilidad (WCAG 2.1 AA), consistencia de hashes SHA-256 e integridad de enlaces internos y externos.
10. **Etapa 10: `auditor_adversarial_ide.py`**:
    - Ejecuta pruebas adversariales continuas: comprobación de inyección de código, higiene de rutas relativas/absolutas, cuadratura demográfica y aritmética estricta, y sondeo HTTP de disponibilidad.

---

## 📊 3. Estándar de Metadatos y Esquema Dual de Datos (`catalogo_ide_cit.json`)

El catálogo institucional opera como **Fuente Única de Verdad (Single Source of Truth)**. Cada capa cuenta con una definición estricta:

```json
{
  "id": "kpi_mud_2017",
  "titulo": "MBHT 2017 — Matriz de Manzanas Censales e Indicadores de Calidad de Vida Urbana",
  "matriz": "mbht",
  "ambito": "tierra",
  "escala": "Manzana Censal (204.906 unidades)",
  "cobertura": "Nacional (16 Regiones de Chile)",
  "bbox": [-109.5, -56.54, -66.42, -17.50],
  "crs": "EPSG:4326 (WGS 84)",
  "tipo_geometria": "MultiPolygon",
  "formula_lineage": "E2SFCA sobre red vial con función de impedancia peatonal de Tobler modificada...",
  "tile_source": "kpi_mud",
  "s3_parquet": "download/MBHT_2017_Nacional_Manzanas.parquet"
}
```

### 3.1 Esquema Dual: Datos Analíticos vs. Teselas Vectoriales

Para optimizar tanto el análisis científico intensivo como la visualización fluida en navegadores web, la IDE CIT implementa un **diseño de esquema dual**:

- **Esquema Analítico Completo (42 columnas en GeoParquet, GeoPackage, Shapefile, CSV)**:
  Contiene los identificadores censales INE (`id_manzcit`, `comuna`, `cod_reg`), variables demográficas (`personas`, `hogares`, `viv_part`), los 6 indicadores peatonales puros (`isal`, `ise`, `iav`, `idep`, `icul`, `iser`), las 4 macro-dimensiones normalizadas (`dim_acc`, `dim_soc`, `dim_seg`, `dim_amb`), el índice final de Bienestar Humano Territorial (`bht`) y la clasificación de Entorno Urbano (`entorno_urbano`).
- **Esquema de Teselas Vectoriales MVT (16 atributos optimizados)**:
  Diseñado para consumo ultra-rápido en WebGL (< 150 ms) en clientes móviles y navegadores, incluyendo únicamente los campos esenciales de visualización, clasificación de Jenks y nombres administrativos.

---

## 🧭 4. Marco Geodésico Nacional, Geodinámica y Sistemas de Coordenadas (ISO 19111)

En estricta conformidad con el marco geodésico oficial del Estado de Chile (Decreto Supremo N° 215/2004 y Res. Ex. N° 34/2018 del Ministerio de Bienes Nacionales e Instituto Geográfico Militar — IGM), la IDE CIT diferencia formalmente entre marco de referencia geodésico, datum elipsoidal, geodinámica activa, CRS de almacenamiento cloud-native y CRS proyectados de análisis:

| Componente Geodésico | Estándar Oficial / Especificación | Fundamento Técnico |
| :--- | :--- | :--- |
| **Marco de Referencia Oficial** | **SIRGAS-Chile** (realización ITRF densificada) | Marco oficial legal de la República de Chile, fijado a la Placa Sudamericana. |
| **Elipsoide de Referencia** | **GRS80** ($a = 6.378.137\text{ m}$, $1/f = 298{,}257222101$) | Geodetic Reference System 1980, adoptado por IUGG y SIRGAS. |
| **CRS de Almacenamiento e Intercambio** | **WGS 84 (EPSG:4326)** | Coordenadas geográficas 2D [latitud, longitud] en grados decimales. Estándar canónico universal para GeoParquet 1.1, STAC 1.0.0, GeoJSON y MVT. |
| **Concordancia GRS80 vs. WGS 84** | Discrepancia elipsoidal: $\Delta b \approx 0{,}105\text{ mm}$ | La diferencia puramente geométrica entre el elipsoide GRS80 y el WGS 84 ($1/f = 298{,}257223563$) es sub-milimétrica en el semieje menor. |
| **Deriva Geodinámica de Placa** | $\sim 2\text{ a }3\text{ cm/año}$ hacia el ENE | Movimiento tectónico continuo de la Placa Sudamericana con respecto al marco global ITRF. Para escalas cartográficas urbanas y censales ($> 1:1.000$), las coordenadas en WGS 84 y SIRGAS-Chile son operativamente equivalentes sin sesgos métricos perceptibles. |
| **CRS Proyectados para Cálculo Métrico** | **UTM Husos 18S, 19S, 12S y 17S** (WGS 84 / SIRGAS-Chile) | Los motores espaciales del CIT-UAI proyectan internamente a: **UTM Huso 18S (EPSG:32718)** y **UTM Huso 19S (EPSG:32719)** en territorio continental; **UTM Huso 12S (EPSG:32712)** en Rapa Nui; y **UTM Huso 17S (EPSG:32717)** en Juan Fernández. Esto elimina distorsiones de distancia métrica en grafos y pendientes DEM. |

---

## 🛡️ 5. Arquitectura de Seguridad, Privacidad y Disponibilidad (OWASP ASVS 5.0)

La Infraestructura de Datos Espaciales (IDE CIT) implementa una arquitectura cloud-native de alta seguridad y disponibilidad, alineada con las directivas del estándar **OWASP Application Security Verification Standard (ASVS 5.0.0 Nivel 2)** y el marco legal chileno:

### 5.1 Matriz de Controles Técnicos de Seguridad

| Dominio ASVS | Control Implementado | Evidencia y Configuración |
| :--- | :--- | :--- |
| **V1: Arquitectura** | Aislamiento estricto de componentes | Almacenamiento S3 protegido con *Origin Access Control* (OAC); acceso web canalizado exclusivamente a través de CDN CloudFront. |
| **V2: Autenticación / Acceso** | Principio de menor privilegio y lectura pública segura | APIs y catálogos operan en modo solo lectura (`GET`/`HEAD`); modificaciones restringidas a pipelines autenticados por IAM con MFA. |
| **V5: Validación y Sanitización** | Prevención anti-DOM-XSS y validación de tipos | Escape contextual de entidades HTML, tipado estricto en el generador web y desinfección exhaustiva antes de renderizado dinámico en el DOM. |
| **V8: Protección de Datos** | Integridad criptográfica SHA-256 | Sumas de verificación SHA-256 precalculadas e inmutables para todos los datasets vectoriales y tabulares (`download/archivos_hash_manifest.json`). |
| **V9: Comunicaciones** | Cifrado en tránsito forzado | TLS 1.3 / 1.2 forzado en CloudFront con cabecera HSTS `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`. |
| **V10: Cabeceras HTTP** | Blindaje contra ataques de contenido | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, CORS abierto para lectura de datos geográficos (`GET`, `HEAD`). |
| **V14: Configuración** | Cero exposición de secretos o credenciales | La plataforma web no almacena llaves privadas en el frontend ni expone credenciales de infraestructura en los repositorios públicos de GitHub. |

### 5.2 Privacidad y Secreto Estadístico (Ley N° 17.374)
- **Secreto Estadístico**: En estricto cumplimiento de la Ley 17.374 del INE, todos los datos geoespaciales agregan la información a nivel de manzana censal o polígonos territoriales mayores.
- **Cero Microdatos Personales**: No se almacenan ni publican identidades individuales, números de cédula (RUT), nombres de propietarios ni localizaciones de domicilios particulares.
- **Imputación con Conservación Total**: Las estimaciones demográficas (Sprague) conservan con exactitud las sumas poblacionales comunales oficiales.

---

## ⚖️ 6. Marco Dual de Aseguramiento de Calidad: Data Quality vs. Model Quality

Uno de los aportes más distintivos de la IDE CIT es la separación formal y metodológica entre la **Calidad Física de los Datos (Data Quality)** y la **Calidad y Rigor del Modelo Espacial (Model Quality)**:

### 6.1 Data Quality (Integridad Física, Estructural y Topológica del Dato)

- **Completitud Exhaustiva (100%)**:
  Verificación de 204.906 manzanas censales con sus 42 campos físicos en los 16 archivos regionales y el nacional consolidado, sin filas truncadas, columnas ausentes ni nulos espurios.
- **Topología Vial y Ruteo Conexo**:
  Grafo vial nacional de 1.589.595 tramos con verificación de *snapping* a 0,5 m y *split* en intersecciones viales.
- **Inmutabilidad Criptográfica SHA-256**:
  Certificación bit a bit de cada uno de los 208 archivos disponibles en el centro de descargas mediante sumas criptográficas SHA-256 (64 hex), verificables en el cliente mediante la Web Crypto API nativa.

### 6.2 Model Quality (Rigor Epistemológico, Físico y Territorial del Modelo)

- **Axioma de Neutralidad Elemental ($W(D) = n_D / N_{\text{total}}$)**:
  En la formulación oficial del CIT-UAI, cada indicador elemental de bienestar posee igual peso relativo de línea base ($1 / N_{\text{total}}$). Queda formalmente prohibido promediar dimensiones como si fueran variables homogéneas, lo cual sobreponderaría artificialmente dimensiones con pocos indicadores.
- **Impedancia Peatonal Física sobre Red Vial (Cero Distancia Euclidiana)**:
  Todo traslado humano se modela estrictamente a lo largo del grafo de ejes viales caminables, aplicando la función cinemática de Tobler modificada por pendientes topográficas (DEM):
  $$W(S) = 6 \cdot \exp\left(-3{,}5 \cdot |S + 0{,}05|\right)$$
  - En terreno plano ($S = 0$): velocidad teórica de $5{,}04\text{ km/h}$.
  - En pendiente ascendente del 15% ($S = +0{,}15$): velocidad de $2{,}98\text{ km/h}$ (reducción de un 40,8%).
  - La velocidad cae por debajo de $2\text{ km/h}$ únicamente a partir de pendientes ascendentes $S \ge +26{,}4\%$ ($S \ge \frac{\ln(3)}{3{,}5} - 0{,}05 \approx 0{,}2639$) o descendentes muy pronunciadas ($S \le -36{,}4\%$).
- **Capacidad Finita y Demanda Concurrente (E2SFCA)**:
  El modelo de accesibilidad E2SFCA en 2 pasos acopla la capacidad finita de absorción del equipamiento (boxes médicos, camas hospitalarias, cupos escolares, metros cuadrados de parque) con la población concurrente en isócronas peatonales con decaimiento continuo gaussiano.
- **Estabilidad Frente a Perturbaciones**:
  Los rankings comunales y regionales exhiben correlación de Spearman $\rho > 0{,}94$ frente a variaciones en el ancho de banda temporal ($t_0 \in \{10, 15, 20\}\text{ min}$), demostrando robustez epistemológica y ausencia de sobreajuste.

---

## ☁️ 7. Arquitectura Cloud-Native IDE 4.0 vs. Paradigma OGC Clásico

### 7.1 Transparencia Arquitectónica

La IDE CIT adopta deliberadamente la arquitectura **Cloud-Native Geospatial (IDE 4.0)**, superando las limitaciones de escalabilidad de los servidores monolíticos tradicionales basados en WFS/WMS transaccionales:

```
[ Usuario Web / Mobile ]          [ Analista / Data Scientist ]         [ Usuario SIG / QGIS ]
          │                                      │                                   │
          ▼                                      ▼                                   ▼
  Mapbox Vector Tiles                  Cloud-Optimized GeoParquet           Conectores QGIS (.qlr)
    (MVT / Protobuf)                  (HTTP Range Requests 206)             (Streaming S3 / MVT)
          │                                      │                                   │
          └───────────────────┬──────────────────┴───────────────────────────────────┘
                              ▼
                 Amazon CloudFront CDN (Edge Cache)
                              │
                              ▼
                 Amazon Simple Storage Service (S3)
             (Catálogo Estático STAC 1.0.0 + GeoParquet)
```

- **Catálogo STAC 1.0.0 Estático de Alta Disponibilidad**:
  En lugar de requerir una base de datos PostgreSQL/PostGIS dedicada con un servicio STAC API dinámico (que presenta cuellos de botella ante picos de demanda y requiere mantenimiento continuo), la IDE expone un catálogo **STAC 1.0.0 estático de alta concurrencia** distribuido en Amazon S3 y CloudFront. Soporta indexación por SpatioTemporal Asset Catalog crawlers, QGIS STAC Browser y bibliotecas Python (`pystac`).
- **GeoParquet 1.1 con Solicitudes por Rango HTTP (Byte-Range Requests - RFC 7233)**:
  Permite que motores modernos como DuckDB, GDAL 3.5+ y GeoPandas consulten metadatos de columnas, estadísticas mínimas/máximas de bounding box y filtros espaciales directamente sobre los archivos remotos en S3 sin necesidad de descargar el dataset completo a disco local.
- **Teselas Vectoriales MVT (Mapbox Vector Tiles)**:
  Servidas a través de CDN con tiempos de respuesta inferiores a **50 ms**, renderizadas mediante WebGL en el navegador del cliente a 60 fps.
- **Conectores SIG QGIS (`.qlr`) de 1 Clic**:
  Integración directa con herramientas de escritorio sin necesidad de configurar manualmente parámetros WFS ni endpoints complejos.

---

## 🏛️ 8. Matriz de Gobernanza Institucional, Preservación y Ciclo de Vida de Incidencias

### 8.1 Roles Institucionales y Cadena de Aprobación

| Rol de Custodia | Responsable Institucional | Responsabilidades Principales |
| :--- | :--- | :--- |
| **Comité Académico-Técnico** | Dirección CIT-UAI · Investigadores Titulares | Aprobación de cambios metodológicos mayores (SemVer MAJOR), calibración de nuevas versiones censales y validación científica de indicadores. |
| **Custodio de Datos Espaciales (Data Steward)** | Equipo de Modelación y Cartografía CIT-UAI | Custodia de la Fuente Única de Verdad (`catalogo_ide_cit.json`), verificación de cuadratura demográfica y certificación de sumas SHA-256. |
| **Equipo DevOps y Seguridad** | Ingeniería de Plataforma CIT-UAI | Operación del pipeline en 10 etapas (`compilar_ecosistema.py`), observabilidad de CDN CloudFront y auditorías de seguridad OWASP. |

### 8.2 Versionado Semántico Geoespacial (SemVer 2.0) y Política de Deprecación

- **Versionado SemVer**:
  - `MAJOR`: Modificación estructural de la metodología (ej. incorporación de nuevos indicadores censales o cambio de algoritmo de accesibilidad).
  - `MINOR`: Incorporación de nuevas coberturas temáticas o paquetes regionales sin alterar esquemas existentes.
  - `PATCH`: Correcciones tipográficas, refinamiento de documentación técnica o actualización de sumas de verificación.
- **Política de Preservación Inmutable (Cold Storage)**:
  Las versiones deprecadas **jamás se eliminan ni sobreescriben**. Cada versión histórica se archiva con su URN permanente y su checksum SHA-256 en almacenamiento frío multi-zona, asegurando que cualquier estudio o publicación científica previa pueda ser auditada y reproducida a perpetuidad.

### 8.3 Canal Público de Reporte y Gestión de Incidencias

- **Canal de Contacto Directo**: `contactocit@uai.cl` y `https://ide.cit.uai.cl/ficha-mbht-2017#sec-gobernanza`.
- **Rastreador Público de Incidencias (Issues)**: Repositorio GitHub institucional con protocolo de respuesta técnica en un plazo máximo de **48 horas hábiles**.
- **Registro Público de Incidencias (Bitácora)**:
  - `INC-2026-01` a `INC-2026-03` *(Cerradas)*: Cuadratura de inventarios regionales 2017, consolidación del diccionario físico de 42 columnas y sincronización de activos STAC.
  - `INC-2026-04` *(Cerrada)*: Corrección de rigor analítico en la formulación de Tobler para pendientes del 15% ($W(0{,}15) \approx 2{,}98\text{ km/h}$).
  - `INC-2026-05` *(En curso)*: Calibración final de los 17 indicadores de la Matriz MBHT 2024 con insumos del Censo 2024 (programada para Q4 2026).

---

*Centro de Inteligencia Territorial (CIT) — Universidad Adolfo Ibáñez.*  
*Diagonal Las Torres 2640, Peñalolén, Santiago de Chile.*  
*Sitio Web Oficial: https://cit.uai.cl / Portal IDE: https://ide.cit.uai.cl*
