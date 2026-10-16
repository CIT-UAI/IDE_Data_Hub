#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de sincronización a S3 e invalidación en CloudFront para IDE CIT.
"""
import mimetypes
import os
import shutil
import time
from pathlib import Path
import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
BUCKET_NAME = "ide.cit.uai.cl"
DISTRIBUTION_ID = "E1POIT4JDVDUUO"

# Autenticación segura: usa variables de entorno estándar (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) o ~/.aws/credentials
session_kwargs = {"region_name": REGION}
if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
    session_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
    session_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")

session = boto3.Session(**session_kwargs)

s3 = session.client("s3")
cloudfront = session.client("cloudfront")

base_dir = Path(__file__).resolve().parent
dist_dir = base_dir / "dist"

files_to_upload = [
    # Archivos HTML estándar y aliases limpios (Clean URLs)
    ("index.html", "index.html"),
    ("index.html", "inicio"),
    ("inicio/index.html", "inicio/index.html"),
    ("descargas-2017.html", "descargas-2017.html"),
    ("descargas-2017.html", "descargas"),
    ("descargas/index.html", "descargas/index.html"),
    ("guia-tecnica.html", "guia-tecnica.html"),
    ("guia-tecnica.html", "guia-tecnica"),
    ("guia-tecnica/index.html", "guia-tecnica/index.html"),
    ("red-ides.html", "red-ides.html"),
    ("red-ides.html", "red-ides"),
    ("red-ides/index.html", "red-ides/index.html"),
    ("ficha-mbht-2017.html", "ficha-mbht-2017.html"),
    ("ficha-mbht-2017.html", "ficha-mbht-2017"),
    ("ficha-mbht-2017/index.html", "ficha-mbht-2017/index.html"),
    ("manifest.json", "manifest.json"),
    ("sitemap.xml", "sitemap.xml"),
    ("robots.txt", "robots.txt"),
    ("security.txt", "security.txt"),
    (".well-known/security.txt", ".well-known/security.txt"),
    ("llms.txt", "llms.txt"),
    ("llms-full.txt", "llms-full.txt"),
    ("site.webmanifest", "site.webmanifest"),
    ("favicon.ico", "favicon.ico"),
    ("version.json", "version.json"),
    ("catalogo.json", "catalogo.json"),
    ("catalogo.csv", "catalogo.csv"),
    ("dcat.json", "dcat.json"),
    ("connection_examples.json", "connection_examples.json"),
    ("data/catalogo_ide_cit.json", "data/catalogo_ide_cit.json"),
    ("data/catalogo_ide_cit.csv", "data/catalogo_ide_cit.csv"),
    ("data/dcat.json", "data/dcat.json"),
    ("data/connection_examples.json", "data/connection_examples.json"),
    ("data/archivos_hash_manifest.json", "data/archivos_hash_manifest.json"),
    ("download/metadata.xml", "download/metadata.xml"),
    ("download/metadata.xml", "metadata.xml"),
    # Estándar STAC 1.0.0
    ("stac/catalog.json", "stac/catalog.json"),
    ("stac/catalog.json", "stac/index.json"),
    ("stac/collection.json", "stac/collection.json"),
    ("stac/censo_imputaciones_2024.json", "stac/censo_imputaciones_2024.json"),
    ("stac/mbht_2017.json", "stac/mbht_2017.json"),
    ("stac/pem_maritorio.json", "stac/pem_maritorio.json"),
    ("stac/equipamientos.json", "stac/equipamientos.json"),
    ("data/stac/collection.json", "data/stac/collection.json"),
    ("stac/index.html", "stac/index.html"),
    ("stac/index.html", "stac"),
    ("stac/index.html", "stac/"),
    # Conectores y Estilos QGIS (.qlr, .qml)
    ("download/qgis/CIT_MBHT_2017_Nacional.qlr", "download/qgis/CIT_MBHT_2017_Nacional.qlr"),
    ("download/qgis/CIT_Servicios_WMS.qlr", "download/qgis/CIT_Servicios_WMS.qlr"),
    ("download/qgis/CIT_MBHT_Simbologia_Jenks.qml", "download/qgis/CIT_MBHT_Simbologia_Jenks.qml"),
    # Descargables PEM actualizados en kilómetros y kilómetros cuadrados
    ("download/PEM_Maritorio_Nacional_Tricontinental.parquet", "download/PEM_Maritorio_Nacional_Tricontinental.parquet"),
    ("download/PEM_Maritorio_Nacional_Tricontinental.gpkg", "download/PEM_Maritorio_Nacional_Tricontinental.gpkg"),
    ("download/PEM_Maritorio_Nacional_Tricontinental.csv", "download/PEM_Maritorio_Nacional_Tricontinental.csv"),
    ("download/PEM_Maritorio_Nacional_Tricontinental_SHP.zip", "download/PEM_Maritorio_Nacional_Tricontinental_SHP.zip"),
    ("download/PEM_Cuencas_Oceanicas_Submarinas.parquet", "download/PEM_Cuencas_Oceanicas_Submarinas.parquet"),
    ("download/PEM_Cuencas_Oceanicas_Submarinas.gpkg", "download/PEM_Cuencas_Oceanicas_Submarinas.gpkg"),
    ("download/PEM_Cuencas_Oceanicas_Submarinas.csv", "download/PEM_Cuencas_Oceanicas_Submarinas.csv"),
    ("download/PEM_Cuencas_Oceanicas_Submarinas_SHP.zip", "download/PEM_Cuencas_Oceanicas_Submarinas_SHP.zip"),
    # Archivo de Verificación Criptográfica Independiente
    ("download/SHA256SUMS.txt", "download/SHA256SUMS.txt"),
    ("download/SHA256SUMS.txt", "SHA256SUMS.txt"),
    ("download/reproducir_verificacion_r15.py", "download/reproducir_verificacion_r15.py")
]

# Agregar automáticamente todos los XML ISO 19139 y certificados
iso_data_dir = base_dir / "data" / "iso_xml"
if iso_data_dir.exists():
    for xf in iso_data_dir.glob("*.xml"):
        files_to_upload.append((f"data/iso_xml/{xf.name}", f"data/iso_xml/{xf.name}"))
        files_to_upload.append((f"data/iso_xml/{xf.name}", f"download/iso_xml/{xf.name}"))
    for jf in iso_data_dir.glob("*.json"):
        files_to_upload.append((f"data/iso_xml/{jf.name}", f"data/iso_xml/{jf.name}"))
        files_to_upload.append((f"data/iso_xml/{jf.name}", f"download/iso_xml/{jf.name}"))

# Agregar automáticamente todas las colecciones STAC generadas
stac_local_dir = base_dir / "stac"
if stac_local_dir.exists():
    for sf in stac_local_dir.glob("*.json"):
        files_to_upload.append((f"stac/{sf.name}", f"stac/{sf.name}"))
    if (stac_local_dir / "index.html").exists():
        files_to_upload.append(("stac/index.html", "stac/index.html"))



print(f"[*] Iniciando sincronización a s3://{BUCKET_NAME}...")

for item in files_to_upload:
    if isinstance(item, tuple):
        src_rel, target_key = item
    else:
        src_rel, target_key = item, item
    rel_path = src_rel
    local_path = base_dir / rel_path
    if not local_path.exists():
        local_path = dist_dir / rel_path
    if not local_path.exists():
        print(f"[-] Archivo no encontrado: {rel_path}")
        continue
    
    # Mantener dist actualizado
    if dist_dir.exists() and local_path != (dist_dir / rel_path):
        target_dist = dist_dir / rel_path
        target_dist.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local_path, target_dist)

    content_type, _ = mimetypes.guess_type(str(local_path))
    if rel_path.endswith(".html"):
        content_type = "text/html; charset=utf-8"
        cache_control = "max-age=0, no-cache, no-store, must-revalidate"
    elif rel_path.endswith(".json") or rel_path.endswith(".webmanifest"):
        content_type = "application/json; charset=utf-8"
        cache_control = "max-age=0, no-cache, no-store, must-revalidate"
    elif rel_path.endswith(".csv"):
        content_type = "text/csv; charset=utf-8"
        cache_control = "max-age=0, no-cache, no-store, must-revalidate"
    elif rel_path.endswith(".xml"):
        content_type = "application/xml; charset=utf-8"
        cache_control = "public, max-age=86400, must-revalidate"
    elif rel_path.endswith(".txt"):
        content_type = "text/plain; charset=utf-8"
        cache_control = "public, max-age=86400, must-revalidate"
    else:
        content_type = content_type or "binary/octet-stream"
        cache_control = "public, max-age=31536000, immutable"

    s3_key = target_key.replace("\\", "/")
    print(f"    Subiendo {s3_key} ({local_path.stat().st_size / 1024:.1f} KB, {content_type})...")
    with open(local_path, "rb") as f:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=f,
            ContentType=content_type,
            CacheControl=cache_control
        )

print("[OK] Todos los archivos críticos fueron sincronizados en S3.")

# Purga de archivos obsoletos o no autorizados en S3 (protección de prelanzamiento noviembre 2026)
obsolete_s3_keys = [
    "download/qgis/CIT_MBHT_2024_VectorTiles.qlr",
    "download/R13_MZ_2024.parquet",
    "data/R13_MZ_2024.parquet"
]
print("[*] Verificando purga de archivos obsoletos en S3...")
for ok in obsolete_s3_keys:
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=ok)
        print(f"    [-] Purgado de S3 si existía: {ok}")
    except Exception as e:
        pass

# También subir imágenes SVG por si se actualizaron
img_dir = dist_dir / "img"
if img_dir.exists():
    for img_file in img_dir.glob("*.svg"):
        s3_key = f"img/{img_file.name}"
        with open(img_file, "rb") as f:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=f,
                ContentType="image/svg+xml",
                CacheControl="public, max-age=31536000, immutable"
            )
        print(f"    Subido vector {s3_key}")

# Crear invalidación en CloudFront
print(f"[*] Creando invalidación en CloudFront ({DISTRIBUTION_ID})...")
caller_ref = f"inv-{int(time.time())}"
res = cloudfront.create_invalidation(
    DistributionId=DISTRIBUTION_ID,
    InvalidationBatch={
        "Paths": {
            "Quantity": 1,
            "Items": ["/*"]
        },
        "CallerReference": caller_ref
    }
)
invalidation_id = res["Invalidation"]["Id"]
print(f"[OK] Invalidación creada exitosamente: {invalidation_id}")
