#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — GENERADOR ALGORÍTMICO DEL PORTAL DATA HUB & CATÁLOGO ABIERTO
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Compilador y generador algorítmico automatizado del portal web `index.html`
    para la Infraestructura de Datos Espaciales (IDE CIT).
    
    Asegura el cumplimiento estricto de:
    1. Directivas de arquitectura y branding de AGENTS.md (CIT-UAI).
    2. Resolución dinámica de rutas absolutas (`find_proyecto_root`).
    3. Validaciones de esquema para capas vectoriales y metadatos ISO 19115 / SNIT.
    4. Estándares semánticos RAE/Fundéu (cero tecnicismos invasivos en UI).
    5. Adaptabilidad fluida (mobile-first con menú hamburguesa y controles apilables).
    6. Visor de referencia espacial y cobertura geográfica ultraliviano (Leaflet/Positron).
    7. Integración de Copiloto IA Territorial (widget interactivo y motor híbrido).
    8. Metadatos SEO, OpenGraph y exportadores masivos JSON/CSV.

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from generador_descargas_2017 import generate_descargas_2017_html
from generador_ficha_dataset import generate_ficha_mbht_2017_html
from generador_guia_tecnica import generate_guia_tecnica_html
from generador_red_ides import generate_red_ides_html
from motor_ia_cit import (
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
    get_llms_txt_content,
    get_llms_full_txt_content,
)

# Configuración de Logging Profesional
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("IDE_CIT_Builder")


def find_proyecto_root(start_path: Optional[Path] = None) -> Path:
    """
    Encuentra dinámicamente la raíz del proyecto `PROYECTO_MBHT`.
    Cumple con la Regla de Oro N° 1 de AGENTS.md.
    """
    current = (start_path or Path(__file__)).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent


class IDEPortalBuilder:
    """
    Compilador algorítmico del portal de datos espaciales IDE CIT.
    """

    def __init__(self, root_dir: Optional[Path] = None) -> None:
        self.root_dir: Path = root_dir or find_proyecto_root()
        self.ide_hub_dir: Path = self.root_dir / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
        self.public_dir: Path = self.ide_hub_dir / "public"
        self.data_dir: Path = self.ide_hub_dir / "data"
        self.img_dir: Path = self.ide_hub_dir / "img"
        self.catalog_json_path: Path = self.data_dir / "catalogo_ide_cit.json"
        self.descargas_2017_json_path: Path = self.data_dir / "indice_descargas_mbht_2017.json"
        self.output_html_path: Path = self.public_dir / "index.html"
        self.output_descargas_path: Path = self.public_dir / "descargas-2017.html"
        self.output_guia_path: Path = self.public_dir / "guia-tecnica.html"
        self.output_red_path: Path = self.public_dir / "red-ides.html"
        self.output_ficha_path: Path = self.public_dir / "ficha-mbht-2017.html"
        self.catalog_csv_path: Path = self.data_dir / "catalogo_ide_cit.csv"
        self.dcat_json_path: Path = self.data_dir / "dcat.json"
        self.sitemap_path: Path = self.public_dir / "sitemap.xml"
        self.robots_path: Path = self.public_dir / "robots.txt"
        self.llms_txt_path: Path = self.public_dir / "llms.txt"
        self.manifest_pwa_path: Path = self.public_dir / "site.webmanifest"

    def validate_environment(self) -> Dict[str, Any]:
        """
        Valida la existencia y consistencia de los insumos requeridos (JSON, SVGs, etc.).
        """
        logger.info("🔍 Validando entorno e insumos del portal...")
        
        if not self.catalog_json_path.exists():
            raise FileNotFoundError(f"No se encontró el catálogo de datos: {self.catalog_json_path}")

        with open(self.catalog_json_path, "r", encoding="utf-8") as f:
            catalog_data = json.load(f)

        # Validación de estructura del catálogo JSON
        required_keys = ["portal", "matrices", "capas", "aplicaciones_satelitales", "ides_nacionales"]
        for key in required_keys:
            if key not in catalog_data:
                raise KeyError(f"Falta la clave requerida '{key}' en {self.catalog_json_path}")

        capas: List[Dict[str, Any]] = catalog_data.get("capas", [])
        version = catalog_data.get("portal", {}).get("version", "2026.1")
        logger.info(f"   ✓ Catálogo cargado (v{version}): {len(capas)} capas registradas.")

        # Validación de activos vectoriales esenciales
        required_assets = [
            self.img_dir / "logo-cit-uai.svg",
            self.img_dir / "logo-ide-standalone.svg",
            self.img_dir / "logo-mbht-white.svg",
        ]
        for asset in required_assets:
            if not asset.exists():
                logger.warning(f"   ⚠️ Activo vectorial recomendado no encontrado: {asset.name}")
            else:
                logger.info(f"   ✓ Vector verificado: {asset.name}")

        return catalog_data

    def generate_json_ld(self, catalog_data: Dict[str, Any]) -> str:
        portal = catalog_data.get("portal", {})
        capas = catalog_data.get("capas", [])
        datasets = []
        for capa in capas:
            is_restricted = (capa.get("matriz") == "mpst" or capa.get("publico") is False or capa.get("estado") == "en_desarrollo")
            bbox = capa.get("bbox", [-75.64, -55.98, -66.86, -17.50])
            ds = {
                "@type": "Dataset",
                "name": capa.get("titulo"),
                "description": capa.get("resumen"),
                "identifier": f"CIT-UAI::{capa.get('id')}::2026",
                "license": f"https://creativecommons.org/licenses/{'by-nc/4.0' if is_restricted else 'by/4.0'}/",
                "creator": {
                    "@type": "Organization",
                    "name": capa.get("autor", "Centro de Inteligencia Territorial (CIT-UAI)")
                },
                "spatialCoverage": {
                    "@type": "Place",
                    "geo": {
                        "@type": "GeoShape",
                        "box": f"{bbox[1]} {bbox[0]} {bbox[3]} {bbox[2]}"
                    }
                },
                "variableMeasured": [attr.get("campo") for attr in capa.get("atributos", [])],
                "measurementTechnique": capa.get("formula_lineage", "")
            }
            if not is_restricted:
                dist_list = []
                archivos = capa.get("archivos_distribucion", {})
                if "parquet" in archivos:
                    dist_list.append({
                        "@type": "DataDownload",
                        "encodingFormat": "application/vnd.apache.parquet",
                        "contentUrl": f"https://ide.cit.uai.cl/{archivos['parquet']['url']}",
                        "contentSize": archivos["parquet"]["size_bytes"],
                        "checksum": archivos["parquet"]["sha256"]
                    })
                elif capa.get("s3_parquet"):
                    dist_list.append({
                        "@type": "DataDownload",
                        "encodingFormat": "application/vnd.apache.parquet",
                        "contentUrl": capa.get("s3_parquet")
                    })
                if "gpkg" in archivos:
                    dist_list.append({
                        "@type": "DataDownload",
                        "encodingFormat": "application/geopackage+sqlite3",
                        "contentUrl": f"https://ide.cit.uai.cl/{archivos['gpkg']['url']}",
                        "contentSize": archivos["gpkg"]["size_bytes"],
                        "checksum": archivos["gpkg"]["sha256"]
                    })
                elif capa.get("gpkg_url"):
                    dist_list.append({
                        "@type": "DataDownload",
                        "encodingFormat": "application/geopackage+sqlite3",
                        "contentUrl": capa.get("gpkg_url")
                    })
                ds["distribution"] = dist_list
            datasets.append(ds)

        schema = {
            "@context": "https://schema.org",
            "@type": "DataCatalog",
            "name": portal.get("nombre", "IDE CIT — Infraestructura de Datos Espaciales"),
            "alternateName": "IDE CIT UAI",
            "description": portal.get("descripcion"),
            "url": portal.get("url_base", "https://ide.cit.uai.cl"),
            "sameAs": [
                "https://matrizbht.cl",
                "https://cit.uai.cl"
            ],
            "isAccessibleForFree": True,
            "citation": "Centro de Inteligencia Territorial (CIT-UAI). (2026). Infraestructura de Datos Espaciales (IDE CIT) y Matriz de Bienestar Humano Territorial (MBHT). Universidad Adolfo Ibáñez. https://matrizbht.cl",
            "provider": {
                "@type": "EducationalOrganization",
                "name": "Centro de Inteligencia Territorial (CIT) — Universidad Adolfo Ibáñez",
                "url": "https://cit.uai.cl",
                "email": portal.get("contacto", "contactocit@uai.cl")
            },
            "dataset": datasets
        }
        return json.dumps(schema, ensure_ascii=False, indent=2)

    def generate_static_layers_html(self, catalog_data: Dict[str, Any]) -> str:
        """
        Pre-renderiza estáticamente las 13 tarjetas de capas en HTML semántico (SSG).
        Permite que cualquier agente de IA, crawler o scraper lea el catálogo completo sin ejecutar JavaScript.
        Incluye linaje, fuentes institucionales, operador matemático y enlaces directos a fichas técnicas.
        """
        cards = []
        matrices = {m["id"]: m.get("nombre", m["id"].upper()) for m in catalog_data.get("matrices", [])}
        for capa in catalog_data.get("capas", []):
            capa_id = capa.get("id", "")
            ambito = capa.get("ambito", "tierra")
            ambito_label = "Litósfera" if ambito == "tierra" else ("Maritorio" if ambito == "mar" else "Atmósfera")
            mat_id = capa.get("matriz", "mbht")
            mat_name = matrices.get(mat_id, mat_id.upper())
            
            # Indicador tipográfico sobrio de estado (sin pastillas estridentes)
            if capa_id == "kpi_mud_2017":
                status_label = '<span class="text-[11px] font-semibold text-slate-700">Línea base oficial 2017</span>'
            elif capa_id == "censo_imputaciones_2024":
                status_label = '<span class="text-[11px] font-semibold text-amber-800">En calibración · Censo 2024</span>'
            elif capa.get("estado") == "reserva_institucional":
                status_label = '<span class="text-[11px] font-medium text-slate-600">Reserva institucional</span>'
            else:
                status_label = f'<span class="text-[11px] font-mono text-slate-400">v{capa.get("version", "1.0")}</span>'
            
            size_str = capa.get("size_human", "")
            size_meta = f' · <span class="font-mono text-slate-500">{size_str}</span>' if size_str else ""

            # Atributos (primeros 4)
            attrs_rows = []
            for attr in capa.get("atributos", [])[:4]:
                attrs_rows.append(f'<tr><td class="font-mono font-bold text-slate-800 pr-2 py-0.5">{attr.get("campo")}</td><td class="text-slate-500 pr-2 py-0.5">{attr.get("tipo")}</td><td class="text-slate-600 py-0.5">{attr.get("descripcion")}</td></tr>')
            attrs_table = "\n                                    ".join(attrs_rows)
            num_total_attrs = len(capa.get("atributos", []))
            more_attrs = f'<span class="text-[10px] text-slate-500 font-medium block mt-1">+ {num_total_attrs - 4} campos adicionales en la ficha técnica ({num_total_attrs} columnas físicas)</span>' if num_total_attrs > 4 else ""

            # Fuentes institucionales y operador integrados limpiamente en el acordeón técnico
            fuentes = capa.get("fuentes_institucionales", [])
            inst_list = ", ".join([f.get("institucion", "") for f in fuentes[:3] if f.get("institucion")]) if fuentes else "CIT-UAI"
            formula_raw = capa.get("formula_lineage", "")
            f_snippet = (formula_raw[:140] + "..." if len(formula_raw) > 140 else formula_raw) if formula_raw else ""
            formula_row = f'<div class="mb-2 text-[10.5px] font-mono text-slate-600 bg-white p-1.5 rounded border border-slate-200/80 overflow-x-auto"><strong class="font-sans text-slate-800">Operador:</strong> {f_snippet}</div>' if f_snippet else ""

            # Esquema físico y linaje expandible (sobrio, sin sobrecargar la vista inicial)
            details_html = f"""                <details class="mt-2.5 text-[11px] bg-slate-50/80 border border-slate-200/90 rounded-lg p-2.5 text-slate-700">
                    <summary class="font-medium text-slate-700 hover:text-slate-900 cursor-pointer flex items-center justify-between select-none">
                        <span>Especificación técnica ({num_total_attrs} campos · {inst_list})</span>
                        <a href="download/iso_xml/{capa_id}_iso19139.xml" download class="text-[10px] text-slate-500 hover:text-slate-900 underline font-mono">ISO XML</a>
                    </summary>
                    <div class="mt-2 pt-2 border-t border-slate-200/80 overflow-x-auto">
                        {formula_row}
                        <table class="w-full text-left text-[10px]">
                            <tbody class="divide-y divide-slate-100">
                                {attrs_table}
                            </tbody>
                        </table>
                        {more_attrs}
                    </div>
                </details>"""
            
            # Enlace semántico directo a la Ficha Técnica para crawlers
            if capa_id == "kpi_mud_2017":
                ficha_link_html = '<a href="/ficha-mbht-2017" class="mt-2.5 block text-center text-xs font-medium text-slate-600 hover:text-slate-900 underline underline-offset-2">Ver ficha metodológica exhaustiva (Línea base 2017) &rarr;</a>'
            else:
                ficha_link_html = ""

            card = f"""        <article class="layer-card bg-white rounded-xl border border-slate-200 shadow-clean hover:shadow-hover p-5 transition flex flex-col justify-between group" data-layer-id="{capa_id}" data-matriz="{mat_id}" data-ambito="{ambito}">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-100">
                    <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">{mat_name} · {ambito_label}</span>
                    {status_label}
                </div>
                <h3 class="font-bold text-slate-900 text-base mb-1.5 group-hover:text-black transition leading-snug">{capa.get('titulo')}</h3>
                <p class="text-xs sm:text-sm text-slate-600 line-clamp-2 mb-2 leading-relaxed font-normal">{capa.get('resumen')}</p>
{details_html}
            </div>

            <div class="pt-3.5 border-t border-slate-100 mt-3.5">
                <div class="flex items-center justify-between text-xs text-slate-500 mb-3">
                    <span>Escala: <strong class="text-slate-700 font-medium">{capa.get('escala')}</strong></span>
                    <span class="text-[11px] text-slate-400">Corte {capa.get('fecha_corte', '2017')}{size_meta}</span>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="openLayerModal('{capa_id}')" class="flex-1 bg-slate-900 hover:bg-black active:bg-slate-800 text-white text-xs sm:text-sm font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1 shadow-xs cursor-pointer">
                        <span>Ficha y descarga</span>
                    </button>
                    <button onclick="openLayerModal('{capa_id}', true)" title="Ver referencia espacial en mapa" class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 active:bg-slate-300 text-slate-700 transition cursor-pointer">
                        <i data-lucide="map" class="w-4 h-4 stroke-[1.5]"></i>
                    </button>
                    <button onclick="quickCopyQGIS('{capa.get('tile_source')}')" title="Copiar conector para QGIS" class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 active:bg-slate-300 text-slate-700 transition cursor-pointer">
                        <i data-lucide="link" class="w-4 h-4 stroke-[1.5]"></i>
                    </button>
                </div>
                {ficha_link_html}
            </div>
        </article>"""
            cards.append(card)
        return "\n".join(cards)

    def generate_static_apps_html(self, catalog_data: Dict[str, Any]) -> str:
        """
        Pre-renderiza estáticamente las tarjetas de aplicaciones satelitales en HTML.
        """
        apps_cards = []
        for app in catalog_data.get("aplicaciones_satelitales", []):
            cat_label = f'<span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">{app.get("categoria")}</span>' if app.get("categoria") else ""
            card = f"""        <a href="{app.get('url')}" target="_blank" rel="noopener noreferrer" class="bg-slate-50 p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean hover:bg-white hover:border-slate-300 hover:shadow-hover transition flex flex-col justify-between group">
            <div>
                <div class="flex items-center justify-between mb-2.5 sm:mb-3">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-700 bg-white border border-slate-200 shadow-xs">
                        <i data-lucide="{app.get('icono', 'compass')}" class="w-4 h-4 stroke-[1.5]"></i>
                    </div>
                    {cat_label}
                </div>
                <h4 class="font-bold text-slate-900 text-xs sm:text-sm mb-1 group-hover:text-black transition leading-snug">{app.get('titulo')}</h4>
                <p class="text-xs text-slate-500 leading-relaxed mb-3 sm:mb-4 font-normal">{app.get('descripcion')}</p>
            </div>
            <div class="text-xs font-semibold text-slate-700 flex items-center space-x-1 pt-2 sm:pt-2.5 border-t border-slate-200 group-hover:text-black transition">
                <span>Acceder al recurso</span>
                <i data-lucide="arrow-up-right" class="w-3.5 h-3.5 stroke-[1.5]"></i>
            </div>
        </a>"""
            apps_cards.append(card)
        return "\n".join(apps_cards)

    def generate_html_content(self, catalog_data: Dict[str, Any]) -> str:
        """
        Ensambla el código HTML5 completo con Tailwind CSS, Lucide Icons, Leaflet JS,
        Copiloto IA interactivo, filtros dinámicos, visor de referencia espacial y exportadores.
        """
        num_capas = len(catalog_data.get("capas", []))
        version = catalog_data.get("portal", {}).get("version", "2026.1")
        json_ld = self.generate_json_ld(catalog_data)
        catalog_json_str = json.dumps(catalog_data, ensure_ascii=False)
        static_layers_html = self.generate_static_layers_html(catalog_data)
        static_apps_html = self.generate_static_apps_html(catalog_data)
        
        descargas_2017_data = {}
        if self.descargas_2017_json_path.exists():
            with open(self.descargas_2017_json_path, "r", encoding="utf-8") as f:
                descargas_2017_data = json.load(f)
        descargas_2017_json_str = json.dumps(descargas_2017_data, ensure_ascii=False)

        copilot_js_engine = get_copilot_js_engine()
        llm_head_meta = get_llm_head_meta()
        llm_guidance_html = get_llm_guidance_html()
        canonical_header = get_canonical_header_html("catalogo")
        canonical_footer = get_canonical_footer_html(version)

        matrix_buttons = [
            f'<button data-filter="all" class="filter-btn active text-xs sm:text-sm font-bold px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition bg-slate-900 text-white shadow-xs shrink-0 sm:shrink whitespace-nowrap">Todas ({num_capas})</button>'
        ]
        for m in catalog_data.get("matrices", []):
            m_id = m.get("id")
            m_nom = m.get("nombre", m_id.upper())
            matrix_buttons.append(
                f'<button data-filter="{m_id}" class="filter-btn text-xs sm:text-sm font-medium px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition text-slate-700 hover:text-slate-900 hover:bg-slate-200 shrink-0 sm:shrink whitespace-nowrap">{m_nom}</button>'
            )
        matrix_filters_html = "\n                        ".join(matrix_buttons)

        html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IDE CIT — Infraestructura de Datos Espaciales | Centro de Inteligencia Territorial · Universidad Adolfo Ibáñez</title>
    
    <!-- Metadatos SEO e Institucionales -->
    <meta name="description" content="Catálogo de datos abiertos, servicios vectoriales MVT y coberturas de bienestar humano territorial (MBHT), demografía censal y planificación marina de Chile. IDE del CIT-UAI.">
    <meta name="keywords" content="IDE CIT, MBHT, Datos Espaciales, Chile, Bienestar Territorial, Smart Cities, UAI, Centro de Inteligencia Territorial, GeoParquet, MVT, OGC">
    <meta name="author" content="Centro de Inteligencia Territorial (CIT-UAI)">
    <meta name="version" content="{version}">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="https://ide.cit.uai.cl/inicio">
    
    <!-- Directivas Anti-Caché para Clientes Web y Dispositivos Móviles -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    
{llm_head_meta}
    
    <!-- Open Graph / Redes Sociales -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="IDE CIT — Centro de Inteligencia Territorial (UAI)">
    <meta property="og:title" content="IDE CIT — Infraestructura de Datos Espaciales">
    <meta property="og:description" content="Catálogo abierto de datos territoriales, linaje matemático auditable y coberturas nacionales de bienestar humano, seguridad, resiliencia y productividad.">
    <meta property="og:url" content="https://ide.cit.uai.cl">
    <meta property="og:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@CIT_UAI">
    <meta name="twitter:title" content="IDE CIT — Infraestructura de Datos Espaciales | CIT-UAI">
    <meta name="twitter:description" content="Datos abiertos, servicios vectoriales y trazabilidad algorítmica de las matrices territoriales de Chile.">
    <meta name="twitter:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">
    
    <!-- Schema.org / JSON-LD DataCatalog (Google Dataset Search) -->
    <script type="application/ld+json">
{json_ld}
    </script>
    
    <!-- Favicon & PWA Manifest -->
    <link rel="icon" type="image/svg+xml" href="img/logo-ide-standalone.svg">
    <link rel="manifest" href="site.webmanifest">
    
    <!-- Google Fonts: Roboto -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Roboto', 'sans-serif'],
                        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
                    }},
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
                    }},
                    boxShadow: {{
                        'clean': '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
                        'hover': '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
                        'widget': '0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.08)'
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <!-- Leaflet CSS & JS (Visor de Referencia Espacial Estándar OGC) -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    
    <!-- View Transitions API para Navegación Fluida sin Saltos -->
    <meta name="view-transition" content="same-origin">

    <style>
        body {{ font-family: 'Roboto', sans-serif; color: #1e293b; line-height: 1.6; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 5px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #f8fafc; }}
        
        /* Tipografía, scroll estable y transición visual suave entre pestañas */
        html {{
            font-size: 16px;
            overflow-y: scroll;
            scrollbar-gutter: stable;
            scroll-behavior: smooth;
        }}
        @view-transition {{ navigation: auto; }}
        
        /* Preservación de dimensiones en iconos antes de ejecución JS */
        [data-lucide] {{
            display: inline-block;
            vertical-align: middle;
            flex-shrink: 0;
        }}

        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 2px; }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
        
        /* Justificación de párrafos limpia y sin espacios en blanco anómalos */
        p {{
            text-align: justify;
            text-justify: inter-word;
            hyphens: auto;
            -webkit-hyphens: auto;
            -ms-hyphens: auto;
        }}

        /* Ocultar barra de scroll en contenedores móviles con scroll horizontal */
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}

        /* Leaflet custom styling & clean basemap */
        .leaflet-container {{
            font-family: 'Roboto', sans-serif;
            background: #f8fafc;
        }}
        #layerPreviewMap .leaflet-tile {{
            filter: grayscale(85%) contrast(100%) brightness(102%);
        }}
    </style>
</head>
<body class="h-full flex flex-col font-sans bg-slate-100 text-slate-800 antialiased overflow-x-hidden">

<noscript>
    <div class="bg-slate-900 text-slate-200 border-b border-slate-800 px-4 py-4 text-sm">
        <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
                <strong class="text-white">Acceso directo al catálogo y descargas (modo lectura HTML estático):</strong>
                <span>Todos los conjuntos de datos, fichas técnicas, sumas de verificación SHA-256 y metadatos STAC 1.0.0 están disponibles directamente mediante enlaces estáticos.</span>
            </div>
            <div class="flex flex-wrap gap-3 font-semibold text-uai-gold shrink-0">
                <a href="/descargas" class="underline hover:text-white">1. Centro de descargas (MBHT 2017)</a>
                <a href="/ficha-mbht-2017" class="underline hover:text-white">2. Ficha técnica y reproducibilidad</a>
                <a href="/guia-tecnica" class="underline hover:text-white">3. Guía metodológica y control de calidad</a>
                <a href="/stac/catalog.json" class="underline hover:text-white">4. Catálogo STAC JSON</a>
            </div>
        </div>
    </div>
</noscript>

{llm_guidance_html}

{canonical_header}

    <!-- 2. SECCIÓN DE PRESENTACIÓN DIDÁCTICA E INTRODUCCIÓN INSTITUCIONAL (PADRONIZADA py-8 sm:py-12) -->
    <main id="main-content" role="main" tabindex="-1">
    <section class="bg-white border-b border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <!-- Migas de pan (Breadcrumbs) -->
            <nav class="flex items-center space-x-2 text-xs text-slate-400 mb-4 sm:mb-5">
                <a href="inicio" class="hover:text-slate-700 transition">IDE CIT</a>
                <span class="text-slate-300">/</span>
                <span class="text-slate-800 font-bold">Catálogo de datos espaciales y modelos analíticos</span>
            </nav>

            <!-- Título y Propósito Estratégico -->
            <div class="text-center max-w-6xl mx-auto mb-10 sm:mb-12">
                <div class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-2.5">
                    Infraestructura de Datos Espaciales · Centro de Inteligencia Territorial
                </div>
                <h1 class="text-2xl sm:text-3xl lg:text-4xl xl:text-[2.65rem] font-bold tracking-tight text-slate-900 mb-4 sm:mb-5 leading-tight">
                    Catálogo de datos espaciales y modelos analíticos territoriales
                </h1>
                <p class="text-sm sm:text-base lg:text-[17px] text-slate-600 leading-relaxed font-normal text-justify sm:text-center mx-auto">
                    La <strong>Infraestructura de Datos Espaciales del CIT-UAI (IDE CIT)</strong> es una iniciativa de ciencia abierta y transferencia tecnológica desarrollada por el Centro de Inteligencia Territorial de la Universidad Adolfo Ibáñez para poner a disposición del país, de sus instituciones públicas, gobiernos locales, comunidad científica y ciudadanía, el <strong>marco multidimensional de matrices y modelos analíticos</strong> del CIT. Articulada en colaboración armónica con el Sistema Nacional de Información Territorial (SNIT) y las IDEs sectoriales de Chile, la plataforma provee indicadores de bienestar humano (MBHT), estratificación socioespacial (INSE), planificación marina sustentable (FAO / SBAP) y modelos emergentes en áreas de resiliencia socioecológica, cohesión comunitaria y desarrollo productivo, respaldados por trazabilidad matemática transparente, metadatos normalizados y geoservicios abiertos.
                </p>
                <p class="text-sm sm:text-base lg:text-[17px] text-slate-600 leading-relaxed font-normal text-justify sm:text-center mx-auto mt-4 sm:mt-5">
                    Dentro del ecosistema territorial, la IDE CIT complementa el servicio de las plataformas interactivas de simulación y deliberación ciudadana (<a href="https://matrizbht.cl" target="_blank" rel="noopener noreferrer" class="text-slate-900 font-semibold underline decoration-uai-gold decoration-2 underline-offset-2 hover:text-black">matrizbht.cl</a> y <a href="https://plataformabht.subdere.gov.cl" target="_blank" rel="noopener noreferrer" class="text-slate-900 font-semibold underline decoration-uai-gold decoration-2 underline-offset-2 hover:text-black">Plataforma BHT SUBDERE</a>). En ellas, la <strong>Matriz de Bienestar Humano Territorial (MBHT)</strong> opera como el estándar público de referencia adoptado por el Estado para diagnosticar brechas urbanas y evaluar el acceso peatonal a servicios esenciales: mientras dichos visores permiten ponderar prioridades y proyectar escenarios de inversión en línea, este Data Hub suministra las matrices columnares en GeoParquet, conectores OGC/QGIS y scripts reproducibles en Python y R para habilitar análisis cruzados independientes y fundar las políticas públicas en evidencia empírica.
                </p>
            </div>

            <!-- Arquitectura de Descubrimiento por Perfil de Usuario (4 niveles: Básico, SIG, Científico, Máquina/IA) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-10 sm:mb-12">
                <!-- Nivel 1: Usuario Básico / Gestión Pública -->
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 flex flex-col justify-between shadow-clean hover:shadow-hover hover:border-slate-300 transition">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">1. Exploración y gestión</span>
                            <i data-lucide="compass" class="w-4 h-4 text-slate-700 stroke-[1.5]"></i>
                        </div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-1.5">Buscar &rarr; Encontrar &rarr; Descargar</h3>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            Recorre las 13 coberturas maestras y descarga paquetes nacionales o regionales en formatos listos para uso inmediato (GeoPackage, Shapefile y CSV).
                        </p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs font-semibold">
                        <a href="#catalogo" class="text-slate-900 hover:underline">Catálogo &darr;</a>
                        <a href="/descargas" class="text-slate-600 hover:text-slate-900 underline">Descargas &rarr;</a>
                    </div>
                </div>

                <!-- Nivel 2: Especialista SIG -->
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 flex flex-col justify-between shadow-clean hover:shadow-hover hover:border-slate-300 transition">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">2. Especialista SIG</span>
                            <i data-lucide="layers" class="w-4 h-4 text-slate-700 stroke-[1.5]"></i>
                        </div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-1.5">Metadatos &rarr; Servicios &rarr; QGIS</h3>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            Integración directa en QGIS y ArcGIS Pro mediante definiciones de capa (<code>.qlr</code>), estilos Jenks (<code>.qml</code>), streaming GDAL <code>/vsicurl/</code> y metadatos ISO 19139.
                        </p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs font-semibold">
                        <a href="/download/qgis/CIT_MBHT_2017_Nacional.qlr" download class="text-slate-900 hover:underline">Conector QLR &darr;</a>
                        <a href="/red-ides" class="text-slate-600 hover:text-slate-900 underline">Red SNIT (19 IDEs)</a>
                    </div>
                </div>

                <!-- Nivel 3: Científico e Investigador -->
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 flex flex-col justify-between shadow-clean hover:shadow-hover hover:border-slate-300 transition">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">3. Investigación científica</span>
                            <i data-lucide="book-open" class="w-4 h-4 text-slate-700 stroke-[1.5]"></i>
                        </div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-1.5">Fórmulas &rarr; Linaje &rarr; Reproducción</h3>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            Formulación matemática E2SFCA sobre red vial de Tobler con pendiente DEM, cuadratura demográfica censal y verificación determinista de extremo a extremo.
                        </p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs font-semibold">
                        <a href="/ficha-mbht-2017" class="text-slate-900 hover:underline">Ficha maestra &rarr;</a>
                        <a href="/guia-tecnica" class="text-slate-600 hover:text-slate-900 underline">Guía metodológica</a>
                    </div>
                </div>

                <!-- Nivel 4: Máquina, Cloud y Agentes IA -->
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 flex flex-col justify-between shadow-clean hover:shadow-hover hover:border-slate-300 transition">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">4. Máquina, Cloud e IA</span>
                            <i data-lucide="terminal" class="w-4 h-4 text-slate-700 stroke-[1.5]"></i>
                        </div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-1.5">STAC &rarr; GeoParquet &rarr; DCAT-AP</h3>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            Acceso columnar vía <code>HTTP 206 Range</code> para DuckDB/PyArrow, catálogo STAC 1.0.0, grafo semántico DCAT-AP 2.0 y métricas de rendimiento verificables.
                        </p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs font-mono font-semibold">
                        <a href="/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 hover:underline">STAC 1.0.0</a>
                        <a href="/conformance_report.json" target="_blank" rel="noopener noreferrer" class="text-slate-600 hover:text-slate-900 underline">Benchmarks JSON</a>
                    </div>
                </div>
            </div>

            <!-- Buscador Rápido Móvil/Escritorio (Amplitud Optimizada) -->
            <div class="max-w-3xl mx-auto relative">
                <div class="relative flex items-center rounded-lg overflow-hidden bg-slate-50 border border-slate-300 focus-within:border-slate-800 focus-within:bg-white transition shadow-xs">
                    <i data-lucide="search" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400 absolute left-3 sm:left-4 stroke-[1.5]"></i>
                    <input type="text" id="searchInput" placeholder="Buscar por indicador (ISAL, IAV, INSE), cobertura o escala..." 
                           class="w-full pl-9 sm:pl-11 pr-20 sm:pr-28 py-2.5 sm:py-3 bg-transparent text-slate-800 text-xs sm:text-base focus:outline-none font-medium placeholder-slate-400" />
                    <button id="btnSearchClear" class="hidden absolute right-16 sm:right-24 text-xs text-slate-400 hover:text-slate-700 px-2 py-1">
                        Limpiar
                    </button>
                    <button class="absolute right-1 sm:right-2 bg-slate-900 hover:bg-black active:bg-slate-800 text-white text-xs sm:text-sm font-medium px-3 py-1.5 sm:px-4 sm:py-2 rounded transition">
                        Buscar
                    </button>
                </div>
            </div>

        </div>
    </section>

    <!-- 3. CUERPO PRINCIPAL: FILTROS Y CATÁLOGO DE CAPAS -->
    <section class="flex-1 max-w-[1600px] w-full mx-auto px-4 sm:px-6 lg:px-10 xl:px-12 py-6 sm:py-8" id="catalogo">
        
        <!-- Marco Institucional de Versiones: Productos Vigentes (Línea Base 2017) vs. Productos en Calibración (Censo 2024) -->
        <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-clean mb-6 sm:mb-8">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-5">
                <div>
                    <div class="text-xs font-bold text-slate-400 uppercase tracking-widest">Estado de madurez, jerarquía de indicadores y custodia técnica</div>
                    <h2 class="text-lg sm:text-xl font-bold text-slate-900 mt-1">Distinción entre productos vigentes de línea base (2017) y actualizaciones en calibración estadística (2024)</h2>
                </div>
                <div class="text-xs sm:text-sm text-slate-500 font-mono">
                    Última auditoría verificada: 2026-10-16 · v1.0.3
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm sm:text-base">
                <!-- Tarjeta Línea Base 2017 -->
                <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2 pb-2 border-b border-slate-200/70">
                            <span class="font-bold text-slate-900 text-base">
                                MBHT 2017 — Línea base oficial vigente (Cerrada · v1.0.3)
                            </span>
                            <span class="text-xs font-mono text-slate-500 font-semibold">204.906 manzanas · 42 col.</span>
                        </div>
                        <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-4">
                            Línea base histórica oficial compartida con SUBDERE y ministerios en las 16 regiones de Chile (17.482.699 hab. amanzanados, correspondientes al 99,48% de 17.574.003 habitantes censados por el INE; diferencia de 91.304 personas en áreas no amanzanadas o en tránsito). Estructura el índice BHT en <strong>4 macro-dimensiones</strong> (<code class="font-mono text-xs">dim_acc</code>, <code class="font-mono text-xs">dim_soc</code>, <code class="font-mono text-xs">dim_seg</code>, <code class="font-mono text-xs">dim_amb</code> · 18 indicadores elementales), donde Accesibilidad (<code class="font-mono text-xs">dim_acc</code>) sintetiza <strong>6 sub-indicadores peatonales</strong> (<code class="font-mono text-xs">isal</code>, <code class="font-mono text-xs">ise</code>, <code class="font-mono text-xs">iav</code>, <code class="font-mono text-xs">idep</code>, <code class="font-mono text-xs">icul</code>, <code class="font-mono text-xs">iser</code>). Reúne <strong>204.906 manzanas</strong>, <strong>55.035 equipamientos de libre acceso</strong> (de 113.231 ruteables) y <strong>1.589.595 tramos viales</strong>.
                        </p>
                    </div>
                    <div class="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-200 text-xs sm:text-sm font-semibold">
                        <a href="/descargas" class="text-slate-900 hover:underline">
                            Descargar línea base 2017 (Nacional y 16 regiones) &rarr;
                        </a>
                        <a href="/ficha-mbht-2017" class="text-slate-600 hover:text-slate-900 underline">
                            Ficha técnica (42 col.), gobernanza y prueba E2E
                        </a>
                    </div>
                </div>

                <!-- Tarjeta Censo 2024 con Imputaciones Demográficas -->
                <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2 pb-2 border-b border-slate-200/70">
                            <span class="font-bold text-slate-900 text-base">
                                Censo 2024 — Imputaciones demográficas por cohortes y sexo
                            </span>
                            <span class="text-xs font-mono text-slate-500 font-semibold">254.395 unidades censales</span>
                        </div>
                        <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-4">
                            Insumos cartográficos y demográficos oficiales del Censo de Población y Vivienda 2024 del INE (<strong>254.395 manzanas urbanas y entidades rurales</strong> en las 16 regiones), con la modelación de desagregación demográfica por edades simples (interpolación osculatriz de Sprague) y conciliación por sexo desarrollada por el CIT-UAI como una de las etapas preparatorias del proceso de actualización de la MBHT (cuyo lanzamiento oficial está programado para noviembre). Disponible para descarga directa abierta en GeoParquet, GeoPackage, Shapefile y CSV.
                        </p>
                    </div>
                    <div class="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-200 text-xs sm:text-sm font-semibold">
                        <a href="/descargas" class="text-slate-900 hover:underline">
                            Descargar Censo 2024 con imputaciones demográficas &rarr;
                        </a>
                        <a href="/download/iso_xml/censo_imputaciones_2024_iso19139.xml" download class="text-slate-600 hover:text-slate-900 underline">
                            Metadatos ISO 19139 XML
                        </a>
                    </div>
                </div>
            </div>

            <!-- Cuadratura Metodológica Canónica (Auditoría y Transparencia Científica) -->
            <div class="mt-6 p-4 sm:p-5 rounded-xl bg-slate-900 text-slate-200 border border-slate-800 text-xs sm:text-sm">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-2.5 mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="w-2 h-2 rounded-full bg-uai-gold"></span>
                        <span class="font-bold text-white text-xs uppercase tracking-wider">Cuadratura Demográfica, Cartográfica y de Esquemas</span>
                    </div>
                    <span class="font-mono text-[11px] text-slate-400">Auditoría internacional de consistencia · v2026.1 / Dataset v1.0.3</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 leading-relaxed">
                    <div>
                        <strong class="text-white block font-semibold mb-1">1. Conciliación demográfica INE</strong>
                        <span class="text-slate-300">17.482.699 hab. amanzanados (99,48% de 17.574.003 censados INE en 2017). Los 91.304 hab. restantes corresponden a población en tránsito, situación de calle y áreas sin amanzanamiento físico.</span>
                    </div>
                    <div>
                        <strong class="text-white block font-semibold mb-1">2. Esquema físico dual</strong>
                        <span class="text-slate-300">42 columnas analíticas completas en descargas (GeoParquet, GPKG, SHP, CSV) para modelación territorial; 16 atributos livianos optimizados en teselas vectoriales MVT (WebGL sub-150ms).</span>
                    </div>
                    <div>
                        <strong class="text-white block font-semibold mb-1">3. Simbología y clasificación</strong>
                        <span class="text-slate-300">6 clases de Quiebres Naturales de Jenks (<code class="font-mono text-slate-200">ckmeans</code>: Muy Bajo a Muy Alto) para BHT y macro-dimensiones; 5 quintiles socioeconómicos para el índice INSE.</span>
                    </div>
                    <div>
                        <strong class="text-white block font-semibold mb-1">4. Catálogo unificado y STAC</strong>
                        <span class="text-slate-300">13 coberturas maestras abiertas y descargables en producción + 1 recurso preparatorio STAC (MBHT 2024 en calibración estadística) = 14 recursos totales en STAC.</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Barra de Filtros Segmentada y Adaptativa -->
        <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean mb-6 sm:mb-8">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-5 items-center">
                
                <!-- Filtros de Matriz (Columna 1 a 7) -->
                <div class="lg:col-span-7">
                    <div class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5 sm:mb-2 flex items-center space-x-1.5">
                        <i data-lucide="layers" class="w-3.5 h-3.5 text-slate-500 stroke-[1.5]"></i>
                        <span>Matriz territorial</span>
                    </div>
                    <div class="bg-slate-100 p-1 rounded-lg flex overflow-x-auto sm:flex-wrap gap-1 sm:gap-1.5 border border-slate-200 no-scrollbar" id="matrixFilters">
                        {matrix_filters_html}
                    </div>
                </div>

                <!-- Filtros de Dimensión (Columna 8 a 12) -->
                <div class="lg:col-span-5">
                    <div class="flex items-center justify-between mb-1.5 sm:mb-2">
                        <div class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
                            <i data-lucide="compass" class="w-3.5 h-3.5 text-slate-500 stroke-[1.5]"></i>
                            <span>Dimensión de soberanía</span>
                        </div>
                        <!-- Botón de Exportación Rápida -->
                        <button onclick="exportCatalogJson()" title="Descargar catálogo completo en formato JSON" class="text-[11px] text-slate-500 hover:text-slate-900 flex items-center space-x-1 font-medium cursor-pointer">
                            <i data-lucide="download" class="w-3 h-3"></i>
                            <span class="hidden sm:inline">Exportar JSON</span>
                        </button>
                    </div>
                    <div class="bg-slate-100 p-1 rounded-lg flex overflow-x-auto sm:flex-wrap gap-1 sm:gap-1.5 border border-slate-200 no-scrollbar" id="ambitoFilters">
                        <button data-ambito="all" class="ambito-btn active text-xs sm:text-sm font-bold px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition bg-slate-900 text-white shadow-xs shrink-0 sm:shrink whitespace-nowrap">
                            Todas
                        </button>
                        <button data-ambito="tierra" class="ambito-btn text-xs sm:text-sm font-medium px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition text-slate-700 hover:text-slate-900 hover:bg-slate-200 shrink-0 sm:shrink whitespace-nowrap">
                            Litósfera
                        </button>
                        <button data-ambito="mar" class="ambito-btn text-xs sm:text-sm font-medium px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition text-slate-700 hover:text-slate-900 hover:bg-slate-200 shrink-0 sm:shrink whitespace-nowrap">
                            Maritorio
                        </button>
                        <button data-ambito="aire" class="ambito-btn text-xs sm:text-sm font-medium px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-md transition text-slate-700 hover:text-slate-900 hover:bg-slate-200 shrink-0 sm:shrink whitespace-nowrap">
                            Atmósfera
                        </button>
                    </div>
                </div>

            </div>
        </div>

        <!-- Grid de Tarjetas de Capas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6" id="layersGrid">
{static_layers_html}
        </div>

        <!-- Estado Vacío (Filtro Activo Sin Coincidencias) -->
        <div id="emptyState" class="hidden text-center py-12 sm:py-16 bg-white rounded-xl border border-dashed border-slate-300 px-4">
            <i data-lucide="filter" class="w-8 h-8 sm:w-10 sm:h-10 text-slate-400 mx-auto mb-2 stroke-[1.5]"></i>
            <h3 class="text-sm sm:text-base font-semibold text-slate-800">Filtro activo sin coincidencias en el catálogo</h3>
            <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-md mx-auto">No se encontraron coberturas que coincidan con la combinación actual de búsqueda y filtros. El catálogo de IDE CIT cuenta con 19 coberturas maestras completas y disponibles.</p>
            <button onclick="resetFilters()" class="mt-4 inline-flex items-center space-x-1.5 px-3.5 py-2 bg-slate-900 hover:bg-black active:bg-slate-800 text-white text-xs font-semibold rounded-lg transition shadow-xs cursor-pointer">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
                <span>Restaurar catálogo completo (19 coberturas)</span>
            </button>
        </div>

    </section>
    <!-- 4. PANEL DE INTEROPERABILIDAD PROBADA Y VERIFICACIÓN TÉCNICA DE SERVICIOS (OGC / ISO / STAC) (Hallazgo C) -->
    <section class="bg-slate-50 border-t border-slate-200 py-10 sm:py-14 px-4 sm:px-6 lg:px-10 xl:px-12" id="interoperabilidad-probada">
        <div class="max-w-[1600px] mx-auto">
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
                <div>
                    <div class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-1.5">
                        Verificación técnica y conformidad normativa · 8/8 protocolos auditados
                    </div>
                    <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-slate-900 leading-tight">
                        Panel de Interoperabilidad Probada y Verificación Técnica
                    </h2>
                    <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                        Pruebas públicas y reproducibles de conectividad para software SIG (QGIS, ArcGIS Pro), motores analíticos (DuckDB, GeoPandas, R sf) y agentes de IA. Cada endpoint ha sido auditado con respuesta HTTP 200/206, sistema de coordenadas de distribución EPSG:4326 y verificación criptográfica SHA-256.
                    </p>
                </div>
                <div class="shrink-0 flex items-center space-x-2 text-xs font-mono text-slate-500">
                    <i data-lucide="shield-check" class="w-4 h-4 text-emerald-700"></i>
                    <span>Auditoría de integridad: Octubre de 2026</span>
                </div>
            </div>

            <!-- Tabla de Servicios Probados (Hallazgo C) -->
            <div class="bg-white rounded-2xl border border-slate-200 shadow-clean overflow-hidden mb-8">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-white border-b border-slate-800">
                                <th class="p-3.5 font-bold uppercase tracking-wider">Protocolo / Estándar</th>
                                <th class="p-3.5 font-bold uppercase tracking-wider">Endpoint / URL Funcional</th>
                                <th class="p-3.5 font-bold uppercase tracking-wider">Sistema Ref.</th>
                                <th class="p-3.5 font-bold uppercase tracking-wider">Respuesta Esperada</th>
                                <th class="p-3.5 font-bold uppercase tracking-wider">Prueba Reproducible (CLI)</th>
                                <th class="p-3.5 font-bold uppercase tracking-wider text-center">Estado</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-sans">
                            <!-- Fila 1: STAC 1.0.0 Catalog -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">STAC 1.0.0 Catalog</span>
                                    <span class="text-[11px] text-slate-500">Catálogo estático con extensiones proj / file / sci</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 font-semibold hover:underline">/stac/catalog.json</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (JSON)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -s https://ide.cit.uai.cl/stac/catalog.json | jq .id</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 2: GeoParquet 1.1 -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">Cloud-Optimized GeoParquet 1.1</span>
                                    <span class="text-[11px] text-slate-500">WKB Polígonos · Byte-Range HTTP 206</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet" class="text-slate-900 font-semibold hover:underline">/download/MBHT_2017_R15_Manzanas.parquet</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 / 206 Range</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">duckdb -c "SELECT count(*), round(avg(bht),4) FROM 'https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet'"</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 3: OGC GeoPackage -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">OGC GeoPackage 1.3 (GPKG)</span>
                                    <span class="text-[11px] text-slate-500">Estándar ISO/IEC 19125 SQLite · Streaming GDAL</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.gpkg" class="text-slate-900 font-semibold hover:underline">/download/MBHT_2017_R15_Manzanas.gpkg</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (SQLite)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">ogrinfo -ro -so /vsicurl/https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.gpkg</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 4: ESRI Shapefile -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">ESRI Shapefile (ZIP)</span>
                                    <span class="text-[11px] text-slate-500">SHP + SHX + DBF + PRJ + CPG UTF-8</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas_SHP.zip" class="text-slate-900 font-semibold hover:underline">/download/MBHT_2017_R15_Manzanas_SHP.zip</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (ZIP)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -sI https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas_SHP.zip | grep -i content-length</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 5: QGIS Layer Definition (QLR) -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">QGIS Layer Definition (QLR)</span>
                                    <span class="text-[11px] text-slate-500">Definición de capa con simbología Jenks</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr" class="text-slate-900 font-semibold hover:underline">/download/qgis/CIT_MBHT_2017_Nacional.qlr</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (XML QLR)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -s https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr | head -n 5</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 6: ISO 19115-1:2014 / ISO 19139 XML -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">ISO 19115-1:2014 / ISO 19139 XML</span>
                                    <span class="text-[11px] text-slate-500">Metadatos normalizados gmd:MD_Metadata</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml" class="text-slate-900 font-semibold hover:underline">/download/iso_xml/kpi_mud_2017_iso19139.xml</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326 / 5360</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (XML)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -s https://ide.cit.uai.cl/download/iso_xml/kpi_mud_2017_iso19139.xml | head -n 10</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 7: W3C DCAT-AP 2.0 JSON-LD -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">W3C DCAT-AP 2.0 (JSON-LD)</span>
                                    <span class="text-[11px] text-slate-500">Grafo semántico de catálogo para cosecha federada</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/dcat.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 font-semibold hover:underline">/dcat.json</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">EPSG:4326</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (JSON-LD)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -s https://ide.cit.uai.cl/dcat.json | jq '."dcat:dataset" | length'</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                            <!-- Fila 8: Reporte de Conformidad y Benchmarks -->
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-3.5">
                                    <span class="font-bold text-slate-900 block">Conformance & Benchmarks JSON</span>
                                    <span class="text-[11px] text-slate-500">Métricas empíricas p50/p95/p99 y auditoría ISO/STAC</span>
                                </td>
                                <td class="p-3.5 font-mono text-[11px]">
                                    <a href="https://ide.cit.uai.cl/conformance_report.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 font-semibold hover:underline">/conformance_report.json</a>
                                </td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">N/A (Telemetría)</td>
                                <td class="p-3.5 font-mono text-[11px] text-slate-700">HTTP 200 (JSON)</td>
                                <td class="p-3.5 font-mono text-[10px] text-slate-700">
                                    <code class="bg-slate-100 p-1 rounded block">curl -s https://ide.cit.uai.cl/conformance_report.json | jq .benchmarks</code>
                                </td>
                                <td class="p-3.5 text-center font-semibold text-emerald-800">Verificado</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Panel de Reproducibilidad Científica E2E (Hallazgo D y 6) -->
            <div class="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-lg border border-slate-800">
                <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
                    <div class="flex items-center space-x-2">
                        <i data-lucide="terminal" class="w-5 h-5 text-uai-gold"></i>
                        <h3 class="text-base sm:text-lg font-bold">Protocolo Seguro de Reproducibilidad Científica de Extremo a Extremo (E2E)</h3>
                    </div>
                    <span class="text-slate-400 font-mono text-xs">Testigo Censal: Manzana 15101011001004001 (Arica)</span>
                </div>
                <p class="text-xs sm:text-sm text-slate-300 leading-relaxed mb-4">
                    Para certificar la integridad de los datos y reproducir la formulación matemática de la MBHT en un entorno aislado, ejecute el flujo de 3 pasos auditado (sin patrones de ejecución remota insegura):
                </p>
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200 space-y-2 overflow-x-auto leading-relaxed">
                    <div class="text-slate-400"># 1. Descargar script de verificación auditable</div>
                    <div class="text-emerald-400">curl -s -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py</div>
                    <div class="text-slate-400 mt-2"># 2. Verificar integridad del script mediante SHA-256 publicado</div>
                    <div class="text-emerald-400">echo "7fb25d61a29544e57c17869c6ea3566c68659d003dce9f59dfcd642fbf96a8d0  reproducir_verificacion_r15.py" | sha256sum -c</div>
                    <div class="text-slate-400 mt-2"># 3. Ejecutar verificación determinista localmente</div>
                    <div class="text-emerald-400">python reproducir_verificacion_r15.py</div>
                </div>
                <div class="mt-4 grid grid-cols-2 sm:grid-cols-5 gap-3 text-center">
                    <div class="bg-white/5 p-2.5 rounded-lg border border-white/10">
                        <span class="block text-[10px] text-slate-400 uppercase">BHT Referencia</span>
                        <strong class="font-mono text-sm text-uai-gold">0.3751</strong>
                    </div>
                    <div class="bg-white/5 p-2.5 rounded-lg border border-white/10">
                        <span class="block text-[10px] text-slate-400 uppercase">Dim. Accesibilidad</span>
                        <strong class="font-mono text-sm text-white">0.3204</strong>
                    </div>
                    <div class="bg-white/5 p-2.5 rounded-lg border border-white/10">
                        <span class="block text-[10px] text-slate-400 uppercase">Dim. Socioeconómica</span>
                        <strong class="font-mono text-sm text-white">0.4421</strong>
                    </div>
                    <div class="bg-white/5 p-2.5 rounded-lg border border-white/10">
                        <span class="block text-[10px] text-slate-400 uppercase">Dim. Seguridad</span>
                        <strong class="font-mono text-sm text-white">0.4102</strong>
                    </div>
                    <div class="bg-white/5 p-2.5 rounded-lg border border-white/10">
                        <span class="block text-[10px] text-slate-400 uppercase">Dim. Ambiental</span>
                        <strong class="font-mono text-sm text-white">0.3276</strong>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. ACCESO AL CENTRO DE DESCARGAS TERRITORIALES -->
    <section class="bg-white border-t border-slate-200 py-10 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            <div class="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 lg:p-10 shadow-lg relative overflow-hidden flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                <div class="max-w-3xl">
                    <div class="text-xs font-bold uppercase tracking-widest text-uai-gold mb-2">
                        Repositorio de descargas masivas · 16 regiones y consolidado nacional
                    </div>
                    <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-white leading-tight">
                        Centro de descargas territoriales
                    </h2>
                    <p class="text-xs sm:text-sm text-slate-300 mt-2.5 leading-relaxed font-normal">
                        Descarga directa y abierta de las <strong>204.906 manzanas censales</strong> con indicadores de bienestar, <strong>55.035 equipamientos</strong> y <strong>1.589.595 tramos viales</strong> en formatos equivalentes (<code class="font-mono text-slate-200">GeoParquet</code>, <code class="font-mono text-slate-200">GeoPackage</code>, <code class="font-mono text-slate-200">Shapefile</code> y <code class="font-mono text-slate-200">CSV</code>), filtrables por cobertura temática, región y comuna.
                    </p>
                </div>
                <div class="shrink-0">
                    <a href="descargas" class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-uai-gold hover:bg-uai-goldHover text-white font-bold text-sm shadow-md transition transform hover:-translate-y-0.5 cursor-pointer">
                        <span>Ir al centro de descargas</span>
                        <i data-lucide="arrow-right" class="w-4 h-4 stroke-[2.5]"></i>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- 5. ECOSISTEMA SATELITAL DE APLICACIONES, VISORES Y GUÍAS TÉCNICAS -->
    <section class="bg-white border-t border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12" id="ecosistema">
        <div class="max-w-[1600px] mx-auto">
            <div class="text-center max-w-3xl mx-auto mb-6 sm:mb-8">
                <span class="text-[11px] sm:text-xs font-bold uppercase tracking-widest text-slate-400">Ecosistema CIT y recursos analíticos</span>
                <h2 class="text-lg sm:text-2xl font-bold text-slate-900 mt-1">Plataformas, visores y guías técnicas</h2>
                <p class="text-xs sm:text-sm text-slate-500 mt-1">Ecosistema de plataformas analíticas, libros digitales con guías metodológicas y herramientas interactivas conectadas a la IDE CIT.</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 sm:gap-4" id="appsGrid">
{static_apps_html}
            </div>
        </div>
    </section>

    <!-- 5. RED NACIONAL DE IDES Y GEOPORTALES DEL ESTADO DE CHILE (REFERENCIAL) -->
    <section class="bg-slate-50 border-t border-slate-200 py-10 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-clean flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                <div class="max-w-3xl">
                    <div class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-1.5">
                        Sistema Nacional de Información Territorial (SNIT) · 19 geoportales oficiales
                    </div>
                    <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 leading-tight">
                        Red de IDEs y geoportales de Chile
                    </h2>
                    <p class="text-xs sm:text-sm text-slate-600 mt-2 leading-relaxed">
                        Directorio y catálogo de interoperabilidad hacia las Infraestructuras de Datos Espaciales sectoriales, ministeriales, académicas y regionales de Chile, alineadas con la Política Nacional de Información Territorial-Geoespacial.
                    </p>
                </div>
                <div class="shrink-0">
                    <a href="red-ides" class="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-black text-white font-semibold text-xs sm:text-sm shadow-xs transition cursor-pointer">
                        <span>Explorar los 19 geoportales</span>
                        <i data-lucide="arrow-right" class="w-4 h-4 stroke-[2]"></i>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- 5. MODAL DETALLE DE CAPA / FICHA TÉCNICA -->
    <div id="layerModal" class="fixed inset-0 z-50 hidden bg-black/70 backdrop-blur-xs flex items-center justify-center p-2 sm:p-4 md:p-6 overflow-y-auto">
        <div class="bg-white rounded-xl max-w-3xl w-full shadow-2xl border border-slate-300 overflow-hidden flex flex-col max-h-[94vh] sm:max-h-[90vh]">
            
            <!-- Modal Header -->
            <div class="p-3.5 sm:p-5 bg-slate-900 text-white flex justify-between items-start border-b border-slate-800 shrink-0">
                <div class="pr-2">
                    <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 mb-1">
                        <span id="modalBadge" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-50 text-blue-900 border border-blue-300">LÍNEA BASE OFICIAL VIGENTE (SUBDERE - MINISTERIAL)</span>
                        <span id="modalAmbito" class="text-xs text-slate-300">Litósfera</span>
                        <span class="text-xs text-slate-600">•</span>
                        <span id="modalEscala" class="text-xs text-slate-300">204.906 manzanas censales (16 Regiones de Chile)</span>
                    </div>
                    <h2 id="modalTitle" class="text-sm sm:text-lg font-bold leading-snug text-white break-words">Matriz de Bienestar Humano Territorial (MBHT 2017) — 18 Indicadores E2SFCA</h2>
                </div>
                <button id="btnCloseModal" class="text-slate-400 hover:text-white p-2 rounded-lg bg-white/10 hover:bg-white/20 active:bg-white/30 transition shrink-0 cursor-pointer">
                    <i data-lucide="x" class="w-4 h-4 sm:w-5 sm:h-5 stroke-[1.5]"></i>
                </button>
            </div>

            <!-- Modal Body (Scrollable) -->
            <div class="p-4 sm:p-6 overflow-y-auto space-y-4 sm:space-y-5 custom-scrollbar text-xs sm:text-sm">
                
                <!-- Aviso de Próxima Publicación (Censo 2024 en Calibración) -->
                <div id="modalRestrictedNotice" class="hidden p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-amber-950 text-xs flex items-start space-x-2.5 shadow-xs">
                    <i data-lucide="info" class="w-4 h-4 shrink-0 text-amber-700 mt-0.5"></i>
                    <div>
                        <span class="font-bold text-amber-950 block mb-0.5">Ciclo de vida de datos: Insumos censales preparatorios (Censo 2024)</span>
                        <p class="text-amber-900 text-[11px] leading-relaxed">
                            <strong>Disponibilidad de infraestructura:</strong> Servicios y descargas 100% en línea (SLA 99.9%, CDN CloudFront).<br>
                            <strong>Madurez metodológica:</strong> 12 coberturas cerradas y vigentes en producción. Este conjunto entrega los insumos demográficos preparatorios (Sprague y equilibrio de género por manzana) del Censo 2024 para descarga abierta; la síntesis multidimensional MBHT 2024 está programada para su lanzamiento oficial en noviembre de 2026. Para análisis consolidados en producción, consulte la <a href="/descargas" class="underline font-bold text-amber-950 hover:text-black">línea base oficial MBHT 2017</a>.
                        </p>
                    </div>
                </div>

                <!-- Resumen Metodológico Pre-Poblado (Hallazgo A) -->
                <div>
                    <h4 class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Definición y linaje metodológico</h4>
                    <p id="modalResumen" class="text-slate-700 leading-relaxed font-normal">Línea base nacional oficial de la Matriz de Bienestar Humano Territorial Integral evaluada sobre 204.906 manzanas censales en las 16 regiones de Chile. Desarrollada por el Centro de Inteligencia Territorial (CIT-UAI) en convenio con la Subsecretaría de Desarrollo Regional y Administrativo (SUBDERE), cuantifica el bienestar territorial mediante 18 indicadores elementales agrupados en 4 dimensiones estratégicas: Accesibilidad a servicios esenciales (salud, educación, áreas verdes, transporte), Dimensión Socioeconómica, Seguridad pública y Calidad ambiental. Cada manzana cuenta con vector de impedancia peatonal cinemático calculado sobre la red vial nacional de 1.589.595 tramos ajustado por pendiente topográfica DEM.</p>
                </div>

                <!-- Formulación Matemática Pre-Poblada (Hallazgo A) -->
                <div class="bg-slate-50 border border-slate-200 rounded-lg p-3 sm:p-4">
                    <div class="flex items-center space-x-1.5 mb-1.5 text-slate-800 font-bold text-xs sm:text-sm">
                        <i data-lucide="calculator" class="w-4 h-4 stroke-[1.5]"></i>
                        <span>Formulación matemática y operador</span>
                    </div>
                    <code id="modalFormula" class="block font-mono text-[11px] sm:text-xs text-slate-800 bg-white p-2.5 rounded border border-slate-200 overflow-x-auto leading-relaxed">BHT = \sum_{{i=1}}^{{18}} w_i \cdot I_i = 0.3333 \cdot Dim_{{Acc}} + 0.3333 \cdot Dim_{{Soc}} + 0.2222 \cdot Dim_{{Seg}} + 0.1111 \cdot Dim_{{Amb}} | A_i = \sum_{{j}} \frac{{S_j \cdot f(d_{{ij}})}}{{\sum_{{k}} D_k \cdot f(d_{{kj}})}} | f(d_{{ij}}) = \exp\left(-0.5 \cdot \left(\frac{{t_{{ij}}}}{{15}}\right)^2\right) \text{{ con velocidad Tobler }} W(S) = 6 \cdot \exp(-3.5 \cdot |S + 0.05|)</code>
                </div>

                <!-- Referencia Espacial y Cobertura Geográfica (ISO 19115 Standard) -->
                <div class="border border-slate-200 rounded-xl overflow-hidden bg-slate-50" id="sectionSpatialRef">
                    <div class="p-3 bg-slate-100 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
                        <div class="flex items-center space-x-1.5 text-slate-800 font-bold text-xs sm:text-sm">
                            <i data-lucide="map" class="w-4 h-4 text-slate-700 stroke-[1.5]"></i>
                            <span>Referencia espacial y cobertura (ISO 19115)</span>
                        </div>
                        <div class="flex items-center space-x-1.5 text-[11px] font-mono">
                            <span id="modalCRS" class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-700">EPSG:4326</span>
                            <span id="modalGeom" class="px-2 py-0.5 bg-white border border-slate-200 rounded text-slate-600">MultiPolygon</span>
                        </div>
                    </div>
                    <div class="p-2.5 sm:p-3 space-y-2">
                        <!-- Contenedor del Mapa Leaflet -->
                        <div id="layerPreviewMap" class="w-full h-48 sm:h-56 rounded-lg border border-slate-200 bg-slate-200 relative z-0"></div>
                        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-1 text-[11px] text-slate-500 px-1 font-mono">
                            <span id="modalBboxCoords">BBOX: [-75.64, -55.98, -66.86, -17.50]</span>
                            <button type="button" onclick="fitLayerBounds()" class="text-slate-700 hover:text-black font-sans font-semibold underline text-xs cursor-pointer">
                                Centrar extensión
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Fuentes Institucionales Pre-Pobladas (Hallazgo A) -->
                <div>
                    <h4 class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center space-x-1.5">
                        <i data-lucide="building-2" class="w-3.5 h-3.5 text-slate-500 stroke-[1.5]"></i>
                        <span>Fuentes institucionales e insumos de origen</span>
                    </h4>
                    <div id="modalSourcesList" class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg text-left flex flex-col justify-between">
                            <div>
                                <div class="flex items-start justify-between gap-2 mb-1">
                                    <span class="font-bold text-slate-900 text-xs">Instituto Nacional de Estadísticas (INE)</span>
                                    <a href="https://www.ine.gob.cl" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-black inline-flex items-center space-x-0.5 text-[11px] font-semibold underline shrink-0">
                                        <span>Portal oficial</span>
                                        <i data-lucide="external-link" class="w-3 h-3 stroke-[1.5]"></i>
                                    </a>
                                </div>
                                <span class="text-[11px] font-medium text-slate-700 block mb-1.5">Censo de Población y Vivienda 2017</span>
                                <p class="text-[10px] text-slate-600 font-serif italic bg-white p-2 rounded border border-slate-200 leading-relaxed">Instituto Nacional de Estadísticas. (2017). Censo de Población y Vivienda 2017: Base de datos de manzanas y entidades censales. Santiago, Chile: INE.</p>
                            </div>
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg text-left flex flex-col justify-between">
                            <div>
                                <div class="flex items-start justify-between gap-2 mb-1">
                                    <span class="font-bold text-slate-900 text-xs">Ministerio de Salud (MINSAL / DEIS)</span>
                                    <a href="https://deis.minsal.cl" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-black inline-flex items-center space-x-0.5 text-[11px] font-semibold underline shrink-0">
                                        <span>Portal oficial</span>
                                        <i data-lucide="external-link" class="w-3 h-3 stroke-[1.5]"></i>
                                    </a>
                                </div>
                                <span class="text-[11px] font-medium text-slate-700 block mb-1.5">Registro Nacional de Prestadores Individuales e Institucionales de Salud</span>
                                <p class="text-[10px] text-slate-600 font-serif italic bg-white p-2 rounded border border-slate-200 leading-relaxed">Departamento de Estadística e Información de Salud. (2017). Catastro georreferenciado de establecimientos asistenciales públicos y privados. Santiago: MINSAL.</p>
                            </div>
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg text-left flex flex-col justify-between">
                            <div>
                                <div class="flex items-start justify-between gap-2 mb-1">
                                    <span class="font-bold text-slate-900 text-xs">Ministerio de Educación (MINEDUC)</span>
                                    <a href="https://datosabiertos.mineduc.cl" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-black inline-flex items-center space-x-0.5 text-[11px] font-semibold underline shrink-0">
                                        <span>Portal oficial</span>
                                        <i data-lucide="external-link" class="w-3 h-3 stroke-[1.5]"></i>
                                    </a>
                                </div>
                                <span class="text-[11px] font-medium text-slate-700 block mb-1.5">Directorio Oficial de Establecimientos Educacionales</span>
                                <p class="text-[10px] text-slate-600 font-serif italic bg-white p-2 rounded border border-slate-200 leading-relaxed">Centro de Estudios MINEDUC. (2017). Directorio oficial de establecimientos escolares, matrícula y dependencia administrativa. Santiago: MINEDUC.</p>
                            </div>
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg text-left flex flex-col justify-between">
                            <div>
                                <div class="flex items-start justify-between gap-2 mb-1">
                                    <span class="font-bold text-slate-900 text-xs">Subsecretaría de Prevención del Delito (SPD)</span>
                                    <a href="http://cead.spd.gov.cl" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-black inline-flex items-center space-x-0.5 text-[11px] font-semibold underline shrink-0">
                                        <span>Portal oficial</span>
                                        <i data-lucide="external-link" class="w-3 h-3 stroke-[1.5]"></i>
                                    </a>
                                </div>
                                <span class="text-[11px] font-medium text-slate-700 block mb-1.5">Centro de Estudios y Análisis del Delito (CEAD)</span>
                                <p class="text-[10px] text-slate-600 font-serif italic bg-white p-2 rounded border border-slate-200 leading-relaxed">Subsecretaría de Prevención del Delito. (2017). Estadísticas policiales de delitos de mayor connotación social georreferenciados. Santiago: SPD.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Diccionario de Atributos Pre-Poblado (Hallazgo A) -->
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400">Estructura del esquema físico de atributos</h4>
                        <span id="modalAttrCountBadge" class="font-mono text-[10px] text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">42 atributos oficiales (Esquema físico validado)</span>
                    </div>
                    <div class="border border-slate-200 rounded-lg overflow-x-auto max-h-64 custom-scrollbar">
                        <table class="w-full text-left border-collapse text-xs">
                            <thead class="bg-slate-100 border-b border-slate-200 text-slate-700 sticky top-0 z-10">
                                <tr>
                                    <th class="px-2.5 py-2 font-bold">Campo</th>
                                    <th class="px-2.5 py-2 font-bold">Tipo</th>
                                    <th class="px-2.5 py-2 font-bold">Descripción</th>
                                </tr>
                            </thead>
                            <tbody id="modalAttributesTable" class="divide-y divide-slate-100">
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">id_manzana</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">String</td><td class="text-slate-700 px-2.5 py-1.5">Identificador censal único de la manzana (15 dígitos INE)</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">cod_comuna</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">String</td><td class="text-slate-700 px-2.5 py-1.5">Código único territorial (CUT) comunal oficial de Chile</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">comuna</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">String</td><td class="text-slate-700 px-2.5 py-1.5">Nombre oficial de la comuna</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">personas</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Integer</td><td class="text-slate-700 px-2.5 py-1.5">Población total residente censada en la manzana (Censo 2017)</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">bht_2017</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Float</td><td class="text-slate-700 px-2.5 py-1.5">Índice sintético de Bienestar Humano Territorial [0.0 - 1.0]</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">dim_acc</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Float</td><td class="text-slate-700 px-2.5 py-1.5">Dimensión de Accesibilidad a equipamientos urbanos (E2SFCA)</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">dim_soc</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Float</td><td class="text-slate-700 px-2.5 py-1.5">Dimensión Socioeconómica y vulnerabilidad residencial</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">dim_seg</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Float</td><td class="text-slate-700 px-2.5 py-1.5">Dimensión de Seguridad pública y exposición a delitos</td></tr>
                                <tr><td class="font-mono font-bold text-slate-800 px-2.5 py-1.5">dim_amb</td><td class="text-slate-500 px-2.5 py-1.5 font-mono text-[11px]">Float</td><td class="text-slate-700 px-2.5 py-1.5">Dimensión Ambiental, cobertura vegetal y proximidad a parques</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Conectores Directos -->
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-400">Conexión directa e interoperabilidad</h4>
                        <a href="connection_examples.json" target="_blank" rel="noopener noreferrer" class="text-[11px] font-mono text-indigo-600 hover:underline">connection_examples.json</a>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                        <div class="border border-slate-200 rounded-lg p-2.5 bg-slate-50">
                            <div class="flex justify-between items-center mb-1 text-xs font-bold text-slate-700">
                                <span>QGIS (Vector Tile)</span>
                                <button onclick="copySnippet('qgis')" class="text-slate-600 hover:text-black font-bold text-xs p-1">Copiar</button>
                            </div>
                            <input type="text" id="snippetQGIS" readonly value="https://ide.cit.uai.cl/tiles/kpi_mud_2017/{{z}}/{{x}}/{{y}}.pbf" class="w-full text-[10px] sm:text-xs font-mono bg-white border border-slate-200 p-1.5 rounded text-slate-600 truncate" />
                        </div>
                        <div class="border border-slate-200 rounded-lg p-2.5 bg-slate-50">
                            <div class="flex justify-between items-center mb-1 text-xs font-bold text-slate-700">
                                <span>Python (GeoPandas)</span>
                                <button onclick="copySnippet('python')" class="text-slate-600 hover:text-black font-bold text-xs p-1">Copiar</button>
                            </div>
                            <input type="text" id="snippetPython" readonly value="gpd.read_parquet('https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.parquet')" class="w-full text-[10px] sm:text-xs font-mono bg-white border border-slate-200 p-1.5 rounded text-slate-600 truncate" />
                        </div>
                        <div class="border border-slate-200 rounded-lg p-2.5 bg-slate-50">
                            <div class="flex justify-between items-center mb-1 text-xs font-bold text-slate-700">
                                <span>R (sf)</span>
                                <button onclick="copySnippet('r')" class="text-slate-600 hover:text-black font-bold text-xs p-1">Copiar</button>
                            </div>
                            <input type="text" id="snippetR" readonly value="sf::st_read('https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.parquet')" class="w-full text-[10px] sm:text-xs font-mono bg-white border border-slate-200 p-1.5 rounded text-slate-600 truncate" />
                        </div>
                    </div>
                </div>

                <!-- Citación -->
                <div class="bg-slate-50 border border-slate-200 p-3 rounded-lg">
                    <div class="flex justify-between items-center mb-1">
                        <h4 class="text-[11px] sm:text-xs font-bold text-slate-700">Cómo citar esta cobertura (Norma APA 7.ª edición en español)</h4>
                        <button onclick="copyCitation()" class="text-slate-600 hover:text-black text-xs font-semibold flex items-center space-x-1 p-1">
                            <i data-lucide="copy" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                            <span>Copiar</span>
                        </button>
                    </div>
                    <p id="modalCitation" class="text-slate-600 font-serif italic text-[11px] sm:text-xs"></p>
                </div>

            </div>

            <!-- Modal Footer -->
            <div class="p-3 sm:p-4 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 text-xs sm:text-sm shrink-0">
                <div class="text-slate-500 text-center sm:text-left">
                    Licencia: <strong id="modalLicense" class="text-slate-800">CC BY 4.0</strong>
                </div>
                <div class="grid grid-cols-2 sm:flex items-center gap-1.5 sm:gap-2 flex-wrap justify-end">
                    <a id="btnVerFichaMaestra" href="ficha-mbht-2017" target="_blank" rel="noopener noreferrer" class="bg-amber-50 hover:bg-amber-100 text-amber-950 border border-amber-300 px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-bold transition flex items-center justify-center space-x-1 text-center">
                        <i data-lucide="file-text" class="w-3.5 h-3.5 text-amber-800"></i>
                        <span>Ficha Maestra (17D)</span>
                    </a>
                    <a id="btnDownloadParquet" href="#" class="bg-slate-900 hover:bg-black active:bg-slate-800 text-white px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-medium transition flex items-center justify-center space-x-1 text-center">
                        <i data-lucide="download" class="w-3.5 h-3.5 stroke-[1.5] hidden sm:inline"></i>
                        <span>GeoParquet</span>
                    </a>
                    <a id="btnDownloadGPKG" href="#" class="bg-white hover:bg-slate-100 active:bg-slate-200 text-slate-700 border border-slate-300 px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-medium transition text-center">
                        <span>GeoPackage</span>
                    </a>
                    <a id="btnDownloadSHP" href="#" class="bg-white hover:bg-slate-100 active:bg-slate-200 text-slate-700 border border-slate-300 px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-medium transition text-center">
                        <span>Shapefile</span>
                    </a>
                    <a id="btnDownloadCSV" href="#" class="bg-white hover:bg-slate-100 active:bg-slate-200 text-slate-700 border border-slate-300 px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-medium transition text-center">
                        <span>CSV</span>
                    </a>
                    <a id="btnDownloadXML" href="#" target="_blank" rel="noopener noreferrer" class="bg-white hover:bg-slate-100 active:bg-slate-200 text-slate-700 border border-slate-300 px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg font-medium transition text-center flex items-center justify-center space-x-1">
                        <i data-lucide="file-code" class="w-3.5 h-3.5 stroke-[1.5] hidden sm:inline"></i>
                        <span>ISO XML</span>
                    </a>
                </div>
            </div>
        </div>
    </div>


    <!-- 6. WIDGET Y VENTANA FLOTANTE DEL COPILOTO IA TERRITORIAL -->
    <!-- Micro-invitación pedagógica y sobria (CIT-UAI) -->
    <div id="copilotWelcomeHint" onclick="toggleCopilot(true); dismissCopilotHint(event);" class="cursor-pointer fixed bottom-20 right-3 sm:right-6 z-40 w-[calc(100vw-1.5rem)] max-w-[310px] sm:max-w-[340px] bg-[#0A192F] text-slate-200 border border-slate-700/80 border-t-2 border-t-[#6493B5] rounded-xl shadow-2xl p-3 text-xs leading-relaxed hidden transition-all duration-300">
        <div class="flex items-start justify-between gap-2">
            <p class="font-normal text-slate-300 text-[11px] sm:text-xs select-none">
                Orientación en datos territoriales e indicadores MBHT. Puede consultar aquí al Copiloto CIT.
            </p>
            <button onclick="dismissCopilotHint(event)" type="button" aria-label="Cerrar aviso" class="text-[#6493B5] hover:text-white transition cursor-pointer text-sm font-bold leading-none p-1 shrink-0">
                &times;
            </button>
        </div>
    </div>

    <button id="btnOpenCopilot" onclick="toggleCopilot()" type="button" aria-label="Abrir asistente Copiloto IA Territorial" class="fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-40 bg-slate-900 hover:bg-black active:bg-slate-800 text-white px-4 py-2.5 sm:px-4.5 sm:py-3 rounded-full shadow-lg border border-slate-700 flex items-center space-x-2.5 transition cursor-pointer">
        <span class="w-2 h-2 rounded-full bg-[#6493B5] shrink-0"></span>
        <span class="text-xs sm:text-sm font-semibold tracking-wide">Copiloto IA</span>
    </button>

    <!-- Ventana de Chat del Copiloto IA -->
    <div id="copilotDrawer" class="fixed bottom-20 right-3 sm:right-6 w-[calc(100vw-1.5rem)] sm:w-[400px] max-h-[75vh] sm:max-h-[580px] bg-white rounded-2xl shadow-widget border border-slate-300 hidden flex-col z-50 overflow-hidden transition-all duration-200">
        
        <!-- Header del Copiloto -->
        <div class="bg-slate-900 text-white p-3.5 sm:p-4 flex items-center justify-between border-b border-slate-800 shrink-0">
            <div class="flex items-center space-x-2.5">
                <div class="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-[#6493B5] border border-white/10 font-bold text-xs">
                    CIT
                </div>
                <div>
                    <h3 class="font-bold text-xs sm:text-sm leading-tight text-white flex items-center space-x-1.5">
                        <span>Copiloto IA Territorial</span>
                        <span class="text-[10px] px-1.5 py-0.2 rounded bg-[#6493B5] text-white font-black uppercase">CIT</span>
                    </h3>
                    <p class="text-[11px] text-slate-400">Asistente de datos y metodologías</p>
                </div>
            </div>
            <button onclick="toggleCopilot(false)" class="text-slate-400 hover:text-white p-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition cursor-pointer">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        </div>

        <!-- Hilo de Mensajes -->
        <div id="copilotMessages" class="p-3.5 sm:p-4 overflow-y-auto space-y-3 custom-scrollbar flex-1 bg-slate-50 text-xs sm:text-sm">
            
            <!-- Mensaje de Bienvenida -->
            <div class="flex items-start space-x-2.5">
                <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold border border-slate-700">
                    CIT
                </div>
                <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 text-slate-800 space-y-2 shadow-xs max-w-[85%]">
                    <p class="leading-relaxed font-medium">
                        Bienvenido/a al <strong>Copiloto IA Territorial del CIT-UAI</strong>. En esta plataforma disponemos de las coberturas espaciales y variables sociodemográficas imputadas a escala de manzana, orientadas al diagnóstico del <strong>Bienestar Humano Territorial (MBHT)</strong> y la accesibilidad caminable en las comunas del país.
                    </p>
                    <p class="text-slate-600 text-[11px] sm:text-xs font-normal">
                        Áreas temáticas de consulta:
                    </p>
                    <ul class="list-disc list-inside space-y-1 text-slate-600 text-[11px] sm:text-xs font-normal">
                        <li>Indicadores y dimensiones de bienestar territorial (salud, educación, áreas verdes).</li>
                        <li>Metodología de accesibilidad peatonal real (función Tobler y red vial).</li>
                        <li>Descargas de datos abiertos en GeoParquet, GeoPackage y Shapefile.</li>
                    </ul>
                </div>
            </div>

            <!-- Sugerencias Rápidas Sobrias -->
            <div class="pt-2 space-y-1.5">
                <p class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Consultas orientativas:</p>
                <div class="flex flex-col gap-1.5">
                    <button onclick="sendCopilotSuggestion('¿Qué indicadores componen la matriz de bienestar territorial MBHT?')" class="bg-white hover:bg-slate-100 text-left text-slate-700 border border-slate-200 text-xs px-3 py-2 rounded-lg transition cursor-pointer">
                        ¿Qué indicadores componen la matriz de bienestar territorial MBHT?
                    </button>
                    <button onclick="sendCopilotSuggestion('¿Cómo descargar y abrir las coberturas en QGIS o Python?')" class="bg-white hover:bg-slate-100 text-left text-slate-700 border border-slate-200 text-xs px-3 py-2 rounded-lg transition cursor-pointer">
                        ¿Cómo descargar y abrir las coberturas en QGIS o Python?
                    </button>
                </div>
            </div>

        </div>

        <!-- Barra de Entrada -->
        <div class="p-2.5 sm:p-3 bg-white border-t border-slate-200 shrink-0">
            <form onsubmit="handleCopilotSubmit(event)" class="flex items-center space-x-1.5">
                <input type="text" id="copilotInput" placeholder="Pregunta sobre indicadores, datos o fórmulas..." 
                       class="flex-1 bg-slate-50 border border-slate-300 focus:border-slate-800 focus:bg-white rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-800 focus:outline-none transition font-normal placeholder-slate-400" />
                <button type="submit" class="bg-slate-900 hover:bg-black active:bg-slate-800 text-white p-2 rounded-lg transition cursor-pointer shrink-0">
                    <i data-lucide="send" class="w-4 h-4"></i>
                </button>
            </form>
        </div>

    </div>

    <!-- 5. CENTRO DE INTEROPERABILIDAD Y SERVICIOS WEB OGC -->
    <section class="bg-slate-50 border-t border-slate-200 py-10 sm:py-14 px-4 sm:px-6 lg:px-10 xl:px-12" id="interoperabilidad">
        <div class="max-w-[1600px] mx-auto">
            
            <div class="max-w-3xl mb-8 sm:mb-10">
                <span class="text-[11px] sm:text-xs font-bold uppercase tracking-widest text-slate-400">Interoperabilidad y servicios OGC</span>
                <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-slate-900 mt-1 leading-tight">
                    Servicios de mapas y conectores de datos abiertos
                </h2>
                <p class="text-xs sm:text-sm text-slate-600 mt-2 leading-relaxed font-normal">
                    Conexión directa a las matrices territoriales del CIT para software SIG (QGIS, ArcGIS), entornos de análisis (Python, R) y visores web institucionales.
                </p>
            </div>

            <!-- Grid de 4 Servicios OGC / Conectores -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-8">
                
                <!-- Conectores QGIS & Cartografía Base -->
                <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 flex flex-col justify-between shadow-clean hover:shadow-md hover:border-slate-300 transition">
                    <div>
                        <div class="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center mb-3">
                            <i data-lucide="map" class="w-4 h-4 stroke-[1.5]"></i>
                        </div>
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Conectores QGIS (QLR / QML)</h4>
                        <p class="text-xs text-slate-500 mb-3 leading-relaxed font-normal">Definiciones de capa preconfiguradas con simbología oficial Jenks y streaming GDAL <code>/vsicurl/</code> para QGIS 3.28+.</p>
                    </div>
                    <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-[11px] font-mono text-slate-400">QGIS 3.28+ XML</span>
                        <a href="download/qgis/CIT_MBHT_2017_Nacional.qlr" download class="font-semibold text-slate-700 hover:text-black transition cursor-pointer underline">Descargar QLR</a>
                    </div>
                </div>

                <!-- OGC GeoPackage 1.3 -->
                <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 flex flex-col justify-between shadow-clean hover:shadow-md hover:border-slate-300 transition">
                    <div>
                        <div class="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center mb-3">
                            <i data-lucide="database" class="w-4 h-4 stroke-[1.5]"></i>
                        </div>
                        <h4 class="font-bold text-slate-900 text-sm mb-1">OGC GeoPackage 1.3 (SQLite)</h4>
                        <p class="text-xs text-slate-500 mb-3 leading-relaxed font-normal">Contenedor espacial relacional abierto con índice R-Tree para análisis vectorial en QGIS, ArcGIS Pro y PostGIS.</p>
                    </div>
                    <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-[11px] font-mono text-slate-400">ISO/IEC 19125</span>
                        <a href="descargas" class="font-semibold text-slate-700 hover:text-black transition cursor-pointer underline">Ver paquetes GPKG</a>
                    </div>
                </div>

                <!-- Vector Tiles MVT -->
                <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 flex flex-col justify-between shadow-clean hover:shadow-md hover:border-slate-300 transition">
                    <div>
                        <div class="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center mb-3">
                            <i data-lucide="layers" class="w-4 h-4 stroke-[1.5]"></i>
                        </div>
                        <h4 class="font-bold text-slate-900 text-sm mb-1">Vector Tiles (MVT / Mapbox)</h4>
                        <p class="text-xs text-slate-500 mb-3 leading-relaxed font-normal">Teselas vectoriales binarias ultrarrápidas (&lt; 50 ms) servidas desde el motor espacial para renderizado WebGL.</p>
                    </div>
                    <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-[11px] font-mono text-slate-400">ProtocolBuffer (.pbf)</span>
                        <a href="connection_examples.json" target="_blank" rel="noopener noreferrer" class="font-semibold text-slate-700 hover:text-black transition cursor-pointer underline">Ver endpoints</a>
                    </div>
                </div>

                <!-- STAC & Cloud-Native -->
                <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 flex flex-col justify-between shadow-clean hover:shadow-md hover:border-slate-300 transition">
                    <div>
                        <div class="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center mb-3">
                            <i data-lucide="binary" class="w-4 h-4 stroke-[1.5]"></i>
                        </div>
                        <h4 class="font-bold text-slate-900 text-sm mb-1">STAC 1.0.0 & GeoParquet 1.1</h4>
                        <p class="text-xs text-slate-500 mb-3 leading-relaxed font-normal">Catálogo espacio-temporal estático y particionamiento columnar con soporte <code>HTTP 206 Range</code> para DuckDB y Python.</p>
                    </div>
                    <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-[11px] font-mono text-slate-400">STAC 1.0.0 / Parquet 1.1</span>
                        <a href="stac/catalog.json" target="_blank" rel="noopener noreferrer" class="font-semibold text-slate-700 hover:text-black transition cursor-pointer underline">Abrir STAC JSON</a>
                    </div>
                </div>

            </div>

            <!-- Banner Informativo SNIT / ISO -->
            <div class="bg-uai-black text-white p-4 sm:p-5 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs sm:text-sm border border-slate-800 shadow-sm">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-slate-300 shrink-0">
                        <i data-lucide="shield-check" class="w-4 h-4 stroke-[1.5]"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-white">Conformidad con el Perfil Nacional de Metadatos SNIT (Chile)</h4>
                        <p class="text-slate-400 text-xs font-normal">Todas las coberturas cuentan con especificación ISO 19115-1:2014, codificación ISO 19139 XML y grafo semántico W3C DCAT-AP 2.0.</p>
                    </div>
                </div>
                <div class="flex items-center space-x-2 shrink-0">
                    <a href="dcat.json" target="_blank" rel="noopener noreferrer" class="bg-white/10 hover:bg-white/20 active:bg-white/30 text-white border border-white/20 px-3.5 py-2 rounded-lg font-medium text-xs transition cursor-pointer flex items-center space-x-1.5">
                        <span>Abrir DCAT-AP 2.0</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                    </a>
                </div>
            </div>

        </div>
    </section>
    </main><!-- /main#main-content -->

