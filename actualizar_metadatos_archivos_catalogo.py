import os
import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
manifest_path = os.path.join(base_dir, "data", "archivos_hash_manifest.json")
cat_path = os.path.join(base_dir, "data", "catalogo_ide_cit.json")

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

def fmt_size(b):
    if not b:
        return "N/D"
    if b > 1024 * 1024:
        return f"{b / (1024*1024):.1f} MB".replace(".", ",")
    return f"{b / 1024:.0f} KB"

# Map layers to specific files in download manifest
file_map = {
    "kpi_mud_2017": {
        "parquet": "MBHT_2017_Nacional_Manzanas.parquet",
        "gpkg": "MBHT_2017_Nacional_Manzanas.gpkg",
        "shp_zip": "MBHT_2017_Nacional_Manzanas_SHP.zip",
        "csv": "MBHT_2017_Nacional_Manzanas.csv"
    },
    "pem_maritorio_nacional": {
        "parquet": "PEM_Maritorio_Nacional_Tricontinental.parquet",
        "gpkg": "PEM_Maritorio_Nacional_Tricontinental.gpkg",
        "shp_zip": "PEM_Maritorio_Nacional_Tricontinental_SHP.zip",
        "csv": "PEM_Maritorio_Nacional_Tricontinental.csv"
    },
    "pem_geomorfologia_gebco": {
        "parquet": "PEM_Geomorfologia_Submarina_GEBCO.parquet",
        "gpkg": "PEM_Geomorfologia_Submarina_GEBCO.gpkg",
        "shp_zip": "PEM_Geomorfologia_Submarina_GEBCO_SHP.zip",
        "csv": "PEM_Geomorfologia_Submarina_GEBCO.csv"
    },
    "pem_montes_submarinos": {
        "parquet": "PEM_Montes_Submarinos_Toponimia.parquet",
        "gpkg": "PEM_Montes_Submarinos_Toponimia.gpkg",
        "shp_zip": "PEM_Montes_Submarinos_Toponimia_SHP.zip",
        "csv": "PEM_Montes_Submarinos_Toponimia.csv"
    },
    "pem_cuencas_oceanicas": {
        "parquet": "PEM_Cuencas_Oceanicas_Submarinas.parquet",
        "gpkg": "PEM_Cuencas_Oceanicas_Submarinas.gpkg",
        "shp_zip": "PEM_Cuencas_Oceanicas_Submarinas_SHP.zip",
        "csv": "PEM_Cuencas_Oceanicas_Submarinas.csv"
    },
    "censo_imputaciones_2024": {
        "parquet": "Censo_Imputaciones_2024_Nacional.parquet",
        "gpkg": "Censo_Imputaciones_2024_Nacional.gpkg",
        "shp_zip": "Censo_Imputaciones_2024_Nacional_SHP.zip",
        "csv": "Censo_Imputaciones_2024_Nacional.csv"
    },
    "inse_socioeconomico": {
        "parquet": "INSE_Socioeconomico_Nacional_2024.parquet",
        "gpkg": "INSE_Socioeconomico_Nacional_2024.gpkg",
        "shp_zip": "INSE_Socioeconomico_Nacional_2024_SHP.zip",
        "csv": "INSE_Socioeconomico_Nacional_2024.csv"
    },
    "equipamientos_2017": {
        "parquet": "Equipamientos_2017_Nacional_Consolidado.parquet",
        "gpkg": "Equipamientos_2017_Nacional_Consolidado.gpkg",
        "shp_zip": "Equipamientos_2017_Nacional_Consolidado_SHP.zip",
        "csv": "Equipamientos_2017_Nacional_Consolidado.csv"
    },
    "red_vial_ejes_2017": {
        "parquet": "Red_Vial_Ejes_2017_Nacional.parquet",
        "gpkg": "Red_Vial_Ejes_2017_Nacional.gpkg",
        "shp_zip": "Red_Vial_Ejes_2017_Nacional_SHP.zip",
        "csv": "Red_Vial_Ejes_2017_Nacional.csv"
    },
    "educacion_inicial_2024": {
        "parquet": "Educacion_Inicial_Jardines_SalasCuna_2024.parquet",
        "gpkg": "Educacion_Inicial_Jardines_SalasCuna_2024.gpkg",
        "shp_zip": "Educacion_Inicial_Jardines_SalasCuna_2024_SHP.zip",
        "csv": "Educacion_Inicial_Jardines_SalasCuna_2024.csv"
    },
    "huella_edificaciones_2024": {
        "parquet": "Huella_Edificaciones_Urbanas_2024.parquet",
        "gpkg": "Huella_Edificaciones_Urbanas_2024.gpkg",
        "shp_zip": "Huella_Edificaciones_Urbanas_2024_SHP.zip",
        "csv": "Huella_Edificaciones_Urbanas_2024.csv"
    }
}

for capa in cat.get("capas", []):
    cid = capa.get("id")
    capa["version"] = capa.get("version") or "1.0.3"
    capa["updated"] = "2026-10-15"
    
    mapping = file_map.get(cid, {})
    capa_archivos = {}
    
    for fmt_key, fname in mapping.items():
        if fname in manifest:
            info = manifest[fname]
            capa_archivos[fmt_key] = {
                "filename": fname,
                "url": f"download/{fname}",
                "size_bytes": info["size_bytes"],
                "size_human": fmt_size(info["size_bytes"]),
                "sha256": info["sha256"]
            }
    
    if capa_archivos:
        capa["archivos_distribucion"] = capa_archivos
        # Set primary size and sha256 from parquet
        if "parquet" in capa_archivos:
            capa["size_bytes"] = capa_archivos["parquet"]["size_bytes"]
            capa["size_human"] = capa_archivos["parquet"]["size_human"]
            capa["sha256"] = capa_archivos["parquet"]["sha256"]
            capa["s3_parquet"] = f"download/{capa_archivos['parquet']['filename']}"
        if "gpkg" in capa_archivos:
            capa["gpkg_url"] = f"download/{capa_archivos['gpkg']['filename']}"
        if "shp_zip" in capa_archivos:
            capa["shp_url"] = f"download/{capa_archivos['shp_zip']['filename']}"
        if "csv" in capa_archivos:
            capa["csv_url"] = f"download/{capa_archivos['csv']['filename']}"

with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, indent=2, ensure_ascii=False)

print(f"Catalogo {cat_path} enriched with machine-readable file metadata!")
