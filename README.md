<div align="center">

# Infraestructura de Datos Espaciales (IDE CIT)
### Centro de Inteligencia Territorial · Escuela de Gobierno · Universidad Adolfo Ibáñez

[![Build Status](https://img.shields.io/badge/Build-1792187921-1e293b?style=flat)](https://ide.cit.uai.cl)
[![Python](https://img.shields.io/badge/Python-3.10%2B-1e293b?style=flat)](https://python.org)
[![STAC](https://img.shields.io/badge/STAC-1.0.0-334155?style=flat)](https://ide.cit.uai.cl/stac/catalog.json)
[![ISO Standard](https://img.shields.io/badge/ISO-19115%20%2F%2019139-334155?style=flat)](https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml)
[![Format](https://img.shields.io/badge/GeoParquet-1.1-475569?style=flat)](https://geoparquet.org)
[![Auditoría](https://img.shields.io/badge/Auditor%C3%ADa-Certificada-0f172a?style=flat)](https://ide.cit.uai.cl)
[![Disponibilidad](https://img.shields.io/badge/SLA-99.9%25%20CloudFront-475569?style=flat)](https://ide.cit.uai.cl)
[![Licencia](https://img.shields.io/badge/Licencia-Institucional%20CIT--UAI-64748b?style=flat)](https://cit.uai.cl)

**Plataforma institucional de datos geoespaciales abiertos, modelación territorial determinista, catálogos normalizados (STAC / ISO) y Copiloto Territorial de Chile.**

[Portal Principal](https://ide.cit.uai.cl) · [Centro de Descargas](https://ide.cit.uai.cl/descargas) · [Guía Técnica Metodológica](https://ide.cit.uai.cl/guia-tecnica) · [Directorio de 19 IDEs SNIT](https://ide.cit.uai.cl/red-ides) · [Catálogo STAC](https://ide.cit.uai.cl/stac/catalog.json)

</div>

---

## 1. Marco Institucional y Propósito Territorial

La **Infraestructura de Datos Espaciales del Centro de Inteligencia Territorial (IDE CIT)** de la Universidad Adolfo Ibáñez constituye la plataforma de referencia para la difusión, interoperabilidad y trazabilidad metodológica de las matrices territoriales de Chile.

Su misión es proveer a la comunidad académica, organismos públicos ministeriales (SUBDERE, MINVU, MDSF, MMA), gobiernos regionales, municipios y a la sociedad civil acceso libre, auditable y determinista a las bases de modelación espacial del país:

1. **MBHT 2017 (Línea Base Oficial Vigente)**: Catastro de 204.906 manzanas censales evaluadas en 18 indicadores multidimensionales (Salud, Educación, Áreas Verdes, Transporte, Seguridad, Vulnerabilidad Socioeconómica y Calidad Ambiental) sobre el grafo vial caminable nacional de 1.589.595 tramos, utilizando la función cinemática de Tobler y el modelo bietápico de absorción flotante E2SFCA.
2. **Censo 2024 (Insumos Demográficos Preparatorios en Calibración)**: Desagregación osculatoria de Sprague de 5.º orden y modelos sintéticos de cohortes etarias por sexo para 18,48 millones de habitantes.
3. **Planificación Espacial Marina (PEM / SBAP)**: Delimitación tricontinental del Maritorio de Chile, Zona Económica Exclusiva (ZEE de 200 millas náuticas) y geomorfología submarina GEBCO / SHOA.
4. **Índice de Nivel Socioeconómico (INSE)**: Estratificación multivariada predial y residencial a escala de manzana censal y entidad rural.
5. **Directorio Oficial SNIT**: Enlaces e interoperabilidad hacia 19 geoportales del Sistema Nacional de Información Territorial de Chile.

---

## 2. Ecosistema de Inteligencia Artificial y Modelos de Lenguaje (LLM)

La IDE CIT integra una capa de interacción mediante Modelos de Lenguaje (LLM) y agentes autónomos, fundamentada en principios de verificabilidad empírica, sobriedad conceptual y gobernanza de datos:

```
                  ┌────────────────────────────────────────┐
                  │    Agentes LLM / Investigadores / UI    │
                  └───────────────────┬────────────────────┘
                                      │
            ┌─────────────────────────┼────────────────────────┐
            ▼                         ▼                        ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│  /llms.txt (Normal.)  │ │  Copiloto Territorial │ │ /llms-full.txt (Ext.) │
│ Resumen contextual   │ │ Motor de consulta NLP │ │ Metadatos completos   │
│ para prompts y agentes│ │ y síntesis de voz TTS │ │ y esquemas semánticos │
└───────────────────────┘ └───────────┬───────────┘ └───────────────────────┘
                                      │
            ┌─────────────────────────┴────────────────────────┐
            ▼                                                  ▼
┌───────────────────────────────────────┐  ┌─────────────────────────────────┐
│ Memoria Episódica DuckDB / Parquet    │  │ Deduplicación Espacial (>300 m) │
│ 231k patrones urbanos aprendidos      │  │ Recomendaciones sin aglomeración│
└───────────────────────────────────────┘  └─────────────────────────────────┘
```

### 2.1. Especificación Estándar para Agentes de IA (`llms.txt` y `llms-full.txt`)
La plataforma implementa la especificación `/llms.txt` para garantizar que modelos de lenguaje y entornos de desarrollo asistido (Claude, Cursor, Copilot, ChatGPT, Perplexity, Antigravity) procesen la información metodológica oficial sin riesgo de alucinación semántica:
- **Resumen Contextual:** [`https://ide.cit.uai.cl/llms.txt`](https://ide.cit.uai.cl/llms.txt) — Directivas conceptuales, delimitación de la línea base 2017 y advertencias de uso analítico.
- **Contexto Exhaustivo:** [`https://ide.cit.uai.cl/llms-full.txt`](https://ide.cit.uai.cl/llms-full.txt) — Diccionario formal de 42 columnas físicas, formulación analítica de los 18 indicadores, extensiones geográficas WGS84 y endpoints de descarga.

### 2.2. Copiloto Territorial CIT (`motor_ia_cit.py` / `copiloto_conversacional_llm.py`)
- **Comprensión Semántica:** Resuelve consultas en lenguaje natural sobre brechas urbanas, accesibilidad a equipamientos y cobertura de servicios comunitarios.
- **Memoria Episódica Determinista:** Conecta con DuckDB y Parquet para consultar matrices de equidad territorial en latencias inferiores a 250 ms.
- **Deduplicación Espacial:** Asegura que cualquier recomendación de inversión pública o emplazamiento de infraestructura esté separada a una distancia física mínima superior a 300 metros respecto a equipamientos existentes.
- **Locución Web Speech API (TTS):** Síntesis vocal orientada a presentaciones ejecutivas mediante `window.speechSynthesis` con precarga controlada de voces en español.

### 2.3. Fundamento Epistémico y Neutralidad Metodológica
- El asistente opera bajo un principio estricto de **humildad académica**: los modelos territoriales constituyen aproximaciones empíricas destinadas a enriquecer la deliberación humana, sin pretender sustituir el juicio técnico ni la deliberación democrática.
- Queda proscrito el empleo de consignas reduccionistas o juicios binarios moralizantes, reconociendo la diversidad geográfica y cultural de Chile (valles transversales, asentamientos periurbanos, quebradas andinas y archipiélagos australes).

---

## 3. Jerarquía y Taxonomía de Coberturas

La IDE CIT establece una demarcación rigurosa entre conjuntos de datos consolidados y procesos en etapa de calibración estadística:

| Cobertura | Insignia Oficial | Estado de Madurez | Custodia Técnica |
| :--- | :--- | :--- | :--- |
| **Matriz BHT 2017** (`kpi_mud_2017`) | Línea Base Oficial Vigente (SUBDERE - Ministerial) | Producción Consolidada | CIT-UAI / SUBDERE |
| **Censo 2024 (Imputaciones)** | Insumo Demográfico Preparatorio (En Calibración) | Preliminar / En Ajuste | CIT-UAI / INE |
| **Planificación Espacial Marina** (`pem_*`) | Fuente Institucional Certificada | Producción Vigente | DIFROL / Armada / MMA |
| **Equipamientos Urbanos 2017** | Catastro Nacional Auditado | 55.035 Establecimientos | CIT-UAI / Ministerios |
| **Red Vial Caminable 2017** | Grafo Ruteable Tobler | 1.589.595 Tramos Viales | CIT-UAI / MOP |

> [!NOTE]
> **Aviso Metodológico — Censo 2024:**  
> La cobertura demográfica del Censo 2024 publicada para descarga abierta entrega insumos preparatorios de población, cohortes y composición por sexo. **No constituye la síntesis multidimensional final MBHT 2024**, cuyo lanzamiento oficial está previsto para **noviembre de 2026**. Para la formulación de diagnósticos e instrumentos de política pública rige la línea base oficial MBHT 2017.

---

## 4. Panel de Interoperabilidad Probada y Servicios Certificados

Cada endpoint y conector publicado en la IDE ha sido validado en producción mediante pruebas automatizadas con código de respuesta `HTTP 200 OK`, sistema geodésico `EPSG:4326` (WGS84) y sumas criptográficas SHA-256:

| Protocolo / Estándar | Endpoint Oficial | Formato / Sistema Ref. | Comando de Verificación (CLI) | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **STAC 1.0.0 Catalog** | `/stac/catalog.json` | JSON · EPSG:4326 | `curl -s https://ide.cit.uai.cl/stac/catalog.json \| jq .id` | Verificado |
| **GeoParquet 1.1** | `/download/MBHT_2017_R15_Manzanas.parquet` | WKB Snappy · EPSG:4326 | `duckdb -c "SELECT count(*), round(avg(bht_2017),4) FROM 'https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet'"` | Verificado |
| **OGC GeoPackage** | `/download/MBHT_2017_R15_Manzanas.gpkg` | SQLite · EPSG:4326 | `ogrinfo -so https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.gpkg mbht_2017_r15` | Verificado |
| **ESRI Shapefile** | `/download/MBHT_2017_R15_Manzanas_SHP.zip` | ZIP (SHP/DBF) · EPSG:4326 | `curl -sI https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas_SHP.zip \| grep -i content-length` | Verificado |
| **QGIS Layer Def.** | `/download/qgis/CIT_MBHT_2017_Nacional.qlr` | XML qgis-qlr · EPSG:4326 | `curl -s https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr \| head -n 5` | Verificado |
| **ISO 19139 XML** | `/download/iso_xml/kpi_mud_2017_iso19139.xml` | XML gmd:MD_Metadata | `curl -s https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml \| head -n 10` | Verificado |

---

## 5. Protocolo de Reproducibilidad Científica de Extremo a Extremo

Para certificar la integridad de los algoritmos y descartar vectores de riesgo en la cadena de distribución de software, la IDE CIT implementa un **procedimiento de 3 pasos auditado** que prescinde de invocaciones remotas automáticas:

```bash
# 1. Descarga aislada del script de verificación
curl -s -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py

# 2. Verificación criptográfica mediante la suma SHA-256 publicada
echo "7fb25d61a29544e57c17869c6ea3566c68659d003dce9f59dfcd642fbf96a8d0  reproducir_verificacion_r15.py" | sha256sum -c

# 3. Ejecución determinista en entorno local
python reproducir_verificacion_r15.py
```

### Valores de Referencia para Calibración (Manzana Testigo `15101011001004001` — Arica):
- **BHT Oficial 2017:** `0.3751` ($\pm 0.0001$)
- **Dimensión Accesibilidad:** `0.3204` ($\pm 0.0001$)
- **Dimensión Socioeconómica:** `0.4421` ($\pm 0.0001$)
- **Dimensión Seguridad:** `0.4102` ($\pm 0.0001$)
- **Dimensión Ambiental:** `0.3276` ($\pm 0.0001$)

---

## 6. Arquitectura del Sistema y Estructura de Código

```
IDE_Data_Hub/
├── generador_portal_ide_cit.py             # Generador SSG de index.html, CSV y DCAT
├── generador_descargas_2017.py             # Generador del centro de descargas territoriales
├── generador_guia_tecnica.py               # Generador de la guía metodológica
├── generador_red_ides.py                   # Generador del directorio de geoportales SNIT
├── generador_ficha_dataset.py              # Generador de la ficha técnica maestra 17D
├── compilar_y_certificar_ecosistema_ide.py # Compilador maestro y orquestador de control de calidad
├── auditor_adversarial_ide.py              # Suite de auditoría adversarial continua (12 vectores)
├── motor_ia_cit.py                         # Motor NLP y telemetría del Copiloto Territorial
├── data/
│   ├── catalogo_ide_cit.json               # Fuente de datos central y linaje metodológico
│   ├── connection_examples.json            # Ejemplos de consumo multi-lenguaje (Python, R, QGIS)
│   └── iso_xml/                            # 29 esquemas XML normalizados ISO 19139
├── stac/                                   # Catálogo STAC 1.0.0 (18 colecciones estructuradas)
├── download/
│   ├── reproducir_verificacion_r15.py      # Script ejecutable de verificación científica E2E
│   └── SHA256SUMS.txt                      # Registro maestro de sumas de comprobación SHA-256
├── requirements.txt                        # Especificación de dependencias mínimas de Python
└── .gitignore                              # Exclusión de datos pesados (>100MB) y archivos de depuración
```

---

## 7. Guía de Ejecución y Desarrollo Local

### Requisitos del Sistema
- Python 3.10 o superior.
- Git 2.40 o superior.

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Compilación Completa del Ecosistema
Ejecuta la regeneración de páginas HTML, catálogos STAC 1.0.0, metadatos ISO y la comprobación de los 658 hashes criptográficos:
```bash
python compilar_y_certificar_ecosistema_ide.py
```

### Previsualización en Servidor Local
- En Windows: Ejecutar `INICIAR_PORTAL_LOCAL.bat`.
- En Linux / macOS:
  ```bash
  python -m http.server 8080
  ```
  Acceder a `http://localhost:8080`.

### Ejecución de la Suite de Auditoría Adversarial
```bash
python auditor_adversarial_ide.py
```

---

## 8. Seguridad de la Información y Divulgación de Vulnerabilidades (RFC 9116)

El Centro de Inteligencia Territorial mantiene una política formal de divulgación coordinada y gestión de incidentes:
- **Contacto de Seguridad Institucional:** `mailto:security@uai.cl`
- **Contacto Administrativo CIT:** `mailto:contactocit@uai.cl`
- **Archivo de Seguridad Canónico:** [`https://ide.cit.uai.cl/.well-known/security.txt`](https://ide.cit.uai.cl/.well-known/security.txt)
- **Vigencia del Registro:** 31 de diciembre de 2027
- **Principio de Cero Secretos:** Aislamiento estricto de credenciales y claves privadas fuera del código fuente versionado.

---

## 9. Propiedad Intelectual, Licenciamiento y Citación Académica

El código fuente de este repositorio se encuentra bajo **Licencia Institucional CIT-UAI**. Los datos geoespaciales abiertos se difunden bajo términos equivalentes a **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

### Citación Oficial en Norma APA 7:
> Centro de Inteligencia Territorial. (2026). *Infraestructura de Datos Espaciales (IDE CIT) y Matriz de Bienestar Humano Territorial (MBHT)*. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl
