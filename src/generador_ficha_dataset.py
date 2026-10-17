#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — GENERADOR DE LA FICHA TÉCNICA MAESTRA (MBHT 2017)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Genera la ficha técnica oficial para el dataset MBHT 2017 (Matriz de
    Bienestar Humano Territorial), preservando la continuidad de estilo,
    paletas, ancho canónico (max-w-[1600px]), rigor matemático y tratamiento
    estricto de mayúsculas en español (sin sobrecarga de etiquetas ni redundancia).
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from motor_ia_cit import (
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
)


def find_proyecto_root(start_path: Optional[Path] = None) -> Path:
    """Encuentra dinámicamente la raíz del proyecto PROYECTO_MBHT."""
    current = (start_path or Path(__file__)).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent


def generate_ficha_mbht_2017_html(catalog_data: Dict[str, Any]) -> str:
    """
    Genera el documento HTML5 para 'ficha-mbht-2017.html' con KaTeX perfecto
    y continuidad formal del ecosistema IDE CIT.
    """
    portal = catalog_data.get("portal", {})
    version = portal.get("version", "2026.2")
    copilot_js_engine = get_copilot_js_engine()
    llm_head_meta = get_llm_head_meta()
    llm_guidance_html = get_llm_guidance_html()
    canonical_header = get_canonical_header_html("catalogo")
    canonical_footer = get_canonical_footer_html(version)

    # Bloques matemáticos en raw strings para evitar escapes accidentales en Python
    formula_tobler_speed = r"$$W(S) = 6 \cdot \exp\left(-3.5 \cdot |S + 0.05|\right)$$"
    formula_tobler_time = r"$$t_e = \frac{L_e}{W(S_e) \cdot \frac{1000}{60}}$$"
    formula_decay = r"$$f(t_{ij}) = \begin{cases} \exp\left( - \frac{1}{2} \left( \frac{t_{ij}}{t_0} \right)^2 \right), & \text{si } t_{ij} \le 2t_0 \\ 0, & \text{si } t_{ij} > 2t_0 \end{cases}$$"
    formula_e2sfca_step1 = r"$$R_j = \frac{S_j}{\sum_{k \in \{t_{kj} \le 2t_0\}} P_k \cdot f(t_{kj})}$$"
    formula_e2sfca_step2 = r"$$A_i = \sum_{j \in \{t_{ij} \le 2t_0\}} R_j \cdot f(t_{ij})$$"
    formula_weight = r"$$W(D) = \frac{n_D}{N_{\text{total}}}$$"
    formula_bht = r"$$\text{BHT}_i = \sum_{D=1}^{M} W(D) \cdot \text{Dim}_{D, i}$$"

    template = r"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50 scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ficha técnica: MBHT 2017 (Línea base nacional) | IDE CIT · Universidad Adolfo Ibáñez</title>
    
    <!-- Metadatos SEO y estándares espaciales -->
    <meta name="description" content="Especificación técnica oficial de la Matriz de Bienestar Humano Territorial (MBHT 2017): formulación matemática Tobler y E2SFCA, linaje de datos, diccionario de variables y descargas verificadas.">
    <meta name="keywords" content="MBHT 2017, ficha técnica, bienestar humano territorial, accesibilidad peatonal, Tobler, E2SFCA, manzanas censales, Chile, CIT UAI">
    <meta name="author" content="Centro de Inteligencia Territorial (CIT-UAI)">
    <meta name="version" content="[[VERSION]]">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="https://ide.cit.uai.cl/ficha-mbht-2017">
    
[[LLM_HEAD_META]]
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="IDE CIT — Centro de Inteligencia Territorial (UAI)">
    <meta property="og:title" content="Ficha técnica: MBHT 2017 (Línea base nacional) | IDE CIT">
    <meta property="og:description" content="Especificación técnica de la Matriz de Bienestar Humano Territorial (MBHT 2017) sobre 204.906 manzanas censales en las 16 regiones de Chile.">
    <meta property="og:url" content="https://ide.cit.uai.cl/ficha-mbht-2017">
    <meta property="og:image" content="https://ide.cit.uai.cl/img/logo-cit-uai.svg">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Ficha técnica: MBHT 2017 (Línea base nacional) | IDE CIT">
    <meta name="twitter:description" content="Especificación técnica de la Matriz de Bienestar Humano Territorial (MBHT 2017) sobre 204.906 manzanas censales en las 16 regiones de Chile.">
    <meta name="twitter:image" content="https://ide.cit.uai.cl/img/logo-cit-uai.svg">

    <!-- Preconnect & Security headers -->
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta name="referrer" content="strict-origin-when-cross-origin">

    <!-- Schema.org / JSON-LD Dataset -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Matriz de Bienestar Humano Territorial (MBHT 2017) — Cobertura nacional de manzanas censales",
        "alternateName": "MBHT_2017_KPI_MUD_NACIONAL",
        "identifier": [
            "urn:uuid:c17-mbht-2017-kpi-mud-nac-v1"
        ],
        "description": "Línea base nacional oficial de la Matriz de Bienestar Humano Territorial Integral evaluada sobre 204.906 manzanas censales del Censo 2017 en las 16 regiones de Chile. Sintetiza 18 indicadores elementales distribuidos en 4 macro-dimensiones del bienestar (Accesibilidad dim_acc, Socioeconómica dim_soc, Seguridad dim_seg y Ambiental dim_amb), donde la macro-dimensión de Accesibilidad integra los 6 indicadores peatonales E2SFCA + Tobler (isal, ise, iav, idep, icul, iser).",
        "url": "https://ide.cit.uai.cl/ficha-mbht-2017",
        "version": "1.0.3",
        "datePublished": "2018-06-15",
        "dateModified": "2026-10-15",
        "license": "https://creativecommons.org/licenses/by/4.0/deed.es",
        "creator": {
            "@type": "EducationalOrganization",
            "name": "Centro de Inteligencia Territorial · Universidad Adolfo Ibáñez",
            "url": "https://cit.uai.cl"
        },
        "publisher": {
            "@type": "EducationalOrganization",
            "name": "Universidad Adolfo Ibáñez",
            "url": "https://www.uai.cl"
        },
        "spatialCoverage": {
            "@type": "Place",
            "geo": {
                "@type": "GeoShape",
                "box": "-55.9800 -75.6443 -17.4984 -66.8622"
            }
        },
        "distribution": [
            {
                "@type": "DataDownload",
                "encodingFormat": "application/vnd.apache.parquet",
                "contentUrl": "https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.parquet",
                "contentSize": "240.9 MB"
            },
            {
                "@type": "DataDownload",
                "encodingFormat": "application/geopackage+sqlite3",
                "contentUrl": "https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.gpkg",
                "contentSize": "343.9 MB"
            },
            {
                "@type": "DataDownload",
                "encodingFormat": "application/zip",
                "contentUrl": "https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas_SHP.zip",
                "contentSize": "204.9 MB"
            },
            {
                "@type": "DataDownload",
                "encodingFormat": "text/csv",
                "contentUrl": "https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.csv",
                "contentSize": "96.2 MB"
            }
        ]
    }
    </script>

    <!-- Favicon y manifiesto PWA -->
    <link rel="icon" type="image/svg+xml" href="/img/logo-ide-standalone.svg">
    <link rel="manifest" href="/site.webmanifest">
    
    <!-- KaTeX para formulación matemática de máxima fidelidad (SRI SHA-384 Verificado) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" integrity="sha384-GvrOXuhMATgEsSwCs4smul74iXGOixntILdUW9XmUC6+HX0sLNAK3q71HotJqlAn" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js" integrity="sha384-cpW21h6RZv/phavutF+AuVYrr+dA8xD9zs6FwLpaCct6O9ctzYFfFr4dgmgccOTx" crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous"></script>

    <!-- CSS Estático de Producción (Tailwind Compilado CIT) -->
    <link rel="stylesheet" href="/css/ide.min.css">

    <!-- Lucide Icons (Local Vendor) -->
    <script src="/vendor/lucide/lucide.min.js"></script>

    <style>
        html {
            font-size: 16px;
            overflow-y: scroll;
            scrollbar-gutter: stable;
            scroll-behavior: smooth;
        }
        [data-lucide] {
            display: inline-block;
            vertical-align: middle;
            flex-shrink: 0;
        }
        .katex-display {
            margin: 0.75rem 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
            padding: 0.25rem 0;
        }
    </style>
