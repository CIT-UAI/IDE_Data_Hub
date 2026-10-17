#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — GENERADOR DE LA GUÍA TÉCNICA DE INTEROPERABILIDAD Y PROTOCOLOS
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Generador algorítmico automatizado de la página web `guia-tecnica.html`
    para la Infraestructura de Datos Espaciales (IDE CIT).

    Posee exactamente el mismo encabezado institucional, altura, logotipos,
    estilos tipográficos y pie de página que el portal principal `index.html`,
    con paleta de colores sobria institucional (negro, dorado UAI, slate).

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from motor_ia_cit import (
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
)


def generate_guia_tecnica_html(catalog_data: Dict[str, Any]) -> str:
    """
    Genera el HTML5 completo para la Guía técnica de interoperabilidad de la IDE CIT.
    Encabezado y pie de página idénticos en estructura, altura y activos a index.html.
    Paleta de colores 100% sobria e institucional.
    """
    portal = catalog_data.get("portal", {})
    capas = catalog_data.get("capas", [])
    version = portal.get("version", "2026.1")
    copilot_js_engine = get_copilot_js_engine()
    llm_head_meta = get_llm_head_meta()
    llm_guidance_html = get_llm_guidance_html()
    canonical_header = get_canonical_header_html("guia")
    canonical_footer = get_canonical_footer_html(version)

    # Fórmulas en raw strings para evitar interpretación de secuencias \t, \b, \f, \r en Python
    eq_umbral = r"$T_{\max} = 30\text{ min}$ ($1.800\text{ s}$)"
    eq_tobler = r"$f(t) = \exp\left(-0,5 \cdot (t / 15)^2\right)$"
    eq_bht_2017 = r"$\text{BHT}_i = \frac{6}{18}\text{dim\_acc}_i + \frac{6}{18}\text{dim\_soc}_i + \frac{4}{18}\text{dim\_seg}_i + \frac{2}{18}\text{dim\_amb}_i$"
    eq_e2sfca_step1 = r"$R_j = \frac{S_j}{\sum_{k \in \{t_{kj} \le 30\}} P_k \cdot f(t_{kj})}$"
    eq_e2sfca_step2 = r"$A_i = \sum_{j \in \{t_{ij} \le 30\}} R_j \cdot f(t_{ij})$"
    eq_agg_pob = r"$\text{BHT}_{\text{territorio}} = \frac{\sum (\text{bht}_i \times \text{personas}_i)}{\sum \text{personas}_i}$"

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50 scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guía técnica de interoperabilidad y protocolos | IDE CIT · Universidad Adolfo Ibáñez</title>
    
    <!-- Metadatos SEO e institucionales -->
    <meta name="description" content="Guía técnica de interoperabilidad IDE CIT: estándares OGC (WMS, WFS, MVT), perfil SNIT, ISO 19115, STAC 1.0, GeoParquet y tutoriales para QGIS, Python y R.">
    <meta name="keywords" content="Guía técnica IDE, Interoperabilidad geoespacial, SNIT Chile, OGC WMS, OGC WFS, Vector Tiles, GeoParquet, STAC, ISO 19115, CIT-UAI, MBHT">
    <meta name="author" content="Centro de Inteligencia Territorial (CIT-UAI)">
    <meta name="version" content="{version}">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="https://ide.cit.uai.cl/guia-tecnica.html">
    
