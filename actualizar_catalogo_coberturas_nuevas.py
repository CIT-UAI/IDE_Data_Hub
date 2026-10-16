#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualiza catalogo_ide_cit.json con:
1. INSE Socioeconómico 2024: solo atributos estrictamente relacionados con INSE.
2. Censo e Imputaciones 2024: rutas de descarga y atributos normalizados.
3. Educación Inicial (Jardines y Salas Cuna 2024).
4. Huella de Edificaciones Urbanas (Buildings 2024).
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_proyecto_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent

ROOT = find_proyecto_root()
CATALOG_PATH = ROOT / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub" / "data" / "catalogo_ide_cit.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    cat = json.load(f)

capas = cat.get("capas", [])

# 1. ACTUALIZAR INSE
for c in capas:
    if c.get("id") == "inse_socioeconomico":
        c["titulo"] = "Índice de Nivel Socioeconómico (INSE) — Manzanas Censales 2024"
        c["cobertura"] = "Nacional (16 Regiones de Chile — 254.268 manzanas censales)"
        c["resumen"] = (
            "Estratificación socioeconómica y patrimonial continua y por quintiles (Q1 a Q5, y S/P sin población) "
            "calibrada a nivel nacional para 254.268 manzanas censales en las 16 regiones de Chile. Integra la caracterización "
            "socioeconómica de los hogares (capital humano y ocupación CIUO) con la valoración patrimonial inmobiliaria de suelo "
            "según Áreas Homogéneas del SII (Ley 17.235) y Valor Guía de Terreno (VGT en UF/m² y $/m²)."
        )
        c["formula_lineage"] = (
            "Calibración econométrica multivariada del Índice de Nivel Socioeconómico a escala de manzana: "
            "INSE = f(Capital Humano, Inserción Ocupacional, Valor Guía de Terreno SII). "
            "Estratificación por quintiles poblacionales Q1 a Q5 y categorización GSE."
        )
        c["s3_parquet"] = "download/INSE_Socioeconomico_Nacional_2024.parquet"
        c["gpkg_url"] = "download/INSE_Socioeconomico_Nacional_2024.gpkg"
        c["shp_url"] = "download/INSE_Socioeconomico_Nacional_2024_SHP.zip"
        c["csv_url"] = "download/INSE_Socioeconomico_Nacional_2024.csv"
        c["atributos"] = [
            {"campo": "MANZ_CIT", "tipo": "String", "descripcion": "Código censal único de la manzana (16 dígitos)"},
            {"campo": "COD_REG", "tipo": "String", "descripcion": "Código oficial de la región"},
            {"campo": "COD_COM", "tipo": "String", "descripcion": "Código único de la comuna (CUT)"},
            {"campo": "COMUNA", "tipo": "String", "descripcion": "Nombre oficial de la comuna"},
            {"campo": "POBLACION", "tipo": "Float", "descripcion": "Población residente censal habitual"},
            {"campo": "INSE_OFIC", "tipo": "Float", "descripcion": "Puntaje de Nivel Socioeconómico Oficial [0.0 - 100.0]"},
            {"campo": "Q_INSE_OFI", "tipo": "String", "descripcion": "Estratificación por quintiles oficial (Q1 a Q5, o S/P sin población)"},
            {"campo": "GSE_OFIC", "tipo": "String", "descripcion": "Grupo Socioeconómico Oficial (ABC1, C2, C3, D, E, S/P)"},
            {"campo": "INSE_PURO", "tipo": "Float", "descripcion": "Puntaje de Nivel Socioeconómico modelo econométrico base"},
            {"campo": "Q_INSE_PUR", "tipo": "String", "descripcion": "Quintil modelo econométrico base"},
            {"campo": "GSE_PURO", "tipo": "String", "descripcion": "Grupo Socioeconómico modelo econométrico base"},
            {"campo": "ES_CAMPAM", "tipo": "String", "descripcion": "Indicador si la manzana corresponde a asentamiento precario / campamento (V/F)"},
            {"campo": "COD_AH", "tipo": "String", "descripcion": "Código de Área Homogénea del SII asignada (Ley 17.235)"},
            {"campo": "VGT_UF", "tipo": "Float", "descripcion": "Valor Guía de Terreno asignado en UF/m²"},
            {"campo": "VGT_M2", "tipo": "Float", "descripcion": "Valor Guía de Terreno asignado en $/m²"}
        ]

# 2. ACTUALIZAR CENSO 2024
for c in capas:
    if c.get("id") == "censo_imputaciones_2024":
        c["titulo"] = "Censo 2024 — Imputaciones Demográficas por Cohortes y Sexo"
        c["cobertura"] = "Nacional (16 Regiones de Chile — 254.268 manzanas censales)"
        c["s3_parquet"] = "download/Censo_Imputaciones_2024_Nacional.parquet"
        c["gpkg_url"] = "download/Censo_Imputaciones_2024_Nacional.gpkg"
        c["shp_url"] = "download/Censo_Imputaciones_2024_Nacional_SHP.zip"
        c["csv_url"] = "download/Censo_Imputaciones_2024_Nacional.csv"
        c["atributos"] = [
            {"campo": "ID_MANZCIT", "tipo": "String", "descripcion": "Código censal único de la manzana (16 dígitos)"},
            {"campo": "COD_REG", "tipo": "Integer", "descripcion": "Código numérico de la región"},
            {"campo": "REGION", "tipo": "String", "descripcion": "Nombre oficial de la región"},
            {"campo": "COD_PROV", "tipo": "Integer", "descripcion": "Código de la provincia"},
            {"campo": "PROVINCIA", "tipo": "String", "descripcion": "Nombre de la provincia"},
            {"campo": "COD_COM", "tipo": "Integer", "descripcion": "Código único de la comuna (CUT)"},
            {"campo": "COMUNA", "tipo": "String", "descripcion": "Nombre de la comuna"},
            {"campo": "CATEGORIA", "tipo": "String", "descripcion": "Categoría territorial censal (Urbana / Rural)"},
            {"campo": "AREA_C", "tipo": "Float", "descripcion": "Superficie de la manzana (m²)"},
            {"campo": "POBLACION_2024", "tipo": "Float", "descripcion": "Total de población residente censal estimada (Censo 2024)"},
            {"campo": "HOMBRES", "tipo": "Float", "descripcion": "Total de población masculina"},
            {"campo": "MUJERES", "tipo": "Float", "descripcion": "Total de población femenina"},
            {"campo": "P_HOMBRES", "tipo": "Float", "descripcion": "Porcentaje de hombres sobre el total comunal/manzana"},
            {"campo": "P_MUJERES", "tipo": "Float", "descripcion": "Porcentaje de mujeres sobre el total comunal/manzana"},
            {"campo": "E0_5", "tipo": "Float", "descripcion": "Población de primera infancia (0 a 5 años) graduada por Sprague"},
            {"campo": "E6_13", "tipo": "Float", "descripcion": "Población escolar básica (6 a 13 años)"},
            {"campo": "E14_17", "tipo": "Float", "descripcion": "Población escolar media (14 a 17 años)"},
            {"campo": "E18_24", "tipo": "Float", "descripcion": "Población juvenil (18 a 24 años)"},
            {"campo": "E25_44", "tipo": "Float", "descripcion": "Población adulta joven (25 a 44 años)"},
            {"campo": "E45_59", "tipo": "Float", "descripcion": "Población adulta intermedia (45 a 59 años)"},
            {"campo": "E60M", "tipo": "Float", "descripcion": "Población adulta mayor (60 años y más)"},
            {"campo": "E65AMAS", "tipo": "Float", "descripcion": "Población adulta mayor (65 años y más)"},
            {"campo": "IND_ENVEJ", "tipo": "Float", "descripcion": "Índice de envejecimiento demográfico (pob 60+ / pob 0-14 * 100)"}
        ]

# 3. AGREGAR EDUCACIÓN INICIAL 2024
ids_existentes = [c.get("id") for c in capas]
if "educacion_inicial_2024" not in ids_existentes:
    capas.append({
        "id": "educacion_inicial_2024",
        "titulo": "Educación Inicial — Catastro Nacional de Jardines Infantiles y Salas Cuna",
        "matriz": "mbht",
        "ambito": "tierra",
        "escala": "Equipamientos georreferenciados (Puntos WGS 84)",
        "cobertura": "Nacional (16 Regiones de Chile — 3.886 establecimientos)",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial CIT-UAI",
        "resumen": (
            "Catastro maestro nacional unificado de establecimientos de educación inicial (jardines infantiles y salas cuna) "
            "para las 16 regiones de Chile. Integra tanto la oferta pública (JUNJI, Integra, VTF, SLEP y Municipal) como la oferta "
            "privada particular subvencionada y particular pagada, detallando capacidad y matrícula por nivel formativo "
            "(Sala Cuna Menor/Mayor, Nivel Medio Menor/Mayor, Prekínder NT1 y Kínder NT2). Insumo base para la evaluación de cobertura "
            "y accesibilidad peatonal infantil en la MBHT."
        ),
        "formula_lineage": (
            "Georreferenciación multiproveedor validada por verificación espacial comunal y cruce con Directorio Oficial MINEDUC / "
            "Subsecretaría de Educación Parvularia (SdEP). Normalización taxonómica de dependencia institucional y desagregación de matrícula."
        ),
        "autor": "Centro de Inteligencia Territorial (CIT-UAI)",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "educacion_inicial_2024",
        "tabla_postgis": "equipamientos.educacion_inicial_2024",
        "s3_parquet": "download/Educacion_Inicial_Jardines_SalasCuna_2024.parquet",
        "gpkg_url": "download/Educacion_Inicial_Jardines_SalasCuna_2024.gpkg",
        "shp_url": "download/Educacion_Inicial_Jardines_SalasCuna_2024_SHP.zip",
        "csv_url": "download/Educacion_Inicial_Jardines_SalasCuna_2024.csv",
        "atributos": [
            {"campo": "id_mbht", "tipo": "String", "descripcion": "Identificador único MBHT del equipamiento"},
            {"campo": "rbd", "tipo": "String", "descripcion": "Rol Base de Datos oficial MINEDUC"},
            {"campo": "nombre_establecimiento", "tipo": "String", "descripcion": "Nombre oficial del jardín infantil o sala cuna"},
            {"campo": "dependencia_macro", "tipo": "String", "descripcion": "Dependencia administrativa macro (Pública / Privada)"},
            {"campo": "dependencia_especifica", "tipo": "String", "descripcion": "Dependencia específica (JUNJI, Integra, VTF, Particular Pagado, etc.)"},
            {"campo": "tipo_establecimiento", "tipo": "String", "descripcion": "Tipología (Jardín Infantil con Sala Cuna, Solo Jardín, Solo Sala Cuna)"},
            {"campo": "tiene_sala_cuna", "tipo": "Integer", "descripcion": "Indicador binario de oferta de sala cuna (0/1)"},
            {"campo": "tiene_nivel_medio", "tipo": "Integer", "descripcion": "Indicador binario de oferta de nivel medio menor/mayor (0/1)"},
            {"campo": "mat_sc_total", "tipo": "Integer", "descripcion": "Total matrícula efectiva en sala cuna"},
            {"campo": "mat_med_total", "tipo": "Integer", "descripcion": "Total matrícula efectiva en nivel medio"},
            {"campo": "mat_total_parvularia", "tipo": "Integer", "descripcion": "Total general de matrícula parvularia"},
            {"campo": "comuna_nom", "tipo": "String", "descripcion": "Nombre de la comuna"},
            {"campo": "region_nom", "tipo": "String", "descripcion": "Nombre de la región"},
            {"campo": "latitud", "tipo": "Float", "descripcion": "Latitud geográfica (EPSG:4326)"},
            {"campo": "longitud", "tipo": "Float", "descripcion": "Longitud geográfica (EPSG:4326)"}
        ],
        "citacion": "Centro de Inteligencia Territorial. (2024). Catastro Maestro Nacional de Educación Inicial Pública y Privada (Salas Cuna y Jardines Infantiles) [Conjunto de datos geoespaciales]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-109.43, -54.94, -67.6, -18.25],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "Point",
        "fuentes_institucionales": [
            {
                "institucion": "Ministerio de Educación [MINEDUC] / Subsecretaría de Educación Parvularia [SdEP]",
                "insumo": "Directorio Oficial de Establecimientos Parvularios 2024",
                "citacion_apa7": "Ministerio de Educación. (2024). Directorio oficial de establecimientos de educación parvularia [Base de datos]. MINEDUC. https://datosabiertos.mineduc.cl",
                "url": "https://datosabiertos.mineduc.cl"
            },
            {
                "institucion": "Junta Nacional de Jardines Infantiles [JUNJI] / Fundación Integra",
                "insumo": "Catastro Operativo de Jardines Infantiles Públicos y Vía Transferencia de Fondos",
                "citacion_apa7": "JUNJI. (2024). Catastro nacional de unidades educativas públicas [Conjunto de datos]. JUNJI. https://www.junji.gob.cl",
                "url": "https://www.junji.gob.cl"
            },
            {
                "institucion": "Centro de Inteligencia Territorial [CIT-UAI]",
                "insumo": "Normalización y Geocodificación Espacial MBHT",
                "citacion_apa7": "Centro de Inteligencia Territorial [CIT-UAI]. (2024). Normalización espacial de equipamientos urbanos para la MBHT [Metodología]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
                "url": "https://ide.cit.uai.cl"
            }
        ]
    })

