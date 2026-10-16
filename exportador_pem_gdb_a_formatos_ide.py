#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — EXTRACTOR Y TRANSFORMADOR DE PLANIFICACIÓN ESPACIAL MARINA (PEM / SBAP)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Extrae, valida, estandariza a WGS 84 (EPSG:4326) y convierte las coberturas
    marinas desde la Geodatabase ESRI oficial (`Cuencas Oceanicas.gdb`) y shapefiles
    asociados hacia los formatos abiertos de ciencia espacial del estándar IDE CIT:
    - Apache GeoParquet 1.1 (compresión columnar zstd/snappy)
    - OGC GeoPackage (.gpkg)
    - ESRI Shapefile comprimido (.zip) con UTF-8
    - Archivo tabular separado por comas (.csv)

Coberturas procesadas:
    1. Maritorio Nacional y ZEE Tricontinental (3,5M km²)
    2. Batimetría y Sondajes de Profundidad SHOA / SBAP (242k puntos)
    3. Geomorfología Submarina GEBCO (11 macro-unidades)
    4. Montes Submarinos y Toponimia Oceánica (2.234 cumbres submarinas)
    5. Cuencas Oceanográficas Submarinas (53.726 cuencas de fondo)
    6. Biodiversidad Marina y Ocurrencias Biológicas IFOP/GBIF (4,52M registros)

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import logging
import os
import shutil
import sys
import time
import zipfile
from pathlib import Path
from typing import Dict, Any, List, Optional

import geopandas as gpd
import pandas as pd
import pyogrio
from shapely import force_2d

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("PEM_ETL_IDE")

# Rutas de Insumos
ARCGIS_PROJECT_DIR = Path.home() / "Documents" / "ArcGIS" / "Projects" / "Cuencas Oceanicas"
GDB_PATH = ARCGIS_PROJECT_DIR / "Cuencas Oceanicas.gdb"
MARITORIO_SHP_PATH = ARCGIS_PROJECT_DIR / "maritorio_chileno.shp"

# Directorio de Salida para la IDE CIT
SCRIPT_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = SCRIPT_DIR / "download"


