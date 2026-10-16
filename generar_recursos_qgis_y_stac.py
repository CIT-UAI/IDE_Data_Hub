#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Recursos QGIS (.qlr), Catálogo Estático STAC 1.0.0 y Clean URLs para IDE CIT.
Centro de Inteligencia Territorial (CIT) — Universidad Adolfo Ibáñez.
"""
import json
import os
import shutil
from pathlib import Path

from motor_ia_cit import (
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
)

BASE_DIR = Path(__file__).resolve().parent
CATALOGO_JSON = BASE_DIR / "data" / "catalogo_ide_cit.json"
STAC_DIR = BASE_DIR / "stac"
QGIS_DIR = BASE_DIR / "download" / "qgis"
DIST_DIR = BASE_DIR / "dist"

def ensure_dirs():
    STAC_DIR.mkdir(parents=True, exist_ok=True)
    QGIS_DIR.mkdir(parents=True, exist_ok=True)
    if DIST_DIR.exists():
        (DIST_DIR / "stac").mkdir(parents=True, exist_ok=True)
        (DIST_DIR / "download" / "qgis").mkdir(parents=True, exist_ok=True)

def generar_stac():
    print("[*] Generando Catálogo Estático STAC 1.0.0...")
    with open(CATALOGO_JSON, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    # 1. Colecciones hijas para el catálogo raíz
    child_links = []
    
    # 2. Generar colecciones individuales para las 13 capas oficiales
    for capa in catalog_data.get("capas", []):
        cid = capa["id"]
        col_id = cid.replace("_", "-")
        titulo = capa["titulo"]
        resumen = capa["resumen"]
        version = f"v{capa.get('version', '1.0.3')}"
        status = "Línea base oficial cerrada y vigente" if cid == "kpi_mud_2017" else ("Insumos censales preparatorios disponibles" if cid == "censo_imputaciones_2024" else "Conjunto de datos oficial vigente")
        bbox = capa.get("bbox", [-109.45, -56.53, -66.41, -17.50])
        
        assets = {}
        if capa.get("s3_parquet"):
            assets["geoparquet"] = {
                "title": f"GeoParquet — {titulo}",
                "type": "application/vnd.apache.parquet",
                "roles": ["data"],
                "href": f"https://ide.cit.uai.cl/{capa['s3_parquet']}"
            }
            if capa.get("size_bytes"):
                assets["geoparquet"]["file:size"] = capa["size_bytes"]
            if capa.get("sha256"):
                assets["geoparquet"]["file:checksum"] = capa["sha256"]
        if capa.get("gpkg_url"):
            assets["geopackage"] = {
                "title": f"OGC GeoPackage — {titulo}",
                "type": "application/geopackage+sqlite3",
                "roles": ["data"],
                "href": f"https://ide.cit.uai.cl/{capa['gpkg_url']}"
            }
        if capa.get("shp_url"):
            assets["shapefile"] = {
                "title": f"Shapefile (.zip) — {titulo}",
                "type": "application/zip",
                "roles": ["data"],
                "href": f"https://ide.cit.uai.cl/{capa['shp_url']}"
            }
        if capa.get("csv_url"):
            assets["csv"] = {
                "title": f"Tabla CSV — {titulo}",
                "type": "text/csv",
                "roles": ["data"],
                "href": f"https://ide.cit.uai.cl/{capa['csv_url']}"
            }
        assets["metadata_iso19139"] = {
            "title": f"Metadatos Oficiales ISO 19115 / ISO 19139 XML — {titulo}",
            "type": "application/xml",
            "roles": ["metadata"],
            "href": f"https://ide.cit.uai.cl/download/iso_xml/{cid}_iso19139.xml"
        }
        
        summaries = {
            "version": [version],
            "status": [status],
            "matriz": [capa.get("matriz", "mbht")],
            "escala": [capa.get("escala", "Nacional")],
            "physical_columns": [len(capa.get("atributos", []))]
        }
        if cid == "kpi_mud_2017":
            summaries["macro_dimensions"] = ["dim_acc (6/18)", "dim_soc (6/18)", "dim_seg (4/18)", "dim_amb (2/18)"]
            summaries["accessibility_subindicators"] = ["isal", "ise", "iav", "idep", "icul", "iser"]
            assets["geoparquet_muestra_r15"] = {
                "title": "Muestra Ligera Reproducible GeoParquet — Región de Arica y Parinacota R15 (3.304 manzanas, 42 columnas, 2,37 MB)",
                "type": "application/vnd.apache.parquet",
                "roles": ["data"],
                "href": "https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet",
                "file:size": 2482961,
                "file:checksum": "712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505"
            }
        elif cid == "censo_imputaciones_2024":
            summaries["demographic_fields"] = ["POBLACION_2024", "HOMBRES", "MUJERES", "E0_5", "E6_13", "E14_17", "E18_24", "E25_44", "E45_59", "E60M", "E65AMAS", "IND_ENVEJ"]
            
        col_json = {
            "stac_version": "1.0.0",
            "type": "Collection",
            "id": col_id,
            "title": titulo,
            "description": resumen,
            "license": "CC-BY-4.0",
            "extent": {
                "spatial": {"bbox": [bbox]},
                "temporal": {"interval": [["2017-01-01T00:00:00Z", "2026-12-31T23:59:59Z"]]}
            },
            "summaries": summaries,
            "links": [
                {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "parent", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "self", "type": "application/json", "href": f"https://ide.cit.uai.cl/stac/{cid}.json"}
            ],
            "assets": assets
        }
        
        with open(STAC_DIR / f"{cid}.json", "w", encoding="utf-8") as f:
            json.dump(col_json, f, indent=2, ensure_ascii=False)
            
        child_links.append({
            "rel": "child",
            "type": "application/json",
            "title": titulo,
            "href": f"https://ide.cit.uai.cl/stac/{cid}.json"
        })
        
        # Aliases para compatibilidad hacia atrás
        if cid == "kpi_mud_2017":
            alias_col = dict(col_json)
            alias_col["id"] = "mbht-2017"
            alias_col["links"] = [
                {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "parent", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "self", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/mbht_2017.json"}
            ]
            with open(STAC_DIR / "mbht_2017.json", "w", encoding="utf-8") as f:
                json.dump(alias_col, f, indent=2, ensure_ascii=False)
        elif cid == "pem_maritorio_nacional":
            alias_col = dict(col_json)
            alias_col["id"] = "pem-maritorio"
            alias_col["links"] = [
                {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "parent", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "self", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/pem_maritorio.json"}
            ]
            with open(STAC_DIR / "pem_maritorio.json", "w", encoding="utf-8") as f:
                json.dump(alias_col, f, indent=2, ensure_ascii=False)
        elif cid == "equipamientos_2017":
            alias_col = dict(col_json)
            alias_col["id"] = "equipamientos-urbanos"
            alias_col["links"] = [
                {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "parent", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
                {"rel": "self", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/equipamientos.json"}
            ]
            with open(STAC_DIR / "equipamientos.json", "w", encoding="utf-8") as f:
                json.dump(alias_col, f, indent=2, ensure_ascii=False)

    # 3. STAC Collection Informativa Oficial: mbht_2024.json (HTTP 200 OK)
    col_mbht_2024 = {
        "stac_version": "1.0.0",
        "type": "Collection",
        "id": "mbht-2024-aviso",
        "title": "Matriz de Bienestar Humano Territorial MBHT 2024 — Publicación Oficial Programada para Noviembre 2026",
        "description": "Aviso oficial del Centro de Inteligencia Territorial (CIT-UAI): La síntesis multidimensional de la Matriz de Bienestar Humano Territorial MBHT 2024 se encuentra en fase final de calibración metodológica y contrastación empírica con los microdatos definitivos del INE, con lanzamiento oficial y publicación de matrices abierta programada para noviembre de 2026. Los insumos demográficos preparatorios de base (254.395 manzanas urbanas y entidades rurales con imputaciones de Sprague y desagregación por sexo) se encuentran 100% disponibles para descarga abierta inmediata en la colección 'censo_imputaciones_2024'. Para análisis retrospectivos y modelos vigentes en producción, consulte la línea base oficial en 'mbht_2017'.",
        "license": "CC-BY-4.0",
        "extent": {
            "spatial": {"bbox": [[-109.45, -56.53, -66.41, -17.50]]},
            "temporal": {"interval": [["2024-01-01T00:00:00Z", "2026-12-31T23:59:59Z"]]}
        },
        "summaries": {
            "version": ["2024-prelanzamiento"],
            "status": ["Publicación oficial programada para noviembre de 2026"],
            "insumos_disponibles": ["censo_imputaciones_2024"],
            "linea_base_vigente": ["mbht_2017"]
        },
        "links": [
            {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
            {"rel": "parent", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
            {"rel": "self", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/mbht_2024.json"},
            {"rel": "related", "type": "application/json", "title": "Censo 2024 — Imputaciones Demográficas por Cohortes y Sexo (Disponible)", "href": "https://ide.cit.uai.cl/stac/censo_imputaciones_2024.json"},
            {"rel": "related", "type": "application/json", "title": "Matriz MBHT 2017 — Línea Base Oficial Vigente (42 Columnas Físicas)", "href": "https://ide.cit.uai.cl/stac/mbht_2017.json"},
            {"rel": "via", "type": "text/html", "title": "Plataforma Canónica MBHT", "href": "https://matrizbht.cl"}
        ],
        "assets": {
            "guia_tecnica": {
                "title": "Guía Técnica y Metodológica IDE CIT",
                "type": "text/html",
                "roles": ["metadata"],
                "href": "https://ide.cit.uai.cl/guia-tecnica"
            },
            "ficha_mbht_2017": {
                "title": "Ficha Técnica Maestra MBHT 2017 (Línea Base Oficial)",
                "type": "text/html",
                "roles": ["metadata"],
                "href": "https://ide.cit.uai.cl/ficha-mbht-2017"
            },
            "insumos_censo_2024": {
                "title": "Colección STAC Censo 2024 Imputaciones Demográficas (Datos Preparatorios Disponibles)",
                "type": "application/json",
                "roles": ["data"],
                "href": "https://ide.cit.uai.cl/stac/censo_imputaciones_2024.json"
            }
        }
    }
    with open(STAC_DIR / "mbht_2024.json", "w", encoding="utf-8") as f:
        json.dump(col_mbht_2024, f, indent=2, ensure_ascii=False)

    child_links.append({
        "rel": "child",
        "type": "application/json",
        "title": "MBHT 2024 — Aviso Oficial de Lanzamiento (Noviembre 2026)",
        "href": "https://ide.cit.uai.cl/stac/mbht_2024.json"
    })
    child_links.append({
        "rel": "child",
        "type": "application/json",
        "title": "Colección Unificada (13 Capas Cartográficas Maestras)",
        "href": "https://ide.cit.uai.cl/stac/collection.json"
    })

    root_catalog = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Catalog",
        "id": "cit-uai-ide-catalog",
        "title": "Catálogo de Datos y Modelos Territoriales — IDE CIT (UAI)",
        "description": "Catálogo espacio-temporal (STAC 1.0.0) de coberturas geoespaciales, matrices de bienestar humano territorial (MBHT 2017/2024), zonificación marina (PEM/FAO/SBAP) e imputaciones demográficas del Centro de Inteligencia Territorial de la Universidad Adolfo Ibáñez.",
        "links": [
            {"rel": "self", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
            {"rel": "root", "type": "application/json", "href": "https://ide.cit.uai.cl/stac/catalog.json"},
        ] + child_links,
        "conformsTo": [
            "https://api.stacspec.org/v1.0.0/core",
            "https://api.stacspec.org/v1.0.0/collections"
        ]
    }
    with open(STAC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(root_catalog, f, indent=2, ensure_ascii=False)

    data_stac_col = BASE_DIR / "data" / "stac" / "collection.json"
    if data_stac_col.exists():
        shutil.copy2(data_stac_col, STAC_DIR / "collection.json")

    if DIST_DIR.exists():
        (DIST_DIR / "stac").mkdir(parents=True, exist_ok=True)
        for stac_file in STAC_DIR.glob("*.json"):
            shutil.copy2(stac_file, DIST_DIR / "stac" / stac_file.name)

    print(f"  [+] STAC 1.0.0 generado exitosamente (catalog.json con {len(child_links)} colecciones hijas).")

def generar_stac_html():
    print("[*] Generando interfaz HTML y visualizador del Catálogo STAC 1.0.0 (stac/index.html)...")
    header_html = get_canonical_header_html("stac")
    footer_html = get_canonical_footer_html("2026.1")
    head_meta = get_llm_head_meta()
    guidance_html = get_llm_guidance_html()

    with open(CATALOGO_JSON, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    cards_html = []
    # Root Catalog Card
    cards_html.append("""                <!-- Root Catalog Card -->
                <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold font-mono text-uai-gold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Catalog Root</span>
                            <span class="text-xs text-slate-400 font-mono">v1.0.0</span>
                        </div>
                        <h3 class="font-bold text-slate-900 text-base mb-1">Catálogo Raíz CIT-UAI</h3>
                        <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                            Índice maestro espacio-temporal con enlaces canónicos a todas las colecciones territoriales activas.
                        </p>
                    </div>
                    <div class="pt-3 border-t border-slate-100">
                        <div class="text-[11px] font-mono text-slate-500 break-all bg-slate-50 p-2 rounded mb-2 select-all">
                            https://ide.cit.uai.cl/stac/catalog.json
                        </div>
                        <a href="https://ide.cit.uai.cl/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="w-full inline-flex items-center justify-center py-1.5 px-3 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition">
                            <i data-lucide="external-link" class="w-3.5 h-3.5 mr-1.5"></i>
                            Abrir JSON
                        </a>
                    </div>
                </div>""")

    # Collections for all 13 official layers
    for capa in catalog_data.get("capas", []):
        cid = capa["id"]
        titulo = capa["titulo"]
        resumen = capa["resumen"]
        ambito = capa.get("ambito", "tierra")
        if cid == "kpi_mud_2017":
            badge_cls = "text-emerald-700 bg-emerald-50 border-emerald-200"
            badge_lbl = "Collection · Vigente"
        elif cid == "censo_imputaciones_2024":
            badge_cls = "text-blue-700 bg-blue-50 border-blue-200"
            badge_lbl = "Collection · Descarga Abierta"
        elif ambito == "mar":
            badge_cls = "text-cyan-700 bg-cyan-50 border-cyan-200"
            badge_lbl = "Collection · Vigente"
        else:
            badge_cls = "text-slate-700 bg-slate-100 border-slate-200"
            badge_lbl = "Collection · Vigente"
            
        cards_html.append(f"""                <!-- {cid} Collection -->
                <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold font-mono {badge_cls} px-2 py-0.5 rounded border">{badge_lbl}</span>
                            <span class="text-xs text-slate-400 font-mono">{cid}</span>
                        </div>
                        <h3 class="font-bold text-slate-900 text-base mb-1">{titulo}</h3>
                        <p class="text-xs text-slate-600 mb-3 leading-relaxed line-clamp-3">
                            {resumen}
                        </p>
                    </div>
                    <div class="pt-3 border-t border-slate-100">
                        <div class="text-[11px] font-mono text-slate-500 break-all bg-slate-50 p-2 rounded mb-2 select-all">
                            https://ide.cit.uai.cl/stac/{cid}.json
                        </div>
                        <a href="https://ide.cit.uai.cl/stac/{cid}.json" target="_blank" rel="noopener noreferrer" class="w-full inline-flex items-center justify-center py-1.5 px-3 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition">
                            <i data-lucide="external-link" class="w-3.5 h-3.5 mr-1.5"></i>
                            Abrir JSON
                        </a>
                    </div>
                </div>""")

    # MBHT 2024 Notice Card
    cards_html.append("""                <!-- MBHT 2024 Notice Card -->
                <div class="bg-amber-50/50 border border-amber-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold font-mono text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-300">Aviso Oficial · Noviembre 2026</span>
                            <span class="text-xs text-slate-400 font-mono">mbht-2024</span>
                        </div>
                        <h3 class="font-bold text-slate-900 text-base mb-1">MBHT 2024 — Aviso de Lanzamiento</h3>
                        <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                            Aviso oficial del CIT-UAI: Publicación oficial de la síntesis multidimensional programada para noviembre de 2026. Insumos demográficos preparatorios disponibles en 'censo_imputaciones_2024'.
                        </p>
                    </div>
                    <div class="pt-3 border-t border-amber-200/60">
                        <div class="text-[11px] font-mono text-slate-500 break-all bg-white p-2 rounded mb-2 select-all border border-amber-200/60">
                            https://ide.cit.uai.cl/stac/mbht_2024.json
                        </div>
                        <a href="https://ide.cit.uai.cl/stac/mbht_2024.json" target="_blank" rel="noopener noreferrer" class="w-full inline-flex items-center justify-center py-1.5 px-3 rounded-lg bg-amber-100 hover:bg-amber-200 text-amber-900 text-xs font-semibold transition">
                            <i data-lucide="external-link" class="w-3.5 h-3.5 mr-1.5"></i>
                            Abrir JSON
                        </a>
                    </div>
                </div>""")

    # Master Collection Card
    cards_html.append("""                <!-- Unified STAC Collection -->
                <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold font-mono text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">Master Collection</span>
                            <span class="text-xs text-slate-400 font-mono">collection.json</span>
                        </div>
                        <h3 class="font-bold text-slate-900 text-base mb-1">Colección Unificada (13 Capas)</h3>
                        <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                            Especificación STAC agregada con los 13 conjuntos territoriales y oceánicos sincronizados con la fuente maestra de metadatos (catalogo_ide_cit.json).
                        </p>
                    </div>
                    <div class="pt-3 border-t border-slate-100">
                        <div class="text-[11px] font-mono text-slate-500 break-all bg-slate-50 p-2 rounded mb-2 select-all">
                            https://ide.cit.uai.cl/stac/collection.json
                        </div>
                        <a href="https://ide.cit.uai.cl/stac/collection.json" target="_blank" rel="noopener noreferrer" class="w-full inline-flex items-center justify-center py-1.5 px-3 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition">
                            <i data-lucide="external-link" class="w-3.5 h-3.5 mr-1.5"></i>
                            Abrir JSON
                        </a>
                    </div>
                </div>""")

    all_cards_str = "\n".join(cards_html)
    num_endpoints = len(cards_html)

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50 scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo STAC 1.0.0 — IDE CIT | Centro de Inteligencia Territorial UAI</title>
    <meta name="description" content="Punto de acceso oficial STAC 1.0.0 (SpatioTemporal Asset Catalog) de la IDE CIT - Universidad Adolfo Ibáñez. Colecciones geoespaciales cloud-native en GeoParquet, Vector Tiles y GeoPackage.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://ide.cit.uai.cl/stac/">
    <link rel="alternate" type="application/json" href="https://ide.cit.uai.cl/stac/catalog.json" title="STAC Catalog JSON">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        uai: {{
                            gold: '#6493B5', citCeleste: '#6493B5',
                            goldHover: '#4e7b9d', citCelesteHover: '#4e7b9d',
                            black: '#000000',
                            charcoal: '#1f1f23',
                            bgSoft: '#f8fafc',
                            border: '#e2e8f0',
                            navy: '#003865',
                            citBlue: '#6493B5'
                        }}
                    }}
                }}
            }}
        }};
    </script>
    {head_meta}
</head>
<body class="flex flex-col min-h-full font-sans text-slate-800 antialiased bg-slate-50 selection:bg-uai-gold/20 selection:text-uai-navy">
    {header_html}
    {guidance_html}

    <main id="main-content" role="main" tabindex="-1" class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <!-- Breadcrumb -->
        <nav class="flex text-xs text-slate-500 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li class="inline-flex items-center">
                    <a href="/" class="hover:text-uai-navy transition flex items-center">
                        <i data-lucide="home" class="w-3.5 h-3.5 mr-1"></i>
                        Inicio
                    </a>
                </li>
                <li>
                    <div class="flex items-center">
                        <i data-lucide="chevron-right" class="w-3.5 h-3.5 mx-1 text-slate-400"></i>
                        <span class="text-slate-400">Interoperabilidad</span>
                    </div>
                </li>
                <li aria-current="page">
                    <div class="flex items-center">
                        <i data-lucide="chevron-right" class="w-3.5 h-3.5 mx-1 text-slate-400"></i>
                        <span class="font-semibold text-slate-900">Catálogo STAC 1.0.0</span>
                    </div>
                </li>
            </ol>
        </nav>

        <!-- Hero Header -->
        <header class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm mb-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-100 text-slate-800 text-xs font-semibold uppercase tracking-wider mb-3">
                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                        <span>SpatioTemporal Asset Catalog · Versión 1.0.0</span>
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Catálogo Geoespacial STAC 1.0.0</h1>
                    <p class="mt-2 text-slate-600 max-w-3xl leading-relaxed text-sm sm:text-base">
                        Punto de acceso estandarizado para descubrimiento, consulta automatizada e ingesta de colecciones territoriales del Centro de Inteligencia Territorial de la Universidad Adolfo Ibáñez (CIT-UAI). Compatible con bibliotecas cliente en Python (<code class="bg-slate-100 px-1 py-0.5 rounded text-xs text-slate-800 font-mono">pystac_client</code>), R (<code class="bg-slate-100 px-1 py-0.5 rounded text-xs text-slate-800 font-mono">rstac</code>) y motores QGIS / ArcGIS.
                    </p>
                </div>
                <div class="flex flex-col sm:flex-row gap-3">
                    <a href="https://ide.cit.uai.cl/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-semibold shadow transition">
                        <i data-lucide="file-json" class="w-4 h-4 mr-2"></i>
                        Ver catalog.json
                    </a>
                    <a href="/descargas" class="inline-flex items-center justify-center px-4 py-2.5 rounded-xl border border-slate-300 hover:bg-slate-100 text-slate-700 text-xs font-semibold transition">
                        <i data-lucide="download" class="w-4 h-4 mr-2"></i>
                        Descargas Directas
                    </a>
                </div>
            </div>
        </header>

        <!-- STAC Collections Grid -->
        <section class="mb-10">
            <div class="flex items-center justify-between mb-4 border-b border-slate-200 pb-2">
                <h2 class="text-lg font-bold text-slate-900 flex items-center">
                    <i data-lucide="layers" class="w-5 h-5 mr-2 text-uai-gold"></i>
                    Colecciones STAC Publicadas
                </h2>
                <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">{num_endpoints} Endpoints JSON</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
{all_cards_str}
            </div>
        </section>

        <!-- Code Snippets Section -->
        <section class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm mb-12">
            <h2 class="text-lg font-bold text-slate-900 mb-2 flex items-center">
                <i data-lucide="code-2" class="w-5 h-5 mr-2 text-uai-navy"></i>
                Consumo Programático del Catálogo STAC
            </h2>
            <p class="text-xs sm:text-sm text-slate-600 mb-6 leading-relaxed">
                Ejemplos directos para consultar, listar e interactuar con el catálogo STAC desde entornos de ciencia de datos:
            </p>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Python Client Snippet -->
                <div class="bg-slate-900 rounded-xl p-5 text-slate-100 font-mono text-xs overflow-x-auto shadow-inner">
                    <div class="flex items-center justify-between text-slate-400 mb-3 pb-2 border-b border-slate-800">
                        <span class="font-bold text-slate-200 flex items-center">
                            <i data-lucide="terminal" class="w-3.5 h-3.5 mr-1.5 text-uai-gold"></i>
                            Python (pystac-client)
                        </span>
                        <span class="text-[11px]">pip install pystac-client</span>
                    </div>
                    <pre class="leading-relaxed"><code><span class="text-amber-400">import</span> pystac_client

<span class="text-slate-500"># 1. Conectar al catlogo STAC 1.0.0 de la IDE CIT</span>
catalog = pystac_client.Client.open(
    <span class="text-emerald-400">"https://ide.cit.uai.cl/stac/catalog.json"</span>
)

<span class="text-slate-500"># 2. Listar colecciones disponibles</span>
<span class="text-cyan-400">print</span>(<span class="text-emerald-400">f"Catlogo: {{catalog.title}}"</span>)
<span class="text-amber-400">for</span> col <span class="text-amber-400">in</span> catalog.get_collections():
    <span class="text-cyan-400">print</span>(<span class="text-emerald-400">f"  [{{col.id}}] {{col.title}}"</span>)</code></pre>
                </div>

                <!-- R Client Snippet -->
                <div class="bg-slate-900 rounded-xl p-5 text-slate-100 font-mono text-xs overflow-x-auto shadow-inner">
                    <div class="flex items-center justify-between text-slate-400 mb-3 pb-2 border-b border-slate-800">
                        <span class="font-bold text-slate-200 flex items-center">
                            <i data-lucide="terminal" class="w-3.5 h-3.5 mr-1.5 text-uai-gold"></i>
                            R (rstac)
                        </span>
                        <span class="text-[11px]">install.packages("rstac")</span>
                    </div>
                    <pre class="leading-relaxed"><code><span class="text-amber-400">library</span>(rstac)

<span class="text-slate-500"># 1. Inicializar conexin STAC</span>
s &lt;- stac(<span class="text-emerald-400">"https://ide.cit.uai.cl/stac/catalog.json"</span>)

<span class="text-slate-500"># 2. Extraer colecciones geoespaciales</span>
cols &lt;- s |&gt; collections() |&gt; get_request()

<span class="text-cyan-400">print</span>(cols)</code></pre>
                </div>
            </div>
        </section>
    </main>

    {footer_html}

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.lucide) lucide.createIcons();
        }});
    </script>
</body>
</html>
"""
    stac_html_path = STAC_DIR / "index.html"
    with open(stac_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [+] STAC HTML generado exitosamente en: {stac_html_path}")

    if DIST_DIR.exists():
        dist_stac_html = DIST_DIR / "stac" / "index.html"
        dist_stac_html.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(stac_html_path, dist_stac_html)

def generar_conectores_qgis():
    print("[*] Generando Conectores de Capa QGIS (.qlr)...")
    
    # Limpieza de conectores obsoletos 2024 (MBHT 2024 se lanza oficialmente en noviembre)
    obsolete_qlr = [
        QGIS_DIR / "CIT_MBHT_2024_VectorTiles.qlr",
        DIST_DIR / "download" / "qgis" / "CIT_MBHT_2024_VectorTiles.qlr"
    ]
    for obs in obsolete_qlr:
        if obs.exists():
            try:
                obs.unlink()
                print(f"  [-] Eliminado conector no autorizado: {obs.name}")
            except Exception:
                pass

    # 1. Conector MBHT 2017 Vector Tiles (Línea Base Oficial Vigente)
    qlr_mvt_2017 = """<!DOCTYPE qgis-layer-definition>
<qlr>
  <maplayers>
    <maplayer autoRefreshTime="0" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08" refreshOnNotifyEnabled="0" type="vector-tile" styleCategories="AllStyleCategories">
      <id>CIT_MBHT_2017_MVT</id>
      <datasource>type=xyz&amp;url=https://ide.cit.uai.cl/tiles/kpi_mud_2017/%7Bz%7D/%7Bx%7D/%7By%7D.pbf&amp;zmax=16&amp;zmin=0</datasource>
      <keywordList>
        <value>CIT-UAI</value>
        <value>MBHT</value>
        <value>Bienestar Humano Territorial</value>
        <value>Censo 2017</value>
      </keywordList>
      <layername>CIT - Matriz de Bienestar Humano Territorial (MBHT 2017)</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <wkt>PROJCRS["WGS 84 / Pseudo-Mercator",BASEGEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]],CONVERSION["Popular Visualisation Pseudo-Mercator",METHOD["Popular Visualisation Pseudo Mercator",ID["EPSG",1024]],PARAMETER["Latitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8801]],PARAMETER["Longitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8802]],PARAMETER["False easting",0,LENGTHUNIT["metre",1],ID["EPSG",8806]],PARAMETER["False northing",0,LENGTHUNIT["metre",1],ID["EPSG",8807]],ID["EPSG",3857]]</wkt>
          <proj4>+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs</proj4>
          <srsid>3857</srsid>
          <srid>3857</srid>
          <authid>EPSG:3857</authid>
          <description>WGS 84 / Pseudo-Mercator</description>
          <projectionacronym>merc</projectionacronym>
          <ellipsoidacronym>EPSG:7030</ellipsoidacronym>
          <geographicflag>false</geographicflag>
        </spatialrefsys>
      </srs>
    </maplayer>
  </maplayers>
</qlr>
"""
    with open(QGIS_DIR / "CIT_MBHT_2017_Nacional.qlr", "w", encoding="utf-8") as f:
        f.write(qlr_mvt_2017)

    # 2. Conector WMS IDE CIT
    qlr_wms = """<!DOCTYPE qgis-layer-definition>
<qlr>
  <maplayers>
    <maplayer autoRefreshTime="0" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08" refreshOnNotifyEnabled="0" type="raster" styleCategories="AllStyleCategories">
      <id>CIT_WMS_IDE</id>
      <datasource>contextualWMSLegend=0&amp;crs=EPSG:4326&amp;dpiMode=7&amp;featureCount=10&amp;format=image/png&amp;layers=ide_cit_mbht&amp;styles=&amp;url=https://ide.cit.uai.cl/wms</datasource>
      <keywordList>
        <value>CIT-UAI</value>
        <value>WMS</value>
        <value>OGC</value>
      </keywordList>
      <layername>CIT - Servicio WMS Oficial (IDE CIT)</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <wkt>GEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]]</wkt>
          <proj4>+proj=longlat +datum=WGS84 +no_defs</proj4>
          <srsid>3452</srsid>
          <srid>4326</srid>
          <authid>EPSG:4326</authid>
          <description>WGS 84</description>
          <projectionacronym>longlat</projectionacronym>
          <ellipsoidacronym>EPSG:7030</ellipsoidacronym>
          <geographicflag>true</geographicflag>
        </spatialrefsys>
      </srs>
    </maplayer>
  </maplayers>
</qlr>
"""
    with open(QGIS_DIR / "CIT_Servicios_WMS.qlr", "w", encoding="utf-8") as f:
        f.write(qlr_wms)
        
    # 3. Estilo QGIS (.qml) para visualización inmediata en municipios
    qml_content = """<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0" styleCategories="AllStyleCategories">
  <renderer-v2 attr="MUD_S" type="graduatedSymbol">
    <ranges>
      <range render="true" symbol="0" lower="0.00" upper="0.28" label="Muy Bajo [0.00 - 0.28]"/>
      <range render="true" symbol="1" lower="0.28" upper="0.41" label="Bajo [0.28 - 0.41]"/>
      <range render="true" symbol="2" lower="0.41" upper="0.52" label="Medio Bajo [0.41 - 0.52]"/>
      <range render="true" symbol="3" lower="0.52" upper="0.62" label="Medio Alto [0.52 - 0.62]"/>
      <range render="true" symbol="4" lower="0.62" upper="0.74" label="Alto [0.62 - 0.74]"/>
      <range render="true" symbol="5" lower="0.74" upper="1.00" label="Muy Alto [0.74 - 1.00]"/>
    </ranges>
    <symbols>
      <symbol name="0" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="215,48,39,255"/><Option name="outline_color" type="QString" value="180,30,20,255"/></Option></layer></symbol>
      <symbol name="1" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="252,141,89,255"/><Option name="outline_color" type="QString" value="200,100,50,255"/></Option></layer></symbol>
      <symbol name="2" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="254,224,139,255"/><Option name="outline_color" type="QString" value="210,180,80,255"/></Option></layer></symbol>
      <symbol name="3" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="217,239,139,255"/><Option name="outline_color" type="QString" value="170,190,80,255"/></Option></layer></symbol>
      <symbol name="4" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="145,207,96,255"/><Option name="outline_color" type="QString" value="100,160,50,255"/></Option></layer></symbol>
      <symbol name="5" type="fill"><layer pass="0" class="SimpleFill"><Option type="Map"><Option name="color" type="QString" value="26,152,80,255"/><Option name="outline_color" type="QString" value="15,100,50,255"/></Option></layer></symbol>
    </symbols>
  </renderer-v2>
</qgis>"""
    with open(QGIS_DIR / "CIT_MBHT_Simbologia_Jenks.qml", "w", encoding="utf-8") as f:
        f.write(qml_content)

    print("  [+] Conectores y Estilos QGIS generados en download/qgis/")

def generar_clean_url_dirs():
    print("[*] Creando estructura de Clean URLs (/inicio, /descargas, /guia-tecnica, /red-ides)...")
    
    routes = [
        ("inicio", "index.html"),
        ("descargas", "descargas-2017.html"),
        ("guia-tecnica", "guia-tecnica.html"),
        ("red-ides", "red-ides.html"),
        ("ficha-mbht-2017", "ficha-mbht-2017.html"),
        ("stac", "stac/index.html")
    ]
    
    for folder_name, src_file in routes:
        target_dir = BASE_DIR / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        src_path = BASE_DIR / src_file
        target_path = target_dir / "index.html"
        if src_path.exists() and src_path.resolve() != target_path.resolve():
            shutil.copy2(src_path, target_path)
            print(f"  [+] Creado {folder_name}/index.html desde {src_file}")
            
        # dist directory copy
        if DIST_DIR.exists():
            dist_target_dir = DIST_DIR / folder_name
            dist_target_dir.mkdir(parents=True, exist_ok=True)
            dist_target_path = dist_target_dir / "index.html"
            if src_path.exists() and src_path.resolve() != dist_target_path.resolve():
                shutil.copy2(src_path, dist_target_path)
            if src_path.exists():
                shutil.copy2(src_path, DIST_DIR / src_file)
                
    if DIST_DIR.exists():
        (DIST_DIR / "download").mkdir(parents=True, exist_ok=True)
        py_verifier = BASE_DIR / "download" / "reproducir_verificacion_r15.py"
        if py_verifier.exists():
            shutil.copy2(py_verifier, DIST_DIR / "download" / "reproducir_verificacion_r15.py")
        sec_txt = BASE_DIR / "security.txt"
        if sec_txt.exists():
            shutil.copy2(sec_txt, DIST_DIR / "security.txt")
        (DIST_DIR / ".well-known").mkdir(parents=True, exist_ok=True)
        wk_sec = BASE_DIR / ".well-known" / "security.txt"
        if wk_sec.exists():
            shutil.copy2(wk_sec, DIST_DIR / ".well-known" / "security.txt")

def main():
    ensure_dirs()
    generar_stac()
    generar_stac_html()
    generar_conectores_qgis()
    generar_clean_url_dirs()
    print("\n[OK] Todos los recursos generados exitosamente.")

if __name__ == "__main__":
    main()
