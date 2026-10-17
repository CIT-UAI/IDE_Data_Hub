#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — GENERADOR DE LA PÁGINA RED DE IDES Y GEOPORTALES DE CHILE
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Generador algorítmico automatizado de la página web `red-ides.html`
    para la Infraestructura de Datos Espaciales (IDE CIT).

    Presenta de forma autónoma, categorizada y con buscador interactivo
    los 19 geoportales e Infraestructuras de Datos Espaciales oficiales del
    Estado chileno y la academia, en el marco de la Política Nacional de
    Gestión de la Información Territorial-Geoespacial (Bienes Nacionales / SNIT).

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from motor_ia_cit import (
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
)


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


def generate_static_ides_html(catalog_data: Dict[str, Any]) -> str:
    """
    Pre-renderiza estáticamente las 19 tarjetas de geoportales en HTML semántico (SSG).
    Permite inspección automatizada inmediata sin requerir ejecución de JavaScript.
    """
    ides_cards = []
    for ide in catalog_data.get("ides_nacionales", []):
        cat_name = ide.get("categoria", "Nacional")
        
        items_html = ""
        if ide.get("que_encontraras"):
            items_li = "".join([f'<li class="flex items-start space-x-1.5 text-[11px] text-slate-600 leading-tight"><span class="text-slate-400 font-bold">·</span><span>{item}</span></li>' for item in ide.get("que_encontraras", [])[:3]])
            items_html = f'<ul class="space-y-1 my-3 pt-2.5 border-t border-slate-100">{items_li}</ul>'

        card = f"""        <article class="ide-card bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean hover:shadow-hover hover:border-slate-300 transition flex flex-col justify-between group" data-ide-id="{ide.get('id')}" data-categoria="{cat_name}">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">{ide.get('institucion')}</span>
                    <span class="text-[11px] font-mono text-slate-400">{cat_name}</span>
                </div>
                <h3 class="font-bold text-slate-900 text-sm sm:text-base mb-1.5 leading-snug group-hover:text-black transition">{ide.get('nombre')}</h3>
                <p class="text-xs text-slate-600 line-clamp-3 leading-relaxed font-normal">{ide.get('descripcion')}</p>
                {items_html}
            </div>
            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <a href="{ide.get('url')}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1.5 bg-slate-900 hover:bg-black text-white text-xs font-semibold py-2 px-3 rounded-lg transition shadow-xs">
                    <span>Visitar geoportal</span>
                    <i data-lucide="external-link" class="w-3.5 h-3.5 stroke-[2]"></i>
                </a>
                <span class="text-[11px] text-slate-500 font-mono">{ide.get('sigla', 'SNIT')}</span>
            </div>
        </article>"""
        ides_cards.append(card)
    return "\n".join(ides_cards)


def generate_red_ides_html(catalog_data: Dict[str, Any]) -> str:
    """
    Genera el código HTML5 completo para la página independiente `red-ides.html`.
    Encabezado, altura, paleta institucional y pie de página idénticos a index.html y guia-tecnica.html.
    """
    portal = catalog_data.get("portal", {})
    version = portal.get("version", "2026.2")
    ides: List[Dict[str, Any]] = catalog_data.get("ides_nacionales", [])
    num_ides = len(ides)
    ides_json_str = json.dumps(ides, ensure_ascii=False)
    static_ides_html = generate_static_ides_html(catalog_data)
    copilot_js_engine = get_copilot_js_engine()
    llm_head_meta = get_llm_head_meta()
    llm_guidance_html = get_llm_guidance_html()
    canonical_header = get_canonical_header_html("red-ides")
    canonical_footer = get_canonical_footer_html(version)

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50 scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red de IDEs y geoportales de Chile | IDE CIT · Universidad Adolfo Ibáñez</title>
    
    <!-- Metadatos SEO e institucionales -->
    <meta name="description" content="Directorio interactivo de los 19 geoportales oficiales e Infraestructuras de Datos Espaciales del Estado de Chile. Acceso directo a geoservicios de ministerios, servicios públicos y centros de investigación.">
    <meta name="keywords" content="IDE Chile, Geoportales Chile, SNIT, IDE MINVU, GEOMOP, SINIA, SNIA DGA, IDE SAF, IDE Energía, Geodatos INE, IDE SUBDERE, Centro OCUC, CIT-UAI">
    <meta name="author" content="Centro de Inteligencia Territorial (CIT-UAI)">
    <meta name="version" content="{version}">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="https://ide.cit.uai.cl/red-ides.html">
    
{llm_head_meta}
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="IDE CIT — Centro de Inteligencia Territorial (UAI)">
    <meta property="og:title" content="Red de IDEs y geoportales de Chile | IDE CIT">
    <meta property="og:description" content="Directorio y catálogo interactivo de los 19 geoportales oficiales e Infraestructuras de Datos Espaciales del Estado de Chile.">
    <meta property="og:url" content="https://ide.cit.uai.cl/red-ides.html">
    <meta property="og:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@CIT_UAI">
    <meta name="twitter:title" content="Red de IDEs y geoportales de Chile | IDE CIT">
    <meta name="twitter:description" content="Directorio interactivo de los 19 geoportales oficiales e IDEs del Estado de Chile. Articulación con el SNIT.">
    <meta name="twitter:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">

    <!-- Schema.org / JSON-LD BreadcrumbList + DataCatalog -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "DataCatalog",
          "name": "Red de IDEs y Geoportales de Chile | IDE CIT",
          "description": "Directorio de los {num_ides} geoportales e Infraestructuras de Datos Espaciales del Estado de Chile articulados con la IDE CIT.",
          "url": "https://ide.cit.uai.cl/red-ides.html",
          "creator": {{"@type": "Organization", "name": "Centro de Inteligencia Territorial (CIT-UAI)", "url": "https://cit.uai.cl"}},
          "inLanguage": "es-CL"
        }},
        {{
          "@type": "BreadcrumbList",
          "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "IDE CIT", "item": "https://ide.cit.uai.cl"}},
            {{"@type": "ListItem", "position": 2, "name": "Red de IDEs de Chile"}}
          ]
        }}
      ]
    }}
    </script>

    <!-- Favicon y manifiesto PWA -->
    <link rel="icon" type="image/svg+xml" href="img/logo-ide-standalone.svg">
    <link rel="manifest" href="site.webmanifest">
    
    <!-- Google Fonts: Roboto y JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">
    
    <!-- CSS Estático de Producción (Tailwind Compilado CIT) -->
    <link rel="stylesheet" href="/css/ide.min.css">
    
    <!-- Lucide Icons (Local Vendor) -->
    <script src="/vendor/lucide/lucide.min.js"></script>
    
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

        /* Ocultar scrollbar horizontal en filtros móviles */
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}

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
    </style>
</head>
<body class="h-full flex flex-col font-sans bg-slate-100 text-slate-800 antialiased overflow-x-hidden">

<noscript>
    <div class="bg-slate-900 text-slate-200 border-b border-slate-800 px-4 py-4 text-sm">
        <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
                <strong class="text-white">Directorio nacional de geoportales (modo lectura HTML estático):</strong>
                <span>Todos los enlaces a las 19 infraestructuras de datos espaciales públicas de Chile están disponibles directamente en las tarjetas inferiores.</span>
            </div>
            <div class="flex flex-wrap gap-3 font-semibold text-uai-gold shrink-0">
                <a href="/inicio" class="underline hover:text-white">Catálogo IDE CIT</a>
                <a href="/descargas" class="underline hover:text-white">Descargas MBHT 2017</a>
                <a href="/ficha-mbht-2017" class="underline hover:text-white">Ficha técnica</a>
                <a href="/guia-tecnica" class="underline hover:text-white">Guía metodológica</a>
            </div>
        </div>
    </div>
</noscript>

{llm_guidance_html}

