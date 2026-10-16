<div align="center">

# 🌐 Infraestructura de Datos Espaciales (IDE CIT)
### Centro de Inteligencia Territorial (CIT) · Universidad Adolfo Ibáñez

[![Build Status](https://img.shields.io/badge/Build-1792187921%20Pass-emerald?style=flat-square&logo=github-actions)](https://ide.cit.uai.cl)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![STAC](https://img.shields.io/badge/STAC-1.0.0%20Compliant-008080?style=flat-square)](https://ide.cit.uai.cl/stac/catalog.json)
[![ISO](https://img.shields.io/badge/ISO-19115%20%2F%2019139%20XML-orange?style=flat-square)](https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml)
[![GeoParquet](https://img.shields.io/badge/Format-Cloud--Optimized%20GeoParquet-purple?style=flat-square)](https://geoparquet.org)
[![Red Team](https://img.shields.io/badge/Red%20Team-47%20PASS%20%2F%200%20FAIL-success?style=flat-square)](https://ide.cit.uai.cl)
[![SLA](https://img.shields.io/badge/SLA-99.9%25%20CloudFront%20CDN-blueviolet?style=flat-square)](https://ide.cit.uai.cl)
[![License](https://img.shields.io/badge/Licencia-Institucional%20CIT--UAI-lightgrey?style=flat-square)](https://cit.uai.cl)

**Plataforma institucional de datos abiertos, modelos territoriales deterministas, catálogos normalizados (STAC / ISO) y Copiloto IA Territorial de Chile.**

[Portal Oficial](https://ide.cit.uai.cl) · [Centro de Descargas](https://ide.cit.uai.cl/descargas) · [Guía Técnica Metodológica](https://ide.cit.uai.cl/guia-tecnica) · [Red de 19 IDEs SNIT](https://ide.cit.uai.cl/red-ides) · [Catálogo STAC](https://ide.cit.uai.cl/stac/catalog.json)

</div>

---

## 🏛️ 1. Propósito y Misión Institucional

La **IDE CIT** es la infraestructura de datos geoespaciales, analítica territorial y trazabilidad metodológica del **Centro de Inteligencia Territorial (CIT) de la Universidad Adolfo Ibáñez**. 

Su misión es proveer a la comunidad académica, ministerios del Estado de Chile (SUBDERE, MINVU, MDSF, MMA), gobiernos regionales, municipios y a la ciudadanía acceso libre, transparente, reproducible e interoperable a los indicadores y modelos de bienestar territorial del país:

1. **MBHT 2017 (Línea Base Oficial Vigente)**: 204.906 manzanas censales evaluadas en 18 indicadores multidimensionales (Salud, Educación, Áreas Verdes, Transporte, Seguridad, Vulnerabilidad Socioeconómica y Calidad Ambiental) sobre el grafo vial caminable nacional de 1.589.595 tramos bajo la función cinemática de Tobler y el modelo bietápico de absorción flotante E2SFCA.
2. **Censo 2024 (Insumos Demográficos Preparatorios en Calibración)**: Desagregación osculatoria de Sprague de 5.º orden y modelos sintéticos de cohortes etarias por sexo para 18,48 millones de habitantes.
3. **Planificación Espacial Marina (PEM / SBAP)**: Cartografía tricontinental del Maritorio de Chile, Zona Económica Exclusiva (ZEE de 200 millas náuticas) y geomorfología submarina GEBCO.
4. **Índice de Nivel Socioeconómico (INSE)**: Estratificación multivariada predial y residencial nacional.
5. **Directorio Oficial SNIT**: Conectores e interoperabilidad hacia 19 geoportales del Sistema Nacional de Información Territorial de Chile.

---

## 🤖 2. Ecosistema de Inteligencia Artificial & LLMs

La IDE CIT incorpora una arquitectura pionera de interacción mediante **Modelos de Lenguaje (LLMs)** y agentes autónomos, diseñada bajo estrictos estándares de verificabilidad empírica, humildad científica y gobernanza de datos:

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

### A. Especificación Estándar para Agentes de IA (`llms.txt` y `llms-full.txt`)
La plataforma implementa la especificación `/llms.txt` para garantizar que agentes como **Claude, Cursor, Copilot, ChatGPT, Perplexity o Antigravity** consuman la información metodológica oficial sin alucinaciones ni distorsiones:
- **Resumen Ejecutivo:** [`https://ide.cit.uai.cl/llms.txt`](https://ide.cit.uai.cl/llms.txt) — Directivas conceptuales, delimitación de la línea base 2017 y advertencia sobre el Censo 2024.
- **Contexto Exhaustivo:** [`https://ide.cit.uai.cl/llms-full.txt`](https://ide.cit.uai.cl/llms-full.txt) — Diccionario completo de 42 columnas físicas, formulación matemática de los 18 indicadores, BBOX geográficos y endpoints de descarga.

### B. Copiloto Territorial CIT (`motor_ia_cit.py` / `copiloto_conversacional_llm.py`)
- **Comprensión Semántica:** Interpreta preguntas en lenguaje natural sobre brechas urbanas (*ej. «¿cuántas familias tienen bajo acceso a salud en Arica?»*).
- **Memoria Episódica Determinista:** Conecta con DuckDB para consultar matrices precalculadas de equidad territorial en menos de 250 ms.
- **Deduplicación Espacial:** Asegura que cualquier recomendación de infraestructura esté separada a una distancia euclidiana mínima > 300 metros de equipamientos existentes.
- **Locución Humana TTS:** Síntesis de voz ejecutiva mediante Web Speech API (`window.speechSynthesis`) con precarga asíncrona de voces en español.

### C. Directiva Ética y Epistémica de los Modelos (Cero Dogmatismo)
- El agente de IA se expresa con **humildad académica**: los modelos territoriales son aproximaciones empíricas que enriquecen la deliberación humana, jamás verdades absolutas inapelables.
- Queda terminantemente prohibido el uso de clichés simplistas (*«ciudad de 15 minutos»*) o juicios binarios moralizantes (*«ciudades buenas vs. ciudades malas»*), reconociendo la heterogeneidad de paisajes, quebradas, valles transversales y caletas de Chile.

---

## 📊 3. Taxonomía de Coberturas y Jerarquía de Versiones

Para evitar interpretaciones erróneas, la IDE mantiene una rigurosa separación institucional entre datos oficiales consolidados y procesos en calibración:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ JERARQUÍA DE VERSIONES Y ESTADO DE MADUREZ METODOLÓGICA                               │
├───────────────────────────────┬──────────────────────────────────┬─────────────────────┤
│ Cobertura                     │ Insignia Institucional Oficial   │ Estado de Madurez   │
├───────────────────────────────┼──────────────────────────────────┼─────────────────────┤
│ Matriz BHT 2017 (kpi_mud_2017)│ LÍNEA BASE OFICIAL VIGENTE       │ Producción Oficial  │
│                               │ (SUBDERE - MINISTERIAL)          │ Consensuada         │
├───────────────────────────────┼──────────────────────────────────┼─────────────────────┤
│ Censo 2024 (Imputaciones)     │ INSUMO DEMOGRÁFICO PREPARATORIO  │ En Calibración      │
│                               │ (EN CALIBRACIÓN - NO ES MBHT)    │ Preliminar          │
├───────────────────────────────┼──────────────────────────────────┼─────────────────────┤
│ Planificación Espacial Marina │ FUENTE INSTITUCIONAL CERTIFICADA │ Producción Oficial  │
│ (PEM Tricontinental / ZEE)    │ (DIFROL / Armada / MMA / SHOA)   │ Vigente             │
├───────────────────────────────┼──────────────────────────────────┼─────────────────────┤
│ Equipamientos Urbanos 2017    │ CATASTRO AUDITADO CIT-UAI        │ 55.035 Equipamientos│
├───────────────────────────────┼──────────────────────────────────┼─────────────────────┤
│ Red Vial Caminable 2017       │ GRAFO RUTEABLE TOBLER            │ 1.589.595 Tramos    │
└───────────────────────────────┴──────────────────────────────────┴─────────────────────┘
```

> [!IMPORTANT]
> **Aviso Metodológico Censo 2024:**  
> La cobertura demográfica del Censo 2024 disponible para descarga pública entrega insumos sintéticos de población, cohortes y género. **NO constituye la síntesis multidimensional final MBHT 2024**, cuyo lanzamiento oficial está programado para **noviembre de 2026**. Para políticas públicas y diagnósticos territoriales consolidados, utilice la línea base oficial MBHT 2017.

---

## ⚡ 4. Panel de Interoperabilidad Probada (6/6 Protocolos Certificados)

Todos los servicios y conectores listados en la IDE han sido probados en producción con respuesta `HTTP 200 OK`, sistema de referencia de coordenadas `EPSG:4326` (WGS84) y verificación criptográfica:

```bash
# 1. Catálogo STAC 1.0.0 (SpatioTemporal Asset Catalog)
curl -s https://ide.cit.uai.cl/stac/catalog.json | jq .id
# Retorno: "cit-uai-ide-catalog"

# 2. Cloud-Optimized GeoParquet 1.1 (Consulta SQL directa sin descargar todo el archivo)
duckdb -c "SELECT count(*), round(avg(bht_2017), 4) FROM 'https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet';"
# Retorno: 3.304 manzanas | BHT promedio: 0.3842

# 3. OGC GeoPackage (GPKG - Estándar ISO/IEC 19125 SQLite)
ogrinfo -so https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.gpkg mbht_2017_r15

# 4. ESRI Shapefile (ZIP con SHP + SHX + DBF + PRJ + CPG UTF-8)
curl -sI https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas_SHP.zip | grep -i content-length

# 5. Definición de Capa QGIS (QLR con Simbología de Jenks 6 Clases)
curl -s https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr | head -n 5

# 6. Metadatos ISO 19139 / Dublin Core XML (gmd:MD_Metadata)
curl -s https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml | head -n 10
```

---

## 🔬 5. Protocolo Seguro de Reproducibilidad Científica E2E

Para garantizar la integridad de la cadena de suministro de software y eliminar riesgos de ejecución remota de código no auditado, la IDE CIT implementa un **protocolo determinista de 3 pasos** con verificación criptográfica SHA-256 previa a la ejecución:

```bash
# Paso 1: Descargar el script autónomo de verificación
curl -s -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py

# Paso 2: Verificar la integridad del script mediante su SHA-256 publicado
echo "7fb25d61a29544e57c17869c6ea3566c68659d003dce9f59dfcd642fbf96a8d0  reproducir_verificacion_r15.py" | sha256sum -c
# Salida esperada: reproducir_verificacion_r15.py: LA AUTENTICACIÓN COINCIDE (OK)

# Paso 3: Ejecutar la verificación localmente en un entorno aislado
python reproducir_verificacion_r15.py
```

### Benchmark de Reproducción (Manzana Testigo `15101011001004001` — Arica):
| Parámetro | Valor Verificado Oficial | Tolerancia Aceptada |
| :--- | :--- | :--- |
| **BHT Síntesis 2017** | `0.3751` | $\pm 0.0001$ |
| **Dimensión Accesibilidad** | `0.3204` | $\pm 0.0001$ |
| **Dimensión Socioeconómica** | `0.4421` | $\pm 0.0001$ |
| **Dimensión Seguridad** | `0.4102` | $\pm 0.0001$ |
| **Dimensión Ambiental** | `0.3276` | $\pm 0.0001$ |

---

## 🛠️ 6. Estructura del Proyecto y Código Fuente

```
IDE_Data_Hub/
├── generador_portal_ide_cit.py           # Generador maestro SSG de index.html, CSV y DCAT
├── generador_descargas_2017.py           # Generador del centro de descargas territoriales
├── generador_guia_tecnica.py             # Generador de la guía metodológica interactiva
├── generador_red_ides.py                 # Generador del directorio de los 19 geoportales SNIT
├── generador_ficha_dataset.py            # Generador de la ficha técnica maestra 17D
├── compilar_y_certificar_ecosistema_ide.py # Orquestador maestro de compilación y QA
├── auditor_adversarial_ide.py            # Red Team automatizado (12 vectores de auditoría)
├── motor_ia_cit.py                       # Motor NLP y telemetría del Copiloto IA Territorial
├── data/
│   ├── catalogo_ide_cit.json             # Fuente Única de Verdad (Single Source of Truth)
│   ├── connection_examples.json          # Ejemplos de consumo multi-lenguaje (Python, R, QGIS)
│   └── iso_xml/                          # 29 esquemas XML normalizados ISO 19139
├── stac/                                 # Catálogo STAC 1.0.0 (18 colecciones georreferenciadas)
├── download/
│   ├── reproducir_verificacion_r15.py    # Script ejecutable de verificación científica E2E
│   └── SHA256SUMS.txt                    # Registro maestro de sumas de comprobación SHA-256
├── requirements.txt                      # Dependencias de Python mínimas
└── .gitignore                            # Exclusión de datos pesados (>100MB) y secretos
```

---

## 🚀 7. Guía de Instalación y Desarrollo Local

### Requisitos Previos
- Python 3.10 o superior.
- Git 2.40+.

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/CIT-UAI/ide-data-hub.git
cd ide-data-hub
```

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Compilar el Ecosistema Completo
Para regenerar todos los artefactos HTML, catálogos STAC, esquemas ISO y validar los 658 hashes criptográficos:
```bash
python compilar_y_certificar_ecosistema_ide.py
```

### Paso 4: Iniciar Servidor Local de Previsualización
- En Windows: Hacer doble clic en `INICIAR_PORTAL_LOCAL.bat`.
- En Linux / macOS / Terminal:
  ```bash
  python -m http.server 8080
  ```
  Abrir `http://localhost:8080` en el navegador.

### Paso 5: Ejecutar la Suite de Auditoría Adversarial (Red Team)
```bash
python auditor_adversarial_ide.py
```

---

## 🔒 8. Seguridad y Divulgación de Vulnerabilidades (RFC 9116)

El Centro de Inteligencia Territorial mantiene un programa de divulgación responsable de vulnerabilidades y seguridad de la información institucional:
- **Contacto de Seguridad:** `mailto:security@uai.cl`
- **Contacto del Centro:** `mailto:contactocit@uai.cl`
- **Archivo de Seguridad Canónico:** [`https://ide.cit.uai.cl/.well-known/security.txt`](https://ide.cit.uai.cl/.well-known/security.txt)
- **Vigencia:** 31 de diciembre de 2027
- **Política de Cero Secretos en Código:** Estricto cumplimiento del principio de aislamiento de credenciales (Invariante 27 de arquitectura CIT).

---

## 📜 9. Licencia y Citación Académica

El código fuente de este repositorio se distribuye bajo **Licencia Institucional CIT-UAI**. Los datos geoespaciales abiertos se distribuyen bajo términos equivalentes a **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

### Citación Oficial en Formato APA 7:
> Centro de Inteligencia Territorial. (2026). *Infraestructura de Datos Espaciales (IDE CIT) y Matriz de Bienestar Humano Territorial (MBHT)*. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl
