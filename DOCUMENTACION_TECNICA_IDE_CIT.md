# 🌐 Infraestructura de Datos Espaciales (IDE CIT) — Documentación Técnica y Registro de Algoritmos

> **Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez**  
> **Ecosistema**: MBHT 2024–2026 (Matriz de Bienestar Humano Territorial)  
> **Versión**: 2026.1  
> **Última Actualización**: 15 de Septiembre de 2026  

---

## 🏛️ 1. Arquitectura General y Propósito

La **IDE CIT** es la plataforma institucional de datos abiertos, interoperabilidad y trazabilidad metodológica del Centro de Inteligencia Territorial. Su propósito es proveer acceso abierto, auditable y de alto rendimiento a las cuatro matrices territoriales de Chile:

1. **MBHT 2017**: Línea base oficial (204.906 manzanas censales, 202.275 equipamientos, red vial de ejes caminables, 18 indicadores en 4 dimensiones, Índice BHT y TOB).
2. **PEM / SBAP**: Planificación Espacial Marina (Maritorio nacional, ZEE de 200 mn y Áreas Marinas Protegidas AMCP-MU bajo Ley SBAP).
3. **Censo 2024 (Imputaciones Demográficas)**: Desagregación etaria y por sexo en 42 cohortes (primera infancia, escolares, adultos y personas mayores) a nivel de manzanas y entidades rurales para las 16 regiones.
4. **INSE**: Índice de Nivel Socioeconómico y estratificación socioespacial y patrimonial a nivel de manzanas y entidades rurales para todo Chile.
5. **SII (Áreas Homogéneas)**: Catastro nacional de 14.157 polígonos de valor guía de terreno (VGT) y avalúos fiscales bajo la Ley 17.235.
6. **MBHT 2024**: Matriz de Bienestar Humano Territorial actualizada a Censo 2024 *(Visible en catálogo con pre-aviso "Próximamente", en fase final de calibración institucional)*.

La arquitectura opera bajo un esquema Cloud-Native Serverless (AWS S3 + CloudFront + GeoParquet + DuckDB) estandarizado con normas internacionales (**ISO 19115-1:2014**, **Perfil Chileno SNIT**, **W3C DCAT-AP 2.0**, **OGC Vector Tiles MVT**, **GeoParquet 1.1** y **STAC 1.0.0**), incorporando un visor de referencia espacial interactivo y un **Copiloto IA Territorial** con síntesis de voz Web Speech API (TTS) y memoria episódica.

---

## ⚙️ 2. Registro de Algoritmos Dedicados por Etapa

Cada fase del ciclo de vida de la IDE cuenta con un algoritmo en Python dedicado, determinista y completamente documentado:

```
07_Aplicaciones_y_Visualizadores_Web/IDE_Data_Hub/
├── generador_portal_ide_cit.py      # [ETAPA 1] Compilador y ensamblador algorítmico del portal
├── validador_metadatos_iso.py       # [ETAPA 2] Validador de esquemas, linaje y perfiles ISO/SNIT
├── verificador_servicios_tiles.py   # [ETAPA 3] Verificador de conectores MVT, GeoParquet y S3
├── data/
│   └── catalogo_ide_cit.json        # Matriz central de capas, atributos y linaje
├── img/                             # Activos vectoriales oficiales (SVG puros)
│   ├── logo-cit-uai.svg             # Imagotipo oficial CIT-UAI
│   ├── logo-ide-standalone.svg      # Emblema oficial IDE CIT
│   └── logo-mbht-white.svg          # Logo oficial MBHT para fondo oscuro
├── index.html                       # Artefacto compilado final (Mobile-First / Tailwind / Leaflet)
└── DOCUMENTACION_TECNICA_IDE_CIT.md # (Este archivo) Registro maestro de arquitectura
```

---

### 📋 Detalle de Algoritmos

#### 🔹 Etapa 1: Compilador Algorítmico del Portal Web y Suite de Datos (`generador_portal_ide_cit.py`)
- **Responsabilidad Única**: Ensamblar y validar el código HTML5 reactivo (`index.html`), estructurar el marcado Schema.org JSON-LD para Google Dataset Search, compilar exportaciones multiformato (CSV, DCAT-AP) y generar el lanzador local batch.
- **Invariantes Implementadas**:
  - `find_proyecto_root(__file__)`: Resolución dinámica e insensible al directorio de trabajo activo.
  - **Doble navegación responsiva**: Menú hamburguesa interactivo para celulares (`< md`) y pestañas horizontales para escritorio (`md+`).
  - **Asistente Territorial / Copiloto IA CIT**: Widget interactivo flotante con síntesis de voz Web Speech API (TTS), sugerencias contextuales y motor de resolución híbrido (API microservicio Capa 3 + fallback local heurístico en < 250 ms).
  - **Visor de Referencia Espacial**: Integración de Leaflet con cartografía base neutral (CartoDB Positron) para visualización de BBOX y CRS sin sobrecarga de memoria.
  - **Resguardo y Reserva de Seguridad (MPST)**: Bloqueo de descargas y servicios MVT para dimensiones en proceso de calibración institucional con organismos públicos.
  - **Interoperabilidad y SEO Internacional**: Marcado Schema.org DataCatalog JSON-LD, catálogo W3C DCAT-AP 2.0 (`data/dcat.json`), índice tabular CSV (`data/catalogo_ide_cit.csv`), `sitemap.xml`, `robots.txt` y `site.webmanifest`.
  - **Lanzador Local Rápido**: Genera `INICIAR_PORTAL_LOCAL.bat` para previsualizar y probar todo el portal en servidor HTTP local en puerto 8080 con 1 clic.
- **Ejecución**:
  ```bash
  python generador_portal_ide_cit.py          # Compila toda la suite, HTML, CSV, DCAT y lanzador
  python generador_portal_ide_cit.py --check  # Valida consistencia sin sobreescribir
  ```

#### 🔹 Etapa 2: Validador y Exportador ISO 19115 / SNIT / STAC (`validador_metadatos_iso.py`)
- **Responsabilidad Única**: Auditar la conformidad de las 10 capas del catálogo con respecto a estándares geográficos internacionales y exportar los esquemas XML ISO 19139 y STAC 1.0.0.
- **Invariantes Implementadas**:
  - **Auditoría de integridad**: Validación de tipos de datos, atributos, formulación matemática auditable y rangos de Bounding Box WGS84.
  - **Exportación XML ISO 19139 / Perfil Chileno SNIT**: Genera 10 archivos XML normalizados en `data/iso_xml/` para cosecha automática por Geonetwork, Geonode, CKAN y SNIT Chile.
  - **Exportación STAC 1.0.0**: Genera la colección Cloud-Native Geospatial en `data/stac/collection.json` para integración con herramientas geoespaciales modernas en Python/QGIS.
- **Ejecución**:
  ```bash
  python validador_metadatos_iso.py               # Auditoría completa + Exportación XML + STAC
  python validador_metadatos_iso.py --audit-only   # Solo auditoría de conformidad
  python validador_metadatos_iso.py --export-xml   # Solo exportación XML ISO 19139
  python validador_metadatos_iso.py --export-stac  # Solo exportación STAC 1.0.0
  ```

#### 🔹 Etapa 3: Verificador Concurrente de Servicios MVT y S3 (`verificador_servicios_tiles.py`)
- **Responsabilidad Única**: Auditoría de conectividad en tiempo real, latencia HTTP (RTT) y disponibilidad de los servidores de teselas vectoriales MVT (Martin), APIs del motor espacial FastAPI y repositorios S3.
- **Invariantes Implementadas**:
  - **Ejecución concurrente multi-hilo (`ThreadPoolExecutor`)**: Evaluación paralela de todos los endpoints en < 1.1 segundos.
  - **Muestreo de teselas Protobuf (`--sample-tiles`)**: Comprobación a nivel de byte de teselas `0/0/0.pbf`.
  - **Generación automatizada de reportes**: Exportación de diagnósticos de telemetría a Markdown (`data/reporte_salud_servicios.md`) y JSON.
- **Ejecución**:
  ```bash
  python verificador_servicios_tiles.py                 # Verificación estándar + Reporte MD
  python verificador_servicios_tiles.py --timeout 1.5   # Verificación rápida con timeout estricto
  python verificador_servicios_tiles.py --sample-tiles  # Muestreo de teselas MVT
  python verificador_servicios_tiles.py --export-json   # Exportación JSON para telemetría
  ```

#### 🔹 Etapa 4: Pipeline de Empaquetado y Preparación de Producción (`desplegador_ide_produccion.py`)
- **Responsabilidad Única**: Chequeos pre-vuelo, empaquetado de distribución en `dist/`, cálculo de hashes criptográficos SHA-256 (`dist/manifest.json`) y generación del script controlado `DESPLEGAR_PORTAL_IDE.bat`.
- **Invariantes Implementadas**:
  - **Modo seguro por defecto (`--dry-run`)**: Opera en modo local/simulación sin publicar remotamente hasta confirmación humana.
  - **Políticas de caché HTTP diferenciadas**: Inmutabilidad para activos estáticos (1 año), revalidación para XML/STAC (24 h) y no-cache para `index.html`.
  - **Manifiesto de Integridad**: Registro de hash SHA-256 por cada uno de los 31 archivos del release en `dist/manifest.json`.
- **Ejecución**:
  ```bash
  python desplegador_ide_produccion.py              # Modo simulación / Dry-run seguro
  python desplegador_ide_produccion.py --build-only # Empaqueta en 'dist/' y genera manifest.json
  ```

---

## 📊 3. Estándar de Metadatos y Esquema JSON (`catalogo_ide_cit.json`)

Cada capa registrada en el catálogo implementa la siguiente estructura estricta:

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `id` | `String` | Identificador único de la capa | `"kpi_mud_2024"` |
| `titulo` | `String` | Nombre formal estandarizado | `"MBHT 2024 — Indicadores de Accesibilidad..."` |
| `matriz` | `Enum` | Matriz territorial de pertenencia | `"mbht" \| "mpst" \| "mrct" \| "mpit"` |
| `ambito` | `Enum` | Dimensión tridimensional | `"tierra" \| "mar" \| "aire"` |
| `escala` | `String` | Unidad mínima de agregación espacial | `"Manzana Censal (254.395 unidades)"` |
| `cobertura` | `String` | Extensión geográfica nominal | `"Nacional (16 Regiones de Chile)"` |
| `bbox` | `Array[4]` | Bounding Box `[MinLon, MinLat, MaxLon, MaxLat]` | `[-75.64, -55.98, -66.86, -17.50]` |
| `crs` | `String` | Sistema de Referencia de Coordenadas | `"EPSG:4326 (WGS 84)"` |
| `tipo_geometria` | `String` | Tipo de entidad espacial | `"MultiPolygon"` |
| `formula_lineage` | `String` | Formulación matemática auditable | `ISAL, ISE... f(t)=exp(-0.5*(t/15)^2)` |
| `tile_source` | `String` | Identificador en servidor de teselas MVT | `"kpi_mud"` |
| `s3_parquet` | `URI` | Ruta al archivo GeoParquet en AWS S3 | `"s3://mbht-data-lake/parquet/..."` |
| `atributos` | `Array` | Diccionario de variables con tipo y glosa | `[{"campo": "mud", "tipo": "Float", ...}]` |

---

---

## 🛡️ 5. Arquitectura de Seguridad, Privacidad y Disponibilidad (OWASP ASVS 5.0)

La Infraestructura de Datos Espaciales (IDE CIT) implementa una arquitectura cloud-native de alta seguridad y disponibilidad, alineada con las directivas del estándar **OWASP Application Security Verification Standard (ASVS 5.0.0 Nivel 2)** y el marco legal chileno:

### 5.1 Matriz de Controles Técnicos de Seguridad

| Dominio ASVS | Control Implementado | Evidencia y Configuración |
| :--- | :--- | :--- |
| **V1: Arquitectura** | Aislamiento estricto de componentes | Almacenamiento S3 protegido con *Origin Access Control* (OAC); acceso web canalizado exclusivamente a través de CDN CloudFront. |
| **V2: Autenticación / Acceso** | Principio de menor privilegio y lectura pública segura | APIs públicas operan en modo solo lectura (`GET`/`HEAD`); modificaciones de datos restringidas a pipelines de despliegue autenticados por IAM. |
| **V5: Validación y Sanitización** | Prevención anti-XSS y validación de tipos | El Copiloto IA y los módulos de consulta procesan entradas mediante escape contextual de entidades HTML (`<[^>]*>`), tipado estricto y sanitización previa a la inyección en el DOM. |
| **V8: Protección de Datos** | Integridad criptográfica SHA-256 | Sumas de verificación SHA-256 precalculadas e inmutables para todos los datasets vectoriales y tabulares (`download/archivos_hash_manifest.json`). |
| **V9: Comunicaciones** | Cifrado en tránsito forzado | TLS 1.3 / 1.2 estricto forzado en Amazon CloudFront con cabecera HSTS `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`. |
| **V10: Cabeceras HTTP** | Blindaje contra ataques de contenido | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, CORS configurado con aislamiento de métodos. |
| **V14: Configuración** | Cero exposición de secretos o credenciales | La plataforma web no almacena llaves de API privadas en el cliente ni expone variables de entorno de infraestructura. |

### 5.2 Privacidad y Secreto Estadístico (Ley N° 17.374)
- **Secreto Estadístico**: En estricto cumplimiento de la Ley 17.374 del Instituto Nacional de Estadísticas (INE), los datos geoespaciales de la IDE CIT agregan la información a nivel de manzana censal o polígonos territoriales mayores.
- **Cero Microdatos Personales**: No se almacenan ni publican identidades individuales, números de cédula (RUT), nombres de propietarios ni localizaciones de domicilios particulares.
- **Imputación con Conservación Total**: Las estimaciones demográficas (Sprague) conservan con rigor matemático las sumas poblacionales comunales oficiales.

### 5.3 Disponibilidad y Resiliencia Cloud-Native
- **SLA de Disponibilidad**: 99.9% de tiempo de actividad garantizado por la infraestructura distribuida multi-AZ de Amazon S3 y CloudFront.
- **Monitoreo de Endpoints de Interoperabilidad**:
  - Catálogo STAC 1.0.0: `https://ide.cit.uai.cl/stac/catalog.json`
  - Colección STAC 1.0.0: `https://ide.cit.uai.cl/stac/collection.json`
  - Metadatos ISO 19139 XML: `https://ide.cit.uai.cl/metadata.xml`
  - Directorio DCAT-AP: `https://ide.cit.uai.cl/dcat.json`
  - Ejemplos de Conexión: `https://ide.cit.uai.cl/connection_examples.json`

---

*Centro de Inteligencia Territorial (CIT) — Universidad Adolfo Ibáñez.*  
*Contacto: contactocit@uai.cl / cit.uai.cl*