{canonical_header}

    <!-- 2. CABECERA HERO DE LA RED DE IDES -->
    <main id="main-content" role="main" tabindex="-1">
    <section class="bg-white border-b border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <!-- Migas de pan (Breadcrumbs) -->
            <nav class="flex items-center space-x-2 text-xs text-slate-400 mb-4 sm:mb-5">
                <a href="inicio" class="hover:text-slate-700 transition">IDE CIT</a>
                <span class="text-slate-300">/</span>
                <span class="text-slate-500 font-medium">Ecosistema geoespacial</span>
                <span class="text-slate-300">/</span>
                <span class="text-slate-800 font-bold">Red de IDEs y geoportales de Chile</span>
            </nav>

            <div class="w-full">
                <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-800 text-[11px] sm:text-xs font-bold uppercase tracking-wider mb-3">
                    <span class="w-2 h-2 rounded-full bg-uai-gold"></span>
                    <span>Ecosistema nacional SNIT · {num_ides} geoportales oficiales e institucionales</span>
                </div>
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
                    Red de IDEs y geoportales de Chile
                </h1>
                <p class="text-sm sm:text-base lg:text-lg text-slate-600 mt-2.5 sm:mt-3 leading-relaxed font-normal w-full">
                    Directorio institucional y punto de enlace hacia las Infraestructuras de Datos Espaciales, geoportales ministeriales, plataformas de monitoreo ambiental y repositorios de datos territoriales del Estado de Chile y el mundo académico. La IDE CIT se articula como un complemento de alto valor agregado a este ecosistema, aportando modelos analíticos de accesibilidad peatonal (E2SFCA), estimaciones de población censal y síntesis espacial multivariable.
                </p>
            </div>

            <!-- Tira de métricas y principios institucionales -->
            <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 border-t border-slate-100 text-xs">
                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
                    <span class="text-[10px] font-bold text-slate-400 uppercase block mb-0.5">Geoportales activos</span>
                    <span class="text-lg sm:text-xl font-bold text-slate-900 font-mono">19 plataformas</span>
                </div>
                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
                    <span class="text-[10px] font-bold text-slate-400 uppercase block mb-0.5">Estado operativo</span>
                    <span class="text-lg sm:text-xl font-bold text-emerald-700 font-mono flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-600"></span>
                        <span>100% en línea</span>
                    </span>
                </div>
                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
                    <span class="text-[10px] font-bold text-slate-400 uppercase block mb-0.5">Gobernanza</span>
                    <span class="text-lg sm:text-xl font-bold text-slate-900">SNIT / BBNN</span>
                </div>
                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
                    <span class="text-[10px] font-bold text-slate-400 uppercase block mb-0.5">Interoperabilidad</span>
                    <span class="text-lg sm:text-xl font-bold text-slate-900 font-mono">OGC / ISO 19115-1</span>
                </div>
            </div>

        </div>
    </section>

    <!-- 3. SECCIÓN PRINCIPAL: FILTROS, BUSCADOR Y TARJETAS DE GEOPORTALES -->
    <section class="flex-1 max-w-[1600px] mx-auto w-full px-4 sm:px-6 lg:px-10 xl:px-12 py-8 sm:py-10 space-y-6">

        <!-- Barra de Control: Buscador y Filtros por Categoría -->
        <div class="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-clean space-y-4">
            
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <!-- Buscador Dinámico -->
                <div class="relative flex-1">
                    <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 stroke-[1.5]"></i>
                    <input type="text" id="searchInput" oninput="filterIdes()" placeholder="Buscar geoportal por nombre, ministerio, temática o insumos (ej: INE, glaciares, vialidad, energía)..." 
                           class="w-full pl-10 pr-10 py-2.5 text-xs sm:text-sm bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:bg-white transition" />
                    <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 p-1 rounded-md transition">
                        <i data-lucide="x" class="w-3.5 h-3.5"></i>
                    </button>
                </div>

                <!-- Contador de resultados -->
                <div class="text-xs text-slate-500 shrink-0 font-medium self-end md:self-center">
                    Mostrando <strong id="resultsCount" class="text-slate-900 font-mono">{num_ides}</strong> de {num_ides} geoportales
                </div>
            </div>

            <!-- Filtros Temáticos por Categoría -->
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar pt-1 border-t border-slate-100" id="ideCategoryFilters">
                <button onclick="setCategoryFilter('all', this)" class="ide-cat-btn active text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-900 text-white transition cursor-pointer whitespace-nowrap shadow-xs">Todas ({num_ides})</button>
                <button onclick="setCategoryFilter('Nacional', this)" class="ide-cat-btn text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition cursor-pointer whitespace-nowrap">Nacionales y multisectoriales</button>
                <button onclick="setCategoryFilter('Urbano', this)" class="ide-cat-btn text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition cursor-pointer whitespace-nowrap">Urbano, vivienda y académico</button>
                <button onclick="setCategoryFilter('Medio Ambiente', this)" class="ide-cat-btn text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition cursor-pointer whitespace-nowrap">Medio ambiente, agua y recursos</button>
                <button onclick="setCategoryFilter('Infraestructura', this)" class="ide-cat-btn text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition cursor-pointer whitespace-nowrap">Infraestructura, energía y regiones</button>
            </div>

        </div>

        <!-- Banner de Adhesión a la Política Nacional de Información Territorial-Geoespacial -->
        <div class="p-4 sm:p-5 rounded-xl bg-white border border-slate-200 shadow-clean flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div class="flex items-start space-x-3.5">
                <div class="w-10 h-10 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center shrink-0 mt-0.5">
                    <i data-lucide="scale" class="w-5 h-5 stroke-[1.5]"></i>
                </div>
                <div>
                    <h3 class="font-bold text-slate-900 text-sm sm:text-base leading-tight">Política Nacional de Gestión de la Información Territorial-Geoespacial</h3>
                    <p class="text-slate-600 text-xs sm:text-sm mt-1 leading-relaxed">
                        Marco oficial de gobernanza, interoperabilidad e integración de datos geoespaciales del Estado de Chile, coordinado por la Secretaría Ejecutiva del SNIT (Ministerio de Bienes Nacionales).
                    </p>
                </div>
            </div>
            <a href="https://www.bienesnacionales.cl/chile-ya-cuenta-con-su-politica-de-gestion-de-la-informacion-territorial-geoespacial/" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-slate-800 bg-slate-50 hover:bg-slate-900 hover:text-white border border-slate-200 hover:border-slate-900 px-3.5 py-2 rounded-lg transition shrink-0 flex items-center space-x-1.5 whitespace-nowrap">
                <span>Ver marco oficial</span>
                <i data-lucide="external-link" class="w-3.5 h-3.5 stroke-[1.5]"></i>
            </a>
        </div>

        <!-- Grid Dinámico de Tarjetas de IDEs -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-4 gap-4 sm:gap-6" id="idesGrid">
{static_ides_html}
        </div>

        <!-- Estado Vacío (Sin resultados) -->
        <div id="noResultsState" class="hidden bg-white p-8 sm:p-12 rounded-xl border border-slate-200 text-center space-y-3">
            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                <i data-lucide="search-x" class="w-6 h-6 stroke-[1.5]"></i>
            </div>
            <h3 class="text-base font-bold text-slate-900">No se encontraron geoportales</h3>
            <p class="text-xs sm:text-sm text-slate-500 max-w-md mx-auto">
                No hay plataformas que coincidan con los criterios de búsqueda o categoría seleccionados.
            </p>
            <button onclick="clearSearch()" class="text-xs font-semibold text-slate-900 hover:underline inline-flex items-center space-x-1">
                <span>Limpiar filtros y ver todos</span>
            </button>
        </div>

    </section>


    <!-- 5. WIDGET Y VENTANA FLOTANTE DEL COPILOTO IA TERRITORIAL -->
    <!-- Micro-invitación pedagógica y sobria (CIT-UAI) -->
    <div id="copilotWelcomeHint" onclick="toggleCopilot(true); dismissCopilotHint(event);" class="cursor-pointer fixed bottom-20 right-3 sm:right-6 z-40 w-[calc(100vw-1.5rem)] max-w-[310px] sm:max-w-[340px] bg-[#0A192F] text-slate-200 border border-slate-700/80 border-t-2 border-t-[#6493B5] rounded-xl shadow-2xl p-3 text-xs leading-relaxed hidden transition-all duration-300">
        <div class="flex items-start justify-between gap-2">
            <p class="font-normal text-slate-300 text-[11px] sm:text-xs select-none">
                Orientación sobre los 19 geoportales del Estado y metodologías MBHT. Puede consultar aquí al Copiloto CIT.
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
                    <p class="text-[11px] text-slate-400">Directorio de geoportales e insumos</p>
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
                        Bienvenido/a al directorio de interoperabilidad territorial del <strong>CIT-UAI</strong>. El fortalecimiento de la red de geoportales públicos es clave para construir diagnósticos integrados de <strong>Bienestar Humano Territorial (MBHT)</strong>, articulando coberturas espaciales y servicios en beneficio de las comunidades.
                    </p>
                    <p class="text-slate-600 text-[11px] sm:text-xs font-normal">
                        Puedo orientarle en la localización y conexión a los 19 geoportales e infraestructuras de datos espaciales del Estado de Chile:
                    </p>
                    <div class="flex flex-col gap-1.5 pt-1">
                        <button onclick="askCopilot('¿Dónde encuentro datos de red vial y obras públicas?')" class="text-xs bg-white hover:bg-slate-100 text-left text-slate-700 px-3 py-2 rounded-lg border border-slate-200 transition cursor-pointer">
                            ¿Dónde encuentro datos de red vial y obras públicas?
                        </button>
                        <button onclick="askCopilot('¿Qué geoportales disponen de cartografía censal y planes reguladores?')" class="text-xs bg-white hover:bg-slate-100 text-left text-slate-700 px-3 py-2 rounded-lg border border-slate-200 transition cursor-pointer">
                            ¿Qué geoportales disponen de cartografía censal y planes reguladores?
                        </button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Formulario de Entrada -->
        <div class="p-2.5 sm:p-3 bg-white border-t border-slate-200 shrink-0">
            <form id="copilotForm" onsubmit="handleCopilotSubmit(event)" class="flex items-center space-x-2">
                <input type="text" id="copilotInput" placeholder="Pregunta sobre los geoportales de Chile..." 
                       class="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:bg-white transition" />
                <button type="submit" class="bg-slate-900 hover:bg-black text-white p-2 sm:p-2.5 rounded-xl transition cursor-pointer shrink-0">
                    <i data-lucide="send" class="w-4 h-4"></i>
                </button>
            </form>
        </div>

    </div>
    </main><!-- /main#main-content -->