# 4. AGREGAR HUELLA DE EDIFICACIONES 2024
if "huella_edificaciones_2024" not in ids_existentes:
    capas.append({
        "id": "huella_edificaciones_2024",
        "titulo": "Huella de Edificaciones Urbanas — Presencia Construida Nacional",
        "matriz": "mbht",
        "ambito": "tierra",
        "escala": "Polígonos de edificaciones (Alta resolución espacial)",
        "cobertura": "Nacional urbana (341.962 polígonos de edificaciones)",
        "fecha_corte": "2024-10-10",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial CIT-UAI",
        "resumen": (
            "Catastro vectorial de huella construida y morfología del entorno edificado para 341.962 polígonos urbanos a nivel nacional. "
            "Identifica la superficie en metros cuadrados, nivel de confianza algorítmica y años de presencia de las estructuras urbanas, "
            "permitiendo modelar la densidad predial, compacidad morfológica y dinámicas de densificación en ciudades chilenas."
        ),
        "formula_lineage": (
            "Detección y extracción vectorial de huella de edificaciones mediante modelos de segmentación satelital y fotogrametría aérea "
            "de alta resolución, con verificación multitemporal de presencia construida."
        ),
        "autor": "Centro de Inteligencia Territorial (CIT-UAI)",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "huella_edificaciones_2024",
        "tabla_postgis": "morfologia.huella_edificaciones_2024",
        "s3_parquet": "download/Huella_Edificaciones_Urbanas_2024.parquet",
        "gpkg_url": "download/Huella_Edificaciones_Urbanas_2024.gpkg",
        "shp_url": "download/Huella_Edificaciones_Urbanas_2024_SHP.zip",
        "csv_url": "download/Huella_Edificaciones_Urbanas_2024.csv",
        "atributos": [
            {"campo": "latitude", "tipo": "Float", "descripcion": "Latitud centroidal de la edificación (EPSG:4326)"},
            {"campo": "longitude", "tipo": "Float", "descripcion": "Longitud centroidal de la edificación (EPSG:4326)"},
            {"campo": "area_in_me", "tipo": "Float", "descripcion": "Área de la huella construida en metros cuadrados (m²)"},
            {"campo": "confidence", "tipo": "Float", "descripcion": "Nivel de confianza de la detección algorítmica [0.0 - 1.0]"},
            {"campo": "full_plus_", "tipo": "String", "descripcion": "Código Plus Code Open Location de localización espacial"},
            {"campo": "years", "tipo": "String", "descripcion": "Años de detección comprobada de presencia construida"}
        ],
        "citacion": "Centro de Inteligencia Territorial. (2024). Catastro Vectorial de Huella y Presencia de Edificaciones Urbanas de Chile [Conjunto de datos geoespaciales]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-75.64, -55.98, -66.86, -17.5],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "Polygon",
        "fuentes_institucionales": [
            {
                "institucion": "Centro de Inteligencia Territorial [CIT-UAI]",
                "insumo": "Catastro Morfológico y Vectorización de Huella Urbana",
                "citacion_apa7": "Centro de Inteligencia Territorial [CIT-UAI]. (2024). Catastro de morfología y huella construida en ciudades chilenas [Base cartográfica]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
                "url": "https://ide.cit.uai.cl"
            }
        ]
    })

cat["capas"] = capas

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, indent=2, ensure_ascii=False)

print(f"✓ Catálogo actualizado con éxito. Total capas: {len(capas)}")