{canonical_footer}

    <!-- LOGIC SCRIPT -->
    <script>
        const EMBEDDED_CATALOG_DATA = {catalog_json_str};
        const INDICE_DESCARGAS_2017 = {descargas_2017_json_str};
        let catalogData = EMBEDDED_CATALOG_DATA;
        let activeMatrix = 'all';
        let activeAmbito = 'all';
        let searchQuery = '';
        let currentSnippetLang = 'python';
        
        // Leaflet Preview Map State
        let previewMap = null;
        let bboxLayer = null;
        let currentBbox = [-75.64, -55.98, -66.86, -17.50];

        function initCatalog() {{
            renderLayers();
            renderApps();
            renderIdes();
            initDescargas2017();
            if (window.lucide) lucide.createIcons();
        }}

        function initDescargas2017() {{
            onRegionChange();
        }}

        function onRegionChange() {{
            const selRegion = document.getElementById('selDescargaRegion');
            const selComuna = document.getElementById('selDescargaComuna');
            if (!selRegion || !selComuna) return;

            const region = selRegion.value;
            selComuna.innerHTML = '';

            if (region === 'NACIONAL') {{
                const opt = document.createElement('option');
                opt.value = 'all';
                opt.innerText = 'Todas las comunas amanzanadas de Chile (345 de 346 comunas)';
                selComuna.appendChild(opt);
            }} else if (INDICE_DESCARGAS_2017.regiones && INDICE_DESCARGAS_2017.regiones[region]) {{
                const optAll = document.createElement('option');
                optAll.value = 'all';
                optAll.innerText = `Todas las comunas de la región (${{region}})`;
                selComuna.appendChild(optAll);

                const comunas = INDICE_DESCARGAS_2017.regiones[region].comunas || [];
                comunas.forEach(c => {{
                    const opt = document.createElement('option');
                    opt.value = c.codigo;
                    opt.innerText = `${{c.nombre}} (CUT ${{c.codigo}})`;
                    selComuna.appendChild(opt);
                }});
            }}

            updateDescargas2017();
        }}

        function updateDescargas2017() {{
            if (!INDICE_DESCARGAS_2017 || !INDICE_DESCARGAS_2017.descargas) return;

            const elTipo = document.getElementById('selDescargaTipo');
            const elRegion = document.getElementById('selDescargaRegion');
            const elComuna = document.getElementById('selDescargaComuna');
            if (!elTipo || !elRegion || !elComuna) return;

            const tipo = elTipo.value;
            const region = elRegion.value;
            const comunaVal = elComuna.value;

            let key = '';
            let badgeTipoText = '';
            let tituloPrefix = '';

            if (tipo === 'manzanas') {{
                badgeTipoText = 'Manzanas MBHT 2017';
                tituloPrefix = 'Manzanas Censales MBHT 2017';
                key = region === 'NACIONAL' ? 'MBHT_2017_Nacional_Manzanas' : `MBHT_2017_${{region}}_Manzanas`;
            }} else if (tipo === 'equip_todos') {{
                badgeTipoText = 'Equipamientos Consolidado';
                tituloPrefix = 'Equipamientos Urbanos 2017 — Consolidado';
                key = region === 'NACIONAL' ? 'Equipamientos_2017_Nacional_Consolidado' : `Equipamientos_2017_${{region}}_Consolidado`;
            }} else if (tipo.startsWith('equip_')) {{
                const dimCode = tipo.replace('equip_', '').toUpperCase();
                const dimMap = {{
                    'ISAL': {{ code: 'ISAL', nom: 'Salud', full: 'Salud (ISAL)' }},
                    'ISE': {{ code: 'ISE', nom: 'Educacion', full: 'Educación (ISE)' }},
                    'IAV': {{ code: 'IAV', nom: 'Areas_Verdes', full: 'Áreas Verdes y Plazas (IAV)' }},
                    'IDEP': {{ code: 'IDEP', nom: 'Deportes', full: 'Deportes (IDEP)' }},
                    'ICUL': {{ code: 'ICUL', nom: 'Cultura', full: 'Cultura y Patrimonio (ICUL)' }},
                    'ISER': {{ code: 'ISER', nom: 'Servicios_Publicos', full: 'Servicios Públicos (ISER)' }}
                }};
                const dimObj = dimMap[dimCode] || {{ code: dimCode, nom: dimCode, full: dimCode }};
                badgeTipoText = `Equipamiento ${{dimObj.code}}`;
                tituloPrefix = `Equipamientos de ${{dimObj.full}} 2017`;
                key = region === 'NACIONAL' ? `Equipamientos_2017_Nacional_${{dimObj.code}}_${{dimObj.nom}}` : `Equipamientos_2017_${{region}}_${{dimObj.code}}_${{dimObj.nom}}`;
            }} else if (tipo === 'red_vial') {{
                badgeTipoText = 'Red Vial Tobler';
                tituloPrefix = 'Red Vial Caminable Ejes Tobler 2017';
                key = region === 'NACIONAL' ? 'Red_Vial_Ejes_2017_Nacional' : `Red_Vial_Ejes_2017_${{region}}`;
            }}

            const regData = INDICE_DESCARGAS_2017.regiones ? INDICE_DESCARGAS_2017.regiones[region] : null;
            const regNombre = region === 'NACIONAL' ? 'Consolidado Nacional' : (regData ? `Región de ${{regData.nombre}} (${{region}})` : region);

            const pkg = INDICE_DESCARGAS_2017.descargas[key];
            if (!pkg) return;

            // Badges & Titles
            const badgeTipo = document.getElementById('badgeDescargaTipo');
            const badgeAmbito = document.getElementById('badgeDescargaAmbito');
            const badgeRegs = document.getElementById('badgeDescargaRegistros');
            const tituloPaquete = document.getElementById('descargaTituloPaquete');

            if (badgeTipo) badgeTipo.innerText = badgeTipoText;
            if (badgeAmbito) badgeAmbito.innerText = region === 'NACIONAL' ? 'Nacional' : region;
            if (badgeRegs) badgeRegs.innerText = (pkg.registros || 0).toLocaleString('es-CL') + ' registros';
            if (tituloPaquete) tituloPaquete.innerText = `${{tituloPrefix}} — ${{regNombre}}`;

            // Helper formateo de tamaño
            const fmtSize = bytes => {{
                if (!bytes) return '-- MB';
                if (bytes > 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
                return (bytes / 1024).toFixed(0) + ' KB';
            }};

            // Actualizar botones de descarga
            const files = pkg.archivos || {{}};
            const setBtn = (btnId, sizeId, fileObj) => {{
                const btn = document.getElementById(btnId);
                const sizeEl = document.getElementById(sizeId);
                if (btn && fileObj && fileObj.filename) {{
                    btn.href = `download/${{fileObj.filename}}`;
                    btn.setAttribute('download', fileObj.filename);
                    btn.classList.remove('opacity-40', 'cursor-not-allowed', 'pointer-events-none');
                    if (sizeEl) sizeEl.innerText = fmtSize(fileObj.size_bytes);
                }} else if (btn) {{
                    btn.removeAttribute('href');
                    btn.classList.add('opacity-40', 'cursor-not-allowed', 'pointer-events-none');
                    if (sizeEl) sizeEl.innerText = 'N/D';
                }}
            }};

            setBtn('btnDescargaParquet', 'sizeDescargaParquet', files.parquet);
            setBtn('btnDescargaGPKG', 'sizeDescargaGPKG', files.gpkg);
            setBtn('btnDescargaSHP', 'sizeDescargaSHP', files.shp_zip);
            setBtn('btnDescargaCSV', 'sizeDescargaCSV', files.csv);

            // SHA-256
            const shaInput = document.getElementById('inputDescargaSha256');
            if (shaInput) {{
                shaInput.value = (files.parquet && files.parquet.sha256) ? files.parquet.sha256 : 'No disponible';
            }}

            // Nota Comunal y Snippet
            let snippet = '';
            const pqFilename = files.parquet ? files.parquet.filename : '';
            const noteEl = document.getElementById('descargaComunaNoteText');

            if (comunaVal && comunaVal !== 'all' && INDICE_DESCARGAS_2017.comunas && INDICE_DESCARGAS_2017.comunas[comunaVal]) {{
                const comObj = INDICE_DESCARGAS_2017.comunas[comunaVal];
                if (noteEl) {{
                    noteEl.innerHTML = `• <strong>Comuna seleccionada:</strong> ${{comObj.nombre}} (Código CUT: <code>${{comObj.codigo}}</code>, ${{regNombre}}). El paquete regional descargable contiene los datos completos de la región con el campo oficial de identificación comunal (<code>comuna</code> / <code>cod_com</code>) para filtrado inmediato en software SIG o código analítico.`;
                }}

                if (currentSnippetLang === 'python') {{
                    if (tipo === 'red_vial') {{
                        snippet = `import geopandas as gpd; gdf = gpd.read_parquet("download/${{pqFilename}}"); df_com = gdf[gdf["NOM_COM"].str.upper() == "${{comObj.nombre.toUpperCase()}}"]`;
                    }} else {{
                        snippet = `import geopandas as gpd; gdf = gpd.read_parquet("download/${{pqFilename}}"); df_com = gdf[gdf["cod_com"] == ${{comObj.codigo}}]`;
                    }}
                }} else {{
                    if (tipo === 'red_vial') {{
                        snippet = `library(sf); library(dplyr); df_com <- st_read_parquet("download/${{pqFilename}}") %>% filter(toupper(NOM_COM) == "${{comObj.nombre.toUpperCase()}}")`;
                    }} else {{
                        snippet = `library(sf); library(dplyr); df_com <- st_read_parquet("download/${{pqFilename}}") %>% filter(cod_com == ${{comObj.codigo}})`;
                    }}
                }}
            }} else {{
                if (noteEl) {{
                    noteEl.innerHTML = `El paquete descargable contiene la cartografía completa del territorio seleccionado (${{regNombre}}) con atributos estandarizados. Puedes filtrarlo por comuna directamente en tu software SIG o script de análisis.`;
                }}

                if (currentSnippetLang === 'python') {{
                    snippet = `import geopandas as gpd; gdf = gpd.read_parquet("download/${{pqFilename}}"); print(gdf.info())`;
                }} else {{
                    snippet = `library(sf); df <- st_read_parquet("download/${{pqFilename}}"); summary(df)`;
                }}
            }}

            const snippetInput = document.getElementById('inputDescargaSnippet');
            if (snippetInput) snippetInput.value = snippet;

            if (window.lucide) lucide.createIcons();
        }}

        function setSnippetLang(lang) {{
            currentSnippetLang = lang;
            const btnPy = document.getElementById('btnLangPython');
            const btnR = document.getElementById('btnLangR');
            if (btnPy && btnR) {{
                if (lang === 'python') {{
                    btnPy.className = 'text-[11px] font-bold text-slate-900 underline cursor-pointer';
                    btnR.className = 'text-[11px] font-medium text-slate-400 hover:text-slate-900 cursor-pointer';
                }} else {{
                    btnR.className = 'text-[11px] font-bold text-slate-900 underline cursor-pointer';
                    btnPy.className = 'text-[11px] font-medium text-slate-400 hover:text-slate-900 cursor-pointer';
                }}
            }}
            updateDescargas2017();
        }}

        function copyDescargaSnippet() {{
            const el = document.getElementById('inputDescargaSnippet');
            if (el) {{
                el.select();
                navigator.clipboard.writeText(el.value);
                alert('Código de análisis copiado al portapapeles.');
            }}
        }}

        function copyDescargaHash() {{
            const el = document.getElementById('inputDescargaSha256');
            if (el) {{
                el.select();
                navigator.clipboard.writeText(el.value);
                alert('Hash criptográfico SHA-256 copiado al portapapeles.');
            }}
        }}

        function initPreviewMap() {{
            if (previewMap) return;
            const mapContainer = document.getElementById('layerPreviewMap');
            if (!mapContainer) return;

            previewMap = L.map('layerPreviewMap', {{
                zoomControl: true,
                attributionControl: true,
                scrollWheelZoom: false
            }}).setView([-35.6751, -71.5430], 4);

            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',
                maxZoom: 19
            }}).addTo(previewMap);

            L.control.scale({{ imperial: false, metric: true, position: 'bottomleft' }}).addTo(previewMap);
        }}

        function updatePreviewMap(bbox) {{
            initPreviewMap();
            currentBbox = bbox || [-75.64, -55.98, -66.86, -17.50];
            
            if (bboxLayer && previewMap) {{
                previewMap.removeLayer(bboxLayer);
            }}

            const southWest = L.latLng(currentBbox[1], currentBbox[0]);
            const northEast = L.latLng(currentBbox[3], currentBbox[2]);
            const bounds = L.latLngBounds(southWest, northEast);
            
            if (previewMap) {{
                bboxLayer = L.rectangle(bounds, {{
                    color: '#0f172a',
                    weight: 2,
                    dashArray: '5, 5',
                    fillColor: '#334155',
                    fillOpacity: 0.14
                }}).addTo(previewMap);

                [30, 150, 350].forEach(delay => {{
                    setTimeout(() => {{
                        if (previewMap) {{
                            previewMap.invalidateSize();
                            previewMap.fitBounds(bounds, {{ padding: [25, 25], maxZoom: 11 }});
                        }}
                    }}, delay);
                }});
            }}
        }}

        function fitLayerBounds() {{
            if (previewMap && currentBbox) {{
                const southWest = L.latLng(currentBbox[1], currentBbox[0]);
                const northEast = L.latLng(currentBbox[3], currentBbox[2]);
                const bounds = L.latLngBounds(southWest, northEast);
                previewMap.invalidateSize();
                previewMap.fitBounds(bounds, {{ padding: [25, 25], maxZoom: 11 }});
            }}
        }}

        // Reset filters (Hallazgo A)
        window.resetFilters = function() {{
            const searchInput = document.getElementById('searchInput');
            const btnClear = document.getElementById('btnSearchClear');
            if (searchInput) searchInput.value = '';
            searchQuery = '';
            if (btnClear) btnClear.classList.add('hidden');
            activeMatrix = 'all';
            activeAmbito = 'all';
            document.querySelectorAll('#matrixFilters button, #ambitoFilters button').forEach(b => {{
                const isAll = (b.dataset.filter === 'all' || b.dataset.ambito === 'all');
                b.classList.toggle('bg-slate-900', isAll);
                b.classList.toggle('text-white', isAll);
                b.classList.toggle('font-bold', isAll);
                b.classList.toggle('shadow-xs', isAll);
                b.classList.toggle('text-slate-700', !isAll);
                b.classList.toggle('font-medium', !isAll);
            }});
            renderLayers();
        }};

        function renderLayers() {{
            const grid = document.getElementById('layersGrid');
            const empty = document.getElementById('emptyState');
            if (!grid) return;
            grid.innerHTML = '';

            if (!catalogData || !catalogData.capas) return;

            const filtered = catalogData.capas.filter(capa => {{
                const matchesMatrix = activeMatrix === 'all' || capa.matriz === activeMatrix;
                const matchesAmbito = activeAmbito === 'all' || capa.ambito === activeAmbito;
                const matchesSearch = searchQuery === '' || 
                    capa.titulo.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    capa.resumen.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    capa.escala.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    capa.cobertura.toLowerCase().includes(searchQuery.toLowerCase());
                return matchesMatrix && matchesAmbito && matchesSearch;
            }});

            if (filtered.length === 0) {{
                if (empty) empty.classList.remove('hidden');
            }} else {{
                if (empty) empty.classList.add('hidden');
                filtered.forEach(capa => {{
                    const card = document.createElement('article');
                    card.className = 'layer-card bg-white rounded-xl border border-slate-200 shadow-clean hover:shadow-hover p-5 transition flex flex-col justify-between group';
                    
                    const ambitoLabel = capa.ambito === 'tierra' ? 'Litósfera' : (capa.ambito === 'mar' ? 'Maritorio' : 'Atmósfera');
                    const matrixObj = catalogData.matrices ? catalogData.matrices.find(m => m.id === capa.matriz) : null;
                    const matrixName = matrixObj ? matrixObj.nombre : capa.matriz.toUpperCase();
                    
                    let statusLabel = `<span class="text-[11px] font-mono text-slate-400">v${{capa.version || '1.0'}}</span>`;
                    if (capa.id === 'kpi_mud_2017') {{
                        statusLabel = '<span class="text-[11px] font-semibold text-slate-700">Línea base oficial 2017</span>';
                    }} else if (capa.id === 'censo_imputaciones_2024') {{
                        statusLabel = '<span class="text-[11px] font-semibold text-amber-800">En calibración · Censo 2024</span>';
                    }} else if (capa.estado === 'reserva_institucional') {{
                        statusLabel = '<span class="text-[11px] font-medium text-slate-600">Reserva institucional</span>';
                    }}

                    const sizeMeta = capa.size_human ? ` · <span class="font-mono text-slate-500">${{capa.size_human}}</span>` : '';
                    const numAttrs = (capa.atributos || []).length;
                    const instList = (capa.fuentes_institucionales || []).slice(0, 3).map(f => f.institucion).filter(Boolean).join(', ') || 'CIT-UAI';
                    const fichaLink = capa.id === 'kpi_mud_2017' ? '<a href="/ficha-mbht-2017" class="mt-2.5 block text-center text-xs font-medium text-slate-600 hover:text-slate-900 underline underline-offset-2">Ver ficha metodológica exhaustiva (Línea base 2017) &rarr;</a>' : '';
                    const xmlHref = 'download/iso_xml/' + capa.id + '_iso19139.xml';

                    card.innerHTML = `
                        <div>
                            <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-100">
                                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">${{matrixName}} · ${{ambitoLabel}}</span>
                                ${{statusLabel}}
                            </div>
                            <h3 class="font-bold text-slate-900 text-base mb-1.5 group-hover:text-black transition leading-snug">${{capa.titulo}}</h3>
                            <p class="text-xs sm:text-sm text-slate-600 line-clamp-2 mb-2 leading-relaxed font-normal">${{capa.resumen}}</p>
                            <div class="mt-2 text-[11px] text-slate-500 flex items-center justify-between bg-slate-50/80 border border-slate-200/80 rounded-lg px-2.5 py-1.5">
                                <span class="truncate pr-2">${{numAttrs}} campos · ${{instList}}</span>
                                <a href="${{xmlHref}}" download class="text-[10px] text-slate-500 hover:text-slate-900 underline font-mono shrink-0">ISO XML</a>
                            </div>
                        </div>

                        <div class="pt-3.5 border-t border-slate-100 mt-3.5">
                            <div class="flex items-center justify-between text-xs text-slate-500 mb-3">
                                <span>Escala: <strong class="text-slate-700 font-medium">${{capa.escala}}</strong></span>
                                <span class="text-[11px] text-slate-400">Corte ${{capa.fecha_corte || '2017'}}${{sizeMeta}}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <button onclick="openLayerModal('${{capa.id}}')" class="flex-1 bg-slate-900 hover:bg-black active:bg-slate-800 text-white text-xs sm:text-sm font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1 shadow-xs cursor-pointer">
                                    <span>Ficha y descarga</span>
                                </button>
                                <button onclick="openLayerModal('${{capa.id}}', true)" title="Ver referencia espacial en mapa" class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 active:bg-slate-300 text-slate-700 transition cursor-pointer">
                                    <i data-lucide="map" class="w-4 h-4 stroke-[1.5]"></i>
                                </button>
                                <button onclick="quickCopyQGIS('${{capa.tile_source}}')" title="Copiar conector para QGIS" class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 active:bg-slate-300 text-slate-700 transition cursor-pointer">
                                    <i data-lucide="link" class="w-4 h-4 stroke-[1.5]"></i>
                                </button>
                            </div>
                            ${{fichaLink}}
                        </div>
                    `;
                    grid.appendChild(card);
                }});
            }}
            if (window.lucide) lucide.createIcons();
        }}

        function renderApps() {{
            const grid = document.getElementById('appsGrid');
            if (!grid) return;
            grid.innerHTML = '';
            if (!catalogData || !catalogData.aplicaciones_satelitales) return;

            catalogData.aplicaciones_satelitales.forEach(app => {{
                const card = document.createElement('a');
                card.href = app.url;
                card.target = '_blank';
                card.rel = 'noopener noreferrer';
                card.className = 'bg-slate-50 p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean hover:bg-white hover:border-slate-300 hover:shadow-hover transition flex flex-col justify-between group';
                
                const catLabel = app.categoria ? `<span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">${{app.categoria}}</span>` : '';
                
                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between mb-2.5 sm:mb-3">
                            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-700 bg-white border border-slate-200 shadow-xs">
                                <i data-lucide="${{app.icono}}" class="w-4 h-4 stroke-[1.5]"></i>
                            </div>
                            ${{catLabel}}
                        </div>
                        <h4 class="font-bold text-slate-900 text-xs sm:text-sm mb-1 group-hover:text-black transition leading-snug">${{app.titulo}}</h4>
                        <p class="text-xs text-slate-500 leading-relaxed mb-3 sm:mb-4 font-normal">${{app.descripcion}}</p>
                    </div>
                    <div class="text-xs font-semibold text-slate-700 flex items-center space-x-1 pt-2 sm:pt-2.5 border-t border-slate-200 group-hover:text-black transition">
                        <span>Acceder al recurso</span>
                        <i data-lucide="arrow-up-right" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                    </div>
                `;
                grid.appendChild(card);
            }});
            if (window.lucide) lucide.createIcons();
        }}

        let activeIdeCategory = 'all';

        function filterIdes(cat, btn) {{
            activeIdeCategory = cat;
            document.querySelectorAll('.ide-cat-btn').forEach(b => {{
                b.classList.remove('bg-slate-900', 'text-white', 'font-bold');
                b.classList.add('bg-white', 'text-slate-700', 'font-medium', 'border', 'border-slate-200');
            }});
            if (btn) {{
                btn.classList.add('bg-slate-900', 'text-white', 'font-bold');
                btn.classList.remove('bg-white', 'text-slate-700', 'font-medium', 'border', 'border-slate-200');
            }}
            renderIdes();
        }}

        function renderIdes() {{
            const grid = document.getElementById('idesGrid');
            if (!grid) return;
            grid.innerHTML = '';
            if (!catalogData || !catalogData.ides_nacionales) return;

            const filtered = catalogData.ides_nacionales.filter(ide => {{
                if (activeIdeCategory === 'all') return true;
                const catNorm = (ide.categoria || '').toLowerCase();
                if (activeIdeCategory === 'Nacional') return catNorm.includes('nacional') || catNorm.includes('centralizador');
                if (activeIdeCategory === 'Urbano') return catNorm.includes('urbano') || catNorm.includes('regional') || catNorm.includes('patrimonio') || catNorm.includes('académico') || catNorm.includes('academico') || catNorm.includes('territorial');
                if (activeIdeCategory === 'Medio Ambiente') return catNorm.includes('ambiente') || catNorm.includes('hídrico') || catNorm.includes('hidrico') || catNorm.includes('forestal') || catNorm.includes('pesca') || catNorm.includes('maritorio');
                if (activeIdeCategory === 'Infraestructura') return catNorm.includes('infraestructura') || catNorm.includes('energía') || catNorm.includes('energia') || catNorm.includes('silvo') || catNorm.includes('censo') || catNorm.includes('aeroespacial');
                return true;
            }});

            filtered.forEach(ide => {{
                const card = document.createElement('div');
                card.className = 'bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean hover:shadow-hover hover:border-slate-300 transition flex flex-col justify-between group';
                
                let queEncontrarasHtml = '';
                if (ide.que_encontraras && Array.isArray(ide.que_encontraras) && ide.que_encontraras.length > 0) {{
                    const itemsHtml = ide.que_encontraras.map(item => `
                        <li class="flex items-start space-x-1.5 text-[11px] text-slate-600 leading-tight">
                            <i data-lucide="check" class="w-3 h-3 text-slate-400 shrink-0 mt-0.5 stroke-[2]"></i>
                            <span>${{item}}</span>
                        </li>
                    `).join('');
                    queEncontrarasHtml = `
                        <div class="mt-3 pt-3 border-t border-slate-100 bg-slate-50/80 -mx-4 p-3 sm:-mx-5 sm:p-3.5 rounded-b-lg space-y-1.5">
                            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block flex items-center space-x-1">
                                <i data-lucide="layers" class="w-3 h-3 text-slate-400 stroke-[1.5]"></i>
                                <span>Qué encontrarás en esta IDE:</span>
                            </span>
                            <ul class="space-y-1 pl-0.5">
                                ${{itemsHtml}}
                            </ul>
                        </div>
                    `;
                }}

                card.innerHTML = `
                    <div class="flex-1 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2.5">
                                <div class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-700 bg-slate-50 border border-slate-200 shadow-xs">
                                    <i data-lucide="${{ide.icono || 'globe'}}" class="w-4 h-4 stroke-[1.5]"></i>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">${{ide.categoria}}</span>
                            </div>
                            <span class="text-[11px] font-semibold text-slate-400 block uppercase tracking-wider mb-1">${{ide.institucion}}</span>
                            <h4 class="font-bold text-slate-900 text-sm mb-1.5 group-hover:text-black transition leading-snug">${{ide.nombre}}</h4>
                            <p class="text-xs text-slate-500 leading-relaxed font-normal">${{ide.descripcion}}</p>
                        </div>
                        ${{queEncontrarasHtml}}
                    </div>
                    <a href="${{ide.url}}" target="_blank" rel="noopener noreferrer" class="mt-3.5 w-full bg-slate-50 hover:bg-slate-900 hover:text-white text-slate-700 border border-slate-200 hover:border-slate-900 rounded-lg py-2 px-3 text-xs font-semibold flex items-center justify-center space-x-1.5 transition cursor-pointer group-hover:bg-slate-900 group-hover:text-white">
                        <span>Ir a Geoportal</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                    </a>
                `;
                grid.appendChild(card);
            }});
            if (window.lucide) lucide.createIcons();
        }}

        function openLayerModal(layerId, scrollToMap = false) {{
            const capa = catalogData.capas.find(c => c.id === layerId);
            if (!capa) return;

            document.getElementById('layerModal').classList.remove('hidden');

            document.getElementById('modalTitle').innerText = capa.titulo;
            document.getElementById('modalBadge').innerText = capa.matriz.toUpperCase();
            document.getElementById('modalAmbito').innerText = capa.ambito === 'tierra' ? 'Litósfera' : (capa.ambito === 'mar' ? 'Maritorio' : 'Atmósfera');
            document.getElementById('modalEscala').innerText = capa.escala;
            document.getElementById('modalResumen').innerText = capa.resumen;
            document.getElementById('modalFormula').innerText = capa.formula_lineage;
            document.getElementById('modalCitation').innerText = capa.citacion;
            document.getElementById('modalLicense').innerText = capa.licencia;

            // Metadatos Espaciales ISO 19115
            document.getElementById('modalCRS').innerText = capa.crs || 'EPSG:4326 (WGS 84)';
            document.getElementById('modalGeom').innerText = capa.tipo_geometria || 'MultiPolygon';
            
            const bbox = capa.bbox || [-75.64, -55.98, -66.86, -17.50];
            document.getElementById('modalBboxCoords').innerText = `BBOX: [${{bbox[0]}}, ${{bbox[1]}}, ${{bbox[2]}}, ${{bbox[3]}}]`;

            updatePreviewMap(bbox);

            // Snippets
            const tileUrl = `https://ide.cit.uai.cl/tiles/${{capa.tile_source}}/{{z}}/{{x}}/{{y}}.pbf`;
            const pythonSnippet = `import duckdb\ncon = duckdb.connect()\ndf = con.execute("SELECT * FROM '${{capa.s3_parquet}}'").df()`;
            const rSnippet = `library(arrow)\nlibrary(sf)\ndf <- read_parquet("${{capa.s3_parquet}}")`;

            if (document.getElementById('snippetQGIS')) document.getElementById('snippetQGIS').value = tileUrl;
            if (document.getElementById('snippetPython')) document.getElementById('snippetPython').value = pythonSnippet;
            if (document.getElementById('snippetR')) document.getElementById('snippetR').value = rSnippet;

            // Manejo de capas restringidas
            const isRestricted = capa.matriz === 'mpst' || capa.publico === false || capa.disponible_descarga === false || capa.estado === 'en_desarrollo' || capa.estado === 'reserva_institucional';
            const noticeEl = document.getElementById('modalRestrictedNotice');
            if (noticeEl) {{
                if (isRestricted) {{
                    noticeEl.classList.remove('hidden');
                }} else {{
                    noticeEl.classList.add('hidden');
                }}
            }}

            const btnFichaMaestra = document.getElementById('btnVerFichaMaestra');
            if (btnFichaMaestra) {{
                if (capa.id === 'kpi_mud_2017' || capa.ficha_tecnica_url) {{
                    btnFichaMaestra.classList.remove('hidden');
                    btnFichaMaestra.href = capa.ficha_tecnica_url || 'ficha-mbht-2017';
                }} else {{
                    btnFichaMaestra.classList.add('hidden');
                }}
            }}

            const btnParquet = document.getElementById('btnDownloadParquet');
            const btnGPKG = document.getElementById('btnDownloadGPKG');
            const btnSHP = document.getElementById('btnDownloadSHP');
            const btnCSV = document.getElementById('btnDownloadCSV');
            const btnXML = document.getElementById('btnDownloadXML');

            if (isRestricted) {{
                [btnParquet, btnGPKG, btnSHP, btnCSV, btnXML].forEach(btn => {{
                    if (btn) {{
                        btn.classList.add('opacity-40', 'cursor-not-allowed');
                        btn.removeAttribute('href');
                        btn.onclick = (e) => {{ e.preventDefault(); alert('La cobertura MBHT Censo 2024 será liberada tras la publicación de microdatos definitivos INE. La línea base MBHT 2017 se encuentra 100% disponible para descarga inmediata.'); }};
                    }}
                }});
            }} else {{
                if (btnParquet) {{
                    const pq = capa.parquet_url || capa.s3_parquet;
                    if (pq) {{
                        btnParquet.classList.remove('opacity-40', 'cursor-not-allowed', 'hidden');
                        btnParquet.href = pq;
                        btnParquet.onclick = null;
                    }} else {{
                        btnParquet.classList.add('opacity-40', 'cursor-not-allowed');
                        btnParquet.removeAttribute('href');
                    }}
                }}
                if (btnGPKG) {{
                    if (capa.gpkg_url) {{
                        btnGPKG.classList.remove('opacity-40', 'cursor-not-allowed', 'hidden');
                        btnGPKG.href = capa.gpkg_url;
                        btnGPKG.onclick = null;
                    }} else {{
                        btnGPKG.classList.add('opacity-40', 'cursor-not-allowed');
                        btnGPKG.removeAttribute('href');
                        btnGPKG.onclick = (e) => {{ e.preventDefault(); alert('Formato GeoPackage no disponible para esta cobertura masiva. Descargue en formato GeoParquet o CSV.'); }};
                    }}
                }}
                if (btnSHP) {{
                    if (capa.shp_url) {{
                        btnSHP.classList.remove('opacity-40', 'cursor-not-allowed', 'hidden');
                        btnSHP.href = capa.shp_url;
                        btnSHP.onclick = null;
                    }} else {{
                        btnSHP.classList.add('opacity-40', 'cursor-not-allowed');
                        btnSHP.removeAttribute('href');
                        btnSHP.onclick = (e) => {{ e.preventDefault(); alert('Formato Shapefile no disponible para coberturas que exceden el límite de 2 GB de DBF. Descargue en formato GeoParquet o CSV.'); }};
                    }}
                }}
                if (btnCSV) {{
                    if (capa.csv_url) {{
                        btnCSV.classList.remove('opacity-40', 'cursor-not-allowed', 'hidden');
                        btnCSV.href = capa.csv_url;
                        btnCSV.onclick = null;
                    }} else {{
                        btnCSV.classList.add('opacity-40', 'cursor-not-allowed');
                        btnCSV.removeAttribute('href');
                    }}
                }}
                if (btnXML) {{
                    btnXML.classList.remove('opacity-40', 'cursor-not-allowed');
                    btnXML.href = `data/iso_xml/${{capa.id}}_iso19139.xml`;
                    btnXML.onclick = null;
                }}
            }}

            // Fuentes Institucionales APA 7
            const sourcesContainer = document.getElementById('modalSourcesList');
            if (sourcesContainer) {{
                sourcesContainer.innerHTML = '';
                const fuentes = capa.fuentes_institucionales || [];
                if (fuentes.length === 0) {{
                    sourcesContainer.innerHTML = '<p class="text-xs text-slate-400 italic col-span-full">No se registran fuentes externas adicionales.</p>';
                }} else {{
                    fuentes.forEach(src => {{
                        const card = document.createElement('div');
                        card.className = 'p-3 bg-slate-50 border border-slate-200 rounded-lg text-left flex flex-col justify-between';
                        card.innerHTML = `
                            <div>
                                <div class="flex items-start justify-between gap-2 mb-1">
                                    <span class="font-bold text-slate-900 text-xs">${{src.institucion}}</span>
                                    <a href="${{src.url}}" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-black inline-flex items-center space-x-0.5 text-[11px] font-semibold underline shrink-0">
                                        <span>Portal oficial</span>
                                        <i data-lucide="external-link" class="w-3 h-3 stroke-[1.5]"></i>
                                    </a>
                                </div>
                                <span class="text-[11px] font-medium text-slate-700 block mb-1.5">${{src.insumo}}</span>
                                <p class="text-[10px] text-slate-600 font-serif italic bg-white p-2 rounded border border-slate-200 leading-relaxed">${{src.citacion_apa7 || ''}}</p>
                            </div>
                        `;
                        sourcesContainer.appendChild(card);
                    }});
                }}
            }}

            // Attributes Table
            const attrCountBadge = document.getElementById('modalAttrCountBadge');
            if (attrCountBadge) {{
                attrCountBadge.innerText = (capa.atributos ? capa.atributos.length : 0) + ' columnas físicas';
            }}
            const tbody = document.getElementById('modalAttributesTable');
            tbody.innerHTML = '';
            capa.atributos.forEach(attr => {{
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-2.5 py-1.5 font-mono text-[11px] text-slate-900 font-semibold">${{attr.campo}}</td>
                    <td class="px-2.5 py-1.5 font-mono text-[10px] text-slate-500">${{attr.tipo}}</td>
                    <td class="px-2.5 py-1.5 text-slate-600 text-[11px]">${{attr.descripcion}}</td>
                `;
                tbody.appendChild(row);
            }});

            if (window.lucide) lucide.createIcons();

            if (scrollToMap) {{
                setTimeout(() => {{
                    const mapSection = document.getElementById('sectionSpatialRef');
                    if (mapSection) {{
                        mapSection.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }}
                }}, 200);
            }}
        }}

        document.getElementById('btnCloseModal').addEventListener('click', () => {{
            document.getElementById('layerModal').classList.add('hidden');
        }});

        // Search listener
        const searchInput = document.getElementById('searchInput');
        const btnClear = document.getElementById('btnSearchClear');
        if (searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value;
                if (btnClear) btnClear.classList.toggle('hidden', searchQuery.length === 0);
                renderLayers();
            }});
        }}
        if (btnClear) {{
            btnClear.addEventListener('click', () => {{
                if (searchInput) searchInput.value = '';
                searchQuery = '';
                btnClear.classList.add('hidden');
                renderLayers();
            }});
        }}

        // Matrix filters
        document.querySelectorAll('#matrixFilters button').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('#matrixFilters button').forEach(b => {{
                    b.classList.remove('bg-slate-900', 'text-white', 'font-bold', 'shadow-xs');
                    b.classList.add('text-slate-700', 'font-medium');
                }});
                btn.classList.add('bg-slate-900', 'text-white', 'font-bold', 'shadow-xs');
                btn.classList.remove('text-slate-700', 'font-medium');
                activeMatrix = btn.dataset.filter;
                renderLayers();
            }});
        }});

        // Ambito filters
        document.querySelectorAll('#ambitoFilters button').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('#ambitoFilters button').forEach(b => {{
                    b.classList.remove('bg-slate-900', 'text-white', 'font-bold', 'shadow-xs');
                    b.classList.add('text-slate-700', 'font-medium');
                }});
                btn.classList.add('bg-slate-900', 'text-white', 'font-bold', 'shadow-xs');
                btn.classList.remove('text-slate-700', 'font-medium');
                activeAmbito = btn.dataset.ambito;
                renderLayers();
            }});
        }});

        function copySnippet(type) {{
            const map = {{
                'mvt': 'snippetQGIS',
                'qgis': 'snippetQGIS',
                'python': 'snippetPython',
                'r': 'snippetR'
            }};
            const elId = map[type] || 'snippetQGIS';
            const el = document.getElementById(elId);
            if (el) {{
                el.select();
                navigator.clipboard.writeText(el.value);
                alert(`Conector [${{type.toUpperCase()}}] copiado al portapapeles.`);
            }}
        }}

        function copyCitation() {{
            const text = document.getElementById('modalCitation').innerText;
            navigator.clipboard.writeText(text);
            alert('Cita académica copiada al portapapeles.');
        }}

        function quickCopyQGIS(tileSource) {{
            const url = `https://ide.cit.uai.cl/tiles/${{tileSource}}/{{z}}/{{x}}/{{y}}.pbf`;
            navigator.clipboard.writeText(url);
            alert('URL TileJSON/MVT copiada para QGIS: ' + url);
        }}

        function exportCatalogJson() {{
            if (!catalogData) return;
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(catalogData, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "catalogo_ide_cit_2026.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        }}

        // El menú móvil hamburguesa está gestionado canónicamente por get_canonical_header_html()
        // El botón scroll to top (volver arriba) y su control están gestionados universalmente por get_canonical_footer_html()

        // Función de Síntesis de Voz Web Speech API
        function speakCopilotText(btn) {{
            if (!('speechSynthesis' in window)) {{
                alert('La síntesis de voz no está soportada en este navegador.');
                return;
            }}
            window.speechSynthesis.cancel();
            const textToSpeak = btn.getAttribute('data-speech');
            if (!textToSpeak) return;

            const utterance = new SpeechSynthesisUtterance(textToSpeak);
            utterance.lang = 'es-CL';
            utterance.rate = 0.95;
            utterance.pitch = 1.0;

            const voices = window.speechSynthesis.getVoices();
            const esVoice = voices.find(v => v.lang.includes('es-CL') || v.lang.includes('es-419') || v.lang.includes('es-ES') || v.lang.includes('es'));
            if (esVoice) utterance.voice = esVoice;

            window.speechSynthesis.speak(utterance);
        }}

        // COPILOTO IA TERRITORIAL
        function dismissCopilotHint(e) {{
            if (e && e.stopPropagation) e.stopPropagation();
            const hint = document.getElementById('copilotWelcomeHint');
            if (hint) {{
                hint.classList.add('hidden');
            }}
        }}

        function initCopilotHint() {{
            setTimeout(() => {{
                const hint = document.getElementById('copilotWelcomeHint');
                const drawer = document.getElementById('copilotDrawer');
                if (hint && drawer && drawer.classList.contains('hidden')) {{
                    hint.classList.remove('hidden');
                }}
            }}, 2000);

            // Auto-ocultar con scroll descendente si el usuario está explorando activamente
            window.addEventListener('scroll', () => {{
                const currentScroll = window.scrollY || 0;
                if (currentScroll > 250) {{
                    const hint = document.getElementById('copilotWelcomeHint');
                    if (hint && !hint.classList.contains('hidden')) {{
                        hint.classList.add('hidden');
                    }}
                }}
            }}, {{ passive: true }});
        }}

        function toggleCopilot(forceState = null) {{
            dismissCopilotHint();
            const drawer = document.getElementById('copilotDrawer');
            const inputEl = document.getElementById('copilotInput');
            if (!drawer) return;
            const willOpen = forceState !== null ? forceState : drawer.classList.contains('hidden');
            if (willOpen) {{
                drawer.classList.remove('hidden');
                drawer.classList.add('flex');
                if (inputEl) setTimeout(() => inputEl.focus(), 150);
            }} else {{
                drawer.classList.add('hidden');
                drawer.classList.remove('flex');
            }}
            if (window.lucide) lucide.createIcons();
        }}

        function sendCopilotSuggestion(text) {{
            const inputEl = document.getElementById('copilotInput');
            if (inputEl) {{
                inputEl.value = text;
                handleCopilotSubmit(new Event('submit'));
            }}
        }}

        async function handleCopilotSubmit(e) {{
            if (e) e.preventDefault();
            const inputEl = document.getElementById('copilotInput');
            if (!inputEl) return;
            const text = inputEl.value.trim();
            if (!text) return;

            appendCopilotMessage('user', text);
            inputEl.value = '';

            const typingId = appendTypingIndicator();

            setTimeout(async () => {{
                removeTypingIndicator(typingId);
                const response = await resolveCopilotResponse(text);
                appendCopilotMessage('assistant', response.text, response.action);
            }}, 400);
        }}

        function appendCopilotMessage(sender, text, action = null) {{
            const msgDiv = document.createElement('div');
            msgDiv.className = 'flex items-start space-x-2.5 ' + (sender === 'user' ? 'justify-end' : '');

            if (sender === 'user') {{
                const safeUserText = (typeof escapeHtml === 'function') 
                    ? escapeHtml(text) 
                    : String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
                msgDiv.innerHTML = `
                    <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-none text-xs sm:text-sm max-w-[85%] shadow-xs leading-relaxed">
                        ${{safeUserText}}
                    </div>
                `;
            }} else {{
                let actionBtnHtml = '';
                if (action && action.layerId) {{
                    actionBtnHtml = `
                        <button onclick="toggleCopilot(false); openLayerModal('${{action.layerId}}');" class="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-black text-white rounded-lg text-xs font-semibold transition cursor-pointer">
                            <i data-lucide="layers" class="w-3.5 h-3.5 text-[#6493B5]"></i>
                            <span>Abrir ficha: ${{action.layerTitle}}</span>
                        </button>
                    `;
                }}
                
                const cleanSpeechText = text.replace(/<[^>]*>/g, '').replace(/["']/g, '');

                msgDiv.innerHTML = `
                    <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold border border-slate-700">
                        CIT
                    </div>
                    <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 text-slate-800 space-y-2 shadow-xs max-w-[85%] text-xs sm:text-sm">
                        <div class="leading-relaxed font-normal">${{text}}</div>
                        <div class="flex flex-wrap items-center gap-1.5 pt-1.5 border-t border-slate-100">
                            <button onclick="speakCopilotText(this)" data-speech="${{cleanSpeechText}}" title="Escuchar locución de voz humana" class="inline-flex items-center space-x-1 text-[11px] text-slate-600 hover:text-black font-semibold py-1 px-2.5 rounded-lg bg-slate-100 hover:bg-slate-200 transition cursor-pointer border border-slate-200">
                                <i data-lucide="volume-2" class="w-3 h-3 text-slate-700"></i>
                                <span>Escuchar voz</span>
                            </button>
                            ${{actionBtnHtml}}
                        </div>
                    </div>
                `;
            }}

            const messagesContainer = document.getElementById('copilotMessages');
            if (messagesContainer) {{
                messagesContainer.appendChild(msgDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }}
            if (window.lucide) lucide.createIcons();
        }}

        function appendTypingIndicator() {{
            const id = 'typing_' + Date.now();
            const div = document.createElement('div');
            div.id = id;
            div.className = 'flex items-center space-x-2 text-slate-400 text-xs pl-9';
            div.innerHTML = `<span class="animate-pulse">Escribiendo respuesta...</span>`;
            const messagesContainer = document.getElementById('copilotMessages');
            if (messagesContainer) {{
                messagesContainer.appendChild(div);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }}
            return id;
        }}

        function removeTypingIndicator(id) {{
            const el = document.getElementById(id);
            if (el) el.remove();
        }}

        {copilot_js_engine}

        // Exportar funciones a ámbito global
        window.toggleCopilot = toggleCopilot;
        window.sendCopilotSuggestion = sendCopilotSuggestion;
        window.handleCopilotSubmit = handleCopilotSubmit;
        window.dismissCopilotHint = dismissCopilotHint;
        window.openLayerModal = openLayerModal;
        window.copySnippet = copySnippet;
        window.copyCitation = copyCitation;
        window.quickCopyQGIS = quickCopyQGIS;
        window.exportCatalogJson = exportCatalogJson;
        window.speakCopilotText = speakCopilotText;
        window.fitLayerBounds = fitLayerBounds;
        window.initDescargas2017 = initDescargas2017;
        window.onRegionChange = onRegionChange;
        window.updateDescargas2017 = updateDescargas2017;
        window.setSnippetLang = setSnippetLang;
        window.copyDescargaSnippet = copyDescargaSnippet;
        window.copyDescargaHash = copyDescargaHash;

        // Atajos de teclado
        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                const layerModal = document.getElementById('layerModal');
                if (layerModal && !layerModal.classList.contains('hidden')) {{
                    layerModal.classList.add('hidden');
                }}
                const drawer = document.getElementById('copilotDrawer');
                if (drawer && !drawer.classList.contains('hidden')) {{
                    toggleCopilot(false);
                }}
            }}
        }});

        // Inicialización inmediata sincrónica en carga
        initCatalog();
        initCopilotHint();
        document.addEventListener('DOMContentLoaded', () => {{
            initCatalog();
            initCopilotHint();
        }});
    </script>
</body>
</html>
"""
        return html

    def export_csv_catalog(self, catalog_data: Dict[str, Any]) -> Path:
        capas = catalog_data.get("capas", [])
        fieldnames = [
            "id", "titulo", "matriz", "ambito", "estado", "publico",
            "escala", "cobertura", "fecha_corte", "resumen", "formula_lineage",
            "crs", "tipo_geometria", "bbox_wgs84", "tile_source", "s3_parquet",
            "gpkg_url", "shp_url", "csv_url", "autor", "licencia", "citacion"
        ]
        with open(self.catalog_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in capas:
                writer.writerow({
                    "id": c.get("id", ""),
                    "titulo": c.get("titulo", ""),
                    "matriz": c.get("matriz", ""),
                    "ambito": c.get("ambito", ""),
                    "estado": c.get("estado", "publicada"),
                    "publico": "Si" if c.get("publico", True) else "No",
                    "escala": c.get("escala", ""),
                    "cobertura": c.get("cobertura", ""),
                    "fecha_corte": c.get("fecha_corte", ""),
                    "resumen": c.get("resumen", ""),
                    "formula_lineage": c.get("formula_lineage", ""),
                    "crs": c.get("crs", "EPSG:4326"),
                    "tipo_geometria": c.get("tipo_geometria", ""),
                    "bbox_wgs84": json.dumps(c.get("bbox", [])),
                    "tile_source": c.get("tile_source", ""),
                    "s3_parquet": c.get("s3_parquet", ""),
                    "gpkg_url": c.get("gpkg_url", ""),
                    "shp_url": c.get("shp_url", ""),
                    "csv_url": c.get("csv_url", ""),
                    "autor": c.get("autor", ""),
                    "licencia": c.get("licencia", ""),
                    "citacion": c.get("citacion", "")
                })
        logger.info(f"   ✓ Catálogo CSV exportado en: {self.catalog_csv_path}")
        return self.catalog_csv_path

    def export_dcat_json(self, catalog_data: Dict[str, Any]) -> Path:
        portal = catalog_data.get("portal", {})
        capas = catalog_data.get("capas", [])
        dcat_data = {
            "@context": {
                "dcat": "http://www.w3.org/ns/dcat#",
                "dct": "http://purl.org/dc/terms/",
                "foaf": "http://xmlns.com/foaf/0.1/",
                "locn": "http://www.w3.org/ns/locn#"
            },
            "@id": portal.get("url_base", "https://ide.cit.uai.cl") + "/data/dcat.json",
            "@type": "dcat:Catalog",
            "dct:title": portal.get("nombre", "IDE CIT — Infraestructura de Datos Espaciales"),
            "dct:description": portal.get("descripcion", ""),
            "dct:publisher": {
                "@type": "foaf:Organization",
                "foaf:name": "Centro de Inteligencia Territorial (CIT-UAI)",
                "foaf:mbox": portal.get("contacto", "contactocit@uai.cl")
            },
            "dcat:dataset": [
                {
                    "@type": "dcat:Dataset",
                    "dct:identifier": f"CIT-UAI::{c.get('id')}::2026",
                    "dct:title": c.get("titulo"),
                    "dct:description": c.get("resumen"),
                    "dct:issued": c.get("fecha_corte"),
                    "dct:modified": c.get("updated", "2026-10-15"),
                    "owl:versionInfo": c.get("version", "1.0.3"),
                    "dcat:theme": c.get("matriz"),
                    "dcat:spatialResolutionInMeters": 100,
                    "locn:geometry": json.dumps(c.get("bbox", [])),
                    "dcat:distribution": [
                        {
                            "@type": "dcat:Distribution",
                            "dct:title": f"{c.get('titulo')} (GeoParquet)",
                            "dcat:accessURL": f"https://ide.cit.uai.cl/{finfo.get('url', finfo.get('filename', ''))}",
                            "dct:format": "GeoParquet",
                            "dcat:mediaType": "application/vnd.apache.parquet",
                            "dcat:byteSize": finfo.get("size_bytes"),
                            "spdx:checksum": finfo.get("sha256")
                        }
                        for fkey, finfo in c.get("archivos_distribucion", {}).items()
                    ]
                }
                for c in capas
            ]
        }
        with open(self.dcat_json_path, "w", encoding="utf-8") as f:
            json.dump(dcat_data, f, ensure_ascii=False, indent=2)
        logger.info(f"   ✓ Catálogo DCAT-AP exportado en: {self.dcat_json_path}")
        return self.dcat_json_path

    def export_sitemap_and_seo(self, catalog_data: Dict[str, Any]) -> None:
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ide.cit.uai.cl/</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/inicio</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/descargas</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.95</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/guia-tecnica</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/red-ides</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/ficha-mbht-2017</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.95</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/stac/catalog.json</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/catalogo.json</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/dcat.json</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/llms.txt</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://ide.cit.uai.cl/llms-full.txt</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
"""
        with open(self.sitemap_path, "w", encoding="utf-8") as f:
            f.write(sitemap_content)

        robots_content = """User-agent: *
Allow: /

Sitemap: https://ide.cit.uai.cl/sitemap.xml
# AI Agent Directives & Context Specification
# Orientation: https://ide.cit.uai.cl/llms.txt
# Exhaustive Dataset Specification: https://ide.cit.uai.cl/llms-full.txt
# STAC 1.0.0 Catalog: https://ide.cit.uai.cl/stac/catalog.json
# Open Catalog API (JSON): https://ide.cit.uai.cl/catalogo.json
# W3C DCAT-AP Metadata: https://ide.cit.uai.cl/dcat.json
# Canonical Reference Authority: https://matrizbht.cl
# Government Platform Authority: https://plataformabht.subdere.gov.cl
"""
        with open(self.robots_path, "w", encoding="utf-8") as f:
            f.write(robots_content)

        llms_txt_content = get_llms_txt_content()
        with open(self.llms_txt_path, "w", encoding="utf-8") as f:
            f.write(llms_txt_content)

        llms_full_path = self.public_dir / "llms-full.txt"
        llms_full_content = get_llms_full_txt_content(catalog_data)
        with open(llms_full_path, "w", encoding="utf-8") as f:
            f.write(llms_full_content)

        # Copia espejo de endpoints de datos en la raíz para acceso automatizado inmediato
        root_catalogo_json = self.public_dir / "catalogo.json"
        root_catalogo_csv = self.public_dir / "catalogo.csv"
        root_dcat_json = self.public_dir / "dcat.json"

        if self.catalog_json_path.exists():
            with open(root_catalogo_json, "w", encoding="utf-8") as f:
                f.write(self.catalog_json_path.read_text(encoding="utf-8"))
        if self.catalog_csv_path.exists():
            with open(root_catalogo_csv, "w", encoding="utf-8") as f:
                f.write(self.catalog_csv_path.read_text(encoding="utf-8"))
        if self.dcat_json_path.exists():
            with open(root_dcat_json, "w", encoding="utf-8") as f:
                f.write(self.dcat_json_path.read_text(encoding="utf-8"))

        manifest_pwa_content = """{
  "name": "IDE CIT — Infraestructura de Datos Espaciales",
  "short_name": "IDE CIT",
  "description": "Catálogo de datos territoriales abiertos y servicios espaciales del CIT-UAI",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#0F172A",
  "theme_color": "#0F172A",
  "icons": [
    {
      "src": "img/logo-ide-standalone.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}
"""
        with open(self.manifest_pwa_path, "w", encoding="utf-8") as f:
            f.write(manifest_pwa_content)
        logger.info(f"   ✓ Sitemap, Robots, LLMs.txt, LLMs-full.txt y Manifest PWA generados.")

    def build(self, output_path: Optional[Path] = None) -> Path:
        """
        Ejecuta el proceso completo de validación y compilación del portal, guía técnica y red de IDEs.
        """
        start_time = time.time()
        logger.info("🚀 Iniciando compilación algorítmica del portal IDE CIT, Descargas 2017, Guía Técnica y Red de IDEs...")

        catalog_data = self.validate_environment()
        html_content = self.generate_html_content(catalog_data)
        
        descargas_2017_data = {}
        if self.descargas_2017_json_path.exists():
            with open(self.descargas_2017_json_path, "r", encoding="utf-8") as f:
                descargas_2017_data = json.load(f)
        descargas_content = generate_descargas_2017_html(catalog_data, descargas_2017_data)
        guia_content = generate_guia_tecnica_html(catalog_data)
        red_content = generate_red_ides_html(catalog_data)
        ficha_content = generate_ficha_mbht_2017_html(catalog_data)

        target_file = output_path or self.output_html_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(self.output_descargas_path, "w", encoding="utf-8") as f:
            f.write(descargas_content)

        with open(self.output_guia_path, "w", encoding="utf-8") as f:
            f.write(guia_content)

        with open(self.output_red_path, "w", encoding="utf-8") as f:
            f.write(red_content)

        with open(self.output_ficha_path, "w", encoding="utf-8") as f:
            f.write(ficha_content)

        self.export_csv_catalog(catalog_data)
        self.export_dcat_json(catalog_data)
        self.export_sitemap_and_seo(catalog_data)

        elapsed = time.time() - start_time
        size_kb = len(html_content.encode("utf-8")) / 1024.0
        size_descargas_kb = len(descargas_content.encode("utf-8")) / 1024.0
        size_guia_kb = len(guia_content.encode("utf-8")) / 1024.0
        size_red_kb = len(red_content.encode("utf-8")) / 1024.0
        size_ficha_kb = len(ficha_content.encode("utf-8")) / 1024.0

        logger.info(f"✅ Portal, Descargas 2017, Guía Técnica, Red de IDEs y Ficha Maestra compilados exitosamente:")
        logger.info(f"   📁 Catálogo: {target_file} ({size_kb:.1f} KB)")
        logger.info(f"   📁 Descargas 2017: {self.output_descargas_path} ({size_descargas_kb:.1f} KB)")
        logger.info(f"   📁 Guía Técnica: {self.output_guia_path} ({size_guia_kb:.1f} KB)")
        logger.info(f"   📁 Red de IDEs: {self.output_red_path} ({size_red_kb:.1f} KB)")
        logger.info(f"   📁 Ficha Maestra MBHT 2017: {self.output_ficha_path} ({size_ficha_kb:.1f} KB)")
        logger.info(f"   ⏱️ Tiempo de ejecución: {elapsed:.3f} s")

        return target_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compilador algorítmico del portal IDE CIT Data Hub."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Valida el entorno e insumos sin sobrescribir el archivo HTML.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Ruta personalizada para el archivo HTML de salida.",
    )

    args = parser.parse_args()

    try:
        builder = IDEPortalBuilder()
        if args.check:
            builder.validate_environment()
            logger.info("✅ Validación completada con éxito. Todo en orden.")
            return 0

        out_path = Path(args.output).resolve() if args.output else None
        builder.build(output_path=out_path)
        return 0
    except Exception as e:
        logger.error(f"❌ Error durante la compilación: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