def ensure_output_dirs() -> None:
    """Crea los directorios de salida necesarios si no existen."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directorio de descarga verificado: {DOWNLOAD_DIR}")


def zip_shapefile(shp_base_name: str, temp_dir: Path, output_zip_path: Path) -> int:
    """Comprime los componentes del Shapefile (.shp, .shx, .dbf, .prj, .cpg) en un archivo ZIP."""
    extensions = [".shp", ".shx", ".dbf", ".prj", ".cpg"]
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for ext in extensions:
            fpath = temp_dir / f"{shp_base_name}{ext}"
            if fpath.exists():
                zf.write(fpath, arcname=f"{shp_base_name}{ext}")
    return output_zip_path.stat().st_size


def export_coverage(
    gdf: gpd.GeoDataFrame,
    base_name: str,
    export_shp: bool = True,
    export_csv: bool = True,
    export_gpkg: bool = True,
) -> Dict[str, Any]:
    """
    Exporta un GeoDataFrame a GeoParquet, GeoPackage, Shapefile (.zip) y CSV.
    """
    ensure_output_dirs()
    results = {}
    temp_dir = DOWNLOAD_DIR / f"_temp_{base_name}"
    
    # 1. Asegurar proyección WGS 84 (EPSG:4326)
    if gdf.crs is None:
        logger.warning(f"  [{base_name}] Sin CRS definido. Asumiendo EPSG:4326.")
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs.to_epsg() != 4326:
        logger.info(f"  [{base_name}] Reproyectando de {gdf.crs.to_string()} a EPSG:4326...")
        gdf = gdf.to_crs("EPSG:4326")

    # 2. Exportar a Apache GeoParquet 1.1
    parquet_path = DOWNLOAD_DIR / f"{base_name}.parquet"
    logger.info(f"  [{base_name}] Exportando GeoParquet...")
    gdf.to_parquet(parquet_path, compression="zstd")
    results["parquet"] = {
        "path": parquet_path,
        "size_mb": parquet_path.stat().st_size / (1024 * 1024),
    }

    # 3. Exportar a OGC GeoPackage (.gpkg) usando pyogrio acelerado
    if export_gpkg:
        gpkg_path = DOWNLOAD_DIR / f"{base_name}.gpkg"
        logger.info(f"  [{base_name}] Exportando GeoPackage (.gpkg)...")
        if gpkg_path.exists():
            gpkg_path.unlink()
        pyogrio.write_dataframe(gdf, gpkg_path, driver="GPKG", layer=base_name)
        results["gpkg"] = {
            "path": gpkg_path,
            "size_mb": gpkg_path.stat().st_size / (1024 * 1024),
        }

    # 4. Exportar a ESRI Shapefile comprimido (.zip) si corresponde
    if export_shp:
        temp_dir.mkdir(parents=True, exist_ok=True)
        try:
            logger.info(f"  [{base_name}] Exportando Shapefile (.zip)...")
            shp_path = temp_dir / f"{base_name}.shp"
            # Asegurar geometrías 2D para compatibilidad con Shapefile legacy si es 3D
            gdf_2d = gdf.copy()
            if gdf_2d.geometry.has_z.any():
                gdf_2d.geometry = force_2d(gdf_2d.geometry)
            
            # Truncar y desduplicar nombres de columnas a 10 caracteres para formato DBF
            seen_cols: Dict[str, int] = {}
            new_cols: Dict[str, str] = {}
            for col in gdf_2d.columns:
                if col == "geometry":
                    continue
                short = col[:10]
                if short in seen_cols:
                    seen_cols[short] += 1
                    short = f"{short[:7]}_{seen_cols[short]}"
                else:
                    seen_cols[short] = 1
                new_cols[col] = short
            
            gdf_shp = gdf_2d.rename(columns=new_cols)
            pyogrio.write_dataframe(gdf_shp, shp_path, driver="ESRI Shapefile", encoding="utf-8")
            zip_path = DOWNLOAD_DIR / f"{base_name}_SHP.zip"
            zip_size = zip_shapefile(base_name, temp_dir, zip_path)
            results["shp"] = {
                "path": zip_path,
                "size_mb": zip_size / (1024 * 1024),
            }
        except Exception as e:
            logger.error(f"  [{base_name}] Error exportando Shapefile: {e}")
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    # 5. Exportar a CSV tabular
    if export_csv:
        logger.info(f"  [{base_name}] Exportando CSV tabular...")
        csv_path = DOWNLOAD_DIR / f"{base_name}.csv"
        df_csv = pd.DataFrame(gdf.drop(columns="geometry"))
        
        # Si son geometrías puntuales, agregar columnas explícitas longitud y latitud aceleradamente
        geom_type = gdf.geometry.iloc[0].geom_type if len(gdf) > 0 else ""
        if "Point" in geom_type:
            df_csv["longitud"] = gdf.geometry.x.to_numpy()
            df_csv["latitud"] = gdf.geometry.y.to_numpy()
        else:
            # Para polígonos, agregar centroide WGS84 para georreferenciación rápida
            try:
                centroids = gdf.geometry.centroid
                df_csv["centroide_lon"] = centroids.x.to_numpy()
                df_csv["centroide_lat"] = centroids.y.to_numpy()
            except Exception:
                pass

        df_csv.to_csv(csv_path, index=False, encoding="utf-8")
        results["csv"] = {
            "path": csv_path,
            "size_mb": csv_path.stat().st_size / (1024 * 1024),
        }

    return results


def procesar_maritorio_nacional() -> Dict[str, Any]:
    """Procesa la delimitación del Maritorio Nacional Tricontinental y ZEE."""
    logger.info("=== PROCESANDO COBERTURA 1: MARITORIO NACIONAL TRICONTINENTAL ===")
    t0 = time.time()
    gdf = pyogrio.read_dataframe(MARITORIO_SHP_PATH)
    logger.info(f"  Cargados {len(gdf):,} polígonos en {time.time()-t0:.2f} s.")
    
    # Estandarizar columnas y metadatos
    if "Shape_Leng" in gdf.columns:
        gdf = gdf.rename(columns={"Shape_Leng": "perimetro_grados", "Shape_Area": "area_grados"})
    gdf["ambito"] = "Maritorio Nacional Tricontinental (Continental, Insular, Antártico)"
    gdf["fuente"] = "CIT-UAI / Armada de Chile / DIFROL"
    
    res = export_coverage(gdf, "PEM_Maritorio_Nacional_Tricontinental")
    logger.info(f"  [OK] Maritorio completado en {time.time()-t0:.2f} s.")
    return res


def procesar_batimetria_shoa() -> Dict[str, Any]:
    """Procesa los sondajes batimétricos y de profundidad marina SHOA / SBAP."""
    logger.info("=== PROCESANDO COBERTURA 2: BATIMETRÍA Y PROFUNDIDAD MARINA SHOA ===")
    t0 = time.time()
    gdf = pyogrio.read_dataframe(GDB_PATH, layer="batimetria_shoa_sbap_Project")
    logger.info(f"  Cargados {len(gdf):,} puntos en {time.time()-t0:.2f} s.")
    
    # Estandarizar nombres legibles
    rename_dict = {
        "prfnddd": "profundidad_metros",
        "insttcn": "institucion",
        "dscrpcn": "carta_nautica",
        "actlzcn": "ano_actualizacion",
        "archv_r": "archivo_origen",
    }
    gdf = gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns})
    
    res = export_coverage(gdf, "PEM_Batimetria_SHOA_SBAP")
    logger.info(f"  [OK] Batimetría completada en {time.time()-t0:.2f} s.")
    return res


def procesar_geomorfologia_submarina() -> Dict[str, Any]:
    """Procesa las macro-unidades geomorfológicas submarinas GEBCO."""
    logger.info("=== PROCESANDO COBERTURA 3: GEOMORFOLOGÍA SUBMARINA GEBCO ===")
    t0 = time.time()
    gdf = pyogrio.read_dataframe(GDB_PATH, layer="geomorfologia_submar_Project1")
    logger.info(f"  Cargadas {len(gdf):,} unidades en {time.time()-t0:.2f} s.")
    
    rename_dict = {
        "geomorfolo": "unidad_geomorfologica",
        "sup_km2": "superficie_km2",
        "fecha_dato": "ano_fuente",
    }
    gdf = gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns})
    
    res = export_coverage(gdf, "PEM_Geomorfologia_Submarina_GEBCO")
    logger.info(f"  [OK] Geomorfología completada en {time.time()-t0:.2f} s.")
    return res


def procesar_montes_submarinos() -> Dict[str, Any]:
    """Procesa los montes submarinos y toponimia oceánica oficial."""
    logger.info("=== PROCESANDO COBERTURA 4: MONTES SUBMARINOS Y TOPONIMIA OCEÁNICA ===")
    t0 = time.time()
    gdf = pyogrio.read_dataframe(GDB_PATH, layer="toponimia_submarina")
    logger.info(f"  Cargados {len(gdf):,} montes y puntos toponímicos en {time.time()-t0:.2f} s.")
    
    rename_dict = {
        "Name": "nombre_monte",
        "FolderPath": "catalogo_categoria",
    }
    gdf = gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns})
    
    # Extraer elevación/cota Z si está presente en la geometría
    if gdf.geometry.has_z.any():
        gdf["elevacion_submarina_m"] = [p.z if hasattr(p, "z") else None for p in gdf.geometry]
    
    res = export_coverage(gdf, "PEM_Montes_Submarinos_Toponimia")
    logger.info(f"  [OK] Montes submarinos completados en {time.time()-t0:.2f} s.")
    return res


def procesar_cuencas_oceanicas() -> Dict[str, Any]:
    """Procesa las cuencas oceánicas y morfología del lecho submarino."""
    logger.info("=== PROCESANDO COBERTURA 5: CUENCAS OCEANOGRÁFICAS SUBMARINAS ===")
    t0 = time.time()
    gdf = pyogrio.read_dataframe(GDB_PATH, layer="RasterT_Basin_F1")
    logger.info(f"  Cargadas {len(gdf):,} cuencas submarinas en {time.time()-t0:.2f} s.")
    
    rename_dict = {
        "Id": "id_cuenca",
        "gridcode": "codigo_cuenca",
        "Shape_Length": "perimetro_grados",
        "Shape_Area": "area_grados",
    }
    gdf = gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns})
    
    res = export_coverage(gdf, "PEM_Cuencas_Oceanicas_Submarinas")
    logger.info(f"  [OK] Cuencas oceánicas completadas en {time.time()-t0:.2f} s.")
    return res


def procesar_biodiversidad_marina() -> Dict[str, Any]:
    """
    Procesa el catastro nacional de biodiversidad marina y especímenes IFOP / GBIF (4,52 millones de puntos).
    Dada su escala masiva (~4,5M puntos), se optimiza en GeoParquet 1.1 de alta compresión y CSV tabular,
    evitando la corrupción del formato Shapefile legacy (que supera el límite de 2 GB de DBF).
    """
    logger.info("=== PROCESANDO COBERTURA 6: BIODIVERSIDAD MARINA Y ESPECIES (IFOP/GBIF) ===")
    t0 = time.time()
    core_cols = ["gbifID", "kingdom", "phylum", "class", "order_", "family", "genus", "species", "scntfcN", "depth", "year", "cntryCd"]
    gdf = pyogrio.read_dataframe(GDB_PATH, layer="ocurrencias_ifop_gbif__Merge", columns=core_cols)
    logger.info(f"  Cargados {len(gdf):,} registros de biodiversidad en {time.time()-t0:.2f} s.")
    
    # Estandarizar nombres y seleccionar campos prioritarios
    rename_dict = {
        "gbifID": "id_gbif",
        "kingdom": "reino",
        "phylum": "filo",
        "class": "clase",
        "order_": "orden",
        "family": "familia",
        "genus": "genero",
        "species": "especie",
        "scntfcN": "nombre_cientifico",
        "depth": "profundidad_m",
        "year": "ano_registro",
        "cntryCd": "codigo_pais",
    }
    gdf = gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns})
    
    # Exportar GeoParquet y CSV (omitiendo Shapefile por exceder límite de 2GB de DBF, y GPKG por tamaño excesivo)
    res = export_coverage(
        gdf,
        "PEM_Biodiversidad_Marina_Especies_IFOP_GBIF",
        export_shp=False,
        export_csv=True,
        export_gpkg=False,
    )
    logger.info(f"  [OK] Biodiversidad marina completada en {time.time()-t0:.2f} s.")
    return res


def main() -> None:
    """Función principal orquestadora de extracción y empaquetado PEM."""
    import argparse

    parser = argparse.ArgumentParser(description="Extractor y conversor PEM para IDE CIT")
    parser.add_argument(
        "--coberturas",
        nargs="+",
        choices=["maritorio", "batimetria", "geomorfologia", "montes", "cuencas", "biodiversidad", "todas"],
        default=["todas"],
        help="Coberturas a procesar",
    )
    args = parser.parse_args()

    print("=" * 80)
    print(" IDE CIT — PIPELINE ETL DE PLANIFICACIÓN ESPACIAL MARINA (PEM / SBAP)")
    print(" Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez")
    print("=" * 80)
    
    if not GDB_PATH.exists():
        logger.error(f"Geodatabase no encontrada en: {GDB_PATH}")
        sys.exit(1)
        
    start_total = time.time()
    targets = set(args.coberturas)
    run_all = "todas" in targets
    
    all_res: Dict[str, Any] = {}
    
    if run_all or "maritorio" in targets:
        all_res["Maritorio Nacional"] = procesar_maritorio_nacional()
    if run_all or "batimetria" in targets:
        all_res["Batimetría SHOA/SBAP"] = procesar_batimetria_shoa()
    if run_all or "geomorfologia" in targets:
        all_res["Geomorfología GEBCO"] = procesar_geomorfologia_submarina()
    if run_all or "montes" in targets:
        all_res["Montes Submarinos"] = procesar_montes_submarinos()
    if run_all or "cuencas" in targets:
        all_res["Cuencas Oceánicas"] = procesar_cuencas_oceanicas()
    if run_all or "biodiversidad" in targets:
        all_res["Biodiversidad IFOP/GBIF"] = procesar_biodiversidad_marina()
    
    total_time = time.time() - start_total
    
    print("\n" + "=" * 80)
    print(f" RESUMEN DE COBERTURAS MARINAS PROCESADAS ({total_time:.2f} s)")
    print("=" * 80)
    
    for name, r in all_res.items():
        print(f"\n* {name}:")
        for fmt, data in r.items():
            print(f"    - {fmt.upper():<10}: {data['path'].name:<55} ({data['size_mb']:>8.2f} MB)")
            
    print("\n" + "=" * 80)
    print(f" Todas las coberturas están listas en: {DOWNLOAD_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
