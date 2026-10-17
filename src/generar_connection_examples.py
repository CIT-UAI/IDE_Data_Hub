import os
import json
import re
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "src" else Path(__file__).resolve().parent
cat_path = base_dir / "data" / "catalogo_ide_cit.json"
conn_path = base_dir / "data" / "connection_examples.json"
root_conn_path = base_dir / "public" / "connection_examples.json"

with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

# 1. Build connection_examples.json
conn_data = {
    "metadata": {
        "title": "IDE CIT — Ejemplos de Conexión y Snippets para Agentes de IA y Software SIG",
        "institution": "Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez",
        "url_portal": "https://ide.cit.uai.cl",
        "license": "Creative Commons Atribución 4.0 Internacional (CC BY 4.0)",
        "updated": "2026-10-08",
        "version": "2026.1",
        "total_layers": len(cat.get("capas", []))
    },
    "connections": []
}

for capa in cat.get("capas", []):
    cid = capa.get("id")
    titulo = capa.get("titulo")
    crs = capa.get("crs", "EPSG:4326 (WGS 84)")
    ver = capa.get("version", "1.0.3")
    upd = capa.get("updated", "2026-10-15")
    archivos = capa.get("archivos_distribucion", {})
    
    pq_url = f"https://ide.cit.uai.cl/{archivos['parquet']['url']}" if "parquet" in archivos else (capa.get("s3_parquet") or f"https://ide.cit.uai.cl/download/{cid}.parquet")
    gpkg_url = f"https://ide.cit.uai.cl/{archivos['gpkg']['url']}" if "gpkg" in archivos else (f"https://ide.cit.uai.cl/{capa.get('gpkg_url')}" if capa.get("gpkg_url") else None)
    
    tile_source = capa.get("tile_source", "")
    tilejson_url = f"https://engine.matrizbht.cl/tiles/{tile_source}/index.json" if tile_source else None
    mvt_tiles_url = f"https://engine.matrizbht.cl/tiles/{tile_source}/{{z}}/{{x}}/{{y}}.pbf" if tile_source else None
    
    # Generate python snippet
    python_snippet = (
        f"import duckdb\n"
        f"import geopandas as gpd\n\n"
        f"con = duckdb.connect()\n"
        f"con.execute('INSTALL spatial; LOAD spatial;')\n"
        f"query = \"SELECT * FROM '{pq_url}' LIMIT 1000;\"\n"
        f"df = con.execute(query).df()\n"
        f"gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkb(df['geometry']) if 'geometry' in df else None, crs='{crs.split()[0]}')\n"
        f"print(f'Cargados {{len(gdf)}} registros de {titulo}')"
    )
    
    # Generate R snippet
    r_snippet = (
        f"library(sf)\n"
        f"library(arrow)\n"
        f"library(dplyr)\n\n"
        f"# Lectura directa desde GeoParquet\n"
        f"url <- '{pq_url}'\n"
        f"df <- read_parquet(url)\n"
        f"sf_layer <- st_as_sf(df, wkt = 'geometry', crs = 4326)\n"
        f"summary(sf_layer)"
    )
    
    # Generate QGIS instructions
    qgis_conector = f"https://ide.cit.uai.cl/download/qgis/CIT_MBHT_2017_Nacional.qlr"
    qgis_tilejson = tilejson_url or "https://engine.matrizbht.cl/tiles/index.json"
    
    conn_data["connections"].append({
        "layer_id": cid,
        "title": titulo,
        "category": capa.get("matriz", "").upper(),
        "dimension": capa.get("ambito", "tierra"),
        "crs": crs,
        "version": ver,
        "updated": upd,
        "endpoints": {
            "parquet_https": pq_url,
            "gpkg_https": gpkg_url,
            "tilejson": tilejson_url,
            "mvt_pbf": mvt_tiles_url,
            "qgis_qlr": qgis_conector,
            "stac_item": f"https://ide.cit.uai.cl/stac/{cid}.json" if (base_dir / "stac" / f"{cid}.json").exists() else "https://ide.cit.uai.cl/stac/catalog.json"
        },
        "data_dictionary": [
            {
                "name": attr.get("campo"),
                "type": attr.get("tipo", "String"),
                "description": attr.get("descripcion", "")
            }
            for attr in capa.get("atributos", [])
        ],
        "code_examples": {
            "python_geopandas": f"import geopandas as gpd; gdf = gpd.read_parquet('{pq_url}')",
            "python_duckdb": python_snippet,
            "r_sf_arrow": r_snippet,
            "qgis_tilejson": qgis_tilejson,
            "curl_head": f"curl -I {pq_url}"
        }
    })

with open(conn_path, "w", encoding="utf-8") as f:
    json.dump(conn_data, f, indent=2, ensure_ascii=False)

with open(root_conn_path, "w", encoding="utf-8") as f:
    json.dump(conn_data, f, indent=2, ensure_ascii=False)

print(f"[OK] connection_examples.json generado en: {conn_path} y {root_conn_path}")
