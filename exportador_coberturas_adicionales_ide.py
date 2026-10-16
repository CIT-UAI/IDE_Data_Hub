#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — EXPORTADOR Y EMPAQUETADOR DE COBERTURAS MAESTRAS ADICIONALES
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Genera y empaqueta en multiformato estándar (GeoParquet, GeoPackage, Shapefile, CSV):
1. INSE 2024: Estratificación Socioeconómica a nivel de manzana (FONDEF NNA + Geometría)
2. Censo 2024: Imputaciones Demográficas por cohortes Sprague a nivel de manzana
3. Educación Inicial: Cobertura Maestra Nacional de Jardines y Salas Cuna 2024
4. Edificaciones Urbanas: Huella y Presencia de Edificaciones (341k polígonos)

Todos los productos se resguardan estrictamente DENTRO del proyecto:
- 07_Aplicaciones_y_Visualizadores_Web/IDE_Data_Hub/download/
- 07_Aplicaciones_y_Visualizadores_Web/IDE_Data_Hub/dist/download/
- data_parquet/
===============================================================================
"""

import os
import sys
import time
import shutil
import argparse
import zipfile
import tempfile
import hashlib
from pathlib import Path
import pandas as pd
import geopandas as gpd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_proyecto_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent

ROOT_DIR = find_proyecto_root()
IDE_HUB_DIR = ROOT_DIR / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
DOWNLOAD_DIR = IDE_HUB_DIR / "download"
DIST_DOWNLOAD_DIR = IDE_HUB_DIR / "dist" / "download"
DATA_PARQUET_DIR = ROOT_DIR / "data_parquet"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
DIST_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
DATA_PARQUET_DIR.mkdir(parents=True, exist_ok=True)

OUT_DIRS = [DOWNLOAD_DIR, DIST_DOWNLOAD_DIR]

def sha256_file(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def export_shp_zip(gdf: gpd.GeoDataFrame, zip_path: Path, base_name: str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        shp_path = Path(tmpdir) / f"{base_name}.shp"
        gdf_clean = gdf.copy()
        
        # Shapefile sólo admite 1 tipo de geometría
        if len(gdf_clean) > 0 and gdf_clean.geometry.geom_type.nunique() > 1:
            gdf_clean["geometry"] = gdf_clean.geometry.apply(
                lambda g: g.representative_point() if g.geom_type in ["Polygon", "MultiPolygon"] else g
            )
            
        for col in gdf_clean.columns:
            if col != "geometry" and pd.api.types.is_datetime64_any_dtype(gdf_clean[col]):
                gdf_clean[col] = gdf_clean[col].astype(str)
                
        gdf_clean.to_file(shp_path, driver="ESRI Shapefile", encoding="utf-8")
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                p = Path(tmpdir) / f"{base_name}{ext}"
                if p.exists():
                    zipf.write(p, arcname=f"{base_name}{ext}")

def save_multiformat(gdf: gpd.GeoDataFrame, base_filename: str, out_dirs: list[Path]) -> dict:
    generated = {}
    print(f"  -> Guardando {base_filename} ({len(gdf):,} registros)...")
    primary_dir = out_dirs[0]
    other_dirs = out_dirs[1:]
    
    # 1. GeoParquet
    pq_name = f"{base_filename}.parquet"
    p_primary = primary_dir / pq_name
    gdf.to_parquet(p_primary)
    for d in other_dirs:
        shutil.copy2(p_primary, d / pq_name)
    generated["parquet"] = {
        "filename": pq_name,
        "size_bytes": p_primary.stat().st_size,
        "sha256": sha256_file(p_primary)
    }
    print(f"     ✓ Parquet: {p_primary.stat().st_size / (1024*1024):.2f} MB")
    
    # 2. GeoPackage
    gpkg_name = f"{base_filename}.gpkg"
    g_primary = primary_dir / gpkg_name
    gdf.to_file(g_primary, driver="GPKG", layer=base_filename)
    for d in other_dirs:
        shutil.copy2(g_primary, d / gpkg_name)
    generated["gpkg"] = {
        "filename": gpkg_name,
        "size_bytes": g_primary.stat().st_size,
        "sha256": sha256_file(g_primary)
    }
    print(f"     ✓ GeoPackage: {g_primary.stat().st_size / (1024*1024):.2f} MB")

    # 3. Shapefile (.zip)
    zip_name = f"{base_filename}_SHP.zip"
    z_primary = primary_dir / zip_name
    export_shp_zip(gdf, z_primary, base_filename)
    for d in other_dirs:
        shutil.copy2(z_primary, d / zip_name)
    generated["shp_zip"] = {
        "filename": zip_name,
        "size_bytes": z_primary.stat().st_size,
        "sha256": sha256_file(z_primary)
    }
    print(f"     ✓ Shapefile: {z_primary.stat().st_size / (1024*1024):.2f} MB")

    # 4. CSV Tabular (con lat/lon centroidales si es espacial)
    csv_name = f"{base_filename}.csv"
    df_csv = pd.DataFrame(gdf.drop(columns=["geometry"]))
    if "LATITUD" not in df_csv.columns:
        centroids = gdf.geometry.representative_point()
        df_csv["LONGITUD"] = centroids.x.round(6)
        df_csv["LATITUD"] = centroids.y.round(6)
        
    c_primary = primary_dir / csv_name
    df_csv.to_csv(c_primary, index=False, encoding="utf-8")
    for d in other_dirs:
        shutil.copy2(c_primary, d / csv_name)
    generated["csv"] = {
        "filename": csv_name,
        "size_bytes": c_primary.stat().st_size,
        "sha256": sha256_file(c_primary)
    }
    print(f"     ✓ CSV: {c_primary.stat().st_size / (1024*1024):.2f} MB")

    return generated

def main():
    print("=" * 80)
    print("EMPAQUETADOR OFICIAL DE COBERTURAS MAESTRAS ADICIONALES (IDE CIT)")
    print("=" * 80)
    t_start = time.time()

    parser = argparse.ArgumentParser(description="Empaquetador de Coberturas Adicionales")
    parser.add_argument("--layer", choices=["all", "jardines", "buildings", "censo", "inse"], default="all", help="Capa a procesar")
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # 1. EDUCACIÓN INICIAL: JARDINES INFANTILES Y SALAS CUNA 2024
    # -------------------------------------------------------------------------
    if args.layer in ["all", "jardines"]:
        print("\n[1/4] Procesando Cobertura Maestra de Jardines y Salas Cuna 2024...")
        p_jardines = ROOT_DIR / "data_geoparquet" / "equipamientos" / "cobertura_maestra_jardines_privados_2024.parquet"
        if p_jardines.exists():
            gdf_jardines = gpd.read_parquet(p_jardines)
            save_multiformat(gdf_jardines, "Educacion_Inicial_Jardines_SalasCuna_2024", OUT_DIRS)
        else:
            print("  ⚠️ No se encontró:", p_jardines)

    # -------------------------------------------------------------------------
    # 2. HUELLA DE EDIFICACIONES URBANAS (341K POLÍGONOS)
    # -------------------------------------------------------------------------
    if args.layer in ["all", "buildings"]:
        print("\n[2/4] Procesando Huella de Edificaciones Urbanas (Buildings)...")
        p_buildings = Path.home() / "Coberturas" / "vectores" / "20241010_presence_buildings_years" / "20241010_presence_buildings_years.shp"
        if p_buildings.exists():
            gdf_b = gpd.read_file(p_buildings)
            gdf_b = gdf_b.to_crs("EPSG:4326")
            save_multiformat(gdf_b, "Huella_Edificaciones_Urbanas_2024", OUT_DIRS)
        else:
            print("  ⚠️ No se encontró:", p_buildings)

    # -------------------------------------------------------------------------
    # 3. CENSO 2024: IMPUTACIONES DEMOGRÁFICAS SPRAGUE A NIVEL DE MANZANA
    # -------------------------------------------------------------------------
    if args.layer in ["all", "censo"]:
        print("\n[3/4] Procesando Censo 2024 e Imputaciones Demográficas a nivel de Manzana...")
        p_maestro = ROOT_DIR / "data_parquet" / "MBHT_MAESTRO_2024_NACIONAL.parquet"
        if p_maestro.exists():
            gdf_maestro = gpd.read_parquet(p_maestro)
            
            # Columnas censales y demográficas estandarizadas
            censo_cols = [
                'ID_MANZCIT', 'COD_REG', 'REGION', 'COD_PROV', 'PROVINCIA', 'COD_COM', 'COMUNA',
                'CATEGORIA', 'AREA_C', 'PERSONAS2', 'HOMBRES_x', 'MUJERES_x', 'P_HOMBRES', 'P_MUJERES',
                'E0_5', 'H0_5', 'M0_5', 'E6_13', 'H6_13', 'M6_13', 'E14_17', 'H14_17', 'M14_17',
                'E18_24', 'H18_24', 'M18_24', 'E25_44', 'H25_44', 'M25_44', 'E45_59', 'H45_59', 'M45_59',
                'E60M', 'H60M', 'M60M', 'E65AMAS', 'H65AMAS', 'M65AMAS', 'H80AMAS', 'M80AMAS',
                'E0A3', 'E0A4', 'E4A5', 'E6A13', 'E7A10', 'E14A18', 'E19A30', 'E60AMAS', 'IND_ENVEJ', 'geometry'
            ]
            cols_presentes = [c for c in censo_cols if c in gdf_maestro.columns]
            gdf_censo = gdf_maestro[cols_presentes].copy()
            
            # Renombrar columnas para consistencia pública
            rename_map = {'HOMBRES_x': 'HOMBRES', 'MUJERES_x': 'MUJERES', 'PERSONAS2': 'POBLACION_2024'}
            gdf_censo = gdf_censo.rename(columns={k: v for k, v in rename_map.items() if k in gdf_censo.columns})
            
            save_multiformat(gdf_censo, "Censo_Imputaciones_2024_Nacional", OUT_DIRS)
        else:
            print("  ⚠️ No se encontró:", p_maestro)

    # -------------------------------------------------------------------------
    # 4. INSE 2024: ESTRATIFICACIÓN SOCIOECONÓMICA A NIVEL DE MANZANA
    # -------------------------------------------------------------------------
    if args.layer in ["all", "inse"]:
        print("\n[4/4] Procesando INSE 2024 a nivel de Manzana (FONDEF NNA + Polígonos)...")
        p_inse_fondef = Path.home() / "investigaciones" / "FONDEF NNA" / "indicadores_fondef_nna" / "00_Insumos_Base" / "12_INSE_Estratificacion_Socioeconomica_2024" / "INSE_2024_ESTRATIFICACION_NACIONAL.parquet"
        p_maestro = ROOT_DIR / "data_parquet" / "MBHT_MAESTRO_2024_NACIONAL.parquet"
        
        if p_inse_fondef.exists() and p_maestro.exists():
            df_inse = pd.read_parquet(p_inse_fondef)
            # Extraer geometrías del maestro
            df_geom = gpd.read_parquet(p_maestro, columns=['ID_MANZCIT', 'geometry'])
            df_geom['ID_MANZCIT'] = df_geom['ID_MANZCIT'].astype(str)
            df_inse['MANZ_CIT'] = df_inse['MANZ_CIT'].astype(str)
            
            # Unir atributos econométricos con geometría de polígonos censales
            gdf_inse = df_geom.merge(df_inse, left_on='ID_MANZCIT', right_on='MANZ_CIT', how='inner')
            
            # FILTRO ESTRICTO: Solo columnas directamente relacionadas con el INSE
            inse_cols_estrictas = [
                'MANZ_CIT', 'COD_REG', 'COD_COM', 'COMUNA', 'POBLACION',
                'INSE_OFIC', 'Q_INSE_OFI', 'GSE_OFIC',
                'INSE_PURO', 'Q_INSE_PUR', 'GSE_PURO',
                'ES_CAMPAM', 'COD_AH', 'VGT_UF', 'VGT_M2',
                'geometry'
            ]
            gdf_inse = gdf_inse[[c for c in inse_cols_estrictas if c in gdf_inse.columns]]
            gdf_inse = gpd.GeoDataFrame(gdf_inse, geometry='geometry', crs="EPSG:4326")
            
            # Resguardar copia maestra permanente en data_parquet/ del proyecto
            pq_local = DATA_PARQUET_DIR / "INSE_2024_NACIONAL_MANZANAS.parquet"
            gdf_inse.to_parquet(pq_local)
            print(f"  ✓ Respaldo maestro permanente en proyecto: {pq_local}")
            print(f"  ✓ Columnas estrictas del INSE ({len(gdf_inse.columns)}): {gdf_inse.columns.tolist()}")
            
            save_multiformat(gdf_inse, "INSE_Socioeconomico_Nacional_2024", OUT_DIRS)
        else:
            print("  ⚠️ No se encontró insumo INSE FONDEF NNA o Maestro.")

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"EMPAQUETADO COMPLETADO EXITOSAMENTE EN {elapsed:.2f} s")
    print(f"Todos los archivos resguardados en: {DOWNLOAD_DIR} y {DIST_DOWNLOAD_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
