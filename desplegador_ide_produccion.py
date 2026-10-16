#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — PIPELINE DE EMPAQUETADO Y DESPLIEGUE A PRODUCCIÓN (S3 / CDN)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Módulo algorítmico dedicado a la preparación, verificación pre-vuelo (pre-flight),
    generación de manifiesto de integridad SHA-256 y empaquetado de producción
    para el portal web de la IDE CIT y sus catálogos abiertos (ISO 19139 / STAC).

    Por directiva de seguridad, opera en modo SIMULACIÓN / DRY-RUN por defecto,
    generando el paquete validado en local sin ejecutar publicaciones remotas
    hasta autorización explícita.

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import logging
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configuración de Logging Profesional
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Desplegador_IDE_CIT")


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


def compute_sha256(file_path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo para verificar integridad."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


class IDEProductionDeployer:
    """
    Pipeline de empaquetado, auditoría de integridad y preparación de despliegue.
    """

    def __init__(self, root_dir: Optional[Path] = None, dist_dir: Optional[Path] = None) -> None:
        self.root_dir: Path = root_dir or find_proyecto_root()
        self.ide_dir: Path = self.root_dir / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
        self.dist_dir: Path = dist_dir or (self.ide_dir / "dist")
        self.data_dir: Path = self.ide_dir / "data"
        self.img_dir: Path = self.ide_dir / "img"

    def preflight_check(self) -> Tuple[bool, List[str]]:
        """
        Verifica que todos los archivos requeridos existan y estén en estado óptimo.
        """
        logger.info("🛫 Ejecutando chequeos pre-vuelo (Pre-flight checks)...")
        errors: List[str] = []

        # 1. Archivos HTML principales (Index, Descargas 2017, Guía Técnica y Red de IDEs)
        index_html = self.ide_dir / "index.html"
        descargas_html = self.ide_dir / "descargas-2017.html"
        guia_html = self.ide_dir / "guia-tecnica.html"
        red_html = self.ide_dir / "red-ides.html"

        if not index_html.exists() or index_html.stat().st_size == 0:
            errors.append("Falta el archivo principal 'index.html' o está vacío.")
        else:
            logger.info(f"   ✓ index.html verificado ({index_html.stat().st_size / 1024:.1f} KB)")

        if not descargas_html.exists() or descargas_html.stat().st_size == 0:
            errors.append("Falta el archivo 'descargas-2017.html' o está vacío.")
        else:
            logger.info(f"   ✓ descargas-2017.html verificado ({descargas_html.stat().st_size / 1024:.1f} KB)")

        if not guia_html.exists() or guia_html.stat().st_size == 0:
            errors.append("Falta el archivo 'guia-tecnica.html' o está vacío.")
        else:
            logger.info(f"   ✓ guia-tecnica.html verificado ({guia_html.stat().st_size / 1024:.1f} KB)")

        if not red_html.exists() or red_html.stat().st_size == 0:
            errors.append("Falta el archivo 'red-ides.html' o está vacío.")
        else:
            logger.info(f"   ✓ red-ides.html verificado ({red_html.stat().st_size / 1024:.1f} KB)")

        # 2. Catálogo central JSON
        catalog_json = self.data_dir / "catalogo_ide_cit.json"
        if not catalog_json.exists():
            errors.append("Falta el catálogo 'catalogo_ide_cit.json'.")
        else:
            logger.info("   ✓ catalogo_ide_cit.json verificado.")

        # 3. Metadatos ISO 19139 XML
        iso_xml_dir = self.data_dir / "iso_xml"
        xml_files = list(iso_xml_dir.glob("*.xml")) if iso_xml_dir.exists() else []
        if len(xml_files) < 6:
            errors.append(f"Se esperaban al menos 6 fichas XML ISO 19139 para Fase 1, encontradas: {len(xml_files)}.")
        else:
            logger.info(f"   ✓ Fichas XML ISO 19139 verificadas: {len(xml_files)} archivos.")

        # 4. Catálogo STAC
        stac_file = self.data_dir / "stac" / "collection.json"
        if not stac_file.exists():
            errors.append("Falta la colección STAC 'data/stac/collection.json'.")
        else:
            logger.info("   ✓ Colección STAC 1.0.0 verificada.")

        # 5. Activos vectoriales SVG
        for svg_name in ["logo-cit-uai.svg", "logo-ide-standalone.svg", "logo-mbht-white.svg"]:
            svg_path = self.img_dir / svg_name
            if not svg_path.exists():
                errors.append(f"Falta el activo vectorial: {svg_name}")
            else:
                logger.info(f"   ✓ Activo vectorial verificado: {svg_name}")

        success = len(errors) == 0
        if success:
            logger.info("✅ Todos los chequeos pre-vuelo fueron aprobados satisfactoriamente.")
        else:
            logger.error(f"❌ Se encontraron {len(errors)} errores en los chequeos pre-vuelo.")
            for err in errors:
                logger.error(f"   - {err}")

        return success, errors

    def build_release_package(self) -> Dict[str, Any]:
        """
        Empaqueta la versión de producción en la carpeta `dist/` y genera el
        manifiesto de integridad con hashes SHA-256 y políticas de caché HTTP.
        """
        logger.info(f"📦 Construyendo paquete de distribución en: {self.dist_dir}...")
        
        # Limpiar y preparar directorio dist
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(parents=True, exist_ok=True)

        manifest: Dict[str, Any] = {
            "proyecto": "IDE CIT — Infraestructura de Datos Espaciales",
            "institucion": "Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez",
            "version": "2026.1",
            "fecha_empaquetado": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "archivos": [],
            "politicas_cache_s3": {
                "html_json": "max-age=0, no-cache, no-store, must-revalidate",
                "activos_estaticos_svg_png": "public, max-age=31536000, immutable",
                "xml_stac": "public, max-age=86400, must-revalidate"
            }
        }

        # 1. Copiar index.html, descargas-2017.html, guia-tecnica.html, red-ides.html y archivos raíz (sitemap, robots, webmanifest, llms.txt)
        for root_file in ["index.html", "descargas-2017.html", "guia-tecnica.html", "red-ides.html", "sitemap.xml", "robots.txt", "llms.txt", "site.webmanifest"]:
            src = self.ide_dir / root_file
            if src.exists():
                shutil.copy2(src, self.dist_dir / root_file)

        # 2. Copiar carpeta img/
        dist_img = self.dist_dir / "img"
        shutil.copytree(self.img_dir, dist_img, ignore=shutil.ignore_patterns("*.tmp", "*~"))

        # 3. Copiar carpeta data/
        dist_data = self.dist_dir / "data"
        shutil.copytree(self.data_dir, dist_data, ignore=shutil.ignore_patterns("*.tmp", "*~", "reporte_*"))

        # 4. Copiar carpeta download/ con coberturas espaciales abiertas
        download_dir = self.ide_dir / "download"
        if download_dir.exists():
            dist_download = self.dist_dir / "download"
            shutil.copytree(download_dir, dist_download, ignore=shutil.ignore_patterns("*.tmp", "*~", "_temp_*"))
            logger.info("   ✓ Coberturas abiertas en 'download/' copiadas a distribución de producción.")

        # 5. Generar Manifiesto de Archivos y Hashes SHA-256
        total_size_bytes = 0
        file_count = 0

        for path in sorted(self.dist_dir.rglob("*")):
            if path.is_file() and path.name != "manifest.json":
                rel_path = path.relative_to(self.dist_dir).as_posix()
                file_size = path.stat().st_size
                sha256_hash = compute_sha256(path)
                total_size_bytes += file_size
                file_count += 1

                # Determinar política de caché recomendada
                if rel_path.endswith((".html", ".json")) and not rel_path.startswith("data/"):
                    cache_ctrl = manifest["politicas_cache_s3"]["html_json"]
                elif rel_path.endswith((".xml", "collection.json")):
                    cache_ctrl = manifest["politicas_cache_s3"]["xml_stac"]
                else:
                    cache_ctrl = manifest["politicas_cache_s3"]["activos_estaticos_svg_png"]

                manifest["archivos"].append({
                    "ruta": rel_path,
                    "tamano_bytes": file_size,
                    "sha256": sha256_hash,
                    "cache_control": cache_ctrl
                })

        manifest["resumen"] = {
            "total_archivos": file_count,
            "peso_total_kb": round(total_size_bytes / 1024.0, 2),
            "peso_total_mb": round(total_size_bytes / (1024.0 * 1024.0), 3)
        }

        # Guardar manifiesto
        manifest_path = self.dist_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Paquete de producción completado exitosamente:")
        logger.info(f"   📁 Directorio: {self.dist_dir}")
        logger.info(f"   📄 Archivos empaquetados: {file_count}")
        logger.info(f"   📦 Peso total: {manifest['resumen']['peso_total_kb']} KB")
        logger.info(f"   🔒 Manifiesto SHA-256: {manifest_path}")

        return manifest

    def generate_deployment_batch_script(self, bucket_name: str = "ide.cit.uai.cl", region: str = "us-east-1") -> Path:
        """
        Genera el script batch `DESPLEGAR_PORTAL_IDE.bat` para ejecución controlada
        por el administrador de infraestructura cuando se autorice la publicación.
        """
        script_path = self.ide_dir / "DESPLEGAR_PORTAL_IDE.bat"
        
        script_content = f"""@echo off
setlocal enabledelayedexpansion
title CIT-UAI -- Publicador de Produccion IDE CIT
color 0B

echo ==============================================================================
echo   CIT-UAI :: DESPLIEGUE A PRODUCCION IDE CIT
echo   Centro de Inteligencia Territorial - Universidad Adolfo Ibanez
echo ==============================================================================
echo Destino AWS S3: s3://{bucket_name}
echo Region AWS:     {region}
echo.

set /p CONFIRM="Esta seguro de sincronizar y publicar a produccion? (S/N): "
if /i not "!CONFIRM!"=="S" (
    echo Despliegue cancelado por el usuario.
    exit /b 0
)

echo.
echo [1/3] Empaquetando y validando release de produccion...
python "%~dp0desplegador_ide_produccion.py" --build-only
if %ERRORLEVEL% neq 0 (
    echo Error durante el empaquetado. Abortando.
    pause
    exit /b 1
)

echo.
echo [2/3] Sincronizando activos estaticos con AWS S3 (cache inmutable)...
aws s3 sync "%~dp0dist" "s3://{bucket_name}" --delete --region {region} --exclude "*.html" --exclude "manifest.json" --exclude "sitemap.xml" --exclude "robots.txt" --cache-control "public, max-age=31536000, immutable"

echo.
echo [3/3] Sincronizando paginas HTML y manifiesto (sin cache para actualizacion inmediata)...
aws s3 cp "%~dp0dist\\index.html" "s3://{bucket_name}/index.html" --region {region} --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\\descargas-2017.html" "s3://{bucket_name}/descargas-2017.html" --region {region} --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\\guia-tecnica.html" "s3://{bucket_name}/guia-tecnica.html" --region {region} --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\\red-ides.html" "s3://{bucket_name}/red-ides.html" --region {region} --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\\sitemap.xml" "s3://{bucket_name}/sitemap.xml" --region {region} --cache-control "public, max-age=86400, must-revalidate" --content-type "application/xml"
aws s3 cp "%~dp0dist\\robots.txt" "s3://{bucket_name}/robots.txt" --region {region} --cache-control "public, max-age=86400, must-revalidate" --content-type "text/plain"
aws s3 cp "%~dp0dist\\manifest.json" "s3://{bucket_name}/manifest.json" --region {region} --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "application/json"

echo.
echo ==============================================================================
echo   PUBLICACION COMPLETADA CON EXITO
echo   Portal disponible en: https://{bucket_name}
echo ==============================================================================
pause
"""
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        logger.info(f"📜 Script de despliegue controlado generado en: {script_path}")
        return script_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pipeline de empaquetado y preparación de despliegue para IDE CIT."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Modo seguro de simulación y auditoría sin transferencias remotas (default: True).",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Construye el paquete 'dist/' y genera el manifiesto SHA-256 localmente.",
    )
    parser.add_argument(
        "--bucket",
        type=str,
        default="ide.cit.uai.cl",
        help="Nombre del bucket S3 institucional de destino (default: ide.cit.uai.cl).",
    )
    parser.add_argument(
        "--region",
        type=str,
        default="us-east-1",
        help="Región de AWS para el despliegue (default: us-east-1).",
    )

    args = parser.parse_args()

    try:
        deployer = IDEProductionDeployer()
        
        # 1. Preflight
        passed, errors = deployer.preflight_check()
        if not passed:
            logger.error("❌ El chequeo pre-vuelo falló. Corrige los errores antes de continuar.")
            return 1

        # 2. Build local release
        manifest = deployer.build_release_package()

        # 3. Generate controlled deployment batch script
        deployer.generate_deployment_batch_script(bucket_name=args.bucket, region=args.region)

        logger.info("🛡️ Modo Simulación / Dry-Run completado. Paquete local listo en 'dist/'.")
        logger.info("   Ninguna acción remota fue ejecutada conforme a la directiva de seguridad.")
        return 0
    except Exception as e:
        logger.error(f"❌ Error durante el pipeline de empaquetado: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