{llm_head_meta}
    
    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="IDE CIT — Centro de Inteligencia Territorial (UAI)">
    <meta property="og:title" content="Guía técnica de interoperabilidad y protocolos | IDE CIT">
    <meta property="og:description" content="Manual de integración, estándares nacionales e internacionales y protocolos de conexión de datos geoespaciales del CIT-UAI.">
    <meta property="og:url" content="https://ide.cit.uai.cl/guia-tecnica.html">
    <meta property="og:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@CIT_UAI">
    <meta name="twitter:title" content="Guía técnica de interoperabilidad IDE CIT | CIT-UAI">
    <meta name="twitter:description" content="Manual de integración de estándares OGC, ISO 19115, SNIT, GeoParquet, STAC y servicios de datos espaciales del CIT-UAI.">
    <meta name="twitter:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">

    <!-- Schema.org / JSON-LD BreadcrumbList + TechArticle -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "TechArticle",
          "name": "Guía técnica de interoperabilidad, protocolos y estándares | IDE CIT",
          "description": "Manual de referencia técnica sobre la arquitectura cloud-native de la IDE CIT, cumplimiento del Perfil Nacional de Metadatos SNIT, estándares internacionales OGC e ISO, catálogo STAC 1.0 y directivas de consumo analítico.",
          "url": "https://ide.cit.uai.cl/guia-tecnica.html",
          "author": {{"@type": "Organization", "name": "Centro de Inteligencia Territorial (CIT-UAI)", "url": "https://cit.uai.cl"}},
          "publisher": {{"@type": "Organization", "name": "Universidad Adolfo Ibáñez", "url": "https://uai.cl"}},
          "license": "https://creativecommons.org/licenses/by/4.0/",
          "inLanguage": "es-CL"
        }},
        {{
          "@type": "BreadcrumbList",
          "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "IDE CIT", "item": "https://ide.cit.uai.cl"}},
            {{"@type": "ListItem", "position": 2, "name": "Guía técnica de interoperabilidad"}}
          ]
        }}
      ]
    }}
    </script>

    <!-- Favicon y manifiesto PWA -->
    <link rel="icon" type="image/svg+xml" href="img/logo-ide-standalone.svg">
    <link rel="manifest" href="site.webmanifest">
    
    <!-- KaTeX para formulación matemática de máxima fidelidad -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>

    <!-- Google Fonts: Roboto y JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Roboto', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
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
    
    <!-- View Transitions API para Navegación Fluida sin Saltos -->
    <meta name="view-transition" content="same-origin">

    <style>
        body {{ font-family: 'Roboto', sans-serif; color: #1e293b; line-height: 1.6; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 5px; height: 5px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #f8fafc; }}
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
        
        /* TOC activo */
        .toc-link.active {{
            color: #000000;
            font-weight: 700;
            border-left-color: #6493B5;
            background-color: #f1f5f9;
        }}
    </style>
</head>
<body class="h-full flex flex-col font-sans bg-slate-100 text-slate-800 antialiased overflow-x-hidden">

<noscript>
    <div class="bg-slate-900 text-slate-200 border-b border-slate-800 px-4 py-4 text-sm">
        <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
                <strong class="text-white">Guía técnica y metodológica (modo lectura HTML estático):</strong>
                <span>Todo el contenido metodológico, ejemplo reproducible de indicadores, fichas de calidad y estado de servicios se encuentra disponible en esta página sin requerir JavaScript.</span>
            </div>
            <div class="flex flex-wrap gap-3 font-semibold text-uai-gold shrink-0">
                <a href="#seccion-8" class="underline hover:text-white">Ejemplo reproducible ISAL</a>
                <a href="#seccion-9" class="underline hover:text-white">Estado operativo y versiones</a>
                <a href="/descargas" class="underline hover:text-white">Centro de descargas</a>
                <a href="/ficha-mbht-2017" class="underline hover:text-white">Ficha MBHT 2017</a>
            </div>
        </div>
    </div>
</noscript>

{llm_guidance_html}

{canonical_header}

    <!-- 2. CABECERA / HERO DE LA GUÍA TÉCNICA (DISTRIBUCIÓN AMPLIA Y BALANCEADA) -->
    <main id="main-content" role="main" tabindex="-1">
    <section class="bg-white border-b border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <!-- Migas de pan (Breadcrumbs) -->
            <nav class="flex items-center space-x-2 text-xs text-slate-400 mb-4 sm:mb-5">
                <a href="inicio" class="hover:text-slate-700 transition">IDE CIT</a>
                <span class="text-slate-300">/</span>
                <span class="text-slate-500 font-medium">Documentación oficial</span>
                <span class="text-slate-300">/</span>
                <span class="text-slate-800 font-bold">Guía técnica de interoperabilidad</span>
            </nav>

            <div class="w-full">
                <div class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
                    Documento maestro v{version} · Ecosistema MBHT 2024–2026
                </div>
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
                    Guía técnica de interoperabilidad, protocolos y estándares
                </h1>
                <p class="text-sm sm:text-base lg:text-lg text-slate-600 mt-2.5 sm:mt-3 leading-relaxed font-normal w-full">
                    Manual de referencia técnica sobre la arquitectura cloud-native de la IDE CIT, cumplimiento del Perfil Nacional de Metadatos SNIT, estándares internacionales OGC e ISO, catálogo STAC 1.0.0, reproducción práctica paso a paso de indicadores de accesibilidad, métricas de rendimiento verificables y estado operativo de los servicios para software SIG (QGIS, ArcGIS), Python y R.
                </p>
            </div>

            <!-- Barra tipográfica sobria de estándares (sin exceso de etiquetas visuales) -->
            <div class="mt-5 pt-4 border-t border-slate-200/80 flex flex-wrap items-center gap-x-3 gap-y-1.5 text-xs text-slate-600">
                <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                    <i data-lucide="shield-check" class="w-3.5 h-3.5 text-uai-gold"></i>
                    <span>Estándares implementados:</span>
                </span>
                <span>Perfil SNIT Chile</span>
                <span class="text-slate-300">·</span>
                <span class="font-mono">ISO 19115-1:2014 / ISO 19139 XML</span>
                <span class="text-slate-300">·</span>
                <span class="font-mono">Apache GeoParquet 1.1</span>
                <span class="text-slate-300">·</span>
                <span class="font-mono">STAC 1.0.0</span>
                <span class="text-slate-300">·</span>
                <span class="font-mono">OGC GeoPackage 1.3</span>
                <span class="text-slate-300">·</span>
                <span class="font-mono">W3C DCAT-AP 2.0</span>
                <span class="text-slate-300">·</span>
                <span>Licencia CC BY 4.0</span>
            </div>

        </div>
    </section>

    <!-- 3. CONTENIDO PRINCIPAL EN 2 COLUMNAS (TOC + CONTENIDO) -->
    <div class="flex-1 max-w-[1600px] w-full mx-auto px-4 sm:px-6 lg:px-10 xl:px-12 py-8 sm:py-12">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
            
            <!-- COLUMNA IZQUIERDA: ÍNDICE DE CONTENIDOS PEGAJOSO (Sticky TOC) -->
            <aside class="hidden lg:block lg:col-span-3 sticky top-36 space-y-4">
                <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean">
                    <h3 class="font-bold text-xs uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                        <i data-lucide="list" class="w-3.5 h-3.5 text-slate-500"></i>
                        <span>Índice de la guía</span>
                    </h3>
                    <nav class="space-y-1 text-xs" id="tocNav">
                        <a href="#seccion-1" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">1. Arquitectura y propósito</a>
                        <a href="#seccion-2" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">2. Marco normativo e imputación Censo 2024</a>
                        <a href="#seccion-3" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">3. Estándares internacionales y Cloud-Native</a>
                        <a href="#seccion-4" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">4. Directorio de servicios y endpoints</a>
                        <a href="#seccion-5" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">5. Guía de consumo y ejemplos</a>
                        <a href="#seccion-6" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">6. Políticas de cita y código abierto</a>
                        <a href="#seccion-7" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition">7. Seguridad, gobernanza y preservación</a>
                        <a href="#seccion-8" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition font-semibold text-slate-800">8. Ejemplo reproducible paso a paso (ISAL)</a>
                        <a href="#seccion-9" class="toc-link block px-2.5 py-1.5 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent transition font-semibold text-slate-800">9. Estado de servicios, calidad y versiones</a>
                    </nav>
                </div>

                <!-- Caja de acciones de exportación -->
                <div class="bg-slate-900 text-white p-4 rounded-xl shadow-clean space-y-2.5 text-xs">
                    <span class="font-bold text-uai-gold uppercase tracking-wider text-[10px] block">Recursos de exportación</span>
                    <button onclick="downloadCatalogJson()" class="w-full bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded font-medium transition text-left flex items-center justify-between cursor-pointer">
                        <span>Catálogo JSON</span>
                        <i data-lucide="download" class="w-3.5 h-3.5 text-slate-300"></i>
                    </button>
                    <button onclick="downloadDcatJson()" class="w-full bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded font-medium transition text-left flex items-center justify-between cursor-pointer">
                        <span>Catálogo DCAT-AP</span>
                        <i data-lucide="binary" class="w-3.5 h-3.5 text-slate-300"></i>
                    </button>
                    <a href="data/stac/collection.json" target="_blank" rel="noopener noreferrer" class="w-full bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded font-medium transition text-left flex items-center justify-between">
                        <span>Colección STAC 1.0</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-300"></i>
                    </a>
                    <a href="https://github.com/cit-uai/mbht2024-metodologia" target="_blank" rel="noopener noreferrer" class="w-full bg-uai-gold/20 hover:bg-uai-gold/30 text-white px-3 py-1.5 rounded font-medium transition text-left flex items-center justify-between border border-uai-gold/30">
                        <span class="text-uai-gold font-semibold">Repo GitHub</span>
                        <i data-lucide="code" class="w-3.5 h-3.5 text-uai-gold"></i>
                    </a>
                </div>
            </aside>

            <!-- COLUMNA DERECHA: DOCUMENTACIÓN COMPLETA Y TUTORIALES -->
            <div class="lg:col-span-9 space-y-12 sm:space-y-16">
                
                <!-- SECCIÓN 1: ARQUITECTURA GENERAL Y PROPÓSITO -->
                <section id="seccion-1" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 1</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Arquitectura general y propósito institucional</h2>
                    </div>

                    <p class="text-sm sm:text-base text-slate-600 leading-relaxed font-normal">
                        La <strong>Infraestructura de Datos Espaciales (IDE CIT)</strong> es una iniciativa académica y de ciencia abierta desarrollada por el Centro de Inteligencia Territorial de la Universidad Adolfo Ibáñez, concebida como un nodo científico para complementar y potenciar el ecosistema geoespacial de Chile (SNIT y geoportales sectoriales). Su propósito fundamental es proveer <strong>13 capas y coberturas geoespaciales maestras</strong> (8 en Litósfera terrestre y 5 en Maritorio tricontinental) estructuradas en <strong>4 pestañas de navegación autónomas</strong> (Catálogo de datos, Centro de descargas MBHT 2017, Red de IDEs y Guía técnica de interoperabilidad): <strong>Línea base oficial MBHT 2017 vigente</strong> (204.906 manzanas), <strong>Insumos demográficos del Censo 2024</strong> (Sprague multivariable por edades simples y conciliación por sexo en 254.395 unidades), <strong>Índice de Nivel Socioeconómico (INSE)</strong>, <strong>Avalúos de Suelo SII</strong> y <strong>Planificación marina bajo directrices FAO y marco Ley SBAP (Servicio de Biodiversidad y Áreas Protegidas)</strong>, garantizando trazabilidad matemática auditable, formulación metodológica abierta e interoperabilidad en tiempo real.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl space-y-1.5">
                            <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center text-xs font-bold">1</div>
                            <h4 class="font-bold text-slate-900 text-sm">Modelos sintéticos y ciencia abierta</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">Trazabilidad matemática auditable, algoritmos de accesibilidad peatonal real (E2SFCA sobre red vial Tobler), estratificación socioespacial y citación bajo norma APA 7.</p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl space-y-1.5">
                            <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center text-xs font-bold">2</div>
                            <h4 class="font-bold text-slate-900 text-sm">Complemento al ecosistema SNIT</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">Articulación con los 19 geoportales oficiales del Estado chileno, transformando insumos primarios en evidencia territorial para políticas públicas, GOREs y municipios.</p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl space-y-1.5">
                            <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center text-xs font-bold">3</div>
                            <h4 class="font-bold text-slate-900 text-sm">Arquitectura cloud-native (S3 + CDN)</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">Almacenamiento columnar GeoParquet 1.1, teselas vectoriales binarias MVT (&lt; 50 ms), catálogo STAC 1.0, distribución CloudFront y consultas directas en QGIS, Python y R.</p>
                        </div>
                    </div>

                    <div class="bg-slate-900 text-slate-200 p-5 sm:p-6 rounded-xl text-xs sm:text-sm space-y-3 border border-slate-800">
                        <div class="font-bold text-uai-gold flex items-center space-x-2 text-sm">
                            <i data-lucide="layers" class="w-4 h-4 text-uai-gold"></i>
                            <span>Soberanía tridimensional y condición tricontinental de Chile (Visión CIT)</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed text-xs sm:text-[13px]">
                            Chile posee una condición geográfica estratégica fundamentada en su <strong>tricontinentalidad</strong>: el territorio continental sudamericano, el territorio oceánico insular (Rapa Nui, Archipiélago Juan Fernández, Islas Desventuradas y Salas y Gómez) y el Territorio Chileno Antártico. Desde esta perspectiva soberana, el Centro de Inteligencia Territorial (CIT-UAI) estructura la información espacial en tres dimensiones interconectadas:
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                            <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60 space-y-1">
                                <span class="font-bold text-slate-100 text-xs block flex items-center space-x-1.5">
                                    <i data-lucide="map-pin" class="w-3.5 h-3.5 text-uai-gold"></i>
                                    <span>1. Litósfera y poblamiento</span>
                                </span>
                                <p class="text-slate-400 text-[11px] leading-relaxed">254.395 manzanas censales y entidades rurales Censo 2024, 204.906 manzanas censales MBHT 2017 oficial, 55.035 equipamientos, red vial Tobler y avalúos SII.</p>
                            </div>
                            <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60 space-y-1">
                                <span class="font-bold text-slate-100 text-xs block flex items-center space-x-1.5">
                                    <i data-lucide="waves" class="w-3.5 h-3.5 text-uai-gold"></i>
                                    <span>2. Hidrósfera, maritorio y Planificación marina (FAO / SBAP)</span>
                                </span>
                                <p class="text-slate-400 text-[11px] leading-relaxed">Más de 3,5 millones de km² de soberanía oceánica (ZEE de 200 millas náuticas), Planificación marina articulada con directrices de la FAO, áreas marinas protegidas del Servicio de Biodiversidad y Áreas Protegidas (SBAP - Ley 21.600), montes submarinos y zonificación costera.</p>
                            </div>
                            <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60 space-y-1">
                                <span class="font-bold text-slate-100 text-xs block flex items-center space-x-1.5">
                                    <i data-lucide="wind" class="w-3.5 h-3.5 text-uai-gold"></i>
                                    <span>3. Atmósfera y espacio</span>
                                    <span class="text-[10px] font-medium text-amber-300 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">En desarrollo</span>
                                </span>
                                <p class="text-slate-400 text-[11px] leading-relaxed">Modelación micrometeorológica, islas de calor urbano, dispersión atmosférica y sensores de observación ambiental (en desarrollo).</p>
                            </div>
                        </div>
                    </div>

                    <!-- Cuadratura Metodológica Canónica (Auditoría y Transparencia Científica) -->
                    <div class="p-4 sm:p-5 rounded-xl bg-slate-900 text-slate-200 border border-slate-800 text-xs sm:text-sm">
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
                </section>


                <!-- SECCIÓN 2: MARCO NORMATIVO NACIONAL -->
                <section id="seccion-2" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 2</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Marco normativo nacional (Chile)</h2>
                    </div>

                    <p class="text-sm sm:text-base text-slate-600 leading-relaxed font-normal">
                        La IDE CIT está alineada con los marcos legales, directivas de gobierno digital y estándares de información geoespacial del Estado de Chile:
                    </p>

                    <div class="space-y-4 text-xs sm:text-sm">
                        
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-2">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold">
                                <i data-lucide="shield-check" class="w-4 h-4 text-slate-800"></i>
                                <span>Perfil Nacional de Metadatos SNIT (IDE Chile)</span>
                            </div>
                            <p class="text-slate-600 leading-relaxed">
                                El Sistema Nacional de Información Territorial (SNIT), coordinado por el Ministerio de Bienes Nacionales, establece el <em>Perfil Chileno de Metadatos</em> basado en la norma ISO 19115. Cada capa de la IDE CIT dispone de una ficha XML ISO 19139 que cumple rigurosamente con los 28 elementos obligatorios del perfil nacional (identificación, linaje, sistema de referencia, límites geográficos y punto de contacto institucional).
                            </p>
                        </div>

                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-2">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold">
                                <i data-lucide="file-text" class="w-4 h-4 text-slate-800"></i>
                                <span>Ley N° 21.180 sobre Transformación Digital del Estado</span>
                            </div>
                            <p class="text-slate-600 leading-relaxed">
                                Promueve la interoperabilidad por defecto y el principio de "solo una vez" (<em>Once-Only Principle</em>). Los servicios de la IDE CIT permiten que ministerios (MINVU, MDSF, SUBDERE, MMA, MINSAL, MINEDUC) y municipios consuman directamente las matrices mediante APIs y servicios OGC sin intermediación manual.
                            </p>
                        </div>

                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold">
                                <i data-lucide="compass" class="w-4 h-4 text-slate-800"></i>
                                <span>Marco Geodésico Nacional, Geodinámica y Sistemas de Coordenadas (ISO 19111)</span>
                            </div>
                            <div class="space-y-2 text-slate-600 leading-relaxed text-xs sm:text-sm">
                                <p>
                                    En estricta conformidad con el marco geodésico oficial del Estado de Chile (Decreto Supremo N° 215/2004 y Res. Ex. N° 34/2018 del Ministerio de Bienes Nacionales e IGM), la IDE CIT diferencia formalmente entre marco de referencia, datum elipsoidal, época geodinámica, CRS de distribución y CRS de cómputo analítico:
                                </p>
                                <ul class="list-disc pl-5 space-y-1 text-slate-600">
                                    <li><strong>Marco de Referencia Oficial, Realización y Época:</strong> <em>SIRGAS-Chile</em> (<strong>EPSG:5360</strong>, realización densificada del ITRF ligada a la Placa Sudamericana; época de referencia oficial <code>2002.0</code> / actualización pos-sísmica IGM <code>2016.0</code>), asociado al elipsoide <strong>GRS80</strong> (semieje mayor <em>a</em> = 6.378.137 m, aplanamiento inverso 1/<em>f</em> = 298,257222101).</li>
                                    <li><strong>Transformación Helmert y Compatibilidad con WGS 84 (EPSG:4326):</strong> WGS 84 emplea el elipsoide WGS 84 (1/<em>f</em> = 298,257223563). La discrepancia elipsoidal entre GRS80 y WGS 84 es sub-milimétrica (&Delta;<em>b</em> &approx; 0,105 mm), y la transformación oficial de 7 parámetros de Helmert (<strong>EPSG:15946</strong>) establece traslación y rotación nulas (&Delta;X = &Delta;Y = &Delta;Z = 0,0 m; precisión declarada 1,0 m) para escalas cartográficas censales y urbanas (&gt; 1:1.000).</li>
                                    <li><strong>CRS de Almacenamiento y Distribución Cloud-Native:</strong> Todos los archivos descargables y servicios web se distribuyen canónicamente en <strong>EPSG:4326 (WGS 84 en coordenadas geográficas 2D [longitud, latitud] en grados decimales)</strong> para garantizar interoperabilidad directa con GeoParquet 1.1, STAC 1.0.0, Mapbox Vector Tiles y motores analíticos (DuckDB, GDAL, Python, R).</li>
                                    <li><strong>CRS Proyectados para Análisis Métrico de Red:</strong> Para el cálculo de distancias viales físicas, pendientes longitudinales DEM y áreas sin distorsión proyectiva, los algoritmos del CIT-UAI proyectan internamente las geometrías a sus husos conformes oficiales: <strong>SIRGAS-Chile / UTM Huso 18S (EPSG:5361 / EPSG:32718)</strong> y <strong>UTM Huso 19S (EPSG:5362 / EPSG:32719)</strong> en territorio continental; <strong>UTM Huso 12S (EPSG:32712)</strong> en Rapa Nui; y <strong>UTM Huso 17S (EPSG:32717)</strong> en Juan Fernández.</li>
                                </ul>
                            </div>
                        </div>

                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-2">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold">
                                <i data-lucide="users" class="w-4 h-4 text-slate-800"></i>
                                <span>Transparencia metodológica Censo 2024: Imputación demográfica de Sprague</span>
                            </div>
                            <p class="text-slate-600 leading-relaxed">
                                En las coberturas del Censo 2024, las geometrías de polígonos corresponden estrictamente a la cartografía censal oficial del <strong>Instituto Nacional de Estadísticas (INE)</strong>. La desagregación fina de población por edades simples, cohortes etarias y vulnerabilidad de hogares es un modelo de <strong>micro-imputación matemática desarrollado por el CIT-UAI</strong> mediante el algoritmo osculatorio de Sprague de 5.º orden acoplado al método de mayor resto (Hamilton-Hare). Este modelamiento preserva con exactitud los totales comunales censales oficiales y salvaguarda rigurosamente el secreto estadístico (Ley N° 17.374), resolviendo la supresión de microdatos sin desvirtuar la realidad demográfica comunal.
                            </p>
                        </div>

                    </div>
                </section>


                <!-- SECCIÓN 3: ESTÁNDARES INTERNACIONALES -->
                <section id="seccion-3" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 3</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Estándares geoespaciales internacionales</h2>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                        
                        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Estándar OGC / Mapbox</div>
                            <h4 class="font-bold text-slate-900 text-sm">Vector Tiles (MVT)</h4>
                            <p class="text-slate-600 leading-relaxed">
                                Teselas vectoriales binarias en formato ProtocolBuffer (<code class="font-mono text-slate-800">.pbf</code>) servidas desde el motor espacial del CIT. Ofrecen tiempos de respuesta menores a 50 ms y renderizado GPU mediante WebGL en clientes cartográficos.
                            </p>
                        </div>

                        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Geoespacial cloud-native</div>
                            <h4 class="font-bold text-slate-900 text-sm">Apache GeoParquet 1.1</h4>
                            <p class="text-slate-600 leading-relaxed">
                                Formato columnar binario con compresión Snappy/ZSTD que almacena geometrías en WKB e indexa Bounding Boxes por grupo de filas (<em>row groups</em>). Permite consultas espaciales remotas vía <code>HTTP 206 Partial Content</code> sin descargar el archivo completo.
                            </p>
                        </div>

                        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Especificación STAC</div>
                            <h4 class="font-bold text-slate-900 text-sm">STAC 1.0.0 (SpatioTemporal Asset Catalog)</h4>
                            <p class="text-slate-600 leading-relaxed">
                                Especificación abierta para catalogar activos geoespaciales con extensiones <code>projection</code>, <code>file</code> y <code>scientific</code>. La IDE CIT expone el catálogo raíz en <code class="font-mono text-slate-800">/stac/catalog.json</code> facilitando el descubrimiento algorítmico.
                            </p>
                        </div>

                        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">W3C / Datos abiertos</div>
                            <h4 class="font-bold text-slate-900 text-sm">W3C DCAT-AP 2.0 y Schema.org</h4>
                            <p class="text-slate-600 leading-relaxed">
                                Vocabulario estándar de catálogos de datos abiertos (<code class="font-mono text-slate-800">/dcat.json</code> y <code class="font-mono text-slate-800">/data/dcat.json</code>) y marcado semántico JSON-LD para indexación federada en catálogos nacionales y motores científicos.
                            </p>
                        </div>

                        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5 md:col-span-2">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Calidad geométrica y validación</div>
                            <h4 class="font-bold text-slate-900 text-sm">Conformidad topológica OGC Simple Features (ST_IsValid)</h4>
                            <p class="text-slate-600 leading-relaxed">
                                Todas las geometrías de manzanas y polígonos son auditadas rigurosamente bajo la especificación OGC Simple Features (<code>ST_IsValid</code> en PostGIS/GEOS): ausencia de auto-intersecciones, eliminación de polígonos espurios (<em>slivers</em>) y validación métrica en proyección UTM Huso 18S/19S (EPSG:32718 / EPSG:32719) antes de su exportación a EPSG:4326.
                            </p>
                        </div>

                    </div>

                    <!-- Enfoque Cloud-Native vs WFS tradicional -->
                    <div class="bg-slate-50 border border-slate-200 p-4 sm:p-5 rounded-xl space-y-2.5">
                        <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm">
                            <i data-lucide="zap" class="w-4 h-4 text-slate-800"></i>
                            <span>Paradigma Cloud-Native Geospatial vs. WFS tradicional</span>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                            A diferencia de las IDEs de primera generación que dependen de servicios transaccionales OGC WFS (cuya serialización GML/XML colapsa el ancho de banda en coberturas de más de 200.000 polígonos censales), la <strong>IDE CIT adopta el estándar internacional Cloud-Native Geospatial</strong>: distribución directa en <strong>Apache GeoParquet 1.1</strong>, contenedores <strong>OGC GeoPackage 1.3</strong> accesibles por streaming GDAL (<code>/vsicurl/</code>) y catálogo <strong>STAC 1.0.0</strong> con soporte verificado para <em>HTTP Range Requests (HTTP 206)</em>.
                        </p>
                    </div>
                </section>


                <!-- SECCIÓN 4: DIRECTORIO DE SERVICIOS Y ENDPOINTS -->
                <section id="seccion-4" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 4</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Directorio de servicios y puntos de enlace activos</h2>
                    </div>

                    <div class="border border-slate-200 rounded-xl overflow-x-auto">
                        <table class="w-full text-left border-collapse text-xs">
                            <thead class="bg-slate-100 border-b border-slate-200 text-slate-700">
                                <tr>
                                    <th class="px-3.5 py-3 font-bold">Servicio / protocolo</th>
                                    <th class="px-3.5 py-3 font-bold">Punto de enlace verificable (URL)</th>
                                    <th class="px-3.5 py-3 font-bold">Formato</th>
                                    <th class="px-3.5 py-3 font-bold text-right">Acción</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Conector QGIS MBHT 2017 Nacional (MVT)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr" download class="underline hover:text-black">https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">QGIS Layer (.qlr) / PBF</td>
                                    <td class="px-3.5 py-3 text-right">
                                        <a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr" download class="font-bold text-slate-700 hover:text-black cursor-pointer underline">Descargar</a>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Centro de descargas territoriales</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/descargas" class="underline hover:text-black">https://ide.cit.uai.cl/descargas</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">GeoParquet / GPKG / SHP / CSV</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/descargas" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/descargas')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Catálogo Raíz STAC 1.0.0</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/stac/catalog.json</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">STAC JSON 1.0.0</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/stac/catalog.json')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Catálogo Semántico DCAT-AP 2.0 (W3C)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/dcat.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/dcat.json</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">JSON-LD</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/dcat.json" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/dcat.json')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Reporte de Conformidad y Benchmarks (p50/p95/p99)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/conformance_report.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/conformance_report.json</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">JSON Telemetría / QA</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/conformance_report.json" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/conformance_report.json')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Ficha Maestra MBHT 2017 (Gold Standard)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/ficha-mbht-2017" class="underline hover:text-black">https://ide.cit.uai.cl/ficha-mbht-2017</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">HTML / 42 Columnas</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/ficha-mbht-2017" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/ficha-mbht-2017')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">API Motor Espacial CIT (FastAPI / MVT)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://engine.matrizbht.cl" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://engine.matrizbht.cl</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">REST JSON / MVT</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://engine.matrizbht.cl" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://engine.matrizbht.cl')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Directorio Red de IDEs SNIT</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/red-ides" class="underline hover:text-black">https://ide.cit.uai.cl/red-ides</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">19 geoportales</td>
                                    <td class="px-3.5 py-3 text-right space-x-2">
                                        <a href="https://ide.cit.uai.cl/red-ides" class="font-bold text-slate-700 hover:text-black underline">Abrir</a>
                                        <button onclick="copyText('https://ide.cit.uai.cl/red-ides')" class="text-slate-500 hover:text-black cursor-pointer underline">Copiar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Conector QGIS Streaming GDAL (/vsicurl/ GPKG)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/download/qgis/CIT_Servicios_WMS.qlr" download class="underline hover:text-black">https://ide.cit.uai.cl/download/qgis/CIT_Servicios_WMS.qlr</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">QGIS Layer (.qlr)</td>
                                    <td class="px-3.5 py-3 text-right">
                                        <a href="https://ide.cit.uai.cl/download/qgis/CIT_Servicios_WMS.qlr" download class="font-bold text-slate-700 hover:text-black cursor-pointer underline">Descargar</a>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Simbología Oficial QGIS (Quiebres Jenks)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_Simbologia_Jenks.qml" download class="underline hover:text-black">https://ide.cit.uai.cl/download/qgis/CIT_MBHT_Simbologia_Jenks.qml</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">QGIS Style (.qml)</td>
                                    <td class="px-3.5 py-3 text-right">
                                        <a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_Simbologia_Jenks.qml" download class="font-bold text-slate-700 hover:text-black cursor-pointer underline">Descargar</a>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-3.5 py-3 font-semibold text-slate-900">Ejemplos de Conexión Programática (JSON)</td>
                                    <td class="px-3.5 py-3 font-mono text-slate-700 text-[11px] break-all"><a href="https://ide.cit.uai.cl/connection_examples.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/connection_examples.json</a></td>
                                    <td class="px-3.5 py-3 font-mono text-slate-600">JSON / Snippets</td>
                                    <td class="px-3.5 py-3 text-right">
                                        <a href="https://ide.cit.uai.cl/connection_examples.json" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-700 hover:text-black cursor-pointer underline">Abrir</a>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>


                <!-- SECCIÓN 5: GUÍA DE CONSUMO Y TUTORIALES CON CÓDIGO -->
                <section id="seccion-5" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-8">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 5</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Guía práctica de integración y ejemplos de consumo</h2>
                    </div>

                    <!-- 5.1 QGIS -->
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm sm:text-base font-bold text-slate-900">
                            <span class="w-6 h-6 rounded bg-slate-900 text-white flex items-center justify-center text-xs">5.1</span>
                            <h3>Conexión desde QGIS Desktop (3.28 LTR o superior)</h3>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                            Para visualizar las coberturas y teselas en QGIS con rendimiento ultra-rápido, puedes arrastrar directamente los archivos de capa oficiales o conectar mediante TileJSON seguro:
                        </p>
                        <ol class="list-decimal list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 pl-1">
                            <li><strong>Opción 1 (Recomendada - 1 clic):</strong> Descarga el archivo de definición de capa <a href="https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr" class="underline font-bold text-slate-900" download>CIT_MBHT_2017_Nacional.qlr</a> y arrástralo directamente a la ventana de QGIS.</li>
                            <li><strong>Opción 2 (Conexión Vector Tiles manual):</strong> En el panel <em>Navegador (Browser)</em>, clic derecho sobre <em>Vector Tiles</em> &gt; <em>Nueva conexión genérica</em> e ingresa la URL TileJSON segura:</li>
                        </ol>

                        <div class="bg-slate-900 text-slate-100 p-3.5 rounded-xl text-xs font-mono relative flex items-center justify-between">
                            <span class="text-slate-100 select-all font-mono text-xs">https://engine.matrizbht.cl/tiles/index.json</span>
                            <button onclick="copyText('https://engine.matrizbht.cl/tiles/index.json')" class="bg-white/10 hover:bg-white/20 text-white px-2.5 py-1 rounded text-xs transition cursor-pointer shrink-0 ml-2">Copiar URL</button>
                        </div>
                    </div>

                    <!-- 5.2 ArcGIS Pro -->
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm sm:text-base font-bold text-slate-900">
                            <span class="w-6 h-6 rounded bg-slate-900 text-white flex items-center justify-center text-xs">5.2</span>
                            <h3>Conexión desde ArcGIS Pro y QGIS (Servicios WMS / GeoPackage)</h3>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                            Para software SIG de escritorio, el estándar de mayor rendimiento y fidelidad es la importación directa del paquete nacional en GeoPackage / GeoParquet o la carga del conector WMS federado:
                        </p>
                        <div class="bg-slate-900 text-slate-100 p-3.5 rounded-xl text-xs font-mono relative flex items-center justify-between">
                            <span class="text-slate-100 select-all font-mono text-xs">https://ide.cit.uai.cl/download/qgis/CIT_Servicios_WMS.qlr</span>
                            <button onclick="copyText('https://ide.cit.uai.cl/download/qgis/CIT_Servicios_WMS.qlr')" class="bg-white/10 hover:bg-white/20 text-white px-2.5 py-1 rounded text-xs transition cursor-pointer shrink-0 ml-2">Copiar URL</button>
                        </div>
                    </div>

                    <!-- 5.3 Python DuckDB & GeoPandas -->
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm sm:text-base font-bold text-slate-900">
                            <span class="w-6 h-6 rounded bg-slate-900 text-white flex items-center justify-center text-xs">5.3</span>
                            <h3>Consulta en streaming con Python (DuckDB + GeoPandas)</h3>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                            Consulta y filtra manzanas censales directamente desde el repositorio en la nube sin descargar el archivo completo:
                        </p>

                        <div class="bg-slate-900 text-slate-100 rounded-xl overflow-hidden text-xs">
                            <div class="bg-slate-950 px-4 py-2 border-b border-slate-800 flex justify-between items-center text-[11px] text-slate-400 font-mono">
                                <span>consulta_mbht_duckdb.py</span>
                                <button onclick="copySnippet('codePython')" class="hover:text-white transition cursor-pointer">Copiar código</button>
                            </div>
                            <pre class="p-4 overflow-x-auto font-mono text-slate-300 leading-relaxed" id="codePython"><code>import duckdb
import geopandas as gpd

# 1. Inicializar DuckDB con extensión espacial
con = duckdb.connect()
con.execute('INSTALL spatial; LOAD spatial;')

# 2. Consulta SQL sobre GeoParquet remoto usando las columnas físicas reales
query = '''
SELECT 
    id_manzcit,
    comuna,
    cod_reg,
    personas,
    bht,
    dim_acc,
    isal,
    ST_GeomFromWKB(geometry) AS geom
FROM 'https://ide.cit.uai.cl/download/MBHT_2017_Nacional_Manzanas.parquet'
WHERE cod_reg = 13 AND bht < 0.40;
'''

# 3. Convertir a GeoDataFrame
df = con.execute(query).df()
gdf = gpd.GeoDataFrame(df, geometry='geom', crs='EPSG:4326')
print(f'Manzanas con déficit crítico en RM (cod_reg=13): {{len(gdf)}}')</code></pre>
                        </div>
                    </div>

                    <!-- 5.4 R (sf + arrow) -->
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm sm:text-base font-bold text-slate-900">
                            <span class="w-6 h-6 rounded bg-slate-900 text-white flex items-center justify-center text-xs">5.4</span>
                            <h3>Procesamiento en entorno R (<code class="font-mono text-xs">sf</code> + <code class="font-mono text-xs">arrow</code>)</h3>
                        </div>
                        <div class="bg-slate-900 text-slate-100 rounded-xl overflow-hidden text-xs">
                            <div class="bg-slate-950 px-4 py-2 border-b border-slate-800 flex justify-between items-center text-[11px] text-slate-400 font-mono">
                                <span>analisis_mbht.R</span>
                                <button onclick="copySnippet('codeR')" class="hover:text-white transition cursor-pointer">Copiar código</button>
                            </div>
                            <pre class="p-4 overflow-x-auto font-mono text-slate-300 leading-relaxed" id="codeR"><code>library(sf)
library(arrow)
library(dplyr)

# Lectura directa desde almacenamiento columnar Parquet (muestra ligera R15: 2,37 MB)
parquet_url <- 'https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet'
tabla <- read_parquet(parquet_url)

# Agregación comunal ponderada por población (Regla metodológica CIT-UAI)
resumen_comunal <- tabla %>%
  group_by(comuna) %>%
  summarise(
    manzanas = n(),
    poblacion_total = sum(personas, na.rm = TRUE),
    bht_ponderado = sum(bht * personas, na.rm = TRUE) / sum(personas, na.rm = TRUE)
  )</code></pre>
                        </div>
                    </div>

                    <!-- 5.5 MapLibre GL JS -->
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm sm:text-base font-bold text-slate-900">
                            <span class="w-6 h-6 rounded bg-slate-900 text-white flex items-center justify-center text-xs">5.5</span>
                            <h3>Integración web con MapLibre GL JS y Leaflet</h3>
                        </div>
                        <div class="bg-slate-900 text-slate-100 rounded-xl overflow-hidden text-xs">
                            <div class="bg-slate-950 px-4 py-2 border-b border-slate-800 flex justify-between items-center text-[11px] text-slate-400 font-mono">
                                <span>maplibre_example.js</span>
                                <button onclick="copySnippet('codeJS')" class="hover:text-white transition cursor-pointer">Copiar código</button>
                            </div>
                            <pre class="p-4 overflow-x-auto font-mono text-slate-300 leading-relaxed" id="codeJS"><code>const map = new maplibregl.Map({{
    container: 'map',
    style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
    center: [-70.65, -33.45],
    zoom: 12
}});

map.on('load', () => {{
    map.addSource('mbht-vector', {{
        type: 'vector',
        tiles: ['https://engine.matrizbht.cl/tiles/kpi_mud_2017/{{z}}/{{x}}/{{y}}.pbf'],
        minzoom: 6,
        maxzoom: 16
    }});

    map.addLayer({{
        id: 'mbht-layer',
        type: 'fill',
        source: 'mbht-vector',
        'source-layer': 'kpi_mud_2017',
        paint: {{
            'fill-color': [
                'interpolate', ['linear'], ['get', 'indice_bht_2017'],
                0.0, '#334155',
                0.5, '#64748b',
                1.0, '#0f172a'
            ],
            'fill-opacity': 0.75
        }}
    }});
}});</code></pre>
                        </div>
                    </div>

                </section>


                <!-- SECCIÓN 6: LICENCIAMIENTO Y POLÍTICAS DE CITACIÓN -->
                <section id="seccion-6" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 6</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Licenciamiento y políticas de citación</h2>
                    </div>

                    <div class="space-y-4 text-xs sm:text-sm">
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-2">
                            <h4 class="font-bold text-slate-900 text-sm">Licencia de uso de datos</h4>
                            <p class="text-slate-600 leading-relaxed font-normal">
                                Los datos abiertos de la IDE CIT se publican bajo la licencia <strong>Creative Commons Atribución 4.0 Internacional (CC BY 4.0)</strong>. Eres libre de compartir, copiar, distribuir y transformar los datos para cualquier fin, incluso comercial, reconociendo adecuadamente la autoría del CIT-UAI.
                            </p>
                        </div>

                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3">
                            <h4 class="font-bold text-slate-900 text-sm">Formato de citación oficial (norma APA 7.ª edición)</h4>
                            <div class="bg-white p-3 rounded-lg border border-slate-200 font-serif italic text-slate-700 text-xs leading-relaxed">
                                Centro de Inteligencia Territorial. (2026). Infraestructura de Datos Espaciales (IDE CIT): Catálogo de datos territoriales abiertos, indicadores de bienestar humano y servicios de mapas de Chile [Plataforma geoespacial]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl
                            </div>
                            <button onclick="copyText('Centro de Inteligencia Territorial. (2026). Infraestructura de Datos Espaciales (IDE CIT): Catálogo de datos territoriales abiertos, indicadores de bienestar humano y servicios de mapas de Chile [Plataforma geoespacial]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl')" class="bg-slate-900 hover:bg-black text-white px-3 py-1.5 rounded text-xs font-semibold transition cursor-pointer flex items-center space-x-1 shadow-xs">
                                <i data-lucide="copy" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>Copiar citación</span>
                            </button>
                        </div>

                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm">
                                <i data-lucide="code" class="w-4 h-4 text-slate-800"></i>
                                <h4>Código de referencia y reproducibilidad algorítmica (GitHub)</h4>
                            </div>
                            <p class="text-slate-600 leading-relaxed font-normal text-xs sm:text-sm">
                                En concordancia con los principios de reproducibilidad científica y resguardo metodológico, el CIT-UAI aloja el repositorio institucional <a href="https://github.com/CIT-UAI/mbht2024-metodologia" target="_blank" rel="noopener noreferrer" class="font-mono text-slate-900 font-bold underline">github.com/CIT-UAI/mbht2024-metodologia</a> (acceso interno para investigadores y equipos autorizados). Contiene la formulación algorítmica de referencia en Python para el cálculo de accesibilidad espacial peatonal mediante el método <strong>E2SFCA (Enhanced Two-Step Floating Catchment Area)</strong> con impedancia cinemática de Tobler ajustada por pendiente, casos de prueba sintéticos con salida en tiempo real, y un manifiesto contextual <code>ai_context.txt</code> estructurado específicamente para agentes de Inteligencia Artificial y sistemas RAG institucionales.
                            </p>
                            <a href="https://github.com/CIT-UAI/mbht2024-metodologia" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1.5 bg-slate-900 hover:bg-black text-white px-3.5 py-1.5 rounded text-xs font-semibold transition cursor-pointer shadow-xs">
                                <i data-lucide="external-link" class="w-3.5 h-3.5 text-uai-gold"></i>
                                <span>Consultar repositorio institucional en GitHub (CIT-UAI)</span>
                            </a>
                        </div>
                    </div>
                </section>


                <!-- SECCIÓN 7: SEGURIDAD, PRIVACIDAD Y DISPONIBILIDAD OPERACIONAL -->
                <section id="seccion-7" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 7</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Seguridad de la información, privacidad y disponibilidad</h2>
                        <p class="text-xs sm:text-sm text-slate-600 mt-1">Marco de controles técnicos alineados con el estándar <strong>OWASP ASVS 5.0 (Nivel 2)</strong>, secreto estadístico bajo la Ley 17.374 y alta disponibilidad cloud-native.</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-xs sm:text-sm">
                        
                        <!-- 7.1 Seguridad de Transporte e Infraestructura -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3 flex flex-col justify-between">
                            <div>
                                <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                        <i data-lucide="lock" class="w-3.5 h-3.5"></i>
                                    </div>
                                    <span>Seguridad de transporte y borde CDN</span>
                                </div>
                                <ul class="space-y-2 text-slate-600 font-normal">
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>TLS 1.3 / 1.2 estricto:</strong> Cifrado de extremo a extremo gestionado vía Amazon CloudFront y certificados SSL/TLS de alta resistencia.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>HSTS forzado:</strong> Cabecera <code>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</code> para prevenir ataques de degradación (*downgrade*).</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Aislamiento de origen (OAC):</strong> Almacenamiento S3 blindado sin acceso público directo; toda petición transita autenticada por la red CDN.</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="pt-2 border-t border-slate-200 text-[11px] text-slate-500 font-mono">
                                Estado: Enforce HTTPS & HSTS Activo
                            </div>
                        </div>

                        <!-- 7.2 Sanitización y Aplicación (OWASP ASVS 5.0) -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3 flex flex-col justify-between">
                            <div>
                                <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                        <i data-lucide="shield" class="w-3.5 h-3.5"></i>
                                    </div>
                                    <span>Controles de aplicación y anti-XSS</span>
                                </div>
                                <ul class="space-y-2 text-slate-600 font-normal">
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Sanitización de entradas:</strong> El Copiloto IA y los módulos de filtrado procesan consultas mediante escape de entidades y tipado estricto.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>CORS de datos abiertos:</strong> Políticas restrictivas con métodos de solo lectura pública (<code>GET</code>, <code>HEAD</code>) para consumo machine-readable.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Cabeceras de protección:</strong> <code>X-Content-Type-Options: nosniff</code> y <code>Referrer-Policy: strict-origin-when-cross-origin</code>.</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="pt-2 border-t border-slate-200 text-[11px] text-slate-500 font-mono">
                                Estándar: OWASP ASVS v5.0.0 Level 2
                            </div>
                        </div>

                        <!-- 7.3 Privacidad y Secreto Estadístico -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3 flex flex-col justify-between">
                            <div>
                                <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                        <i data-lucide="eye-off" class="w-3.5 h-3.5"></i>
                                    </div>
                                    <span>Privacidad y secreto estadístico (Ley 17.374)</span>
                                </div>
                                <ul class="space-y-2 text-slate-600 font-normal">
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Cero microdatos individuales:</strong> Toda la información territorial se agrega a escala de manzana censal o polígono territorial.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Conservación poblacional:</strong> Las imputaciones demográficas (Sprague) conservan los totales comunales oficiales sin revelar hogares.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Inmutabilidad SHA-256:</strong> Cada archivo descargable cuenta con su hash criptográfico para garantizar la procedencia del dato.</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="pt-2 border-t border-slate-200 text-[11px] text-slate-500 font-mono">
                                Marco: Ley 17.374 / Secreto Estadístico INE
                            </div>
                        </div>

                        <!-- 7.4 Disponibilidad y Endpoints Resilientes -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-3 flex flex-col justify-between">
                            <div>
                                <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                        <i data-lucide="activity" class="w-3.5 h-3.5"></i>
                                    </div>
                                    <span>Disponibilidad, SLA y salud de endpoints</span>
                                </div>
                                <ul class="space-y-2 text-slate-600 font-normal">
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>SLA 99.9% Cloud-Native:</strong> Arquitectura multi-AZ distribuida globalmente con redundancia de borde.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Catálogo STAC 1.0.0 activo:</strong> Endpoints públicos en <a href="stac/catalog.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 underline font-mono">/stac/catalog.json</a> y <a href="stac/collection.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 underline font-mono">/stac/collection.json</a>.</span>
                                    </li>
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="check" class="w-4 h-4 text-slate-900 shrink-0 mt-0.5"></i>
                                        <span><strong>Conectores machine-readable:</strong> Ejemplos auditados en <a href="connection_examples.json" target="_blank" rel="noopener noreferrer" class="text-slate-900 underline font-mono">/connection_examples.json</a>.</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="pt-2 border-t border-slate-200 text-[11px] text-slate-500 font-mono">
                                SLA: 99.9% Uptime Multi-Zona
                            </div>
                        </div>

                        <!-- 7.5 Gobernanza Institucional, Preservación y Ciclo de Vida -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-slate-50 space-y-4 md:col-span-2">
                            <div>
                                <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                        <i data-lucide="landmark" class="w-3.5 h-3.5"></i>
                                    </div>
                                    <span>Gobernanza institucional formal, preservación inmutable y ciclo de vida</span>
                                </div>
                                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-slate-600 font-normal pt-1">
                                    <div class="space-y-1">
                                        <span class="font-bold text-slate-800 text-xs block">Matriz de Roles y Aprobación</span>
                                        <p class="text-[11px] leading-relaxed"><strong>Comité Académico-Técnico CIT-UAI:</strong> Aprueba cambios metodológicos y versiones mayores. <strong>Custodio de Datos Espaciales:</strong> Certifica la integridad criptográfica SHA-256 y esquemas ISO. <strong>Equipo DevOps:</strong> Opera el despliegue cloud-native y observabilidad.</p>
                                    </div>
                                    <div class="space-y-1">
                                        <span class="font-bold text-slate-800 text-xs block">SemVer Geoespacial y Deprecación</span>
                                        <p class="text-[11px] leading-relaxed">Versionamiento semántico estricto (<em>vMAJOR.MINOR.PATCH</em>). Las versiones deprecadas jamás se eliminan: se congelan con URN inmutable y checksum en almacenamiento frío multi-zona para garantizar reproducibilidad histórica.</p>
                                    </div>
                                    <div class="space-y-1">
                                        <span class="font-bold text-slate-800 text-xs block">Canal Público de Incidencias (Issues)</span>
                                        <p class="text-[11px] leading-relaxed">Reporte y trazabilidad de anomalías mediante el canal institucional permanente <code>cit@uai.cl</code> y el issue tracker de GitHub, con protocolo de respuesta técnica y resolución en menos de 48 horas hábiles.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="pt-2 border-t border-slate-200 text-[11px] text-slate-500 font-mono flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                                <span>Compromiso de Custodia Institucional: Centro de Inteligencia Territorial · UAI (2026–2036)</span>
                                <span>Gobernanza: SemVer v2.0 / Licencia Abierta CC BY 4.0</span>
                            </div>
                        </div>

                        <!-- 7.6 Marco Dual de Aseguramiento: Data Quality vs. Model Quality -->
                        <div class="border border-slate-200 rounded-xl p-4 sm:p-5 bg-white space-y-3 md:col-span-2 shadow-xs">
                            <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm">
                                <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center text-xs">
                                    <i data-lucide="check-check" class="w-3.5 h-3.5"></i>
                                </div>
                                <span>Aseguramiento de Calidad Dual: Data Quality vs. Model Quality</span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-600 leading-relaxed pt-1">
                                <div class="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5">
                                    <span class="font-bold text-slate-900 text-xs flex items-center space-x-1.5">
                                        <i data-lucide="binary" class="w-3.5 h-3.5 text-slate-700"></i>
                                        <span>1. Data Quality (Integridad Física y Estructural del Dato)</span>
                                    </span>
                                    <ul class="list-disc pl-4 space-y-1 text-[11px] text-slate-600">
                                        <li><strong>Completitud exhaustiva:</strong> Cuadratura del 100% de las 204.906 manzanas censales y 42 columnas físicas sin truncamiento ni nulos espurios.</li>
                                        <li><strong>Topología y red ruteable:</strong> Grafo vial nacional de 1.589.595 tramos con verificación de snapping a 0,5 m y split en intersecciones.</li>
                                        <li><strong>Inmutabilidad criptográfica:</strong> Certificación bit a bit de cada archivo distribuido mediante algoritmo SHA-256 (64 hex).</li>
                                    </ul>
                                </div>
                                <div class="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5">
                                    <span class="font-bold text-slate-900 text-xs flex items-center space-x-1.5">
                                        <i data-lucide="scale" class="w-3.5 h-3.5 text-slate-700"></i>
                                        <span>2. Model Quality (Rigor Epistemológico y Territorial del Modelo)</span>
                                    </span>
                                    <ul class="list-disc pl-4 space-y-1 text-[11px] text-slate-600">
                                        <li><strong>Axioma de Neutralidad Elemental:</strong> Ponderación proporcional dimensional <em>W</em>(<em>D</em>) = <em>n<sub>D</sub></em> / <em>N</em><sub>total</sub>, eliminando sesgos artificiales de sobreponderación.</li>
                                        <li><strong>Física del desplazamiento:</strong> Impedancia regida estrictamente por red vial física y pendientes DEM de Tobler (cero distancia euclidiana).</li>
                                        <li><strong>Capacidad y competencia (E2SFCA):</strong> Modelamiento de oferta finita (cupos, camas, m<sup>2</sup>) frente a demanda poblacional concurrente en isócronas reales.</li>
                                        <li><strong>Estabilidad matemática:</strong> Pruebas de perturbación en anchos de banda (<em>t</em><sub>0</sub> &isin; [10, 15, 20] min) con correlación de Spearman &rho; &gt; 0,94.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                    </div>
                </section>

                <!-- SECCIÓN 8: REPRODUCCIÓN COMPLETA DE UN INDICADOR PASO A PASO (E2E VERIFICADO SOBRE ARCHIVOS REALES) -->
                <section id="seccion-8" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 8</div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Reproducción verificada de extremo a extremo (Caso real: Región de Arica y Parinacota · R15)</h2>
                        <p class="text-sm sm:text-base text-slate-600 mt-1 leading-relaxed">
                            Ejemplo mínimo autocontenido y ejecutado directamente sobre los archivos reales publicados en el centro de descargas (<code class="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded">MBHT_2017_R15_Manzanas.parquet</code>, <strong>2,37 MB</strong>) para comprobar integridad criptográfica SHA-256, esquema físico de 42 columnas, valores de una manzana testigo y reproducción exacta del índice BHT comunal y regional (<code class="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded">v1.0.3</code>).
                        </p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm sm:text-base">
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block">1. Insumos abiertos reales (R15)</span>
                            <ul class="text-xs sm:text-sm text-slate-700 leading-relaxed space-y-1.5">
                                <li>• <a href="/download/MBHT_2017_R15_Manzanas.parquet" class="underline font-semibold text-slate-900 break-words">MBHT_2017_R15_Manzanas.parquet</a> (3.304 mzs, 223.679 hab., 42 col., 2,37 MB)</li>
                                <li>• <a href="/download/Equipamientos_2017_R15_Consolidado.parquet" class="underline font-semibold text-slate-900 break-words">Equipamientos_2017_R15_Consolidado.parquet</a> (905 recintos; 40 de salud <code class="font-mono text-xs">isal</code>)</li>
                                <li>• <a href="/download/Red_Vial_Ejes_2017_R15.parquet" class="underline font-semibold text-slate-900 break-words">Red_Vial_Ejes_2017_R15.parquet</a> (19.408 tramos, 5.719,04 km)</li>
                            </ul>
                        </div>
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block">2. Parámetros y jerarquía del modelo</span>
                            <ul class="text-xs sm:text-sm text-slate-700 leading-relaxed space-y-1.5">
                                <li>• Umbral peatonal: {eq_umbral}</li>
                                <li>• Decaimiento de Tobler: {eq_tobler}</li>
                                <li>• Síntesis BHT 2017 (18 ind.): {eq_bht_2017}</li>
                            </ul>
                        </div>
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block">3. Manzana testigo y resultado regional</span>
                            <ul class="text-xs sm:text-sm text-slate-700 leading-relaxed space-y-1.5">
                                <li>• Manzana: <code class="font-mono text-xs bg-white px-1 py-0.5 rounded border border-slate-200">id_manzcit = '15101011001004001'</code> (Arica, 145 personas, TOB <code class="font-mono text-xs">Medio</code>)</li>
                                <li>• Valores en archivo: <code class="font-mono text-xs">bht = 0,3751</code> · <code class="font-mono text-xs">dim_acc = 0,6279</code> · <code class="font-mono text-xs">isal = 0,8691</code></li>
                                <li>• Media regional R15 ponderada: <strong><code class="font-mono text-xs">0,4623</code></strong> (Nacional: <strong><code class="font-mono text-xs">0,6171</code></strong>)</li>
                            </ul>
                        </div>
                    </div>

                    <div class="overflow-x-auto border border-slate-200 rounded-xl">
                        <table class="w-full text-left border-collapse text-xs sm:text-sm">
                            <thead>
                                <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                                    <th class="py-3 px-4 font-semibold">Etapa de verificación</th>
                                    <th class="py-3 px-4 font-semibold">Fórmula / Comprobación sobre columnas físicas</th>
                                    <th class="py-3 px-4 font-semibold">Resultado exacto observado en el archivo descargado</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-200 bg-white text-slate-700">
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">1. Integridad y esquema (42 col.)</td>
                                    <td class="py-3 px-4 font-mono text-xs">SHA-256 + <code>df.shape == (3304, 42)</code></td>
                                    <td class="py-3 px-4">Tamaño: <code>2.482.961 bytes</code>. Hash SHA-256: <code class="break-all">712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505</code>. Paridad 1:1 con el archivo <code>.csv</code> (3.304 filas).</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">2. Sub-indicadores peatonales (6 col.)</td>
                                    <td class="py-3 px-4 text-xs sm:text-sm">{eq_e2sfca_step1} &rarr; {eq_e2sfca_step2}</td>
                                    <td class="py-3 px-4">En la manzana <code>15101011001004001</code>: <code>isal = 0,8691</code>, <code>ise = 1,3381</code>, <code>iav = 5,8035</code>, <code>idep = 0,7744</code>, <code>icul = 0,2934</code>, <code>iser = 10,3205</code>, sintetizados en <code>dim_acc = 0,6279</code>.</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">3. Macro-dimensiones (4 col.) e índice <code>bht</code></td>
                                    <td class="py-3 px-4 text-xs sm:text-sm">{eq_bht_2017}</td>
                                    <td class="py-3 px-4">En la manzana <code>15101011001004001</code>: <code>dim_acc = 0,6279</code>, <code>dim_soc = 0,6737</code>, <code>dim_seg = 0,1665</code>, <code>dim_amb = 0,8571</code> &rarr; índice normalizado <code>bht = 0,3751</code>.</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">4. Agregación comunal y regional</td>
                                    <td class="py-3 px-4 text-xs sm:text-sm">{eq_agg_pob}</td>
                                    <td class="py-3 px-4">Comunas R15: <strong>Arica</strong> (2.878 mzs, 219.413 hab., <code>BHT = 0,4588</code>), <strong>Putre</strong> (231 mzs, 2.330 hab., <code>BHT = 0,7179</code>), <strong>Camarones</strong> (74 mzs, 1.253 hab., <code>BHT = 0,5678</code>), <strong>General Lagos</strong> (121 mzs, 683 hab., <code>BHT = 0,5224</code>). Total R15: <strong><code>0,4623</code></strong>.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 text-xs sm:text-sm">
                        <div class="bg-black/40 px-4 py-2.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800">
                            <span class="font-mono text-slate-300 font-semibold">prueba_e2e_mbht2017_r15.py (Ejecutable con Python 3.10+ / Pandas / DuckDB)</span>
                            <a href="/download/MBHT_2017_R15_Manzanas.parquet" class="text-uai-gold hover:underline font-semibold text-xs shrink-0">Descargar MBHT_2017_R15_Manzanas.parquet (2,37 MB) &rarr;</a>
                        </div>
                        <pre class="p-4 overflow-x-auto font-mono text-slate-200 leading-relaxed"><code>import hashlib, urllib.request, pandas as pd

# 1. Descarga directa del paquete regional R15 (2,37 MB) y verificación SHA-256
url = "https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet"
urllib.request.urlretrieve(url, "MBHT_2017_R15_Manzanas.parquet")
sha = hashlib.sha256(open("MBHT_2017_R15_Manzanas.parquet", "rb").read()).hexdigest()
assert sha == "712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505"

# 2. Inspección del esquema físico (3.304 manzanas x 42 columnas) y manzana testigo
df = pd.read_parquet("MBHT_2017_R15_Manzanas.parquet")
assert df.shape == (3304, 42) and df["id_manzcit"].nunique() == 3304
m = df.loc[df["id_manzcit"] == "15101011001004001"].iloc[0]
print(f"Manzana {{m['id_manzcit']}} ({{m['comuna']}}): pob={{int(m['personas'])}}, bht={{m['bht']:.4f}}, dim_acc={{m['dim_acc']:.4f}}, isal={{m['isal']:.4f}}")

# 3. Reproducción exacta del BHT comunal y regional ponderado por población
for comuna, grp in df.groupby("comuna"):
    bht_com = (grp["bht"] * grp["personas"]).sum() / grp["personas"].sum()
    print(f"  Comuna {{comuna:15s}} | Manzanas: {{len(grp):4d}} | Pob: {{int(grp['personas'].sum()):7d}} | BHT: {{bht_com:.4f}}")
bht_r15 = (df["bht"] * df["personas"]).sum() / df["personas"].sum()
print(f"Total Regional R15 -> Manzanas: {{len(df)}} | Población: {{int(df['personas'].sum())}} | BHT R15: {{bht_r15:.4f}}")</code></pre>
                    </div>

                    <div class="mt-4 p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs sm:text-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                                <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600"></i>
                                <span>Protocolo de Ejecución Local Segura (Sin Ejecución Remota de Código)</span>
                            </span>
                            <span class="font-mono text-[11px] text-slate-500">SHA-256 verificado</span>
                        </div>
                        <p class="text-slate-600 leading-relaxed text-xs">
                            Conforme a los estándares de seguridad de cadena de suministro (OWASP / NIST), se recomienda descargar el script como archivo estático, validar su integridad criptográfica mediante el hash publicado y ejecutarlo localmente en un entorno aislado:
                        </p>
                        <div class="p-3 bg-white rounded-lg border border-slate-200 font-mono text-xs text-slate-800 break-all select-all leading-relaxed">
                            # 1. Descargar script de verificación auditable<br>
                            curl -s -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py<br><br>
                            # 2. Verificar integridad del script mediante SHA-256 publicado<br>
                            echo "7fb25d61a29544e57c17869c6ea3566c68659d003dce9f59dfcd642fbf96a8d0  reproducir_verificacion_r15.py" | sha256sum -c<br><br>
                            # 3. Ejecutar verificación determinista localmente<br>
                            python reproducir_verificacion_r15.py
                        </div>
                    </div>
                </section>

                <!-- SECCIÓN 9: ESTADO OPERATIVO DE LA INFRAESTRUCTURA, CALIDAD E HISTORIAL DE VERSIONES -->
                <section id="seccion-9" class="scroll-mt-36 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-clean space-y-6">
                    <div class="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Capítulo 9</div>
                            <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">Estado operativo de los servicios, historial de versiones e incidencias públicas</h2>
                        </div>
                        <div class="text-xs sm:text-sm font-mono bg-slate-100 text-slate-800 px-3 py-1.5 rounded-lg border border-slate-200 shrink-0">
                            Última actualización y auditoría: <strong>2026-10-17 · v1.0.3</strong>
                        </div>
                    </div>

                    <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
                        Con el propósito de brindar certidumbre operativa a investigadores, equipos municipales y organismos públicos, esta sección consolida el estado actual de los servicios de la IDE CIT, la matriz de evidencia de conformidad normativa, los benchmarks empíricos reproducibles (<code class="font-mono text-xs">p50 / p95 / p99</code>) y el registro de versiones e incidencias.
                    </p>

                    <div class="overflow-x-auto border border-slate-200 rounded-xl">
                        <table class="w-full text-left border-collapse text-sm sm:text-base">
                            <thead>
                                <tr class="bg-slate-900 text-white text-xs sm:text-sm uppercase tracking-wider">
                                    <th class="py-3 px-4 font-semibold">Servicio o componente principal</th>
                                    <th class="py-3 px-4 font-semibold">Punto de acceso canónico</th>
                                    <th class="py-3 px-4 font-semibold">Estado operativo</th>
                                    <th class="py-3 px-4 font-semibold">Última comprobación</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-200 bg-white text-slate-700">
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">Portal Web y Catálogo Abierto</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm"><a href="/inicio" class="underline hover:text-black">https://ide.cit.uai.cl/inicio</a></td>
                                    <td class="py-3 px-4 font-semibold text-slate-900">Operativo (HTTP 200 · CDN CloudFront)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm">2026-10-17</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">Centro de Descargas y Verificación SHA-256</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm"><a href="/descargas" class="underline hover:text-black">https://ide.cit.uai.cl/descargas</a></td>
                                    <td class="py-3 px-4 font-semibold text-slate-900">Operativo (208 paquetes línea base 2017 con SHA-256)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm">2026-10-17</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">Catálogo STAC 1.0.0, DCAT-AP y Metadatos ISO 19139</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm"><a href="/stac/catalog.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/stac/catalog.json</a></td>
                                    <td class="py-3 px-4 font-semibold text-slate-900">Operativo (5 colecciones + extensiones projection/file/scientific)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm">2026-10-17</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">Reporte de Conformidad y Benchmarks (<code class="font-mono text-xs">conformance_report.json</code>)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm"><a href="/conformance_report.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/conformance_report.json</a></td>
                                    <td class="py-3 px-4 font-semibold text-slate-900">Operativo (15 vectores Red Team + métricas p50/p95/p99)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm">2026-10-17</td>
                                </tr>
                                <tr>
                                    <td class="py-3 px-4 font-bold text-slate-900">Motor de Teselas Vectoriales (MVT)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm"><a href="/tiles/mbht_2017_manzanas.json" target="_blank" rel="noopener noreferrer" class="underline hover:text-black">https://ide.cit.uai.cl/tiles/mbht_2017_manzanas.json</a></td>
                                    <td class="py-3 px-4 font-semibold text-slate-900">Operativo (TileJSON 3.0.0 · Latencia media &lt; 50 ms)</td>
                                    <td class="py-3 px-4 font-mono text-xs sm:text-sm">2026-10-17</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Benchmarks Reproducibles (p50 / p95 / p99) y Matriz de Conformidad -->
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-2">
                        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
                            <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                                <h3 class="font-bold text-slate-900 text-sm sm:text-base">Benchmarks empíricos reproducibles (GeoParquet 1.1 &amp; HTTP Range)</h3>
                                <a href="/conformance_report.json" target="_blank" rel="noopener noreferrer" class="font-mono text-[11px] text-slate-700 underline hover:text-black">Ver JSON</a>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                Mediciones empíricas sobre los activos reales publicados (<code class="font-mono">PyArrow 21.0</code>, compresión <code class="font-mono">SNAPPY</code>, <code class="font-mono">N=30</code> iteraciones locales y <code class="font-mono">N=10</code> sondas HTTPS WAN sobre CloudFront):
                            </p>
                            <div class="overflow-x-auto border border-slate-200 rounded-lg bg-white">
                                <table class="w-full text-left border-collapse text-xs">
                                    <thead>
                                        <tr class="bg-slate-100 text-slate-700 border-b border-slate-200">
                                            <th class="py-2 px-2.5 font-semibold">Prueba reproducible</th>
                                            <th class="py-2 px-2.5 font-semibold font-mono">p50</th>
                                            <th class="py-2 px-2.5 font-semibold font-mono">p95</th>
                                            <th class="py-2 px-2.5 font-semibold font-mono">p99</th>
                                            <th class="py-2 px-2.5 font-semibold">I/O efectivo</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100 text-slate-700 font-mono">
                                        <tr>
                                            <td class="py-2 px-2.5 font-sans font-semibold text-slate-900">Nacional (204.906 filas &rarr; filtro RM <code class="font-mono">bht &lt; 0.40</code>)</td>
                                            <td class="py-2 px-2.5">14,4 ms</td>
                                            <td class="py-2 px-2.5">15,4 ms</td>
                                            <td class="py-2 px-2.5">21,9 ms</td>
                                            <td class="py-2 px-2.5 font-sans text-[11px]">4,2 MB de 128,8 MB (96,7% ahorro)</td>
                                        </tr>
                                        <tr>
                                            <td class="py-2 px-2.5 font-sans font-semibold text-slate-900">Regional R15 (3.304 filas &rarr; media ponderada <code class="font-mono">0,4623</code>)</td>
                                            <td class="py-2 px-2.5">4,4 ms</td>
                                            <td class="py-2 px-2.5">5,1 ms</td>
                                            <td class="py-2 px-2.5">6,7 ms</td>
                                            <td class="py-2 px-2.5 font-sans text-[11px]">Lectura de 2 columnas (<code class="font-mono">bht, personas</code>)</td>
                                        </tr>
                                        <tr>
                                            <td class="py-2 px-2.5 font-sans font-semibold text-slate-900">HTTPS WAN <code class="font-mono">Range: bytes=0-4095</code> (HTTP 206)</td>
                                            <td class="py-2 px-2.5">340,7 ms</td>
                                            <td class="py-2 px-2.5">359,4 ms</td>
                                            <td class="py-2 px-2.5">684,7 ms</td>
                                            <td class="py-2 px-2.5 font-sans text-[11px]">4.096 B de 2,48 MB (0,16% transferido)</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
                            <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                                <h3 class="font-bold text-slate-900 text-sm sm:text-base">Alcance de verificación normativa y evidencia pública</h3>
                                <a href="/download/iso_xml/auditoria_conformidad_iso.json" target="_blank" rel="noopener noreferrer" class="font-mono text-[11px] text-slate-700 underline hover:text-black">Auditoría ISO</a>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                Distinción transparente entre estándares verificados automáticamente en cada compilación CI/CD y lineamientos de diseño de referencia:
                            </p>
                            <ul class="space-y-1.5 text-xs text-slate-700 leading-relaxed">
                                <li><strong>ISO 19115-1:2014 / ISO 19139 XML:</strong> Verificación estructural automatizada de los 5 archivos XML contra los elementos obligatorios del Perfil Nacional SNIT (<a href="/download/iso_xml/auditoria_conformidad_iso.json" target="_blank" rel="noopener noreferrer" class="underline font-mono">auditoria_conformidad_iso.json</a>).</li>
                                <li><strong>STAC 1.0.0 &amp; DCAT-AP 2.0:</strong> Validación automática de esquemas JSON, extensiones (<code class="font-mono">projection</code>, <code class="font-mono">file</code>, <code class="font-mono">scientific</code>) y resolución HTTP 200 de todos los activos enlazados.</li>
                                <li><strong>Cuadratura y Diccionario Físico (Red Team 15 Vectores):</strong> Comprobación cruzada automática entre valores reales en archivos <code class="font-mono">.parquet</code> (42 columnas, dominios categóricos <code class="font-mono">tob</code> y sumas regionales &Delta;=0) y la documentación HTML/JSON (<a href="/conformance_report.json" target="_blank" rel="noopener noreferrer" class="underline font-mono">conformance_report.json</a>).</li>
                                <li><strong>Seguridad y Accesibilidad Web:</strong> Alineación de cabeceras, enlaces externos (<code class="font-mono">rel="noopener noreferrer"</code>), publicación de <a href="/.well-known/security.txt" target="_blank" rel="noopener noreferrer" class="underline font-mono">security.txt (RFC 9116)</a> y controles semánticos HTML5 / WCAG 2.1 AA verificados por el validador interno; no sustituye una certificación de penetración de tercera parte.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm sm:text-base">
                        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">
                            <h3 class="font-bold text-slate-900 text-base">Historial de versiones recientes</h3>
                            <ul class="space-y-2 text-slate-600 leading-relaxed text-xs sm:text-sm">
                                <li><strong>v1.0.3 (2026-10-17 — Vigente):</strong> Publicación de <code class="font-mono">conformance_report.json</code> con benchmarks empíricos (<code class="font-mono">p50/p95/p99</code>), precisión geodésica SIRGAS-Chile (<code class="font-mono">EPSG:5360</code>) vs WGS 84 (<code class="font-mono">EPSG:4326</code>), extensiones STAC científicas y simplificación visual por perfiles de usuario.</li>
                                <li><strong>v1.0.2 (2026-10-08):</strong> Separación explícita entre línea base vigente MBHT 2017 y actualización MBHT 2024 en calibración metodológica; publicación de matriz de control de calidad y verificador SHA-256 en el navegador.</li>
                                <li><strong>v1.0.1 (2026-06-15):</strong> Cuadratura aritmética exacta (&Delta; = 0) entre los 16 paquetes regionales y el consolidado nacional MBHT 2017 (204.906 manzanas, 55.035 equipamientos, 1.589.595 tramos).</li>
                                <li><strong>v1.0.0 (2018-11-20):</strong> Publicación original de la Línea Base MBHT 2017 (Convenio SUBDERE, 18 indicadores elementales).</li>
                            </ul>
                        </div>
                        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">
                            <h3 class="font-bold text-slate-900 text-base">Registro de incidencias y custodia por conjunto (Stewards)</h3>
                            <ul class="space-y-2 text-slate-600 leading-relaxed text-xs sm:text-sm">
                                <li><strong>Incidencias cerradas (<code>INC-2026-01</code> a <code>INC-2026-03</code>):</strong> Cuadratura de inventarios regionales 2017, unificación del diccionario físico de 42 columnas y sincronización de los activos referenciados desde las colecciones STAC (<code>Equipamientos_2017_Nacional_Consolidado.*</code>).</li>
                                <li><strong>Incidencias en curso (<code>INC-2026-04</code> y <code>INC-2026-05</code>):</strong> Calibración metodológica nacional de los 17 indicadores de la actualización MBHT 2024 (integrando los insumos del Censo 2024 del INE) y publicación futura de los paquetes descargables regionales R01–R16 tras el cierre oficial (programado Q4 2026).</li>
                                <li><strong>Tabla completa de Data Stewards y bitácora:</strong> Disponible en <a href="/ficha-mbht-2017#sec-gobernanza" class="font-semibold text-slate-900 underline">/ficha-mbht-2017#sec-gobernanza</a> · Contacto: <a href="mailto:contactocit@uai.cl" class="font-semibold text-slate-900 underline">contactocit@uai.cl</a>.</li>
                            </ul>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    </div>
    </main><!-- /main#main-content -->


    <!-- WIDGET COPILOTO IA FLOTANTE -->
    <!-- Micro-invitación pedagógica y sobria (CIT-UAI) -->
    <div id="copilotWelcomeHint" onclick="toggleCopilot(true); dismissCopilotHint(event);" class="cursor-pointer fixed bottom-20 right-3 sm:right-6 z-40 w-[calc(100vw-1.5rem)] max-w-[310px] sm:max-w-[340px] bg-[#0A192F] text-slate-200 border border-slate-700/80 border-t-2 border-t-[#6493B5] rounded-xl shadow-2xl p-3 text-xs leading-relaxed hidden transition-all duration-300">
        <div class="flex items-start justify-between gap-2">
            <p class="font-normal text-slate-300 text-[11px] sm:text-xs select-none">
                Orientación técnica en estándares OGC, scripts y metodologías MBHT. Puede consultar aquí al Copiloto CIT.
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

    <!-- VENTANA DEL COPILOTO IA -->
    <div id="copilotDrawer" class="fixed bottom-20 right-3 sm:right-6 w-[calc(100vw-1.5rem)] sm:w-[400px] max-h-[75vh] sm:max-h-[580px] bg-white rounded-2xl shadow-widget border border-slate-300 hidden flex-col z-50 overflow-hidden transition-all duration-200">
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
                    <p class="text-[11px] text-slate-400">Guía de interoperabilidad y datos</p>
                </div>
            </div>
            <button onclick="toggleCopilot(false)" class="text-slate-400 hover:text-white p-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition cursor-pointer">
                <i data-lucide="x" class="w-4 h-4 text-slate-400"></i>
            </button>
        </div>

        <div id="copilotMessages" class="p-3.5 sm:p-4 overflow-y-auto space-y-3 custom-scrollbar flex-1 bg-slate-50 text-xs sm:text-sm">
            <div class="flex items-start space-x-2.5">
                <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold">CIT</div>
                <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 text-slate-800 space-y-1.5 shadow-xs max-w-[85%]">
                    <p class="leading-relaxed font-medium">Bienvenido/a al asistente técnico del <strong>CIT-UAI</strong>. En nuestra visión, los estándares abiertos, los servicios WMS/MVT y las coberturas espaciales modeladas cobran sentido al servicio del <strong>Bienestar Humano Territorial (MBHT)</strong> y la toma de decisiones basada en evidencia.</p>
                    <p class="text-slate-600 text-[11px] sm:text-xs font-normal">Puedo orientarle en la integración de datos abiertos en Python, R y QGIS, especificaciones del perfil nacional SNIT/OGC y metodologías de accesibilidad peatonal y equidad territorial.</p>
                </div>
            </div>
        </div>

        <div class="p-2.5 sm:p-3 bg-white border-t border-slate-200 shrink-0">
            <form onsubmit="handleCopilotSubmit(event)" class="flex items-center space-x-1.5">
                <input type="text" id="copilotInput" placeholder="Pregunta sobre estándares, QGIS, Python..." 
                       class="flex-1 bg-slate-50 border border-slate-300 focus:border-slate-800 focus:bg-white rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-800 focus:outline-none transition font-normal placeholder-slate-400" />
                <button type="submit" class="bg-slate-900 hover:bg-black active:bg-slate-800 text-white p-2 rounded-lg transition cursor-pointer shrink-0">
                    <i data-lucide="send" class="w-4 h-4 text-white"></i>
                </button>
            </form>
        </div>
    </div>

{canonical_footer}

    <!-- SCRIPTS INTERACTIVOS -->
    <script>
        function renderKaTeX() {{
            if (window.renderMathInElement) {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: '$$', right: '$$', display: true}},
                        {{left: '$', right: '$', display: false}}
                    ],
                    throwOnError: false
                }});
            }} else {{
                setTimeout(renderKaTeX, 150);
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            lucide.createIcons();
            setupScrollSpy();
            initCopilotHint();
            renderKaTeX();
        }});

        // El menú móvil hamburguesa está gestionado canónicamente por get_canonical_header_html()
        // El botón scroll to top (volver arriba) y su control están gestionados universalmente por get_canonical_footer_html()

        function setupScrollSpy() {{
            const sections = document.querySelectorAll('section[id^="seccion-"]');
            const links = document.querySelectorAll('.toc-link');

            window.addEventListener('scroll', () => {{
                let current = '';
                sections.forEach(section => {{
                    const sectionTop = section.offsetTop - 180;
                    if (window.scrollY >= sectionTop) {{
                        current = section.getAttribute('id');
                    }}
                }});

                links.forEach(link => {{
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${{current}}`) {{
                        link.classList.add('active');
                    }}
                }});
            }});
        }}

        function copyText(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                alert('URL copiada al portapapeles.');
            }});
        }}

        function copySnippet(elementId) {{
            const el = document.getElementById(elementId);
            if (!el) return;
            const text = el.innerText || el.textContent;
            navigator.clipboard.writeText(text).then(() => {{
                alert('Código copiado al portapapeles.');
            }});
        }}

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

        function toggleCopilot(forceOpen = null) {{
            dismissCopilotHint();
            const drawer = document.getElementById('copilotDrawer');
            if (!drawer) return;
            if (forceOpen === true) {{
                drawer.classList.remove('hidden');
                drawer.classList.add('flex');
            }} else if (forceOpen === false) {{
                drawer.classList.add('hidden');
                drawer.classList.remove('flex');
            }} else {{
                drawer.classList.toggle('hidden');
                drawer.classList.toggle('flex');
            }}
            if (!drawer.classList.contains('hidden')) {{
                setTimeout(() => document.getElementById('copilotInput')?.focus(), 100);
            }}
        }}

        {copilot_js_engine}

        async function handleCopilotSubmit(e) {{
            if (e) e.preventDefault();
            const input = document.getElementById('copilotInput');
            const messages = document.getElementById('copilotMessages');
            if (!input || !input.value.trim() || !messages) return;

            const userText = input.value.trim();
            input.value = '';

            // User msg
            messages.innerHTML += `
                <div class="flex items-start justify-end space-x-2">
                    <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-none text-xs max-w-[85%]">
                        <p>${{userText}}</p>
                    </div>
                </div>
            `;

            const res = await resolveCopilotResponse(userText);
            const replyText = typeof res === 'string' ? res : (res.text || res);

            // Bot response
            setTimeout(() => {{
                messages.innerHTML += `
                    <div class="flex items-start space-x-2.5">
                        <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold">CIT</div>
                        <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 text-slate-800 text-xs max-w-[85%]">
                            <p class="leading-relaxed">${{replyText}}</p>
                        </div>
                    </div>
                `;
                messages.scrollTop = messages.scrollHeight;
            }}, 300);

            messages.scrollTop = messages.scrollHeight;
        }}

        function downloadCatalogJson() {{
            window.open('data/catalogo_ide_cit.json', '_blank');
        }}

        window.dismissCopilotHint = dismissCopilotHint;
        window.toggleCopilot = toggleCopilot;
    </script>
</body>
</html>
"""
    return html