</head>
<body class="min-h-full flex flex-col font-sans text-slate-800 antialiased bg-slate-100 selection:bg-slate-900 selection:text-white">
    <noscript>
        <div class="bg-slate-900 text-white py-3 px-4 border-b border-slate-700 text-xs sm:text-sm">
            <div class="max-w-[1600px] mx-auto flex flex-wrap items-center justify-between gap-3">
                <span><strong>Modo HTML estático activo:</strong> Esta ficha técnica y todos los enlaces de descarga directa (.parquet, .gpkg, .zip, .csv) son 100% accesibles sin JavaScript.</span>
                <div class="flex items-center gap-4 underline font-semibold">
                    <a href="/inicio" class="text-white">Catálogo</a>
                    <a href="/descargas" class="text-white">Descargas</a>
                    <a href="/guia-tecnica" class="text-white">Guía Técnica</a>
                    <a href="/download/MBHT_2017_Nacional_Manzanas.parquet" class="text-uai-gold">GeoParquet Nacional</a>
                </div>
            </div>
        </div>
    </noscript>

    [[CANONICAL_HEADER]]

    <!-- 2. CABECERA HERO SOBRIA (CON EL ANCHO CANÓNICO 1600PX Y SIN SOBRECARGA DE ETIQUETAS) -->
    <main id="main-content" role="main" tabindex="-1">
    <section class="bg-white border-b border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <!-- Barra superior: Migas de pan + Acciones -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4 sm:mb-6">
                <nav class="flex items-center space-x-2 text-xs text-slate-400" aria-label="Ruta de navegación">
                    <a href="inicio" class="hover:text-slate-700 transition">IDE CIT</a>
                    <span class="text-slate-300">/</span>
                    <a href="inicio#catalogo" class="hover:text-slate-700 transition text-slate-500 font-medium">Catálogo de capas</a>
                    <span class="text-slate-300">/</span>
                    <span class="text-slate-800 font-bold">Línea base oficial MBHT 2017</span>
                </nav>

                <div class="flex items-center gap-2.5 shrink-0">
                    <a href="/download/iso_xml/kpi_mud_2017_iso19139.xml" download class="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-700 hover:text-black bg-slate-100 hover:bg-slate-200 border border-slate-300 px-3.5 py-2 rounded-lg transition shadow-xs">
                        <i data-lucide="file-code" class="w-4 h-4 text-slate-600"></i>
                        <span>metadata.xml (ISO 19139)</span>
                    </a>
                    <a href="/descargas" class="inline-flex items-center space-x-1.5 text-xs font-semibold text-white bg-slate-900 hover:bg-black px-4 py-2 rounded-lg transition shadow-xs">
                        <i data-lucide="download" class="w-4 h-4 text-[#6493B5]"></i>
                        <span>Centro de descargas</span>
                    </a>
                </div>
            </div>

            <!-- Bloque Titular y Resumen a Ancho Completo (100% width) -->
            <div class="w-full">
                <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-800 text-[11px] sm:text-xs font-bold uppercase tracking-wider mb-3">
                    <span class="w-2 h-2 rounded-full bg-uai-gold"></span>
                    <span>Línea base oficial vigente 2017 · 204.906 manzanas · 4 macro-dimensiones (18 indicadores) · 42 columnas verificadas</span>
                </div>
                
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-slate-900 leading-tight w-full">
                    Matriz de Bienestar Humano Territorial Integral (MBHT 2017)
                </h1>
                
                <p class="text-sm sm:text-base lg:text-lg text-slate-600 mt-2.5 sm:mt-3 leading-relaxed font-normal w-full max-w-none">
                    Esta ficha documenta la <strong>cobertura maestra integral de manzanas censales (<code class="font-mono text-sm">MBHT_2017_Nacional_Manzanas</code>)</strong>. El conjunto sintetiza <strong>18 indicadores elementales</strong> agrupados en <strong>4 macro-dimensiones del bienestar</strong> —Accesibilidad (<code class="font-mono text-sm">dim_acc</code>), Socioeconómica (<code class="font-mono text-sm">dim_soc</code>), Seguridad (<code class="font-mono text-sm">dim_seg</code>) y Ambiental (<code class="font-mono text-sm">dim_amb</code>)— para construir el índice global <code class="font-mono text-sm">bht</code>. A su vez, la macro-dimensión de Accesibilidad (<code class="font-mono text-sm">dim_acc</code>) está integrada por los <strong>6 indicadores temáticos de acceso peatonal a equipamientos</strong> (<code class="font-mono text-sm">isal</code>, <code class="font-mono text-sm">ise</code>, <code class="font-mono text-sm">iav</code>, <code class="font-mono text-sm">idep</code>, <code class="font-mono text-sm">icul</code>, <code class="font-mono text-sm">iser</code>), modelados sobre la red vial continua con impedancia topográfica de Tobler y el método bietápico E2SFCA.
                </p>
            </div>

            <!-- Métricas clave estructuradas -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mt-8 pt-6 border-t border-slate-100 text-xs">
                <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    <span class="text-slate-500 block font-normal">Unidades y atributos</span>
                    <span class="text-slate-900 font-bold text-sm sm:text-base font-mono mt-0.5 block">204.906 mzs · 42 cols</span>
                </div>
                <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    <span class="text-slate-500 block font-normal">Estructura de síntesis</span>
                    <span class="text-slate-900 font-bold text-sm sm:text-base font-mono mt-0.5 block">4 dims · 18 indicadores</span>
                </div>
                <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    <span class="text-slate-500 block font-normal">Oferta pública y red vial</span>
                    <span class="text-slate-900 font-bold text-sm sm:text-base font-mono mt-0.5 block">55.035 eq · 1.589.595 ejes</span>
                </div>
                <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    <span class="text-slate-500 block font-normal">Estado y versión</span>
                    <span class="text-slate-900 font-bold text-sm sm:text-base mt-0.5 block">Vigente · v1.0.3 (CC BY 4.0)</span>
                </div>
            </div>

            <!-- Navegación interna de la ficha técnica -->
            <nav class="flex flex-wrap items-center gap-2 mt-6 pt-4 border-t border-slate-100 text-xs sm:text-sm text-slate-600" aria-label="Secciones de la ficha">
                <span class="text-slate-400 font-medium mr-1">Secciones:</span>
                <a href="#sec-identidad" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">1. Alcance y arquitectura de dimensiones</a>
                <a href="#sec-linaje" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">2. Linaje y cuadratura</a>
                <a href="#sec-metodologia" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">3. Formulación y sensibilidad</a>
                <a href="#sec-diccionario" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">4. Diccionario físico (42 columnas)</a>
                <a href="#sec-descargas" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">5. Descargas y reproducción E2E</a>
                <a href="#sec-gobernanza" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition">6. Gobernanza, versiones e incidencias</a>
            </nav>

        </div>
    </section>

    <!-- 3. CONTENEDOR PRINCIPAL CANÓNICO (MAX-W 1600PX) -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-10 xl:px-12 py-10 sm:py-14 w-full space-y-8">

        <!-- SECCIÓN 1: IDENTIDAD, ALCANCE Y ARQUITECTURA DE DIMENSIONES -->
        <section id="sec-identidad" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">01</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Alcance del producto, articulación dimensional y metadatos formales</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Relación exacta entre el índice global BHT, las 4 macro-dimensiones y los 6 indicadores de accesibilidad a equipamientos.</p>
                    </div>
                </div>
            </div>

            <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-5 font-normal">
                Para evitar cualquier ambigüedad entre la documentación metodológica, el catálogo y los archivos físicos descargables, se explicita la relación jerárquica entre los productos que componen la línea base <strong>MBHT 2017</strong>: el archivo maestro de manzanas (<code class="font-mono text-xs sm:text-sm bg-slate-100 px-1.5 py-0.5 rounded">MBHT_2017_Nacional_Manzanas.*</code>) contiene simultáneamente la <strong>MBHT Integral (4 macro-dimensiones que sintetizan 18 indicadores elementales)</strong> y el desglose completo de los <strong>6 indicadores temáticos de accesibilidad peatonal</strong> que alimentan la primera macro-dimensión (<code class="font-mono text-xs sm:text-sm bg-slate-100 px-1.5 py-0.5 rounded">dim_acc</code>).
            </p>

            <!-- Tabla explicativa de la jerarquía 4 Macro-Dimensiones vs 6 Sub-dimensiones de Accesibilidad -->
            <div class="overflow-x-auto border border-slate-200 rounded-xl mb-6">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                        <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                            <th class="py-3 px-4 font-semibold">Macro-dimensión de la MBHT Integral</th>
                            <th class="py-3 px-4 font-semibold">Campo en archivo de manzanas</th>
                            <th class="py-3 px-4 font-semibold text-center">Peso neutro ($n_D / 18$)</th>
                            <th class="py-3 px-4 font-semibold">Indicadores elementales que la componen y coberturas asociadas</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 text-slate-700 bg-white">
                        <tr>
                            <td class="py-3.5 px-4 font-bold text-slate-900">1. Dimensión de Accesibilidad</td>
                            <td class="py-3.5 px-4 font-mono font-bold text-slate-900">dim_acc, dim_acc_bruto</td>
                            <td class="py-3.5 px-4 text-center font-mono font-semibold">6 / 18 (33,33%)</td>
                            <td class="py-3.5 px-4 leading-relaxed">
                                Integrada por los <strong>6 indicadores de accesibilidad peatonal E2SFCA + Tobler</strong> incluidos como columnas en el mismo archivo de manzanas: Salud (<code class="font-mono">isal</code>), Educación (<code class="font-mono">ise</code>), Áreas Verdes (<code class="font-mono">iav</code>), Deporte (<code class="font-mono">idep</code>), Cultura (<code class="font-mono">icul</code>) y Servicios Públicos (<code class="font-mono">iser</code>). Estos 6 indicadores se calculan a partir del catastro de <strong>55.035 equipamientos de libre acceso</strong> (<code class="font-mono">Equipamientos_2017_*</code>) y los <strong>1.589.595 tramos viales</strong> (<code class="font-mono">Red_Vial_Ejes_2017_*</code>).
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3.5 px-4 font-bold text-slate-900">2. Dimensión Socioeconómica</td>
                            <td class="py-3.5 px-4 font-mono font-bold text-slate-900">dim_soc, dim_soc_bruto</td>
                            <td class="py-3.5 px-4 text-center font-mono font-semibold">6 / 18 (33,33%)</td>
                            <td class="py-3.5 px-4 leading-relaxed">
                                Sintetiza <strong>6 indicadores elementales</strong> censales y habitacionales (escolaridad del jefe de hogar, inserción laboral, hacinamiento, materialidad de vivienda, acceso a servicios básicos y dependencia demográfica).
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3.5 px-4 font-bold text-slate-900">3. Dimensión de Seguridad</td>
                            <td class="py-3.5 px-4 font-mono font-bold text-slate-900">dim_seg, dim_seg_bruto</td>
                            <td class="py-3.5 px-4 text-center font-mono font-semibold">4 / 18 (22,22%)</td>
                            <td class="py-3.5 px-4 leading-relaxed">
                                Sintetiza <strong>4 indicadores elementales</strong> de seguridad urbana y exposición delictual en el espacio público (delitos graves y leves contra las personas y contra la propiedad).
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3.5 px-4 font-bold text-slate-900">4. Dimensión Ambiental</td>
                            <td class="py-3.5 px-4 font-mono font-bold text-slate-900">dim_amb, dim_amb_bruto</td>
                            <td class="py-3.5 px-4 text-center font-mono font-semibold">2 / 18 (11,11%)</td>
                            <td class="py-3.5 px-4 leading-relaxed">
                                Sintetiza <strong>2 indicadores elementales</strong> de calidad ambiental urbana (cobertura vegetacional efectiva NDVI e isla de calor / amplitud térmica superficial).
                            </td>
                        </tr>
                        <tr class="bg-slate-50 font-semibold text-slate-900">
                            <td class="py-3.5 px-4 font-bold">Índice Sintético Global MBHT 2017</td>
                            <td class="py-3.5 px-4 font-mono font-bold">bht, bht_bruto, tob</td>
                            <td class="py-3.5 px-4 text-center font-mono font-bold">18 / 18 (100,0%)</td>
                            <td class="py-3.5 px-4 leading-relaxed">
                                Síntesis ponderada proporcional $\text{BHT}_i = \frac{6}{18}\text{dim\_acc}_i + \frac{6}{18}\text{dim\_soc}_i + \frac{4}{18}\text{dim\_seg}_i + \frac{2}{18}\text{dim\_amb}_i$, con tipología territorial consolidada en tres macro-estratos (<code class="font-mono">tob</code>: Alto, Medio, Bajo) y discretización cartográfica de 6 clases por Quiebres Naturales de Jenks sobre la variable numérica continua <code class="font-mono">bht</code>.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 text-sm pt-5 border-t border-slate-100">
                <div class="space-y-4">
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Título canónico oficial</span>
                        <span class="text-slate-900 font-bold text-base leading-snug">Matriz de Bienestar Humano Territorial (MBHT 2017) — Cobertura nacional de manzanas censales</span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Acrónimo institucional</span>
                        <span class="font-mono font-semibold text-slate-800 text-sm">MBHT_2017_KPI_MUD_NACIONAL</span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Identificador persistente URN</span>
                        <span class="font-mono text-xs sm:text-sm text-slate-700 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 block truncate">urn:uuid:c17-mbht-2017-kpi-mud-nac-v1</span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Custodio y responsable técnico</span>
                        <span class="text-slate-900 font-medium text-sm sm:text-base">Unidad de Modelación Espacial e Infraestructura de Datos · CIT-UAI (<a href="mailto:contactocit@uai.cl" class="underline">contactocit@uai.cl</a>)</span>
                    </div>
                </div>

                <div class="space-y-4">
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Sistema de referencia de coordenadas</span>
                        <span class="text-slate-800 font-medium text-sm sm:text-base">Distribución: EPSG:4326 (WGS 84) · Marco oficial: SIRGAS-Chile (EPSG:5360, GRS80; Helmert EPSG:15946 &Delta;=0,0 m)</span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Línea base temporal y estado</span>
                        <span class="text-slate-800 text-sm sm:text-base">Censo de Población y Vivienda 2017 (INE) · <strong>Estado: Vigente / Estable (v1.0.3)</strong></span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Conformidad de metadatos y esquema físico</span>
                        <span class="text-slate-800 text-sm sm:text-base">ISO 19115-1:2014 / ISO 19139 XML · 42 columnas verificadas en los 4 formatos</span>
                    </div>
                    <div>
                        <span class="text-xs font-semibold text-slate-500 block uppercase tracking-wider mb-1">Licencia de publicación</span>
                        <span class="text-slate-800 text-sm sm:text-base">Creative Commons Atribución 4.0 Internacional (CC BY 4.0)</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECCIÓN 2: LINAJE Y VALIDACIÓN JERÁRQUICA DEL CATASTRO -->
        <section id="sec-linaje" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">02</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Linaje, validación jerárquica y cuadratura nacional</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Trazabilidad desde las fuentes primarias del Estado y conciliación aritmética entre particiones regionales.</p>
                    </div>
                </div>
            </div>

            <div class="text-sm sm:text-base text-slate-600 leading-relaxed space-y-5 font-normal">
                <p>
                    La cartografía base y la demografía provienen del Instituto Nacional de Estadísticas (INE). La oferta territorial se construye a partir de catastros sectoriales oficiales de ministerios y servicios públicos (Salud, Educación, Vivienda y Urbanismo, Obras Públicas, Deportes y Registro Civil), vinculados a la red física de ejes viales con pendientes calculadas sobre el Modelo Digital de Elevación (DEM).
                </p>

                <!-- Criterio metodológico en 3 niveles -->
                <div class="bg-slate-50 rounded-xl p-5 sm:p-6 border border-slate-200">
                    <h3 class="font-bold text-slate-900 mb-3 text-sm sm:text-base tracking-normal">Criterio metodológico: proceso de selección y validación jerárquica del catastro de equipamientos</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-xs">
                            <span class="font-bold text-slate-900 block text-sm sm:text-base mb-1">1. Catastro bruto inicial</span>
                            <span class="font-mono text-slate-900 block mb-2 font-bold text-base sm:text-lg">202.275 registros</span>
                            <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">Consolidación exhaustiva de servicios y recintos a partir de registros administrativos sectoriales del Estado.</p>
                        </div>
                        <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-xs">
                            <span class="font-bold text-slate-900 block text-sm sm:text-base mb-1">2. Catastro maestro ruteable</span>
                            <span class="font-mono text-slate-900 block mb-2 font-bold text-base sm:text-lg">113.231 equipamientos</span>
                            <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">Depuración posicional, corrección topológica y conexión nodo a nodo al grafo de 1.589.595 tramos viales.</p>
                        </div>
                        <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-xs">
                            <span class="font-bold text-slate-900 block text-sm sm:text-base mb-1">3. Línea base oficial MBHT</span>
                            <span class="font-mono text-slate-900 block mb-2 font-bold text-base sm:text-lg">55.035 equipamientos</span>
                            <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">Subconjunto auditado de servicios comunitarios gratuitos y de acceso irrestricto que componen la matriz abierta.</p>
                        </div>
                    </div>
                </div>

                <p class="pt-1">
                    <strong class="text-slate-900 font-semibold">Conciliación y cuadratura aritmética nacional ($\Delta = 0$):</strong> La suma de las 16 particiones regionales distribuidas en el Centro de descargas coincide exactamente con los totales consolidados nacionales en todas las coberturas: $\sum_{r=1}^{16} N_r = 204.906$ manzanas censales, $\sum_{r=1}^{16} P_r = 17.482.699$ habitantes residentes amanzanados (correspondientes al 99,48% de los 17.574.003 habitantes censados por el INE a nivel nacional; los 91.304 habitantes restantes corresponden a población en tránsito, personas en situación de calle y áreas rurales no amanzanadas), $\sum_{r=1}^{16} E_r = 55.035$ equipamientos de línea base pública y $\sum_{r=1}^{16} V_r = 1.589.595$ tramos viales ruteables, garantizando consistencia de inventario y cuadratura demográfica estricta entre vistas comunales, regionales y nacionales.
                </p>

                <!-- Tabla de Universos Demográficos y Estados de Publicación -->
                <div class="overflow-x-auto bg-white rounded-xl border border-slate-200 shadow-xs my-4">
                    <table class="w-full text-left text-xs sm:text-sm border-collapse">
                        <thead>
                            <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Conjunto / Producto</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Estado de publicación</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Población modelada</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Unidades territoriales</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Función metodológica</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 text-slate-600">
                            <tr>
                                <td class="py-2.5 px-3.5 font-bold text-slate-900">MBHT 2017 (Línea Base Oficial)</td>
                                <td class="py-2.5 px-3.5 font-semibold text-xs text-slate-900">Vigente en producción (v1.0.3)</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">17.482.699 hab. <span class="text-slate-400 block text-[11px]">(99,48% de 17.574.003 censados INE)</span></td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">204.906 manzanas censales</td>
                                <td class="py-2.5 px-3.5 leading-relaxed text-xs">Medición oficial del Bienestar Humano Territorial: 18 indicadores elementales, 4 macro-dimensiones, 42 columnas físicas, ruteo peatonal en 1,59M tramos viales.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3.5 font-bold text-slate-900">Censo 2024 — Insumo Demográfico</td>
                                <td class="py-2.5 px-3.5 font-semibold text-xs text-slate-800">Disponible como insumo abierto</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">~18,48 millones hab. <span class="text-slate-400 block text-[11px]">(7,66M viviendas · 6,62M hogares)</span></td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">254.395 manzanas y entidades</td>
                                <td class="py-2.5 px-3.5 leading-relaxed text-xs">Insumo demográfico abierto desagregado por cohortes etarias (0 a 100+ años) y sexo mediante algoritmo osculatorio Sprague + IPF, preservando totales oficiales del INE.</td>
                            </tr>
                            <tr class="bg-slate-50/50">
                                <td class="py-2.5 px-3.5 font-bold text-slate-900">Actualización MBHT 2024</td>
                                <td class="py-2.5 px-3.5 font-medium text-xs text-slate-600">En calibración metodológica</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs text-slate-400">Población Censo 2024</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs text-slate-400">254.395 manzanas y entidades</td>
                                <td class="py-2.5 px-3.5 leading-relaxed text-xs text-slate-500">Nueva síntesis BHT 2024 en calibración estadística final. <strong>Lanzamiento oficial programado para noviembre de 2026.</strong> No se distribuye en la IDE para evitar colisión con la línea base vigente.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- SECCIÓN 3: METODOLOGÍA Y FORMULACIÓN MATEMÁTICA -->
        <section id="sec-metodologia" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">03</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Metodología de cálculo y formulación matemática</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Fundamentos de accesibilidad espacial continua, función de Tobler y modelo bietápico E2SFCA.</p>
                    </div>
                </div>
            </div>

            <div class="text-sm sm:text-base text-slate-600 leading-relaxed space-y-8 font-normal">
                <!-- 1. Función de Tobler -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">1. Velocidad peatonal e impedancia topográfica de Waldo Tobler (1993)</h3>
                    <p class="mb-3">
                        Todo traslado humano en los modelos del CIT-UAI se computa estrictamente sobre la red vial continua de ejes de transporte (cero distancia euclidiana). La velocidad de marcha humana $W(S)$ varía exponencialmente en función de la pendiente longitudinal adimensional del tramo vial $S = \frac{\Delta h}{L} = \frac{h_{\text{destino}} - h_{\text{origen}}}{L}$ calculada sobre el Modelo Digital de Elevación (DEM), donde $S > 0$ representa un ascenso (subida), $S < 0$ un descenso (bajada) y $S = 0$ terreno horizontal:
                    </p>
                    <div class="bg-slate-50 p-4 sm:p-6 rounded-xl border border-slate-200 text-center my-4">
                        [[FORMULA_TOBLER_SPEED]]
                    </div>
                    <div class="space-y-3 text-slate-600 text-xs sm:text-sm mt-3 leading-relaxed">
                        <p>
                            Donde $W(S)$ denota la velocidad de marcha resultante en $\text{km/h}$. La formulación captura fielmente el comportamiento biomecánico del desplazamiento peatonal según el gradiente topográfico:
                        </p>
                        <div class="overflow-x-auto border border-slate-200 rounded-xl bg-white shadow-xs my-3">
                            <table class="w-full text-xs text-left">
                                <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                                    <tr>
                                        <th class="py-2.5 px-3.5">Gradiente / Pendiente ($S$)</th>
                                        <th class="py-2.5 px-3.5">Condición del Terreno</th>
                                        <th class="py-2.5 px-3.5 font-mono">Velocidad Teórica $W(S)$</th>
                                        <th class="py-2.5 px-3.5 text-right">Variación vs. Plano</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100 font-mono text-[11px] text-slate-600">
                                    <tr class="hover:bg-slate-50 transition">
                                        <td class="py-2 px-3.5 font-semibold text-slate-800">$S = -0{,}05$ ($-5\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Descenso suave (óptimo biomecánico de máxima velocidad)</td>
                                        <td class="py-2 px-3.5 font-bold text-emerald-700">$6{,}00\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-emerald-600 font-sans">+19,0%</td>
                                    </tr>
                                    <tr class="bg-slate-50/60 font-semibold text-slate-900">
                                        <td class="py-2 px-3.5">$S = 0{,}00$ ($0\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Terreno plano horizontal (línea base de referencia)</td>
                                        <td class="py-2 px-3.5 font-bold">$5{,}04\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right font-sans">0,0% (Base)</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50 transition">
                                        <td class="py-2 px-3.5 text-slate-800">$S = +0{,}10$ ($+10\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Ascenso moderado</td>
                                        <td class="py-2 px-3.5">$3{,}55\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-amber-700 font-sans">-29,6%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50 transition">
                                        <td class="py-2 px-3.5 text-slate-800">$S = +0{,}15$ ($+15\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Ascenso fuerte (rampas y calles inclinadas)</td>
                                        <td class="py-2 px-3.5 font-bold text-amber-800">$2{,}98\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-amber-700 font-sans">-40,8%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50 transition">
                                        <td class="py-2 px-3.5 text-slate-800">$S = +0{,}20$ ($+20\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Ascenso empinado (quebradas y cerros habitados)</td>
                                        <td class="py-2 px-3.5">$2{,}50\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-rose-700 font-sans">-50,4%</td>
                                    </tr>
                                    <tr class="bg-rose-50/50 hover:bg-rose-50 transition">
                                        <td class="py-2 px-3.5 font-bold text-rose-900">$S \ge +0{,}264$ ($+26{,}4\%$)</td>
                                        <td class="py-2 px-3.5 font-sans text-rose-800">Ascenso extremo (umbral analítico estricto: $W \le 2{,}00\text{ km/h}$)</td>
                                        <td class="py-2 px-3.5 font-bold text-rose-800">$\le 2{,}00\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-rose-700 font-sans">&le; -60,3%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50 transition">
                                        <td class="py-2 px-3.5 text-slate-800">$S = +0{,}30$ ($+30\%$)</td>
                                        <td class="py-2 px-3.5 font-sans">Ascenso muy escarpado</td>
                                        <td class="py-2 px-3.5">$1{,}76\text{ km/h}$</td>
                                        <td class="py-2 px-3.5 text-right text-rose-700 font-sans">-65,1%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <p class="text-[11px] text-slate-500 italic">
                            *Nota metodológica de resolución analítica:* Al despejar el umbral de marcha lenta $W(S) \le 2{,}00\text{ km/h}$, se obtiene analíticamente $|S + 0{,}05| \ge \frac{\ln(3)}{3{,}5} \approx 0{,}3139$. Esto demuestra con exactitud matemática que en ascenso la velocidad cae por debajo de $2{,}00\text{ km/h}$ a partir del $26{,}4\%$ de pendiente ($S \ge +0{,}264$), mientras que en una pendiente ascendente del $15\%$ ($S = +0{,}15$) la velocidad efectiva es estrictamente de $2{,}98\text{ km/h}$ ($W(0{,}15) = 6 \cdot e^{-0{,}70} \approx 2{,}9795\text{ km/h}$).
                        </p>
                    </div>
                </div>

                <!-- 2. Tiempo de viaje en tramo vial -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">2. Tiempo de fricción en la red vial</h3>
                    <p class="mb-3">
                        El costo temporal $t_e$ (en minutos) requerido para recorrer un tramo vial $e$ de longitud $L_e$ (en metros) con pendiente $S_e$ se computa como:
                    </p>
                    <div class="bg-slate-50 p-4 sm:p-6 rounded-xl border border-slate-200 text-center my-4">
                        [[FORMULA_TOBLER_TIME]]
                    </div>
                    <p class="text-slate-500 text-xs sm:text-sm mt-2">
                        El tiempo acumulado entre una manzana censal $i$ y un equipamiento $j$ ($t_{ij}$) se determina mediante algoritmos de ruta mínima sobre el grafo vial ruteable nacional de 1.589.595 tramos.
                    </p>
                </div>

                <!-- 3. Decaimiento gaussiano -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">3. Función de decaimiento continuo gaussiano</h3>
                    <p class="mb-3">
                        La fricción espacial y la disminución de la propensión al viaje peatonal se modelan mediante una función continua sin umbrales arbitrarios:
                    </p>
                    <div class="bg-slate-50 p-4 sm:p-6 rounded-xl border border-slate-200 text-center my-4">
                        [[FORMULA_DECAY]]
                    </div>
                    <p class="text-slate-500 text-xs sm:text-sm mt-2">
                        Donde $t_0$ es el radio de captación temporal calibrado según la escala y naturaleza del equipamiento.
                    </p>
                </div>

                <!-- 4. E2SFCA -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">4. Modelo bietápico de área de captación flotante (E2SFCA)</h3>
                    <p class="mb-3">
                        El modelo equilibra la capacidad finita de oferta de cada servicio frente a la demanda poblacional concurrente a través de dos etapas sucesivas:
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 my-4">
                        <div class="bg-slate-50 p-4 sm:p-5 rounded-xl border border-slate-200 text-center">
                            <span class="text-slate-800 font-bold block mb-2 text-sm sm:text-base">Paso 1: Ratio de oferta del equipamiento ($j$)</span>
                            [[FORMULA_E2SFCA_STEP1]]
                            <p class="text-slate-500 text-xs sm:text-sm mt-3 leading-relaxed">
                                $S_j$ es la capacidad física instalada ($m^2$, boxes o cupos) del servicio $j$, y $P_k$ es la población residente censada en la manzana $k$.
                            </p>
                        </div>
                        <div class="bg-slate-50 p-4 sm:p-5 rounded-xl border border-slate-200 text-center">
                            <span class="text-slate-800 font-bold block mb-2 text-sm sm:text-base">Paso 2: Accesibilidad acumulada en la manzana ($i$)</span>
                            [[FORMULA_E2SFCA_STEP2]]
                            <p class="text-slate-500 text-xs sm:text-sm mt-3 leading-relaxed">
                                $A_i$ cuantifica el puntaje integrado de acceso efectivo del que disponen los hogares de la unidad censal $i$.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 5. Axioma de neutralidad elemental -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">5. Axioma de neutralidad elemental y síntesis BHT</h3>
                    <p class="mb-3">
                        En la formulación oficial del CIT-UAI, cada indicador elemental de bienestar posee una ponderación neutra y proporcional de línea base ($W(D) = n_D / N_{\text{total}}$), descartando promedios aritméticos simples entre macrodimensiones que distorsionan el peso de las variables:
                    </p>
                    <div class="bg-slate-50 p-4 sm:p-6 rounded-xl border border-slate-200 text-center my-4">
                        [[FORMULA_WEIGHT]]
                        <div class="mt-3"></div>
                        [[FORMULA_BHT]]
                    </div>
                    <p class="text-slate-500 text-xs sm:text-sm mt-2">
                        En la línea base oficial MBHT 2017 ($N_{\text{total}} = 18$ indicadores): Accesibilidad ($6/18 = 33,33\%$), Socioeconómica ($6/18 = 33,33\%$), Seguridad ($4/18 = 22,22\%$) y Ambiental ($2/18 = 11,11\%$). Cada indicador individual pesa exactamente $1/18 \approx 5,56\%$.
                    </p>
                </div>

                <!-- 6. Sensibilidad paramétrica y evolución longitudinal -->
                <div>
                    <h3 class="font-bold text-slate-900 text-base sm:text-lg mb-2">6. Análisis de sensibilidad paramétrica y evolución longitudinal (2017–2024)</h3>
                    <p class="mb-4">
                        La estabilidad empírica del modelo se evalúa mediante pruebas de perturbación sobre el ancho de banda gaussiano ($t_0 \in \{10, 15, 20\}\text{ min}$, manteniendo correlación de rango de Spearman $\rho > 0,94$ a escala comunal) y el factor exponencial de pendiente de Tobler (crítico en topografías de cerros y quebradas con $S > 12\%$). La evolución metodológica entre la línea base 2017 y la actualización censal 2024 conserva la formulación física para permitir comparabilidad intertemporal:
                    </p>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs sm:text-sm border-collapse border border-slate-200 rounded-xl overflow-hidden">
                            <thead>
                                <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                                    <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider">Parámetro metodológico</th>
                                    <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider">Línea base oficial MBHT 2017</th>
                                    <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider">Actualización nacional MBHT 2024</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100 text-slate-600">
                                <tr>
                                    <td class="py-3 px-3.5 font-semibold text-slate-900">Universo censal modelado</td>
                                    <td class="py-3 px-3.5">204.906 manzanas urbanas (Censo 2017)</td>
                                    <td class="py-3 px-3.5">254.395 manzanas y entidades (Censo 2024)</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-3.5 font-semibold text-slate-900">Impedancia y red vial</td>
                                    <td class="py-3 px-3.5">Grafo ruteable (1.589.595 tramos) con función de Tobler</td>
                                    <td class="py-3 px-3.5">Grafo continuo actualizado con pendiente DEM de alta resolución</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-3.5 font-semibold text-slate-900">Ponderación neutral ($W(D)$)</td>
                                    <td class="py-3 px-3.5">18 indicadores ($1/18 \approx 5,56\%$ por indicador elemental)</td>
                                    <td class="py-3 px-3.5">17 indicadores ($1/17 \approx 5,88\%$ por indicador elemental)</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-3.5 font-semibold text-slate-900">Estratificación territorial</td>
                                    <td class="py-3 px-3.5">Quiebres Naturales de Jenks (6 clases, algoritmo ckmeans)</td>
                                    <td class="py-3 px-3.5">Quiebres Naturales de Jenks (6 clases, distribución normalizada)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECCIÓN 4: DICCIONARIO DE VARIABLES -->
        <section id="sec-diccionario" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">04</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Diccionario de variables de la capa (Esquema físico de 42 columnas)</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Correspondencia exacta 1:1 con los nombres de columna presentes en <code class="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded text-slate-800">MBHT_2017_Nacional_Manzanas.parquet</code> y sus equivalentes (.gpkg, .shp, .csv).</p>
                    </div>
                </div>
            </div>

            <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-5 font-normal">
                El archivo consolidado contiene <strong>42 columnas físicas</strong> organizadas en cinco bloques: identificadores territoriales (7), demografía y vivienda censal (11), índice sintético y tipología (3), las cuatro macro-dimensiones del bienestar en versión normalizada y bruta (8), los seis sub-indicadores de accesibilidad peatonal en versión estandarizada y previa (12), y la geometría poligonal (1).
            </p>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                                        <thead>
                        <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                            <th class="py-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50 text-center">#</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Columna física</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Tipo</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50 text-center">Nulos</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Rango / Dominio</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Descripción técnica y rol en el modelo</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-slate-600">
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">1</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">id_manzcit</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">string</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">No</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Clave primaria</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Identificador único de manzana CIT-UAI (204.906 registros únicos nacionales). Concatenación CUT y código censal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">2</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">cod_reg</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">int64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">No</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">1 a 16</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Código Único Territorial de la región (CUT oficial SUBDERE / INE).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">3</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">cod_prov</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">int64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">No</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Código provincial</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Código Único Territorial de la provincia correspondiente a la unidad.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">4</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">cod_com</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">int64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">No</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Código comunal</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Código Único Territorial de la comuna correspondiente a la unidad.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">5</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">tob</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">string</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Alto / Medio / Bajo</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Tipología de Oportunidad de Bienestar territorial clasificada en tres macro-estratos (Alto, Medio y Bajo). La discretización cartográfica de 6 clases se aplica sobre la variable numérica continua <code class="font-mono text-xs">bht</code> mediante Quiebres Naturales de Jenks.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">6</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">manz_en</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">string</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">URBANO / RURAL</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Clasificación oficial de entidad o manzana censal asignada por el INE (Censo 2017).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">7</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">personas</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 habitantes</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Población residente habitual empadronada en la manzana (Censo 2017).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">8</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">area</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">m²</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Superficie planimétrica en metros cuadrados del polígono censal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">9</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">hog_n</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 hogares</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cantidad total de hogares particulares residentes en la unidad (Censo 2017).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">10</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">total_v</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 viviendas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cantidad total de viviendas censadas (particulares y colectivas, Censo 2017).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">11</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">bht</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">[0.00 - 1.00]</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Índice sintético de Bienestar Humano Territorial</strong> (media nacional: 0,6171; RM: 0,5918).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">12</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">bht_bruto</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar bruto</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Valor sintético preliminar del BHT previo a la normalización lineal regional.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">13</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_acc</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">[0.00 - 1.00]</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Macro-dimensión 1: Accesibilidad peatonal a servicios esenciales</strong> (ponderación: 6/18 = 33,33%).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">14</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_acc_bruto</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar bruto</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Puntuación de accesibilidad combinada previa al re-escalamiento min-max.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">15</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">iav</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Áreas Verdes:</strong> Acceso peatonal a plazas y parques públicos (modelo E2SFCA + Tobler).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">16</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">iav_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar m²</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Capacidad de absorción y dotación superficial de áreas verdes en el entorno peatonal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">17</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">icul</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Cultura:</strong> Acceso peatonal a centros culturales, museos y bibliotecas.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">18</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">icul_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar dotación</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Dotación y oferta de recintos culturales comunitarios en el entorno peatonal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">19</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">idep</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Deporte:</strong> Acceso peatonal a recintos y polideportivos públicos.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">20</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">idep_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar dotación</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Capacidad de absorción y recintos deportivos disponibles en el entorno peatonal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">21</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">isal</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Salud:</strong> Acceso peatonal a centros de salud primaria (CESFAM/CECOSF) y hospitales.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">22</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">isal_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar dotación</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Capacidad de absorción medida en boxes de atención y complejidad asistencial.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">23</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">iser</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Servicios:</strong> Acceso peatonal a servicios públicos y trámites del Estado.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">24</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">iser_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar dotación</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Concentración y diversidad de ventanillas de atención pública en el entorno peatonal.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">25</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">ise</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Continuo ≥ 0</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Sub-indicador Educación:</strong> Acceso peatonal a establecimientos de educación básica y media.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">26</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">ise_pre</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar matrícula</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Capacidad de absorción en matrícula y vacantes escolares oficiales reportadas por MINEDUC.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">27</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_amb</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">[0.00 - 1.00]</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Macro-dimensión 4: Calidad ambiental urbana</strong> (ponderación: 2/18 = 11,11%).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">28</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_amb_bruto</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar bruto</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Puntuación ambiental compuesta previa a la normalización min-max.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">29</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_soc</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">[0.00 - 1.00]</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Macro-dimensión 2: Condición socioeconómica y habitacional</strong> (ponderación: 6/18 = 33,33%).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">30</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_soc_bruto</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar bruto</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Puntuación de carencias censales socioeconómicas previa a la normalización.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">31</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_seg</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">[0.00 - 1.00]</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed"><strong>Macro-dimensión 3: Seguridad ciudadana y entorno</strong> (ponderación: 4/18 = 22,22%).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">32</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">dim_seg_bruto</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Escalar bruto</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Tasa delictual georreferenciada previa a la inversión y normalización.</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">33</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e0a3</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal estimada de 0 a 3 años (primera infancia, demanda salas cuna).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">34</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e7a10</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal estimada de 7 a 10 años (primer ciclo básico).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">35</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e4a5</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal estimada de 4 a 5 años (educación preescolar, nivel transición).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">36</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e6a13</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal estimada de 6 a 13 años (educación básica obligatoria).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">37</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e14a18</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal estimada de 14 a 18 años (educación media).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">38</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e4a18</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal consolidada de 4 a 18 años (demanda escolar total).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">39</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e15a24</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal de 15 a 24 años (juventud censal).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">40</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">e19a30</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">float64</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">≥ 0 personas</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Cohorte etaria censal de 19 a 30 años (adultos jóvenes).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">41</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">geometry</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">binary / WKB</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">EPSG:4326</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Geometría poligonal en Well-Known Binary georreferenciada en WGS 84 (omitida en CSV).</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-3 font-mono text-xs text-slate-400 text-center">42</td>
                            <td class="py-2.5 px-3.5 font-mono font-semibold text-slate-900">comuna</td>
                            <td class="py-2.5 px-3.5 font-mono text-xs text-slate-600">string</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 text-center">Sí</td>
                            <td class="py-2.5 px-3.5 font-medium text-xs text-slate-700">Toponimia</td>
                            <td class="py-2.5 px-3.5 text-xs text-slate-600 leading-relaxed">Nombre oficial de la comuna correspondiente a la unidad censal.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- SECCIÓN 5: DESCARGAS, PRUEBA E2E REPRODUCIBLE, INTEROPERABILIDAD Y CITACIÓN -->
        <section id="sec-descargas" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">05</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Distribución multiformato, prueba reproducible de extremo a extremo y citación</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Paridad estructural entre formatos abiertos, verificación criptográfica SHA-256 y ejercicio mínimo reproducible sobre archivos reales.</p>
                    </div>
                </div>
            </div>

            <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-5 font-normal">
                Los cuatro formatos de distribución se compilan de manera simultánea a partir de una misma matriz maestra, garantizando equivalencia exacta en el universo de registros (204.906 manzanas), esquema de atributos y vigencia temporal. Las sumas de verificación criptográfica pueden auditarse en <a href="/download/SHA256SUMS.txt" class="text-slate-900 font-semibold underline hover:text-black">SHA256SUMS.txt</a>.
            </p>

            <!-- Tabla de descargas oficiales -->
            <div class="overflow-x-auto mb-6">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Formato</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Archivo</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Equivalencia de registros</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Tamaño oficial</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50 text-right">Acceso</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-slate-600">
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">GeoParquet 1.1</td>
                            <td class="py-3 px-3.5 font-mono text-xs sm:text-sm text-slate-700">MBHT_2017_Nacional_Manzanas.parquet</td>
                            <td class="py-3 px-3.5 text-slate-600">204.906 manzanas · 42 col. (100%)</td>
                            <td class="py-3 px-3.5 font-mono font-medium text-slate-700">240,9 MB</td>
                            <td class="py-3 px-3.5 text-right">
                                <a href="/download/MBHT_2017_Nacional_Manzanas.parquet" class="text-slate-900 font-bold hover:underline">Descargar</a>
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">OGC GeoPackage</td>
                            <td class="py-3 px-3.5 font-mono text-xs sm:text-sm text-slate-700">MBHT_2017_Nacional_Manzanas.gpkg</td>
                            <td class="py-3 px-3.5 text-slate-600">204.906 manzanas · 42 col. (100%)</td>
                            <td class="py-3 px-3.5 font-mono font-medium text-slate-700">343,9 MB</td>
                            <td class="py-3 px-3.5 text-right">
                                <a href="/download/MBHT_2017_Nacional_Manzanas.gpkg" class="text-slate-900 font-bold hover:underline">Descargar</a>
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Shapefile (.zip)</td>
                            <td class="py-3 px-3.5 font-mono text-xs sm:text-sm text-slate-700">MBHT_2017_Nacional_Manzanas_SHP.zip</td>
                            <td class="py-3 px-3.5 text-slate-600">204.906 manzanas · 42 col. (100%)</td>
                            <td class="py-3 px-3.5 font-mono font-medium text-slate-700">204,9 MB</td>
                            <td class="py-3 px-3.5 text-right">
                                <a href="/download/MBHT_2017_Nacional_Manzanas_SHP.zip" class="text-slate-900 font-bold hover:underline">Descargar</a>
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Tabular CSV</td>
                            <td class="py-3 px-3.5 font-mono text-xs sm:text-sm text-slate-700">MBHT_2017_Nacional_Manzanas.csv</td>
                            <td class="py-3 px-3.5 text-slate-600">204.906 manzanas · 41 col. (100%)</td>
                            <td class="py-3 px-3.5 font-mono font-medium text-slate-700">96,2 MB</td>
                            <td class="py-3 px-3.5 text-right">
                                <a href="/download/MBHT_2017_Nacional_Manzanas.csv" class="text-slate-900 font-bold hover:underline">Descargar</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- PRUEBA DE REPRODUCCIÓN DE EXTREMO A EXTREMO (E2E) -->
            <div id="sec-reproducibilidad" class="bg-slate-50 rounded-xl border border-slate-200 p-5 sm:p-6 mb-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                    <h3 class="text-base sm:text-lg font-bold text-slate-900">Prueba de descarga y reproducción de extremo a extremo (Región de Arica y Parinacota · R15)</h3>
                    <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-white border border-slate-200 text-slate-700">Muestra ligera: 2,37 MB · 3.304 manzanas</span>
                </div>
                <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-4 font-normal">
                    Para verificar empíricamente el contenido sin descargar los 240,9 MB del consolidado nacional, cualquier investigador puede ejecutar la siguiente prueba sobre el recorte oficial de la <strong>Región de Arica y Parinacota (<code class="font-mono text-xs">R15</code>)</strong> (<a href="/download/MBHT_2017_R15_Manzanas.parquet" class="text-slate-900 font-semibold underline hover:text-black">MBHT_2017_R15_Manzanas.parquet</a>). Todos los valores que se muestran a continuación provienen de la lectura directa del archivo físico publicado:
                </p>

                <div class="overflow-x-auto bg-white rounded-lg border border-slate-200 mb-4">
                    <table class="w-full text-left text-xs sm:text-sm border-collapse">
                        <thead>
                            <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Parámetro de control</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Archivo Regional R15 (<code class="font-mono text-[11px]">MBHT_2017_R15_Manzanas.parquet</code>)</th>
                                <th class="py-2.5 px-3.5 text-xs uppercase tracking-wider">Consolidado Nacional (<code class="font-mono text-[11px]">MBHT_2017_Nacional_Manzanas.parquet</code>)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 text-slate-600">
                            <tr>
                                <td class="py-2.5 px-3.5 font-semibold text-slate-900">Tamaño exacto y SHA-256</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">2.482.961 bytes · <span class="text-slate-500">712d1d16193a4dee...9ea6132d134505</span></td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">252.572.936 bytes · <span class="text-slate-500">4a123b83ea1cefa1...c25ea40b9c3fc2a</span></td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3.5 font-semibold text-slate-900">Universo y esquema</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">3.304 manzanas · 42 columnas · 223.679 personas</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs">204.906 manzanas · 42 columnas · 17.482.699 personas</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3.5 font-semibold text-slate-900">Media BHT ponderada por población</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs font-bold text-slate-900">0,4623 (Arica: 0,4588 · Putre: 0,7179 · Camarones: 0,5678 · G. Lagos: 0,5224)</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs font-bold text-slate-900">0,6171 nacional (Región Metropolitana R13: 0,5918 ≈ 0,60)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3.5 font-semibold text-slate-900">Manzana testigo (<code class="font-mono text-xs">15101011001004001</code>)</td>
                                <td class="py-2.5 px-3.5 font-mono text-xs" colspan="2">Comuna: <code class="font-mono">Arica</code> · Población: <code class="font-mono">145</code> · TOB: <code class="font-mono">Medio</code> · <code class="font-mono">bht = 0,3751</code> · <code class="font-mono">dim_acc = 0,6279</code> (<code class="font-mono">isal=0,8691</code>, <code class="font-mono">ise=1,3381</code>, <code class="font-mono">iav=5,8035</code>, <code class="font-mono">idep=0,7744</code>, <code class="font-mono">icul=0,2934</code>, <code class="font-mono">iser=10,3205</code>) · <code class="font-mono">dim_soc = 0,6737</code> · <code class="font-mono">dim_seg = 0,1665</code> · <code class="font-mono">dim_amb = 0,8571</code></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="mb-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                        <span class="text-xs font-semibold text-slate-700">1. Código Python reproducible de verificación mínima:</span>
                        <a href="/download/reproducir_verificacion_r15.py" class="text-xs font-mono font-bold text-slate-900 underline hover:text-black">Descargar script ejecutable autónomo (.py)</a>
                    </div>
                    <pre class="bg-slate-900 text-slate-200 p-4 rounded-xl font-mono text-xs sm:text-[13px] overflow-x-auto leading-relaxed">import hashlib, urllib.request, pandas as pd

url = "https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet"
urllib.request.urlretrieve(url, "MBHT_2017_R15_Manzanas.parquet")

# 1. Verificación criptográfica SHA-256
sha256 = hashlib.sha256(open("MBHT_2017_R15_Manzanas.parquet", "rb").read()).hexdigest()
assert sha256 == "712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505"

# 2. Verificación de esquema físico (3.304 filas x 42 columnas) y manzana testigo
df = pd.read_parquet("MBHT_2017_R15_Manzanas.parquet")
assert df.shape == (3304, 42) and df["id_manzcit"].nunique() == 3304
m = df.loc[df["id_manzcit"] == "15101011001004001"].iloc[0]
assert round(m["bht"], 4) == 0.3751 and round(m["dim_acc"], 4) == 0.6279

# 3. Reproducción del BHT regional ponderado por población (Regla de agregación CIT-UAI)
bht_r15 = (df["bht"] * df["personas"]).sum() / df["personas"].sum()
print(f"Verificación exitosa -> Manzanas: {len(df)} | Población: {int(df['personas'].sum())} | BHT R15: {bht_r15:.4f}")
# Salida esperada: Verificación exitosa -> Manzanas: 3304 | Población: 223679 | BHT R15: 0.4623</pre>
                </div>

                <div class="mb-4">
                    <span class="text-xs font-semibold text-slate-700 block mb-1.5">2. Ejecución local segura en dos pasos (Descarga auditada y ejecución independiente en terminal):</span>
                    <div class="p-3 bg-white rounded-lg border border-slate-200 font-mono text-xs text-slate-800 break-all select-all leading-relaxed">
                        # 1. Descargar script de verificación auditable<br>
                        curl -s -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py<br><br>
                        # 2. Verificar integridad del script mediante SHA-256 publicado<br>
                        echo "7fb25d61a29544e57c17869c6ea3566c68659d003dce9f59dfcd642fbf96a8d0  reproducir_verificacion_r15.py" | sha256sum -c<br><br>
                        # 3. Ejecutar verificación determinista localmente<br>
                        python reproducir_verificacion_r15.py
                    </div>
                </div>

                <div>
                    <span class="text-xs font-semibold text-slate-700 block mb-1.5">3. Registro de salida de la ejecución en consola (Salida real verificada con exit code 0):</span>
                    <pre class="bg-slate-950 text-emerald-400 p-4 rounded-xl font-mono text-[11px] sm:text-xs overflow-x-auto leading-relaxed border border-slate-800">================================================================================
IDE CIT — PROTOCOLO CANÓNICO DE REPRODUCIBILIDAD INDEPENDIENTE
Universidad Adolfo Ibáñez · Centro de Inteligencia Territorial
================================================================================
[*] Descargando paquete oficial R15 desde: https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet ...
    Descargado exitosamente (2,482,961 bytes).

[1/4] Verificación Criptográfica SHA-256 (Integridad de Distribución)...
    [OK] Hash SHA-256 coincidente al 100%: 712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505

[2/4] Validación de Esquema Físico (Paridad 1:1 con Ficha Técnica)...
    Dimensiones observadas en Parquet: 3,304 filas x 42 columnas
    [OK] Cuadratura exacta de universo: 3.304 manzanas censales y 42 columnas físicas.

[3/4] Reproducción Analítica Celda por Celda (Manzana Testigo Arica Centro)...
    Manzana: 15101011001004001 | Comuna: Arica | Personas: 145 | Tipología: Medio
    • isal     =   0.8691 (esperado:   0.8691, diff: 0.000000) -> [OK] Accesibilidad a Salud
    • ise      =   1.3381 (esperado:   1.3381, diff: 0.000000) -> [OK] Accesibilidad a Educación
    • iav      =   5.8035 (esperado:   5.8035, diff: 0.000000) -> [OK] Accesibilidad a Áreas Verdes
    • idep     =   0.7744 (esperado:   0.7744, diff: 0.000000) -> [OK] Accesibilidad a Deporte
    • icul     =   0.2934 (esperado:   0.2934, diff: 0.000000) -> [OK] Accesibilidad a Cultura
    • iser     =  10.3205 (esperado:  10.3205, diff: 0.000000) -> [OK] Accesibilidad a Servicios
    • dim_acc  =   0.6279 (esperado:   0.6279, diff: 0.000000) -> [OK] Macro-dimensión Accesibilidad Peatonal
    • bht      =   0.3751 (esperado:   0.3751, diff: 0.000000) -> [OK] Índice de Bienestar Humano Territorial (BHT)
    [OK] Todos los valores de la manzana testigo coinciden con tolerancia cero.

[4/4] Reproducción del BHT Regional Ponderado por Población...
    Población total modelada en R15: 223,679 habitantes
    BHT regional calculado: 0.4623 (Valor oficial: 0.4623)
    [OK] Agregación demográfica regional reproducida con éxito.

================================================================================
[OK] VEREDICTO: REPRODUCIBILIDAD CIENTÍFICA INDEPENDIENTE CONFIRMADA
================================================================================</pre>
                </div>
            </div>

            <!-- Interoperabilidad y enlaces externos -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 mb-6 text-sm">
                <a href="/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="p-4 bg-slate-50 hover:bg-slate-100 rounded-xl border border-slate-200 transition flex items-center justify-between">
                    <div>
                        <span class="font-bold text-slate-900 block text-sm sm:text-base">Catálogo STAC 1.0.0 (JSON)</span>
                        <span class="text-slate-500 text-xs sm:text-sm">/stac/catalog.json · Acceso directo API</span>
                    </div>
                    <i data-lucide="external-link" class="w-4 h-4 text-slate-400"></i>
                </a>
                <a href="/guia-tecnica#seccion-8" class="p-4 bg-slate-50 hover:bg-slate-100 rounded-xl border border-slate-200 transition flex items-center justify-between">
                    <div>
                        <span class="font-bold text-slate-900 block text-sm sm:text-base">Guía de Reproducibilidad</span>
                        <span class="text-slate-500 text-xs sm:text-sm">Flujo completo en Python, R y QGIS</span>
                    </div>
                    <i data-lucide="arrow-right" class="w-4 h-4 text-slate-400"></i>
                </a>
                <a href="https://github.com/CIT-UAI/mbht2024-metodologia" target="_blank" rel="noopener noreferrer" class="p-4 bg-slate-50 hover:bg-slate-100 rounded-xl border border-slate-200 transition flex items-center justify-between">
                    <div>
                        <span class="font-bold text-slate-900 block text-sm sm:text-base">Repositorio metodológico</span>
                        <span class="text-slate-500 text-xs sm:text-sm">Código Python en GitHub (CIT-UAI)</span>
                    </div>
                    <i data-lucide="external-link" class="w-4 h-4 text-slate-400"></i>
                </a>
            </div>

            <!-- Citación formal -->
            <div class="pt-5 border-t border-slate-100 text-sm">
                <span class="text-slate-800 font-bold block mb-2.5 text-xs sm:text-sm tracking-wide">Citación académica recomendada (BibTeX):</span>
                <pre class="bg-slate-900 text-slate-200 p-4 sm:p-5 rounded-xl font-mono text-xs sm:text-[13px] overflow-x-auto leading-relaxed">@dataset{cit_uai_mbht_2017,
  author       = {{Centro de Inteligencia Territorial (CIT-UAI)}},
  title        = {{Matriz de Bienestar Humano Territorial (MBHT 2017) — Cobertura nacional de manzanas censales}},
  year         = {2018},
  publisher    = {{Universidad Adolfo Ibáñez}},
  address      = {Santiago, Chile},
  howpublished = {Infraestructura de Datos Espaciales IDE CIT},
  url          = {https://ide.cit.uai.cl/ficha-mbht-2017}
}</pre>
            </div>
        </section>

        <!-- SECCIÓN 6: GOBERNANZA DE DATOS, HISTORIAL DE VERSIONES Y REGISTRO DE INCIDENCIAS -->
        <section id="sec-gobernanza" class="scroll-mt-28 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-clean">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
                <div class="flex items-center space-x-3">
                    <span class="w-8 h-8 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center justify-center font-mono">06</span>
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Gobernanza operativa: custodia técnica, historial de versiones y registro de incidencias</h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Asignación nominal de responsables por conjunto de datos, bitácora detallada de entregas y auditoría pública de observaciones.</p>
                    </div>
                </div>
            </div>

            <p class="text-sm sm:text-base text-slate-600 leading-relaxed mb-5 font-normal">
                La gobernanza de la IDE CIT se ejerce mediante tres instrumentos verificables en el propio portal: una tabla de custodia técnica por producto, un historial de versiones con trazabilidad sobre los cambios de esquema y empaquetado, y un registro abierto de incidencias técnicas donde se documentan tanto los hallazgos resueltos como los procesos en curso.
            </p>

            <!-- 6.1 Tabla de Responsables Técnicos por Conjunto de Datos -->
            <h3 class="text-base sm:text-lg font-bold text-slate-900 mb-3">1. Responsables técnicos y custodia por conjunto de datos (Data Stewards)</h3>
            <div class="overflow-x-auto mb-7">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Conjunto de datos</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Unidad técnica responsable (CIT-UAI)</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Versión y estado</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Ciclo de revisión</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Canal de incidencias</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-slate-600">
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">MBHT 2017 — Manzanas Censales (204.906 reg.)</td>
                            <td class="py-3 px-3.5 text-slate-600">Área de Modelación Espacial e Indicadores Urbanos</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">v1.0.3 · Línea base vigente</td>
                            <td class="py-3 px-3.5 text-slate-600">Permanente (cierre censal 2017; mantenimiento de metadatos)</td>
                            <td class="py-3 px-3.5 font-mono text-xs"><a href="mailto:contactocit@uai.cl" class="text-slate-900 underline">contactocit@uai.cl</a></td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Catastro Nacional de Equipamientos 2017 (55.035 reg.)</td>
                            <td class="py-3 px-3.5 text-slate-600">Área de Datos Territoriales y Catastros Sectoriales</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">v1.0.3 · Línea base vigente</td>
                            <td class="py-3 px-3.5 text-slate-600">Anual (contraste con DEIS Minsal, Mineduc y MINVU)</td>
                            <td class="py-3 px-3.5 font-mono text-xs"><a href="mailto:contactocit@uai.cl" class="text-slate-900 underline">contactocit@uai.cl</a></td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Red Vial Caminable con Impedancia Tobler (1.589.595 reg.)</td>
                            <td class="py-3 px-3.5 text-slate-600">Laboratorio de Redes de Transporte y Geomática</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">v1.0.3 · Línea base vigente</td>
                            <td class="py-3 px-3.5 text-slate-600">Semestral (validación topológica de grafos y DEM SRTM)</td>
                            <td class="py-3 px-3.5 font-mono text-xs"><a href="mailto:contactocit@uai.cl" class="text-slate-900 underline">contactocit@uai.cl</a></td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Censo 2024 — Imputaciones Demográficas por Cohortes y Sexo (254.395 unidades)</td>
                            <td class="py-3 px-3.5 text-slate-600">Área de Demografía y Estadística CIT-UAI</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">v1.0.3 · Publicado vigente</td>
                            <td class="py-3 px-3.5 text-slate-600">Insumo demográfico abierto para la futura MBHT 2024 (lanzamiento oficial nov. 2026)</td>
                            <td class="py-3 px-3.5 font-mono text-xs"><a href="mailto:contactocit@uai.cl" class="text-slate-900 underline">contactocit@uai.cl</a></td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-semibold text-slate-900">Planificación Espacial Marina (PEM) — Maritorio (42 capas)</td>
                            <td class="py-3 px-3.5 text-slate-600">Núcleo de Sistemas Socio-Ecológicos y Costeros</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">v1.0.0 · Publicado vigente</td>
                            <td class="py-3 px-3.5 text-slate-600">Anual (sincronización SHOA / SUBPESCA / SBAP)</td>
                            <td class="py-3 px-3.5 font-mono text-xs"><a href="mailto:contactocit@uai.cl" class="text-slate-900 underline">contactocit@uai.cl</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 6.2 Historial de versiones desarrollado -->
            <h3 class="text-base sm:text-lg font-bold text-slate-900 mb-3">2. Historial de versiones y control de cambios del catálogo</h3>
            <div class="overflow-x-auto mb-7">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Versión</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Fecha</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Alcance de la entrega</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Detalle técnico de cambios verificables</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-slate-600">
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-bold text-slate-900">v1.0.3</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-10-15</td>
                            <td class="py-3 px-3.5 font-semibold text-slate-800">Alineación canónica de diccionario (42 col.), STAC S3 y prueba E2E</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Unificación documental entre las 4 macro-dimensiones (<code class="font-mono text-xs">dim_acc</code>, <code class="font-mono text-xs">dim_soc</code>, <code class="font-mono text-xs">dim_seg</code>, <code class="font-mono text-xs">dim_amb</code>) y los 6 sub-indicadores de accesibilidad (<code class="font-mono text-xs">isal</code>.. <code class="font-mono text-xs">iser</code>); homologación de enlaces de activos en <code class="font-mono text-xs">stac/equipamientos.json</code> y adición de prueba reproducible sobre R15.</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-semibold text-slate-900">v1.0.2</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-10-08</td>
                            <td class="py-3 px-3.5 font-semibold text-slate-800">Publicación abierta de Censo 2024 (imputaciones Sprague) y control de calidad</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Publicación para descarga abierta de los insumos demográficos del Censo 2024 con imputaciones de edades simples y sexo desarrolladas por CIT-UAI. Incorporación de sumas criptográficas <code class="font-mono text-xs">SHA256SUMS.txt</code> (208 archivos) y verificador Web Crypto API en el navegador.</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-semibold text-slate-900">v1.0.1</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-06-15</td>
                            <td class="py-3 px-3.5 font-semibold text-slate-800">Confección de paquetes nacionales consolidados y cuadratura regional</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Empaquetado simultáneo en 4 formatos abiertos (GeoParquet, GeoPackage, Shapefile y CSV) para las 16 regiones y el consolidado nacional, verificando suma exacta de 204.906 manzanas, 55.035 equipamientos y 1.589.595 tramos viales.</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-semibold text-slate-900">v1.0.0</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2018-11-20</td>
                            <td class="py-3 px-3.5 font-semibold text-slate-800">Publicación original de la Línea Base MBHT 2017 (Convenio SUBDERE)</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Lanzamiento oficial del modelo de Bienestar Humano Territorial sobre el Censo 2017 (18 indicadores en 4 dimensiones) y despliegue en el visor institucional <code class="font-mono text-xs">matrizbht.cl</code>.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 6.3 Registro público de incidencias y observaciones abiertas -->
            <h3 class="text-base sm:text-lg font-bold text-slate-900 mb-3">3. Registro público de incidencias técnicas y observaciones de auditoría</h3>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">ID</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Fecha</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Componente</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Descripción de la observación y resolución aplicada</th>
                            <th class="py-3 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-700 bg-slate-50">Estado</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-slate-600">
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-bold text-slate-900">INC-2026-01</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-09-28</td>
                            <td class="py-3 px-3.5 font-medium text-slate-800">Inventario regional 2017</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Discrepancia en tabla descriptiva antigua entre sumas parciales y total nacional. Se regeneró la tabla contra los archivos físicos verificando cuadratura exacta (204.906 manzanas, 55.035 equipamientos, 1.589.595 tramos).</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">Cerrada (v1.0.1)</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-bold text-slate-900">INC-2026-02</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-10-14</td>
                            <td class="py-3 px-3.5 font-medium text-slate-800">Nomenclatura dimensional y <code class="font-mono text-xs">tob</code></td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Se unificó la jerarquía canónica (4 macro-dimensiones <code class="font-mono text-xs">dim_acc..dim_amb</code> vs. 6 sub-indicadores <code class="font-mono text-xs">isal..iser</code>) y el dominio de 3 macro-estratos de <code class="font-mono text-xs">tob</code> (<code class="font-mono text-xs">Alto</code>, <code class="font-mono text-xs">Medio</code>, <code class="font-mono text-xs">Bajo</code>) en todos los diccionarios JSON y fichas HTML.</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">Cerrada (v1.0.3)</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-bold text-slate-900">INC-2026-03</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-10-15</td>
                            <td class="py-3 px-3.5 font-medium text-slate-800">Activos STAC y extensiones</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Se homologaron las URL de <code class="font-mono text-xs">stac/equipamientos.json</code> hacia los consolidados nacionales reales y se añadieron las extensiones STAC <code class="font-mono text-xs">projection</code>, <code class="font-mono text-xs">file</code> y <code class="font-mono text-xs">scientific</code>.</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">Cerrada (v1.0.3)</td>
                        </tr>
                        <tr>
                            <td class="py-3 px-3.5 font-mono font-bold text-slate-900">INC-2026-04</td>
                            <td class="py-3 px-3.5 font-mono text-xs text-slate-600">2026-10-15</td>
                            <td class="py-3 px-3.5 font-medium text-slate-800">Deslinde MBHT 2024 vs. Insumos Censo 2024</td>
                            <td class="py-3 px-3.5 text-slate-600 leading-relaxed">Se establece con estricto rigor que la MBHT 2024 no se carga en esta IDE hasta su lanzamiento oficial en noviembre de 2026; la IDE provee de forma abierta los insumos demográficos del Censo 2024 procesados con las imputaciones de cohortes y sexo desarrolladas por el CIT-UAI.</td>
                            <td class="py-3 px-3.5 font-mono text-xs font-semibold text-slate-800">Cerrada (v1.0.3)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

    </div>
    </main>

    [[CANONICAL_FOOTER]]

    [[LLM_GUIDANCE_HTML]]

    <script>
    [[COPILOT_JS_ENGINE]]
    </script>

    <script>
        function renderKaTeX() {
            if (typeof renderMathInElement !== 'undefined') {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '\\[', right: '\\]', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\(', right: '\\)', display: false}
                    ],
                    throwOnError: false
                });
            } else {
                setTimeout(renderKaTeX, 100);
            }
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                if (typeof lucide !== 'undefined') lucide.createIcons();
                renderKaTeX();
            });
        } else {
            if (typeof lucide !== 'undefined') lucide.createIcons();
            renderKaTeX();
        }
    </script>
</body>
</html>
"""

    html = (
        template.replace("[[VERSION]]", version)
        .replace("[[LLM_HEAD_META]]", llm_head_meta)
        .replace("[[CANONICAL_HEADER]]", canonical_header)
        .replace("[[CANONICAL_FOOTER]]", canonical_footer)
        .replace("[[LLM_GUIDANCE_HTML]]", llm_guidance_html)
        .replace("[[COPILOT_JS_ENGINE]]", copilot_js_engine)
        .replace("[[FORMULA_TOBLER_SPEED]]", formula_tobler_speed)
        .replace("[[FORMULA_TOBLER_TIME]]", formula_tobler_time)
        .replace("[[FORMULA_DECAY]]", formula_decay)
        .replace("[[FORMULA_E2SFCA_STEP1]]", formula_e2sfca_step1)
        .replace("[[FORMULA_E2SFCA_STEP2]]", formula_e2sfca_step2)
        .replace("[[FORMULA_WEIGHT]]", formula_weight)
        .replace("[[FORMULA_BHT]]", formula_bht)
    )

    return html


def main() -> int:
    root = find_proyecto_root()
    ide_hub_dir = root / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
    data_dir = ide_hub_dir / "data"
    catalog_json_path = data_dir / "catalogo_ide_cit.json"
    output_html_path = ide_hub_dir / "public" / "ficha-mbht-2017.html"

    with open(catalog_json_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    html_content = generate_ficha_mbht_2017_html(catalog_data)

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Ficha técnica maestra generada exitosamente en: {output_html_path}")
    print(f"  Tamaño: {len(html_content):,} bytes")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
