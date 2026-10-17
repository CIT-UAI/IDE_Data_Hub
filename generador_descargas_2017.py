"""
generador_descargas_2017.py
Generador autónomo y canónico de la página 'descargas-2017.html' de la IDE CIT.
Centro de Descargas Territoriales — Matriz de Bienestar Humano Territorial (MBHT 2017).

Arquitectura y Directivas:
- Cumple con AGENTS.md (find_proyecto_root, estándares UAI, sobriedad institucional).
- Comparte el encabezado canónico con get_canonical_header_html("descargas").
- Comparte el pie de página institucional con get_canonical_footer_html(version).
- Implementa selectores dinámicos multiformato (GeoParquet, GeoPackage, Shapefile, CSV).
- Verificación criptográfica SHA-256 y snippets de análisis listos en Python y R.
- Copiloto IA Territorial integrado en drawer modal con síntesis de voz.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from motor_ia_cit import (
    find_proyecto_root,
    get_canonical_footer_html,
    get_canonical_header_html,
    get_copilot_js_engine,
    get_llm_guidance_html,
    get_llm_head_meta,
)

logger = logging.getLogger("Descargas2017Builder")


def generate_static_downloads_table(descargas_2017_data: Dict[str, Any]) -> str:
    """
    Genera una tabla semántica HTML con el catálogo de descargas de las 16 regiones y el consolidado nacional.
    Permite a cualquier bot, crawler o agente de IA extraer la lista completa de archivos descargables.
    """
    regiones_info = [
        ("Nacional", "Chile Consolidado (16 Regiones)", "204.906", "55.035", "1.589.595"),
        ("R15", "Arica y Parinacota", "3.304", "905", "19.408"),
        ("R01", "Tarapacá", "3.247", "763", "20.909"),
        ("R02", "Antofagasta", "7.357", "1.117", "36.385"),
        ("R03", "Atacama", "5.529", "1.293", "36.006"),
        ("R04", "Coquimbo", "12.251", "3.448", "94.779"),
        ("R05", "Valparaíso", "25.321", "4.976", "159.189"),
        ("R13", "Metropolitana de Santiago", "55.754", "15.226", "267.480"),
        ("R06", "O'Higgins", "11.004", "4.476", "90.578"),
        ("R07", "Maule", "14.774", "5.089", "135.554"),
        ("R16", "Ñuble", "6.522", "1.569", "79.448"),
        ("R08", "Biobío", "19.150", "6.160", "230.224"),
        ("R09", "La Araucanía", "15.394", "3.414", "167.663"),
        ("R14", "Los Ríos", "6.371", "1.481", "66.192"),
        ("R10", "Los Lagos", "13.421", "3.999", "139.772"),
        ("R11", "Aysén", "2.154", "614", "18.902"),
        ("R12", "Magallanes y de la Antártica Chilena", "3.353", "505", "27.106"),
    ]
    rows = []
    for cod, nombre, mzs, equips, vias in regiones_info:
        is_nac = (cod == "Nacional")
        bg_cls = "bg-slate-50 font-bold" if is_nac else "hover:bg-slate-50"
        rows.append(f"""<tr class="{bg_cls} transition border-b border-slate-100">
            <td class="px-3.5 py-2.5 font-semibold text-slate-900">{cod}</td>
            <td class="px-3.5 py-2.5 text-slate-700">{nombre}</td>
            <td class="px-3.5 py-2.5 font-mono text-slate-600 text-right">{mzs}</td>
            <td class="px-3.5 py-2.5 font-mono text-slate-600 text-right">{equips}</td>
            <td class="px-3.5 py-2.5 font-mono text-slate-600 text-right">{vias}</td>
            <td class="px-3.5 py-2.5 text-center">
                <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-800 font-mono text-[11px]">GeoParquet · GPKG · SHP · CSV</span>
            </td>
        </tr>""")
    rows_html = "\n".join(rows)

    return f"""
            <!-- Tabla Semántica de Coberturas Descargables para Usuarios e Inspección IA -->
            <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-clean mb-12">
                <div class="flex items-center justify-between mb-4 border-b border-slate-100 pb-3">
                    <div>
                        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Inventario Nacional Completo</span>
                        <h3 class="text-lg sm:text-xl font-bold text-slate-900">Coberturas disponibles por región y nivel nacional</h3>
                    </div>
                    <span class="text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700">16 Regiones + Consolidado</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs sm:text-sm text-slate-600">
                        <thead class="bg-slate-100 text-slate-800 uppercase font-bold text-[11px]">
                            <tr>
                                <th class="px-3.5 py-2.5">Código</th>
                                <th class="px-3.5 py-2.5">Territorio / Región</th>
                                <th class="px-3.5 py-2.5 text-right">Manzanas</th>
                                <th class="px-3.5 py-2.5 text-right">Equipamientos</th>
                                <th class="px-3.5 py-2.5 text-right">Tramos Viales</th>
                                <th class="px-3.5 py-2.5 text-center">Formatos Abiertos</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
    """


def generate_descargas_2017_html(catalog_data: Dict[str, Any], descargas_2017_data: Dict[str, Any]) -> str:
    """
    Genera el documento HTML completo y canónico para 'descargas-2017.html'.
    """
    portal = catalog_data.get("portal", {})
    version = portal.get("version", "2026.1")
    copilot_js_engine = get_copilot_js_engine()
    llm_head_meta = get_llm_head_meta()
    llm_guidance_html = get_llm_guidance_html()
    canonical_header = get_canonical_header_html("descargas")
    canonical_footer = get_canonical_footer_html(version)
    descargas_2017_json_str = json.dumps(descargas_2017_data, ensure_ascii=False)
    static_downloads_table = generate_static_downloads_table(descargas_2017_data)

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-50 scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centro de descargas territoriales | IDE CIT · Universidad Adolfo Ibáñez</title>
    
    <!-- Metadatos SEO e Institucionales -->
    <meta name="description" content="Descargas abiertas MBHT 2017: 204.906 manzanas censales con indicadores de bienestar, 55.035 equipamientos y 1.589.595 tramos viales en GeoParquet, GeoPackage y Shapefile.">
    <meta name="keywords" content="MBHT 2017, Descargas datos abiertos, Manzanas censales Chile, Equipamientos urbanos, Red vial caminable, GeoParquet, GeoPackage, Shapefile, CSV, CIT UAI">
    <meta name="author" content="Centro de Inteligencia Territorial (CIT-UAI)">
    <meta name="version" content="{version}">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="https://ide.cit.uai.cl/descargas">
    
{llm_head_meta}
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="IDE CIT — Centro de Inteligencia Territorial (UAI)">
    <meta property="og:title" content="Centro de descargas territoriales | IDE CIT">
    <meta property="og:description" content="Descarga abierta y gratuita de cartografía censal 2017, equipamientos de bienestar humano y red vial nacional en formatos abiertos y eficientes.">
    <meta property="og:url" content="https://ide.cit.uai.cl/descargas">
    <meta property="og:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@CIT_UAI">
    <meta name="twitter:title" content="Descargas MBHT 2017 | IDE CIT - CIT UAI">
    <meta name="twitter:description" content="204.906 manzanas censales, equipamientos e infraestructura peatonal de Chile listos para descargar y analizar.">
    <meta name="twitter:image" content="https://matrizbht.cl/_nuxt/img/logo-black.9616122.svg">

    <!-- Schema.org / JSON-LD DataCatalog -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": "Centro de Descargas Territoriales — IDE CIT",
        "description": "Repositorio de descargas abiertas de la línea base oficial de la Matriz de Bienestar Humano Territorial (MBHT 2017) a escala de manzana censal en Chile.",
        "url": "https://ide.cit.uai.cl/descargas",
        "provider": {{
            "@type": "EducationalOrganization",
            "name": "Centro de Inteligencia Territorial · Universidad Adolfo Ibáñez",
            "url": "https://cit.uai.cl"
        }},
        "license": "https://creativecommons.org/licenses/by/4.0/deed.es",
        "spatialCoverage": "Chile (16 Regiones, 345 Comunas)"
    }}
    </script>

    <!-- Favicon y manifiesto PWA -->
    <link rel="icon" type="image/svg+xml" href="img/logo-ide-standalone.svg">
    <link rel="manifest" href="site.webmanifest">
    
    <!-- Google Fonts: Roboto y JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">

    <!-- Tailwind CSS v3 -->
    <script src="https://cdn.tailwindcss.com"></script>
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
    </style>
</head>
<body class="h-full flex flex-col font-sans bg-slate-100 text-slate-800 antialiased overflow-x-hidden">

<noscript>
    <div class="bg-slate-900 text-slate-200 border-b border-slate-800 px-4 py-4 text-sm">
        <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
                <strong class="text-white">Acceso directo sin JavaScript:</strong>
                <span>La tabla maestra inferior contiene los enlaces estáticos directos a los paquetes nacionales y a las 16 regiones en GeoParquet, GeoPackage, Shapefile y CSV.</span>
            </div>
            <div class="flex flex-wrap gap-3 font-semibold text-uai-gold shrink-0">
                <a href="download/MBHT_2017_Nacional_Manzanas.parquet" class="underline hover:text-white">Manzanas (.parquet)</a>
                <a href="download/Equipamientos_2017_Nacional_Consolidado.parquet" class="underline hover:text-white">Equipamientos (.parquet)</a>
                <a href="download/Red_Vial_Ejes_2017_Nacional.parquet" class="underline hover:text-white">Red vial (.parquet)</a>
                <a href="download/SHA256SUMS.txt" class="underline hover:text-white">SHA256SUMS.txt</a>
            </div>
        </div>
    </div>
</noscript>

{llm_guidance_html}

{canonical_header}

    <!-- 2. CABECERA HERO DE DESCARGAS TERRITORIALES -->
    <main id="main-content" role="main" tabindex="-1">
    <section class="bg-white border-b border-slate-200 py-8 sm:py-12 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <!-- Migas de pan (Breadcrumbs) -->
            <nav class="flex items-center space-x-2 text-xs text-slate-400 mb-4 sm:mb-5">
                <a href="inicio" class="hover:text-slate-700 transition">IDE CIT</a>
                <span class="text-slate-300">/</span>
                <span class="text-slate-500 font-medium">Descargas abiertas</span>
                <span class="text-slate-300">/</span>
                <span class="text-slate-800 font-bold">Línea base oficial MBHT 2017</span>
            </nav>

            <div class="w-full">
                <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-800 text-[11px] sm:text-xs font-bold uppercase tracking-wider mb-3">
                    <span class="w-2 h-2 rounded-full bg-uai-gold"></span>
                    <span>Línea base oficial 2017 (v1.0.3) · 204.906 manzanas (17.482.699 hab.) · 42 columnas físicas · 55.035 equipamientos</span>
                </div>
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
                    Centro de descargas territoriales
                </h1>
                <p class="text-sm sm:text-base lg:text-lg text-slate-600 mt-2.5 sm:mt-3 leading-relaxed font-normal w-full">
                    Repositorio de descarga directa, abierta y gratuita de las coberturas maestras de la línea base oficial de la Matriz de Bienestar Humano Territorial (MBHT 2017). Selecciona la cobertura temática, la región y la comuna para descargar los archivos en formatos optimizados para software SIG y ciencia de datos.
                </p>
            </div>

            <!-- Pastillas de características técnicas -->
            <div class="mt-6 flex flex-wrap gap-2 text-xs">
                <span class="px-2.5 py-1 rounded-md bg-slate-900 text-white font-semibold flex items-center space-x-1.5 shadow-xs">
                    <i data-lucide="shield-check" class="w-3.5 h-3.5 text-uai-gold"></i>
                    <span>Línea Base Oficial MBHT 2017 (v1.0.3)</span>
                </span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">Esquema 42 Columnas Físicas</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">GeoParquet 1.1</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">GeoPackage (.gpkg)</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">Shapefile (.zip)</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">CSV UTF-8</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">EPSG:4326 (WGS 84)</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">SHA-256 Verificado</span>
                <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200 font-medium">Licencia Abierta CC BY 4.0</span>
            </div>

            <!-- Cuadratura Metodológica Canónica (Línea Base Oficial) -->
            <div class="mt-6 p-4 sm:p-5 rounded-xl bg-slate-900 text-slate-200 border border-slate-800 text-xs sm:text-sm">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-2.5 mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="w-2 h-2 rounded-full bg-uai-gold"></span>
                        <span class="font-bold text-white text-xs uppercase tracking-wider">Cuadratura Demográfica y Esquema Físico (v1.0.3)</span>
                    </div>
                    <span class="font-mono text-[11px] text-slate-400">Verificado con tolerancia cero (&Delta; = 0)</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 leading-relaxed">
                    <div>
                        <strong class="text-white block font-semibold mb-1">Población censal amanzanada</strong>
                        <span class="text-slate-300">17.482.699 habitantes en 204.906 manzanas censales (99,48% de 17.574.003 censados INE). Los 91.304 hab. restantes corresponden a población en tránsito, situación de calle y áreas sin amanzanamiento físico.</span>
                    </div>
                    <div>
                        <strong class="text-white block font-semibold mb-1">Esquema analítico exhaustivo</strong>
                        <span class="text-slate-300">Los 4 formatos de descarga (GeoParquet, GeoPackage, Shapefile y CSV) contienen las 42 columnas físicas canónicas completas (bht, dimensiones, subindicadores, demografía por tramos etarios y linaje).</span>
                    </div>
                    <div>
                        <strong class="text-white block font-semibold mb-1">Separación MBHT 2017 / 2024</strong>
                        <span class="text-slate-300">Línea base oficial vigente MBHT 2017 cerrada (<code class="font-mono text-slate-200">v1.0.3</code>). La actualización integral MBHT 2024 tiene lanzamiento oficial previsto para noviembre de 2026.</span>
                    </div>
                </div>
            </div>

        </div>
    </section>

    <!-- 3. PANEL DE CONTROL INTERACTIVO DE DESCARGAS -->
    <section class="py-10 sm:py-14 px-4 sm:px-6 lg:px-10 xl:px-12">
        <div class="max-w-[1600px] mx-auto">
            
            <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-clean mb-10">
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
                    
                    <!-- Selector 1: Cobertura / Tema -->
                    <div>
                        <label for="selDescargaTipo" class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                            <i data-lucide="layers" class="w-3.5 h-3.5 text-slate-500"></i>
                            <span>1. Cobertura / Tema</span>
                        </label>
                        <select id="selDescargaTipo" onchange="updateDescargas2017()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-slate-800 font-medium focus:ring-2 focus:ring-slate-900 focus:border-slate-900 outline-none transition shadow-xs">
                            <optgroup label="Cartografía Censal e Indicadores">
                                <option value="manzanas" selected>Manzanas Censales MBHT 2017 (Indicadores y MUD)</option>
                            </optgroup>
                            <optgroup label="Equipamientos Urbanos">
                                <option value="equip_todos">Equipamientos Urbanos — Consolidado (Todos los servicios)</option>
                                <option value="equip_isal">Salud (ISAL — Hospitales, CESFAM, Postas, Clínicas)</option>
                                <option value="equip_ise">Educación (ISE — Jardines, Escuelas, Liceos, CFT/Univ)</option>
                                <option value="equip_iav">Áreas Verdes y Plazas (IAV — Parques, plazas, recreación)</option>
                                <option value="equip_idep">Deportes (IDEP — Estadios, canchas, polideportivos)</option>
                                <option value="equip_icul">Cultura y Patrimonio (ICUL — Teatros, museos, bibliotecas)</option>
                                <option value="equip_iser">Servicios Públicos (ISER — Municipios, bomberos, oficinas)</option>
                            </optgroup>
                            <optgroup label="Red Vial y Caminabilidad">
                                <option value="red_vial">Red Vial Caminable Ejes Tobler (Vías peatonales modeladas)</option>
                            </optgroup>
                        </select>
                    </div>

                    <!-- Selector 2: Región -->
                    <div>
                        <label for="selDescargaRegion" class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                            <i data-lucide="map-pin" class="w-3.5 h-3.5 text-slate-500"></i>
                            <span>2. Región</span>
                        </label>
                        <select id="selDescargaRegion" onchange="onRegionChange()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-slate-800 font-medium focus:ring-2 focus:ring-slate-900 focus:border-slate-900 outline-none transition shadow-xs">
                            <option value="NACIONAL" selected>Consolidado Nacional (Chile Completo)</option>
                            <optgroup label="Regiones de Chile">
                                <option value="R15">Región de Arica y Parinacota (R15)</option>
                                <option value="R01">Región de Tarapacá (R01)</option>
                                <option value="R02">Región de Antofagasta (R02)</option>
                                <option value="R03">Región de Atacama (R03)</option>
                                <option value="R04">Región de Coquimbo (R04)</option>
                                <option value="R05">Región de Valparaíso (R05)</option>
                                <option value="R13">Región Metropolitana de Santiago (R13)</option>
                                <option value="R06">Región de O'Higgins (R06)</option>
                                <option value="R07">Región del Maule (R07)</option>
                                <option value="R16">Región de Ñuble (R16)</option>
                                <option value="R08">Región del Biobío (R08)</option>
                                <option value="R09">Región de La Araucanía (R09)</option>
                                <option value="R14">Región de Los Ríos (R14)</option>
                                <option value="R10">Región de Los Lagos (R10)</option>
                                <option value="R11">Región de Aysén (R11)</option>
                                <option value="R12">Región de Magallanes (R12)</option>
                            </optgroup>
                        </select>
                    </div>

                    <!-- Selector 3: Comuna (Filtrado Inteligente) -->
                    <div>
                        <label for="selDescargaComuna" class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                            <i data-lucide="compass" class="w-3.5 h-3.5 text-slate-500"></i>
                            <span>3. Comuna (Filtrado y atributos)</span>
                        </label>
                        <select id="selDescargaComuna" onchange="updateDescargas2017()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-slate-800 font-medium focus:ring-2 focus:ring-slate-900 focus:border-slate-900 outline-none transition shadow-xs">
                            <option value="all">Todas las comunas de Chile (345 comunas)</option>
                        </select>
                    </div>

                </div>

                <!-- Tarjeta del Paquete Seleccionado -->
                <div class="mt-6 pt-6 border-t border-slate-200">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                        <div>
                            <div class="flex items-center gap-2 flex-wrap mb-1.5">
                                <span id="badgeDescargaTipo" class="text-xs font-bold px-2.5 py-0.5 rounded bg-slate-900 text-uai-gold border border-slate-800">Manzanas MBHT 2017</span>
                                <span id="badgeDescargaAmbito" class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-200 text-slate-700">Nacional</span>
                                <span id="badgeDescargaRegistros" class="text-xs text-slate-500 font-mono">204.906 registros</span>
                            </div>
                            <h3 id="descargaTituloPaquete" class="text-base sm:text-lg font-bold text-slate-900">
                                Manzanas censales MBHT 2017 — Consolidado nacional
                            </h3>
                            <p class="text-xs text-slate-500 mt-0.5">Línea base oficial MBHT 2017 · Sistema de coordenadas EPSG:4326 (WGS 84) / SIRGAS-Chile</p>
                        </div>

                        <!-- Ayuda y Documentación Rápida -->
                        <div class="flex items-center space-x-2 shrink-0">
                            <a href="ficha-mbht-2017" class="text-xs font-semibold text-slate-900 hover:text-black bg-slate-100 hover:bg-slate-200 border border-slate-300 px-3 py-2 rounded-lg transition flex items-center space-x-1.5 shadow-xs">
                                <i data-lucide="file-text" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>Ficha técnica</span>
                            </a>
                            <a href="guia-tecnica" class="text-xs font-semibold text-slate-700 hover:text-black bg-white hover:bg-slate-100 border border-slate-300 px-3 py-2 rounded-lg transition flex items-center space-x-1.5 shadow-xs">
                                <i data-lucide="book-open" class="w-3.5 h-3.5 text-slate-600"></i>
                                <span>Ver guía técnica</span>
                            </a>
                            <button onclick="toggleCopilot(true)" class="text-xs font-semibold text-uai-gold hover:text-white bg-slate-900 hover:bg-black px-3 py-2 rounded-lg transition flex items-center space-x-1.5 shadow-xs cursor-pointer">
                                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-uai-gold"></i>
                                <span>Consultar al Copiloto</span>
                            </button>
                        </div>
                    </div>

                    <!-- 4 Tarjetas de Formatos de Descarga Directa -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 sm:gap-4 mb-6">
                        
                        <!-- Formato 1: GeoParquet (Recomendado) -->
                        <div class="bg-white border-2 border-slate-900 rounded-xl p-4 shadow-sm flex flex-col justify-between relative overflow-hidden group">
                            <div class="absolute top-0 right-0 bg-slate-900 text-uai-gold text-[9px] font-bold px-2 py-0.5 rounded-bl uppercase tracking-wider">
                                Recomendado
                            </div>
                            <div>
                                <div class="flex items-center space-x-2 mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-900 text-uai-gold flex items-center justify-center font-bold text-xs">PQ</div>
                                    <span class="font-bold text-slate-900 text-sm">GeoParquet 1.1</span>
                                </div>
                                <p class="text-xs text-slate-500 leading-relaxed font-normal mb-3">Compresión columnar Snappy. Máxima velocidad de lectura y menor tamaño en disco.</p>
                            </div>
                            <div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 font-mono">
                                    <span>Tamaño:</span>
                                    <span id="sizeDescargaParquet" class="font-semibold text-slate-700">240,9 MB</span>
                                </div>
                                <a id="btnDescargaParquet" href="download/MBHT_2017_Nacional_Manzanas.parquet" download class="w-full bg-slate-900 hover:bg-black active:bg-slate-800 text-white text-xs font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-xs cursor-pointer">
                                    <i data-lucide="download" class="w-3.5 h-3.5 stroke-[2]"></i>
                                    <span>Descargar .parquet</span>
                                </a>
                            </div>
                        </div>

                        <!-- Formato 2: GeoPackage (Estándar OGC) -->
                        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-clean hover:shadow-hover hover:border-slate-300 transition flex flex-col justify-between group">
                            <div>
                                <div class="flex items-center space-x-2 mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">GP</div>
                                    <span class="font-bold text-slate-900 text-sm">GeoPackage</span>
                                </div>
                                <p class="text-xs text-slate-500 leading-relaxed font-normal mb-3">Estándar internacional OGC basado en SQLite. Ideal para visualización directa en QGIS y ArcGIS.</p>
                            </div>
                            <div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 font-mono">
                                    <span>Tamaño:</span>
                                    <span id="sizeDescargaGPKG" class="font-semibold text-slate-700">343,9 MB</span>
                                </div>
                                <a id="btnDescargaGPKG" href="download/MBHT_2017_Nacional_Manzanas.gpkg" download class="w-full bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 hover:border-slate-400 text-xs font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-xs cursor-pointer">
                                    <i data-lucide="download" class="w-3.5 h-3.5 text-slate-600 stroke-[2]"></i>
                                    <span>Descargar .gpkg</span>
                                </a>
                            </div>
                        </div>

                        <!-- Formato 3: Shapefile (Compatibilidad Legacy) -->
                        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-clean hover:shadow-hover hover:border-slate-300 transition flex flex-col justify-between group">
                            <div>
                                <div class="flex items-center space-x-2 mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">SHP</div>
                                    <span class="font-bold text-slate-900 text-sm">Shapefile (.zip)</span>
                                </div>
                                <p class="text-xs text-slate-500 leading-relaxed font-normal mb-3">Empaquetado ESRI comprimido (.shp, .shx, .dbf, .prj) con proyección WGS 84 incorporada.</p>
                            </div>
                            <div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 font-mono">
                                    <span>Tamaño:</span>
                                    <span id="sizeDescargaSHP" class="font-semibold text-slate-700">204,9 MB</span>
                                </div>
                                <a id="btnDescargaSHP" href="download/MBHT_2017_Nacional_Manzanas_SHP.zip" download class="w-full bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 hover:border-slate-400 text-xs font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-xs cursor-pointer">
                                    <i data-lucide="download" class="w-3.5 h-3.5 text-slate-600 stroke-[2]"></i>
                                    <span>Descargar .zip</span>
                                </a>
                            </div>
                        </div>

                        <!-- Formato 4: CSV Tabular -->
                        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-clean hover:shadow-hover hover:border-slate-300 transition flex flex-col justify-between group">
                            <div>
                                <div class="flex items-center space-x-2 mb-2">
                                    <div class="w-7 h-7 rounded bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">CSV</div>
                                    <span class="font-bold text-slate-900 text-sm">CSV Tabular</span>
                                </div>
                                <p class="text-xs text-slate-500 leading-relaxed font-normal mb-3">Texto delimitado por comas con codificación UTF-8 para Excel, SPSS, R o bases de datos relacionales.</p>
                            </div>
                            <div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 font-mono">
                                    <span>Tamaño:</span>
                                    <span id="sizeDescargaCSV" class="font-semibold text-slate-700">96,2 MB</span>
                                </div>
                                <a id="btnDescargaCSV" href="download/MBHT_2017_Nacional_Manzanas.csv" download class="w-full bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 hover:border-slate-400 text-xs font-semibold py-2 px-3 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-xs cursor-pointer">
                                    <i data-lucide="download" class="w-3.5 h-3.5 text-slate-600 stroke-[2]"></i>
                                    <span>Descargar .csv</span>
                                </a>
                            </div>
                        </div>

                    </div>

                    <!-- Barra de Integridad Criptográfica SHA-256 -->
                    <div class="p-3.5 bg-slate-100 rounded-xl border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs mb-6">
                        <div class="flex items-center space-x-2.5 overflow-hidden w-full sm:w-auto">
                            <i data-lucide="hash" class="w-4 h-4 text-slate-600 shrink-0"></i>
                            <div class="overflow-hidden">
                                <span class="font-bold text-slate-800 block text-[11px]">Integridad criptográfica (SHA-256 Parquet):</span>
                                <input id="inputDescargaSha256" type="text" readonly value="4a123b83ea1cefa18661c25ea40b9c3fc2a319cf6a45abbbd72a2cb30c069f2a" class="font-mono text-[11px] text-slate-600 bg-transparent border-none p-0 w-full sm:w-96 outline-none select-all truncate" />
                            </div>
                        </div>
                        <div class="flex items-center space-x-2 shrink-0">
                            <button onclick="copyDescargaHash()" class="text-xs font-semibold text-slate-700 hover:text-black bg-white hover:bg-slate-200 border border-slate-300 px-3 py-1.5 rounded-lg transition flex items-center space-x-1 cursor-pointer">
                                <i data-lucide="copy" class="w-3 h-3 text-slate-600"></i>
                                <span>Copiar hash</span>
                            </button>
                            <a href="download/SHA256SUMS.txt" download class="text-xs font-semibold text-slate-700 hover:text-black bg-white hover:bg-slate-200 border border-slate-300 px-3 py-1.5 rounded-lg transition flex items-center space-x-1 cursor-pointer">
                                <i data-lucide="file-check" class="w-3 h-3 text-slate-600"></i>
                                <span>SHA256SUMS.txt</span>
                            </a>
                        </div>
                    </div>

                    <!-- Comando de Verificación Local Independiente -->
                    <div class="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-600 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-1 font-mono">
                        <span class="text-slate-500 font-sans font-medium">Verificación local en terminal:</span>
                        <div class="space-x-2">
                            <span>Windows: <code>certutil -hashfile MBHT_2017_Nacional_Manzanas.parquet SHA256</code></span>
                            <span class="text-slate-300">|</span>
                            <span>Linux/macOS: <code>sha256sum -c SHA256SUMS.txt</code></span>
                        </div>
                    </div>

                    <!-- Verificador de Integridad de Archivos en el Navegador (Web Crypto API SHA-256) -->
                    <div class="bg-white border-2 border-dashed border-slate-300 hover:border-[#6493B5] rounded-xl p-4 sm:p-5 mb-6 transition text-center" id="shaDropZone">
                        <input type="file" id="shaFileInput" class="hidden" onchange="handleShaFileSelect(event)" />
                        <div class="flex flex-col items-center justify-center space-y-2">
                            <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600">
                                <i data-lucide="shield-check" class="w-5 h-5 text-[#6493B5]"></i>
                            </div>
                            <div>
                                <h4 class="text-xs sm:text-sm font-bold text-slate-800">Verificador de Integridad Criptográfica en el Navegador (Web Crypto API)</h4>
                                <p class="text-[11px] text-slate-500 max-w-xl mx-auto mt-0.5">
                                    Arrastra aquí tu archivo descargado (.parquet, .gpkg, .zip, .csv) o <button type="button" onclick="document.getElementById('shaFileInput').click()" class="text-[#6493B5] font-semibold hover:underline cursor-pointer">haz clic para seleccionarlo</button>. El hash se calcula 100% en tu navegador sin subir datos a ningún servidor.
                                </p>
                            </div>
                            <div id="shaVerifyResult" class="hidden w-full mt-2 pt-2 border-t border-slate-100 text-xs text-left">
                                <!-- Resultado interactivo -->
                            </div>
                        </div>
                    </div>

                    <!-- Código de Ejemplo en Python y R para Carga Directa -->
                    <div class="bg-slate-900 rounded-xl p-4 text-white">
                        <div class="flex items-center justify-between mb-2">
                            <div class="flex items-center space-x-3">
                                <span class="text-xs font-bold text-uai-gold uppercase tracking-wider">Lectura directa en script</span>
                                <div class="flex items-center space-x-2 text-xs">
                                    <button id="btnLangPython" onclick="setSnippetLang('python')" class="text-[11px] font-bold text-slate-900 underline cursor-pointer">Python (GeoPandas)</button>
                                    <span class="text-slate-600">|</span>
                                    <button id="btnLangR" onclick="setSnippetLang('r')" class="text-[11px] font-medium text-slate-400 hover:text-slate-900 cursor-pointer">R (sf / arrow)</button>
                                </div>
                            </div>
                            <button onclick="copyDescargaSnippet()" class="text-[11px] font-medium text-slate-300 hover:text-white flex items-center space-x-1 cursor-pointer">
                                <i data-lucide="copy" class="w-3 h-3"></i>
                                <span>Copiar código</span>
                            </button>
                        </div>
                        <div class="relative">
                            <input id="inputDescargaSnippet" type="text" readonly value="import geopandas as gpd; gdf = gpd.read_parquet('download/...')" class="w-full bg-black/50 border border-slate-800 rounded-lg px-3 py-2 text-xs font-mono text-slate-200 outline-none select-all" />
                        </div>
                        <p id="descargaComunaNoteText" class="text-[11px] text-slate-400 mt-2 leading-relaxed">
                            El paquete descargable contiene la cartografía completa del territorio seleccionado con atributos estandarizados. Puedes filtrarlo por comuna directamente en tu software SIG o script de análisis.
                        </p>
                    </div>

                </div>

            </div>

            <!-- Ficha de Control de Calidad Visible por Conjunto de Datos (Línea Base MBHT 2017 y Serie 2024) -->
            <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-clean mb-10">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-5">
                    <div>
                        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest">Control de calidad sistemático y gobernanza de datos</div>
                        <h2 class="text-lg sm:text-xl font-bold text-slate-900 mt-1">Matriz de verificación estructural, estado metodológico y custodia técnica</h2>
                        <p class="text-sm sm:text-base text-slate-600 mt-1">
                            El control de calidad certifica la <strong>validez geométrica y estructural automatizada</strong> (topología OGC, ausencia de IDs duplicados y sumas SHA-256, superada al 100% en todos los conjuntos) y el <strong>estado de validación metodológica</strong> de las coberturas abiertas vigentes (<code class="font-mono text-xs">v1.0.3</code>). La actualización integral MBHT 2024 tiene su lanzamiento oficial programado para noviembre; en esta plataforma se proveen los insumos demográficos del Censo 2024 con desagregación por Sprague y género.
                        </p>
                    </div>
                    <div class="text-xs font-mono text-slate-700 bg-slate-50 border border-slate-200 px-3.5 py-2.5 rounded-lg shrink-0 leading-relaxed">
                        <div>Auditoría: <strong>2026-10-15</strong> · Geometría OGC: <strong>100% (5/5)</strong></div>
                        <div>Estado metodológico: <strong>5 conjuntos vigentes · MBHT 2024 en nov.</strong></div>
                    </div>
                </div>

                <div class="overflow-x-auto border border-slate-200 rounded-xl mb-5">
                    <table class="w-full text-left border-collapse text-xs sm:text-sm">
                        <thead>
                            <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                                <th class="py-3 px-3.5 font-semibold">Conjunto de datos</th>
                                <th class="py-3 px-3.5 font-semibold text-right">Registros</th>
                                <th class="py-3 px-3.5 font-semibold">Cobertura y esquema</th>
                                <th class="py-3 px-3.5 font-semibold text-center">Geometría OGC</th>
                                <th class="py-3 px-3.5 font-semibold text-center">Atributos y nulos</th>
                                <th class="py-3 px-3.5 font-semibold text-center">IDs dup.</th>
                                <th class="py-3 px-3.5 font-semibold">Unidad responsable (Steward)</th>
                                <th class="py-3 px-3.5 font-semibold">Estado metodológico y versión</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 bg-white text-slate-700">
                            <tr class="hover:bg-slate-50">
                                <td class="py-3.5 px-3.5 font-bold text-slate-900">MBHT 2017 — Manzanas censales</td>
                                <td class="py-3.5 px-3.5 text-right font-mono font-bold text-slate-900">204.906</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Nacional (16 reg.) · 42 col. (4 macro-dim. + 6 acc.)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono text-emerald-800 font-semibold">100,0% válida</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">100,0% (0 nulos)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">0</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Modelación Espacial CIT-UAI</td>
                                <td class="py-3.5 px-3.5 font-semibold text-emerald-900">Cerrado vigente · v1.0.3</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="py-3.5 px-3.5 font-bold text-slate-900">Equipamientos 2017 (Línea base abierta)</td>
                                <td class="py-3.5 px-3.5 text-right font-mono font-bold text-slate-900">55.035</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Nacional (libre acceso; de 113.231 ruteables)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono text-emerald-800 font-semibold">100,0% válida</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">100,0% (0 nulos)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">0</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Datos y Catastros Sectoriales</td>
                                <td class="py-3.5 px-3.5 font-semibold text-emerald-900">Cerrado vigente · v1.0.3</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="py-3.5 px-3.5 font-bold text-slate-900">Red vial caminable Tobler 2017</td>
                                <td class="py-3.5 px-3.5 text-right font-mono font-bold text-slate-900">1.589.595</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Nacional (16 reg.) · Grafo continuo con DEM</td>
                                <td class="py-3.5 px-3.5 text-center font-mono text-emerald-800 font-semibold">100,0% válida</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">100,0% (0 nulos)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">0</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Lab. Redes y Geomática CIT</td>
                                <td class="py-3.5 px-3.5 font-semibold text-emerald-900">Cerrado vigente · v1.0.3</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="py-3.5 px-3.5 font-bold text-slate-900">Censo 2024 (Imputación Sprague y Género)</td>
                                <td class="py-3.5 px-3.5 text-right font-mono font-bold text-slate-900">254.395</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Nacional (manzanas y entidades censales)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono text-emerald-800 font-semibold">100,0% válida</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">100,0% (0 nulos)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">0</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Demografía y Estadística CIT</td>
                                <td class="py-3.5 px-3.5 font-semibold text-emerald-900">Cerrado vigente · v1.0.3</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="py-3.5 px-3.5 font-bold text-slate-900">Maritorio tricontinental y océano (PEM)</td>
                                <td class="py-3.5 px-3.5 text-right font-mono font-bold text-slate-900">4.585.566</td>
                                <td class="py-3.5 px-3.5 text-slate-600">ZEE, cuencas (53.726), montes (2.234) y GBIF/IFOP</td>
                                <td class="py-3.5 px-3.5 text-center font-mono text-emerald-800 font-semibold">100,0% válida</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">100,0% (0 nulos)</td>
                                <td class="py-3.5 px-3.5 text-center font-mono">0</td>
                                <td class="py-3.5 px-3.5 text-slate-600">Núcleo Socio-Ecológico Costero</td>
                                <td class="py-3.5 px-3.5 font-semibold text-emerald-900">Cerrado vigente · v1.0.0</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs sm:text-sm text-slate-600 bg-slate-50 border border-slate-200 rounded-xl p-4">
                    <div>
                        <strong class="text-slate-900">Trazabilidad de versiones, bitácora de incidencias y prueba de reproducción E2E:</strong>
                        <span>Consulta el historial detallado (<code class="font-mono text-xs">v1.0.0</code> a <code class="font-mono text-xs">v1.0.3</code>), el registro de incidencias (<code class="font-mono text-xs">INC-2026-01</code> a <code class="font-mono text-xs">INC-2026-05</code>) y el script verificable sobre R15 en la ficha técnica y guía metodológica.</span>
                    </div>
                    <div class="flex items-center space-x-3 shrink-0 font-semibold">
                        <a href="ficha-mbht-2017#sec-gobernanza" class="text-slate-900 underline hover:text-black">Gobernanza e incidencias</a>
                        <span class="text-slate-300">|</span>
                        <a href="guia-tecnica#seccion-8" class="text-slate-900 underline hover:text-black">Prueba E2E reproducible</a>
                    </div>
                </div>
            </div>

{static_downloads_table}

        </div>
    </section>
    </main>

    <!-- WIDGET COPILOTO IA FLOTANTE -->
    <!-- Micro-invitación pedagógica y sobria (CIT-UAI) -->
    <div id="copilotWelcomeHint" onclick="toggleCopilot(true); dismissCopilotHint(event);" class="cursor-pointer fixed bottom-20 right-3 sm:right-6 z-40 w-[calc(100vw-1.5rem)] max-w-[310px] sm:max-w-[340px] bg-[#0A192F] text-slate-200 border border-slate-700/80 border-t-2 border-t-[#6493B5] rounded-xl shadow-2xl p-3 text-xs leading-relaxed hidden transition-all duration-300">
        <div class="flex items-start justify-between gap-2">
            <p class="font-normal text-slate-300 text-[11px] sm:text-xs select-none">
                Orientación en descargas masivas de la MBHT y GeoParquet. Puede consultar aquí al Copiloto CIT.
            </p>
            <button onclick="dismissCopilotHint(event)" type="button" aria-label="Cerrar aviso" class="text-[#6493B5] hover:text-white transition cursor-pointer text-sm font-bold leading-none p-1 shrink-0">
                &times;
            </button>
        </div>
    </div>

    <button id="btnOpenCopilot" onclick="toggleCopilot(true)" type="button" aria-label="Abrir asistente Copiloto IA Territorial" class="fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-40 bg-slate-900 hover:bg-black active:bg-slate-800 text-white px-4 py-2.5 sm:px-4.5 sm:py-3 rounded-full shadow-lg border border-slate-700 flex items-center space-x-2.5 transition cursor-pointer">
        <span class="w-2 h-2 rounded-full bg-[#6493B5] shrink-0"></span>
        <span class="text-xs sm:text-sm font-semibold tracking-wide">Copiloto IA</span>
    </button>

    <!-- 4. COPILOTO IA TERRITORIAL DRAWER MODAL -->
    <div id="copilotDrawer" class="fixed inset-0 z-50 hidden bg-black/60 backdrop-blur-xs flex justify-end transition-opacity">
        <div class="bg-white w-full max-w-md h-full shadow-2xl flex flex-col justify-between border-l border-slate-200">
            
            <!-- Copilot Header -->
            <div class="p-4 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
                <div class="flex items-center space-x-2.5">
                    <div class="w-8 h-8 rounded-lg bg-slate-800 text-[#6493B5] flex items-center justify-center font-bold text-xs border border-slate-700">
                        <i data-lucide="sparkles" class="w-4 h-4 text-[#6493B5]"></i>
                    </div>
                    <div>
                        <h3 class="text-sm font-bold text-white flex items-center space-x-1.5">
                            <span>Copiloto IA Territorial</span>
                            <span class="w-2 h-2 rounded-full bg-[#6493B5] animate-ping"></span>
                        </h3>
                        <p class="text-[11px] text-slate-400">CIT-UAI · Asistente en lenguaje natural</p>
                    </div>
                </div>
                <button onclick="toggleCopilot(false)" aria-label="Cerrar Copiloto" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Sugerencias rápidas -->
            <div class="p-3 bg-slate-50 border-b border-slate-200 overflow-x-auto no-scrollbar flex items-center space-x-2 shrink-0">
                <button onclick="sendCopilotSuggestion('¿Dónde descargo los datos de la MBHT 2017?')" class="text-[11px] bg-white border border-slate-200 hover:border-slate-300 text-slate-700 font-medium py-1 px-2.5 rounded-full whitespace-nowrap shadow-xs hover:bg-slate-100 transition cursor-pointer">
                    Descargas
                </button>
                <button onclick="sendCopilotSuggestion('¿Cuál es la diferencia entre GeoParquet y Shapefile?')" class="text-[11px] bg-white border border-slate-200 hover:border-slate-300 text-slate-700 font-medium py-1 px-2.5 rounded-full whitespace-nowrap shadow-xs hover:bg-slate-100 transition cursor-pointer">
                    GeoParquet vs Shapefile
                </button>
                <button onclick="sendCopilotSuggestion('¿Cómo abro los datos en QGIS o R?')" class="text-[11px] bg-white border border-slate-200 hover:border-slate-300 text-slate-700 font-medium py-1 px-2.5 rounded-full whitespace-nowrap shadow-xs hover:bg-slate-100 transition cursor-pointer">
                    Abrir en QGIS
                </button>
            </div>

            <!-- Copilot Chat Log -->
            <div id="copilotMessages" class="flex-1 p-4 overflow-y-auto space-y-3 custom-scrollbar text-xs sm:text-sm">
                <!-- Mensaje de Bienvenida -->
                <div class="flex items-start space-x-2.5">
                    <div class="w-7 h-7 rounded-full bg-slate-900 text-[#6493B5] flex items-center justify-center text-xs shrink-0 font-bold border border-slate-700">
                        CIT
                    </div>
                    <div class="bg-slate-100 p-3 rounded-2xl rounded-tl-none text-slate-800 space-y-2 shadow-xs max-w-[85%]">
                        <p class="font-normal leading-relaxed">
                            Bienvenido/a al repositorio de datos abiertos del <strong>CIT-UAI</strong>. La información geoespacial que ponemos a tu disposición representa la línea base del <strong>Bienestar Humano Territorial (MBHT)</strong>: un esfuerzo científico y ético por cuantificar el acceso real de los hogares a servicios esenciales en todo Chile.
                        </p>
                        <p class="text-slate-600 text-[11px] sm:text-xs font-normal">
                            Pregúntame sobre coberturas temáticas, formatos disponibles (GeoParquet, GeoPackage, Shapefile) o cómo importar los datos a tu código en Python o R.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Copilot Input Box -->
            <form onsubmit="handleCopilotSubmit(event)" class="p-3 bg-white border-t border-slate-200 flex items-center space-x-2 shrink-0">
                <input id="copilotInput" type="text" placeholder="Escribe tu consulta territorial..." class="flex-1 bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900" />
                <button type="submit" aria-label="Enviar mensaje" class="p-2 bg-slate-900 hover:bg-black active:bg-slate-800 text-white rounded-lg transition cursor-pointer shadow-xs">
                    <i data-lucide="send" class="w-4 h-4"></i>
                </button>
            </form>

        </div>
    </div>


{canonical_footer}

    <!-- SCRIPT DE INTERACTIVIDAD Y MOTOR DE DESCARGAS 2017 -->
    <script>
        const INDICE_DESCARGAS_2017 = {descargas_2017_json_str};
        let currentSnippetLang = 'python';

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
                opt.innerText = 'Todas las comunas de Chile (345 comunas)';
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
                tituloPrefix = 'Manzanas censales MBHT 2017';
                key = region === 'NACIONAL' ? 'MBHT_2017_Nacional_Manzanas' : `MBHT_2017_${{region}}_Manzanas`;
            }} else if (tipo === 'equip_todos') {{
                badgeTipoText = 'Equipamientos consolidado';
                tituloPrefix = 'Equipamientos urbanos 2017 — Consolidado';
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
                badgeTipoText = 'Red vial Tobler';
                tituloPrefix = 'Red vial caminable Tobler 2017';
                key = region === 'NACIONAL' ? 'Red_Vial_Ejes_2017_Nacional' : `Red_Vial_Ejes_2017_${{region}}`;
            }}

            const regData = INDICE_DESCARGAS_2017.regiones ? INDICE_DESCARGAS_2017.regiones[region] : null;
            const regNombre = region === 'NACIONAL' ? 'Consolidado nacional' : (regData ? `Región de ${{regData.nombre}} (${{region}})` : region);

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

            // Helper formateo de tamaño con decimal en coma española
            const fmtSize = bytes => {{
                if (!bytes) return '-- MB';
                if (bytes > 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1).replace('.', ',') + ' MB';
                return (bytes / 1024).toFixed(0).toLocaleString('es-CL') + ' KB';
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
            const btn = window.event ? window.event.currentTarget : null;
            if (el) {{
                el.select();
                navigator.clipboard.writeText(el.value).then(() => {{
                    if (btn) {{
                        const orig = btn.innerHTML;
                        btn.innerHTML = '<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i><span class="text-emerald-700 font-bold">¡Copiado!</span>';
                        if (window.lucide) lucide.createIcons();
                        setTimeout(() => {{ btn.innerHTML = orig; if (window.lucide) lucide.createIcons(); }}, 2000);
                    }}
                }}).catch(() => {{
                    document.execCommand('copy');
                }});
            }}
        }}

                function copyDescargaHash() {{
            const el = document.getElementById('inputDescargaSha256');
            const btn = window.event ? window.event.currentTarget : null;
            if (el) {{
                el.select();
                navigator.clipboard.writeText(el.value).then(() => {{
                    if (btn) {{
                        const orig = btn.innerHTML;
                        btn.innerHTML = '<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i><span class="text-emerald-700 font-bold">¡Copiado!</span>';
                        if (window.lucide) lucide.createIcons();
                        setTimeout(() => {{ btn.innerHTML = orig; if (window.lucide) lucide.createIcons(); }}, 2000);
                    }}
                }}).catch(() => {{
                    document.execCommand('copy');
                }});
            }}
        }}

        // =========================================================================
        // Verificador Criptográfico Web Crypto API SHA-256 en Cliente
        // =========================================================================
        function initShaDropZone() {{
            const dropZone = document.getElementById('shaDropZone');
            if (!dropZone) return;
            ['dragenter', 'dragover'].forEach(eventName => {{
                dropZone.addEventListener(eventName, (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.add('border-[#6493B5]', 'bg-slate-50');
                }}, false);
            }});
            ['dragleave', 'drop'].forEach(eventName => {{
                dropZone.addEventListener(eventName, (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.remove('border-[#6493B5]', 'bg-slate-50');
                }}, false);
            }});
            dropZone.addEventListener('drop', (e) => {{
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files && files.length > 0) processShaFile(files[0]);
            }}, false);
        }}

        function handleShaFileSelect(e) {{
            if (e.target.files && e.target.files.length > 0) {{
                processShaFile(e.target.files[0]);
            }}
        }}

        async function processShaFile(file) {{
            const resEl = document.getElementById('shaVerifyResult');
            if (!resEl) return;
            resEl.classList.remove('hidden');
            resEl.innerHTML = `
                <div class="flex items-center space-x-2 text-slate-600">
                    <span class="w-3 h-3 border-2 border-[#6493B5] border-t-transparent rounded-full animate-spin"></span>
                    <span class="font-mono text-[11px]">Calculando hash SHA-256 de <strong>${{file.name}}</strong> (${{(file.size / (1024*1024)).toFixed(2)}} MB)...</span>
                </div>
            `;
            try {{
                const arrayBuffer = await file.arrayBuffer();
                const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const computedHash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                
                const expectedParquetHash = "4a123b83ea1cefa18661c25ea40b9c3fc2a319cf6a45abbbd72a2cb30c069f2a";
                const expectedGpkgHash = "3db07960a5d2ac94d4443c5ba59a3715655db8aabf040e01993180c316e1d230";
                const expectedShpHash = "9899f31ae5aa104b40e9c4bbfd4030eb1b8e2b3fb431544b1d103fc720f8cb32";
                const expectedCsvHash = "ebea6ee15f32639345b0f7ce1b3211f808d17b55b3b7d7283d180c48721d5cf5";

                const currentExpected = (document.getElementById('inputDescargaSha256')?.value || '').trim().toLowerCase();
                const matchesCurrent = computedHash === currentExpected;
                const matchesAny = matchesCurrent || [expectedParquetHash, expectedGpkgHash, expectedShpHash, expectedCsvHash].includes(computedHash);

                if (matchesAny) {{
                    resEl.innerHTML = `
                        <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-900 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                            <div class="flex items-center space-x-2">
                                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-600 shrink-0"></i>
                                <div>
                                    <span class="font-bold text-xs">¡Integridad Criptográfica Verificada y Auténtica!</span>
                                    <p class="text-[11px] font-mono text-emerald-700 truncate max-w-xl">${{computedHash}}</p>
                                </div>
                            </div>
                            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold shrink-0">100% Válido</span>
                        </div>
                    `;
                }} else {{
                    resEl.innerHTML = `
                        <div class="p-3 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                            <div class="flex items-center space-x-2">
                                <i data-lucide="info" class="w-4 h-4 text-amber-600 shrink-0"></i>
                                <div>
                                    <span class="font-bold text-xs">Hash Calculado Exitosamente</span>
                                    <p class="text-[11px] font-mono text-amber-800 truncate max-w-xl">${{computedHash}}</p>
                                </div>
                            </div>
                            <span class="text-[10px] text-amber-700 shrink-0">Verifica contra SHA256SUMS.txt</span>
                        </div>
                    `;
                }}
                if (window.lucide) lucide.createIcons();
            }} catch (err) {{
                resEl.innerHTML = `<span class="text-rose-600 text-xs">Error leyendo archivo: ${{err.message}}</span>`;
            }}
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
                msgDiv.innerHTML = `
                    <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-none text-xs sm:text-sm max-w-[85%] shadow-xs leading-relaxed">
                        ${{text}}
                    </div>
                `;
            }} else {{
                let actionBtnHtml = '';
                if (action && action.layerId) {{
                    actionBtnHtml = `
                        <a href="inicio" class="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-black text-white rounded-lg text-xs font-semibold transition cursor-pointer">
                            <i data-lucide="layers" class="w-3.5 h-3.5 text-[#6493B5]"></i>
                            <span>Ver en catálogo: ${{action.layerTitle}}</span>
                        </a>
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

        // Exportar a ámbito global
        window.toggleCopilot = toggleCopilot;
        window.sendCopilotSuggestion = sendCopilotSuggestion;
        window.handleCopilotSubmit = handleCopilotSubmit;
        window.speakCopilotText = speakCopilotText;
        window.initDescargas2017 = initDescargas2017;
        window.onRegionChange = onRegionChange;
        window.updateDescargas2017 = updateDescargas2017;
        window.setSnippetLang = setSnippetLang;
        window.copyDescargaSnippet = copyDescargaSnippet;
        window.copyDescargaHash = copyDescargaHash;

        // Atajos de teclado
        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                const drawer = document.getElementById('copilotDrawer');
                if (drawer && !drawer.classList.contains('hidden')) {{
                    toggleCopilot(false);
                }}
            }}
        }});

        window.handleShaFileSelect = handleShaFileSelect;
        window.processShaFile = processShaFile;

        // Inicialización sincrónica
        document.addEventListener('DOMContentLoaded', () => {{
            initDescargas2017();
            initShaDropZone();
            initCopilotHint();
            if (window.lucide) lucide.createIcons();
        }});
        initDescargas2017();
        initCopilotHint();
        if (window.lucide) lucide.createIcons();
    </script>
</body>
</html>
"""
    return html


def main() -> int:
    import json
    import sys
    root = find_proyecto_root()
    ide_hub_dir = root / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
    data_dir = ide_hub_dir / "data"
    catalog_json_path = data_dir / "catalogo_ide_cit.json"
    descargas_json_path = data_dir / "indice_descargas_mbht_2017.json"
    output_html_path = ide_hub_dir / "descargas-2017.html"

    with open(catalog_json_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    descargas_2017_data = {}
    if descargas_json_path.exists():
        with open(descargas_json_path, "r", encoding="utf-8") as f:
            descargas_2017_data = json.load(f)

    html_content = generate_descargas_2017_html(catalog_data, descargas_2017_data)

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Centro de Descargas generado exitosamente en: {output_html_path}")
    print(f"  Tamaño: {len(html_content):,} bytes")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