{canonical_footer}

    <!-- 7. SCRIPT DE INTERACTIVIDAD, FILTROS Y COPILOTO IA -->
    <script>
        // Catálogo de IDEs inyectado desde Python
        const idesData = {ides_json_str};
        let currentCategory = 'all';

        // Render inicial al cargar el DOM
        document.addEventListener('DOMContentLoaded', () => {{
            renderIdesGrid(idesData);
            if (window.lucide) lucide.createIcons();
            initCopilotHint();
            
            // Menú móvil
            const menuBtn = document.getElementById('mobileMenuBtn');
            const mobileMenu = document.getElementById('mobileMenu');
            if (menuBtn && mobileMenu) {{
                menuBtn.addEventListener('click', () => {{
                    mobileMenu.classList.toggle('hidden');
                }});
            }}
        }});

        function closeMobileMenu() {{
            const mobileMenu = document.getElementById('mobileMenu');
            if (mobileMenu) mobileMenu.classList.add('hidden');
        }}

        // El botón scroll to top (volver arriba) y su control están gestionados universalmente por get_canonical_footer_html()

        function setCategoryFilter(category, btn) {{
            currentCategory = category;
            document.querySelectorAll('.ide-cat-btn').forEach(b => {{
                b.classList.remove('active', 'bg-slate-900', 'text-white', 'shadow-xs', 'font-bold');
                b.classList.add('bg-slate-100', 'text-slate-700', 'font-medium');
            }});
            btn.classList.remove('bg-slate-100', 'text-slate-700', 'font-medium');
            btn.classList.add('active', 'bg-slate-900', 'text-white', 'shadow-xs', 'font-bold');
            filterIdes();
        }}

        function filterIdes() {{
            const query = (document.getElementById('searchInput').value || '').trim().toLowerCase();
            const clearBtn = document.getElementById('clearSearchBtn');
            if (clearBtn) {{
                if (query.length > 0) clearBtn.classList.remove('hidden');
                else clearBtn.classList.add('hidden');
            }}

            const filtered = idesData.filter(ide => {{
                // Filtro por categoría
                let matchCat = true;
                if (currentCategory !== 'all') {{
                    const catLower = (ide.categoria || '').toLowerCase();
                    if (currentCategory === 'Nacional') {{
                        matchCat = catLower.includes('nacional') || catLower.includes('coordinación') || catLower.includes('centralizador');
                    }} else if (currentCategory === 'Urbano') {{
                        matchCat = catLower.includes('urbano') || catLower.includes('habitacional') || catLower.includes('académico') || catLower.includes('censos') || catLower.includes('estadística');
                    }} else if (currentCategory === 'Medio Ambiente') {{
                        matchCat = catLower.includes('ambiente') || catLower.includes('hídrico') || catLower.includes('forestal') || catLower.includes('silvo') || catLower.includes('pesca');
                    }} else if (currentCategory === 'Infraestructura') {{
                        matchCat = catLower.includes('infraestructura') || catLower.includes('energía') || catLower.includes('regional') || catLower.includes('aeroespacial') || catLower.includes('obras') || catLower.includes('patrimonio');
                    }}
                }}

                // Filtro por texto
                let matchText = true;
                if (query.length > 0) {{
                    const queStr = (ide.que_encontraras || []).join(' ');
                    const fullText = ((ide.nombre || '') + ' ' + (ide.titulo || '') + ' ' + (ide.institucion || '') + ' ' + (ide.categoria || '') + ' ' + (ide.descripcion || '') + ' ' + queStr).toLowerCase();
                    matchText = fullText.includes(query);
                }}

                return matchCat && matchText;
            }});

            renderIdesGrid(filtered);
        }}

        function clearSearch() {{
            const input = document.getElementById('searchInput');
            if (input) input.value = '';
            filterIdes();
        }}

        function renderIdesGrid(items) {{
            const grid = document.getElementById('idesGrid');
            const noResults = document.getElementById('noResultsState');
            const counter = document.getElementById('resultsCount');

            if (counter) counter.innerText = items.length;

            if (!items || items.length === 0) {{
                grid.classList.add('hidden');
                noResults.classList.remove('hidden');
                return;
            }}

            grid.classList.remove('hidden');
            noResults.classList.add('hidden');
            grid.innerHTML = '';

            items.forEach(ide => {{
                const card = document.createElement('div');
                card.className = "group bg-white rounded-xl p-4 sm:p-5 border border-slate-200 shadow-clean hover:shadow-hover hover:border-slate-400 transition flex flex-col justify-between";

                let queEncontrarasHtml = '';
                if (ide.que_encontraras && Array.isArray(ide.que_encontraras) && ide.que_encontraras.length > 0) {{
                    const itemsHtml = ide.que_encontraras.map(item => `
                        <li class="flex items-start space-x-1.5 text-[11px] text-slate-600 leading-tight">
                            <span class="text-slate-400 font-bold">·</span>
                            <span>${{item}}</span>
                        </li>
                    `).join('');
                    queEncontrarasHtml = `
                        <div class="mt-3 pt-3 border-t border-slate-100 bg-slate-50/80 -mx-4 p-3 sm:-mx-5 sm:p-3.5 rounded-b-lg space-y-1.5">
                            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Coberturas e insumos principales</span>
                            <ul class="space-y-1 pl-0.5">
                                ${{itemsHtml}}
                            </ul>
                        </div>
                    `;
                }}

                card.innerHTML = `
                    <div class="flex-1 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">${{ide.institucion}}</span>
                                <span class="text-[11px] font-mono text-slate-400">${{ide.categoria}}</span>
                            </div>
                            <h4 class="font-bold text-slate-900 text-sm sm:text-base mb-1.5 group-hover:text-black transition leading-snug">${{ide.nombre}}</h4>
                            <p class="text-xs text-slate-600 leading-relaxed font-normal">${{ide.descripcion}}</p>
                        </div>
                        ${{queEncontrarasHtml}}
                    </div>
                    <a href="${{ide.url}}" target="_blank" rel="noopener noreferrer" class="mt-3.5 w-full bg-slate-50 hover:bg-slate-900 hover:text-white text-slate-700 border border-slate-200 hover:border-slate-900 rounded-lg py-2 px-3 text-xs font-semibold flex items-center justify-center space-x-1.5 transition cursor-pointer group-hover:bg-slate-900 group-hover:text-white">
                        <span>Ir al geoportal</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                    </a>
                `;
                grid.appendChild(card);
            }});

            if (window.lucide) lucide.createIcons();
        }}

        // ==========================================
        // COPILOTO IA TERRITORIAL
        // ==========================================
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

        function toggleCopilot(forceState = null) {{
            dismissCopilotHint();
            const drawer = document.getElementById('copilotDrawer');
            if (forceState !== null) {{
                if (forceState) drawer.classList.remove('hidden'), drawer.classList.add('flex');
                else drawer.classList.add('hidden'), drawer.classList.remove('flex');
            }} else {{
                drawer.classList.toggle('hidden');
                drawer.classList.toggle('flex');
            }}
            if (!drawer.classList.contains('hidden')) {{
                setTimeout(() => document.getElementById('copilotInput')?.focus(), 150);
            }}
        }}

        function handleCopilotSubmit(e) {{
            e.preventDefault();
            const input = document.getElementById('copilotInput');
            const q = input.value.trim();
            if (!q) return;
            askCopilot(q);
            input.value = '';
        }}

        async function askCopilot(question) {{
            toggleCopilot(true);
            const container = document.getElementById('copilotMessages');
            
            // Mensaje usuario
            const userMsg = document.createElement('div');
            userMsg.className = "flex items-start justify-end space-x-2";
            userMsg.innerHTML = `
                <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-none text-xs sm:text-sm max-w-[85%] shadow-xs">
                    <p>${{question}}</p>
                </div>
            `;
            container.appendChild(userMsg);
            container.scrollTop = container.scrollHeight;

            // Respuesta determinista inteligente del motor CIT
            const res = await resolveCopilotResponse(question);
            const replyText = typeof res === 'string' ? res : (res.text || res);

            setTimeout(() => {{
                const botMsg = document.createElement('div');
                botMsg.className = "flex items-start space-x-2.5";
                botMsg.innerHTML = `
                    <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold border border-slate-700">
                        CIT
                    </div>
                    <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 text-slate-800 space-y-2 shadow-xs max-w-[85%] text-xs sm:text-sm">
                        <p class="leading-relaxed">${{replyText}}</p>
                    </div>
                `;
                container.appendChild(botMsg);
                container.scrollTop = container.scrollHeight;
                if (window.lucide) lucide.createIcons();
            }}, 200);
        }}

        {copilot_js_engine}
        window.dismissCopilotHint = dismissCopilotHint;
        window.toggleCopilot = toggleCopilot;
    </script>
</body>
</html>
"""
    return html


def main() -> None:
    """Función de entrada para la generación de red-ides.html."""
    root_dir = find_proyecto_root()
    ide_dir = root_dir / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
    catalog_path = ide_dir / "data" / "catalogo_ide_cit.json"
    output_path = ide_dir / "public" / "red-ides.html"

    print(f"[*] Leyendo catálogo central: {catalog_path}")
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    print(f"[*] Generando página independiente 'red-ides.html'...")
    html_content = generate_red_ides_html(catalog_data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] 'red-ides.html' generada exitosamente ({len(html_content):,} bytes) en: {output_path}")


if __name__ == "__main__":
    main()
