#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de actualización del catálogo IDE CIT para integrar las 6 coberturas
de Planificación Espacial Marina (PEM / SBAP / Maritorio).
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
CATALOGO_PATH = DATA_DIR / "catalogo_ide_cit.json"

nuevas_capas_pem = [
    {
        "id": "pem_maritorio_nacional",
        "titulo": "Maritorio nacional y Zona Económica Exclusiva (ZEE) tricontinental",
        "matriz": "pem",
        "ambito": "mar",
        "escala": "Polígonos de soberanía y jurisdicción marítima (394 unidades)",
        "cobertura": "Tricontinental (Chile Continental, Insular y Territorio Antártico Chileno — 3.500.000 km²)",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial DIFROL / Armada / MMA",
        "resumen": "Delimitación vectorial oficial del Maritorio chileno bajo una perspectiva tricontinental y de soberanía oceánica integral (Chile continental, insular y Territorio Antártico Chileno). Comprende las líneas de base, Aguas Interiores, Mar Territorial (12 millas náuticas), Zona Contigua (24 mn), Zona Económica Exclusiva (200 mn) y plataforma continental, consolidando más de 3,5 millones de kilómetros cuadrados de océano nacional.",
        "formula_lineage": "Delimitación de espacios marítimos soberanos provista por DIFROL, SHOA y MMA conforme a la CONVEMAR y la Política Nacional de Uso del Borde Costero (PNUBC). Homologación geodésica WGS84 (EPSG:4326).",
        "autor": "CIT-UAI en colaboración con DIFROL y Armada de Chile",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "pem_maritorio_nacional",
        "tabla_postgis": "maritorio.maritorio_nacional",
        "s3_parquet": "s3://mbht-data-lake/parquet/PEM_Maritorio_Nacional_Tricontinental.parquet",
        "parquet_url": "download/PEM_Maritorio_Nacional_Tricontinental.parquet",
        "gpkg_url": "download/PEM_Maritorio_Nacional_Tricontinental.gpkg",
        "shp_url": "download/PEM_Maritorio_Nacional_Tricontinental_SHP.zip",
        "csv_url": "download/PEM_Maritorio_Nacional_Tricontinental.csv",
        "atributos": [
            {
                "campo": "OBJECTID",
                "tipo": "Integer",
                "descripcion": "Identificador secuencial del polígono marítimo"
            },
            {
                "campo": "perimetro_km",
                "tipo": "Float",
                "descripcion": "Perímetro geodésico del polígono marítimo en kilómetros (km)"
            },
            {
                "campo": "area_km2",
                "tipo": "Float",
                "descripcion": "Área superficial geodésica del polígono en kilómetros cuadrados (km²)"
            },
            {
                "campo": "ambito",
                "tipo": "String",
                "descripcion": "Ámbito geográfico tricontinental (Continental, Insular, Antártico)"
            },
            {
                "campo": "fuente",
                "tipo": "String",
                "descripcion": "Institución técnica de custodia y delimitación"
            }
        ],
        "citacion": "Centro de Inteligencia Territorial, & Dirección Nacional de Fronteras y Límites del Estado. (2024). Delimitación oficial del Maritorio nacional tricontinental y Zona Económica Exclusiva [Conjunto de datos geoespaciales]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-131.0, -90.0, -50.0, -17.5],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "MultiPolygon",
        "fuentes_institucionales": [
            {
                "institucion": "Dirección Nacional de Fronteras y Límites del Estado [DIFROL]",
                "insumo": "Límites Internacionales y Espacios de Soberanía Marítima",
                "citacion_apa7": "Dirección Nacional de Fronteras y Límites del Estado [DIFROL]. (2024). Delimitación de espacios marítimos internacionales y plataforma continental extendida [Documento oficial]. Ministerio de Relaciones Exteriores de Chile. https://difrol.gob.cl",
                "url": "https://difrol.gob.cl"
            },
            {
                "institucion": "Servicio Hidrográfico y Oceanográfico de la Armada [SHOA]",
                "insumo": "Cartografía Náutica y Líneas de Base Oficiales",
                "citacion_apa7": "Servicio Hidrográfico y Oceanográfico de la Armada [SHOA]. (2024). Cartografía oficial de líneas de base y aguas interiores de la República de Chile [Base cartográfica]. Armada de Chile. http://www.shoa.cl",
                "url": "http://www.shoa.cl"
            },
            {
                "institucion": "Ministerio del Medio Ambiente [MMA]",
                "insumo": "Áreas Marinas Costeras Protegidas y Zonificación del Borde Costero",
                "citacion_apa7": "Ministerio del Medio Ambiente [MMA]. (2024). Catastro nacional de áreas marinas protegidas y política de borde costero [Base de datos geográfica]. MMA. https://mma.gob.cl",
                "url": "https://mma.gob.cl"
            }
        ]
    },
    {
        "id": "pem_geomorfologia_gebco",
        "titulo": "Geomorfología submarina y macro-unidades de relieve oceánico (GEBCO)",
        "matriz": "pem",
        "ambito": "mar",
        "escala": "Polígonos de macro-unidades fisiográficas de fondo marino (11 macro-unidades)",
        "cobertura": "Margen continental y cuencas oceánicas adyacentes a Chile",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial GEBCO / IHO",
        "resumen": "Zonificación geomorfológica del lecho y fondo submarino nacional categorizada conforme al estándar internacional GEBCO (General Bathymetric Chart of the Oceans / IHO). Delimita las grandes provincias fisiográficas oceánicas: Fosa de Atacama/Perú-Chile, plataforma continental, talud continental, fosas abisales, dorsales oceánicas (Dorsal de Chile, Cordillera de Nazca, Cordillera de Salas y Gómez) y llanuras abisales.",
        "formula_lineage": "Clasificación morfométrica de relieve submarino basada en mallas globales GEBCO / IHO y validación fisiográfica regional. Reproyección a WGS84 (EPSG:4326).",
        "autor": "CIT-UAI con insumos de GEBCO / UNESCO / OHI",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "pem_geomorfologia_gebco",
        "tabla_postgis": "maritorio.geomorfologia_gebco",
        "s3_parquet": "s3://mbht-data-lake/parquet/PEM_Geomorfologia_Submarina_GEBCO.parquet",
        "parquet_url": "download/PEM_Geomorfologia_Submarina_GEBCO.parquet",
        "gpkg_url": "download/PEM_Geomorfologia_Submarina_GEBCO.gpkg",
        "shp_url": "download/PEM_Geomorfologia_Submarina_GEBCO_SHP.zip",
        "csv_url": "download/PEM_Geomorfologia_Submarina_GEBCO.csv",
        "atributos": [
            {
                "campo": "unidad_geomorfologica",
                "tipo": "String",
                "descripcion": "Tipo de unidad morfológica submarina (plataforma, talud, fosa, dorsal, etc.)"
            },
            {
                "campo": "superficie_km2",
                "tipo": "Float",
                "descripcion": "Superficie de la macro-unidad en kilómetros cuadrados"
            },
            {
                "campo": "ano_fuente",
                "tipo": "String",
                "descripcion": "Año de publicación del modelo geomorfológico GEBCO"
            }
        ],
        "citacion": "General Bathymetric Chart of the Oceans [GEBCO], & Centro de Inteligencia Territorial. (2024). Geomorfología y provincias fisiográficas de los fondos oceánicos de Chile [Conjunto de datos geoespaciales]. IHO / Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-120.0, -58.0, -66.0, -18.0],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "MultiPolygon",
        "fuentes_institucionales": [
            {
                "institucion": "General Bathymetric Chart of the Oceans [GEBCO]",
                "insumo": "Global Undersea Feature and Geomorphology Grid",
                "citacion_apa7": "GEBCO Compilation Group. (2024). GEBCO Grid: Global bathymetric and undersea terrain models [Conjunto de datos espaciales]. British Oceanographic Data Centre. https://www.gebco.net",
                "url": "https://www.gebco.net"
            },
            {
                "institucion": "Organización Hidrográfica Internacional [IHO]",
                "insumo": "Estándar de Nomenclatura y Formas del Fondo Oceánico",
                "citacion_apa7": "International Hydrographic Organization [IHO]. (2024). Standardization of undersea feature names: Guidelines and bathymetric gazetteer [Publicación B-6]. IHO. https://iho.int",
                "url": "https://iho.int"
            }
        ]
    },
    {
        "id": "pem_montes_submarinos",
        "titulo": "Montes submarinos y toponimia oceánica oficial",
        "matriz": "pem",
        "ambito": "mar",
        "escala": "Puntual 3D con elevación y toponimia (2.234 cumbres submarinas)",
        "cobertura": "Cordilleras submarinas y dorsales del Mar Chileno y ZEE",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial IHO / SHOA",
        "resumen": "Catastro de montes submarinos, guyots, cañones y relieves destacados del lecho oceánico chileno con toponimia oficial reconocida por la Organización Hidrográfica Internacional (OHI) y SHOA. Incluye 2.234 cimas y estructuras orográficas submarinas esenciales para la conservación de la biodiversidad marina bentónica y pelágica, hábitats de corales de profundidad y montes de Nazca-Desventuradas y Salas y Gómez.",
        "formula_lineage": "Nomenclatura oficial SCUFN (Sub-Committee on Undersea Feature Names) de GEBCO/IHO combinada con batimetría de alta resolución y cotas geodésicas Z WGS84.",
        "autor": "CIT-UAI en base a SCUFN / GEBCO / SHOA",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "pem_montes_submarinos",
        "tabla_postgis": "maritorio.montes_submarinos",
        "s3_parquet": "s3://mbht-data-lake/parquet/PEM_Montes_Submarinos_Toponimia.parquet",
        "parquet_url": "download/PEM_Montes_Submarinos_Toponimia.parquet",
        "gpkg_url": "download/PEM_Montes_Submarinos_Toponimia.gpkg",
        "shp_url": "download/PEM_Montes_Submarinos_Toponimia_SHP.zip",
        "csv_url": "download/PEM_Montes_Submarinos_Toponimia.csv",
        "atributos": [
            {
                "campo": "nombre_monte",
                "tipo": "String",
                "descripcion": "Nombre o toponimia oficial del monte submarino o accidente oceánico"
            },
            {
                "campo": "catalogo_categoria",
                "tipo": "String",
                "descripcion": "Categoría morfoestructural (Guyot, Seamount, Ridge, Trench, Hill)"
            },
            {
                "campo": "elevacion_submarina_m",
                "tipo": "Float",
                "descripcion": "Cota batimétrica o elevación sobre el lecho marino en metros"
            }
        ],
        "citacion": "Sub-Committee on Undersea Feature Names [SCUFN], & Centro de Inteligencia Territorial. (2024). Catastro de montes submarinos y toponimia del relieve oceánico chileno [Conjunto de datos geoespaciales]. IHO / GEBCO / Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-115.0, -56.0, -68.0, -18.5],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "Point",
        "fuentes_institucionales": [
            {
                "institucion": "Sub-Committee on Undersea Feature Names [SCUFN / IHO]",
                "insumo": "Gazetteer of Undersea Feature Names",
                "citacion_apa7": "IHO-IOC GEBCO Sub-Committee on Undersea Feature Names [SCUFN]. (2024). IHO-IOC GEBCO gazetteer of undersea feature names [Base de datos toponímica]. NOAA NCEI. https://www.gebco.net/data_and_products/undersea_feature_names/",
                "url": "https://www.gebco.net"
            }
        ]
    },
    {
        "id": "pem_cuencas_oceanicas",
        "titulo": "Cuencas oceanográficas y morfología del lecho submarino",
        "matriz": "pem",
        "ambito": "mar",
        "escala": "Polígonos de delimitación morfométrica de cuencas de fondo (53.726 unidades)",
        "cobertura": "Lecho del Pacífico Suroriental y cuencas marinas de Chile",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial CIT-UAI",
        "resumen": "Delimitación espacial morfométrica de 53.726 cuencas y subcuencas oceanográficas submarinas del lecho del Pacífico Suroriental chileno. Modela el drenaje de sedimentos submarinos, cañones tributarios y circulación de fondo, permitiendo caracterizar la conectividad ecológica y las dinámicas hidrogeomorfológicas de los ecosistemas marinos profundos.",
        "formula_lineage": "Extracción hidrológica/oceanográfica algorítmica sobre modelos digitales batimétricos globales y corrección topológica WGS84 (EPSG:4326).",
        "autor": "Centro de Inteligencia Territorial (CIT-UAI)",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "pem_cuencas_oceanicas",
        "tabla_postgis": "maritorio.cuencas_oceanicas",
        "s3_parquet": "s3://mbht-data-lake/parquet/PEM_Cuencas_Oceanicas_Submarinas.parquet",
        "parquet_url": "download/PEM_Cuencas_Oceanicas_Submarinas.parquet",
        "gpkg_url": "download/PEM_Cuencas_Oceanicas_Submarinas.gpkg",
        "shp_url": "download/PEM_Cuencas_Oceanicas_Submarinas_SHP.zip",
        "csv_url": "download/PEM_Cuencas_Oceanicas_Submarinas.csv",
        "atributos": [
            {
                "campo": "id_cuenca",
                "tipo": "Integer",
                "descripcion": "Identificador único de la cuenca oceanográfica submarina"
            },
            {
                "campo": "codigo_cuenca",
                "tipo": "Integer",
                "descripcion": "Código morfométrico de drenaje abisal"
            },
            {
                "campo": "perimetro_km",
                "tipo": "Float",
                "descripcion": "Perímetro geodésico de la cuenca oceanográfica en kilómetros (km)"
            },
            {
                "campo": "area_km2",
                "tipo": "Float",
                "descripcion": "Área superficial geodésica de la cuenca en kilómetros cuadrados (km²)"
            }
        ],
        "citacion": "Centro de Inteligencia Territorial. (2024). Modelo morfométrico de cuencas oceanográficas y lecho abisal del Pacífico Suroriental chileno [Conjunto de datos geoespaciales]. Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-118.0, -56.0, -68.0, -18.0],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "MultiPolygon",
        "fuentes_institucionales": [
            {
                "institucion": "Centro de Inteligencia Territorial [CIT-UAI]",
                "insumo": "Modelo Morfométrico Abisal y Drenaje Submarino",
                "citacion_apa7": "Centro de Inteligencia Territorial [CIT-UAI]. (2024). Modelación de cuencas oceanográficas profundas de la ZEE chilena [Modelo digital y base geoespacial]. Universidad Adolfo Ibáñez. https://matrizbht.cl",
                "url": "https://matrizbht.cl"
            }
        ]
    },
    {
        "id": "pem_biodiversidad_especies",
        "titulo": "Biodiversidad marina y catálogo de especies (IFOP / GBIF / SBAP)",
        "matriz": "pem",
        "ambito": "mar",
        "escala": "Puntual georreferenciada masiva (4.529.201 registros de biodiversidad)",
        "cobertura": "Ecosistemas marinos y costeros de Chile (Reinos Animalia, Plantae, Chromista, etc.)",
        "fecha_corte": "2024-12-31",
        "publico": True,
        "disponible_descarga": True,
        "estado": "activo",
        "badge_estado": "Oficial IFOP / GBIF / SBAP",
        "resumen": "Consolidado nacional de ocurrencias biológicas y biodiversidad marina de Chile, integrando 4.529.201 observaciones georreferenciadas desde las campañas científicas del Instituto de Fomento Pesquero (IFOP) y la Infraestructura Mundial de Información en Biodiversidad (GBIF). Abarca taxonomía completa (reino, filo, clase, orden, familia, género, especie y nombre científico), profundidad de colecta y año de observación, permitiendo análisis de distribución de especies, bioindicadores y diseño de redes de áreas protegidas marinas bajo la Ley SBAP.",
        "formula_lineage": "Estandarización taxonómica Darwin Core sobre registros de prospecciones de investigación pesquera de IFOP y nodos GBIF en aguas jurisdiccionales chilenas. Optimizado en GeoParquet 1.1 columnar comprimido.",
        "autor": "CIT-UAI con datos de IFOP / GBIF / MMA",
        "licencia": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "tile_source": "pem_biodiversidad_especies",
        "tabla_postgis": "maritorio.biodiversidad_especies",
        "s3_parquet": "s3://mbht-data-lake/parquet/PEM_Biodiversidad_Marina_Especies_IFOP_GBIF.parquet",
        "parquet_url": "download/PEM_Biodiversidad_Marina_Especies_IFOP_GBIF.parquet",
        "gpkg_url": None,
        "shp_url": None,
        "csv_url": "download/PEM_Biodiversidad_Marina_Especies_IFOP_GBIF.csv",
        "atributos": [
            {
                "campo": "id_gbif",
                "tipo": "String",
                "descripcion": "Identificador universal único del espécimen o avistamiento (GBIF ID)"
            },
            {
                "campo": "reino",
                "tipo": "String",
                "descripcion": "Reino taxonómico (Animalia, Plantae, Chromista, Fungi, etc.)"
            },
            {
                "campo": "filo",
                "tipo": "String",
                "descripcion": "Filo o división biológica"
            },
            {
                "campo": "clase",
                "tipo": "String",
                "descripcion": "Clase taxonómica"
            },
            {
                "campo": "orden",
                "tipo": "String",
                "descripcion": "Orden taxonómico"
            },
            {
                "campo": "familia",
                "tipo": "String",
                "descripcion": "Familia biológica"
            },
            {
                "campo": "genero",
                "tipo": "String",
                "descripcion": "Género taxonómico"
            },
            {
                "campo": "especie",
                "tipo": "String",
                "descripcion": "Epíteto específico de la especie"
            },
            {
                "campo": "nombre_cientifico",
                "tipo": "String",
                "descripcion": "Nombre científico completo del taxón"
            },
            {
                "campo": "profundidad_m",
                "tipo": "Float",
                "descripcion": "Profundidad marina de muestreo en metros"
            },
            {
                "campo": "ano_registro",
                "tipo": "Integer",
                "descripcion": "Año de colecta u observación del espécimen"
            },
            {
                "campo": "codigo_pais",
                "tipo": "String",
                "descripcion": "Código ISO del país jurisdiccional (CL)"
            }
        ],
        "citacion": "Instituto de Fomento Pesquero [IFOP], Global Biodiversity Information Facility [GBIF], & Centro de Inteligencia Territorial. (2024). Catastro nacional de biodiversidad y ocurrencias de especies marinas de Chile [Conjunto de datos geoespaciales]. IFOP / GBIF / Universidad Adolfo Ibáñez. https://ide.cit.uai.cl",
        "bbox": [-115.0, -58.0, -66.0, -18.0],
        "crs": "EPSG:4326 (WGS 84)",
        "tipo_geometria": "Point",
        "fuentes_institucionales": [
            {
                "institucion": "Instituto de Fomento Pesquero [IFOP]",
                "insumo": "Cruceros Científicos y Catastro de Recursos Pesqueros y Bentónicos",
                "citacion_apa7": "Instituto de Fomento Pesquero [IFOP]. (2024). Catálogo de cruceros oceanográficos e investigación biológica pesquera en Chile [Conjunto de datos biológicos]. IFOP. https://www.ifop.cl",
                "url": "https://www.ifop.cl"
            },
            {
                "institucion": "Global Biodiversity Information Facility [GBIF]",
                "insumo": "Ocurrencias Georreferenciadas de Fauna y Flora Marina",
                "citacion_apa7": "GBIF.org. (2024). GBIF Occurrence Download: Marine taxa of the Chilean Exclusive Economic Zone [Conjunto de datos abiertos]. GBIF. https://doi.org/10.15468/dl.marine_cl",
                "url": "https://www.gbif.org"
            }
        ]
    }
]

def actualizar():
    with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    capas = catalogo.get("capas", [])
    nuevas_capas = []
    reemplazado = False

    for capa in capas:
        if capa.get("id") == "pem_espacios_maritimos":
            # Reemplazar por las 6 coberturas marinas detalladas
            nuevas_capas.extend(nuevas_capas_pem)
            reemplazado = True
        else:
            nuevas_capas.append(capa)

    if not reemplazado:
        # Si ya se habían agregado o no estaba el id exacto, buscar y actualizar
        capas_existentes_pem = {c["id"] for c in nuevas_capas_pem}
        capas_filtradas = [c for c in nuevas_capas if c["id"] not in capas_existentes_pem]
        capas_filtradas.extend(nuevas_capas_pem)
        nuevas_capas = capas_filtradas

    catalogo["capas"] = nuevas_capas

    with open(CATALOGO_PATH, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)

    print(f"Catálogo actualizado con éxito en: {CATALOGO_PATH}")
    print(f"Total de capas en el catálogo: {len(nuevas_capas)}")

if __name__ == "__main__":
    actualizar()
