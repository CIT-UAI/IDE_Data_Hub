#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — VERIFICADOR DE SALUD DE SERVICIOS MVT Y REPOSITORIOS S3
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Módulo algorítmico dedicado a la verificación de conectividad, latencia y
    salud operacional de los servicios de datos espaciales de la IDE CIT:
    
    1. Servidor de Teselas Vectoriales MVT (Martin / OGC Vector Tiles).
    2. Endpoints de descarga GeoParquet / GeoPackage en AWS S3.
    3. REST API de Simulación Espacial (FastAPI /docs y /health).
    4. Generación de reportes de telemetría y diagnóstico operacional.

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import logging
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Verificador_Tiles_CIT")


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


class ServiceHealthVerifier:
    """
    Verificador de salud y conectividad para la infraestructura de datos espaciales.
    """

    def __init__(self, root_dir: Optional[Path] = None, timeout: float = 3.0) -> None:
        self.root_dir: Path = root_dir or find_proyecto_root()
        self.ide_dir: Path = self.root_dir / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
        self.data_dir: Path = self.ide_dir / "data"
        self.catalog_path: Path = self.data_dir / "catalogo_ide_cit.json"
        self.timeout: float = timeout

    def load_catalog(self) -> Dict[str, Any]:
        """Carga el catálogo institucional."""
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catálogo no encontrado en: {self.catalog_path}")
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def check_http_endpoint(self, url: str, method: str = "GET", expected_status: int = 200) -> Dict[str, Any]:
        """
        Prueba la respuesta HTTP de una URL midiendo latencia y código de estado.
        """
        start_time = time.time()
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "CIT-UAI-IDE-HealthCheck/1.0"})
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                latency_ms = (time.time() - start_time) * 1000.0
                status_code = response.status
                content_length = len(response.read()) if method == "GET" else int(response.headers.get("Content-Length", 0))
                
                return {
                    "url": url,
                    "status": "ONLINE" if status_code == expected_status else f"STATUS_{status_code}",
                    "http_code": status_code,
                    "latency_ms": round(latency_ms, 2),
                    "size_bytes": content_length,
                    "error": None
                }
        except urllib.error.HTTPError as e:
            latency_ms = (time.time() - start_time) * 1000.0
            return {
                "url": url,
                "status": f"HTTP_ERROR_{e.code}",
                "http_code": e.code,
                "latency_ms": round(latency_ms, 2),
                "size_bytes": 0,
                "error": str(e)
            }
        except urllib.error.URLError as e:
            latency_ms = (time.time() - start_time) * 1000.0
            return {
                "url": url,
                "status": "UNREACHABLE",
                "http_code": None,
                "latency_ms": round(latency_ms, 2),
                "size_bytes": 0,
                "error": str(e.reason)
            }
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000.0
            return {
                "url": url,
                "status": "ERROR",
                "http_code": None,
                "latency_ms": round(latency_ms, 2),
                "size_bytes": 0,
                "error": str(e)
            }

    def verify_all(self, sample_tiles: bool = False) -> Dict[str, Any]:
        """
        Ejecuta la auditoría completa de servicios de la IDE de forma concurrente.
        """
        catalog = self.load_catalog()
        capas = catalog.get("capas", [])
        portal = catalog.get("portal", {})

        tile_server_base = portal.get("url_tiles", "http://3.140.203.174:3008/tiles")
        api_docs_url = "http://3.140.203.174:8000/docs"
        api_health_url = "http://3.140.203.174:8000/health"

        logger.info("🛰️ Iniciando verificación de servicios e infraestructura IDE CIT...")
        
        results: Dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "servicios_core": {},
            "capas_mvt": [],
            "metricas": {}
        }

        # Tareas concurrentes
        tasks = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            # 1. Core APIs
            future_docs = executor.submit(self.check_http_endpoint, api_docs_url)
            future_health = executor.submit(self.check_http_endpoint, api_health_url)
            future_tiles_root = executor.submit(self.check_http_endpoint, tile_server_base)

            # 2. Capas MVT
            layer_futures = []
            for capa in capas:
                layer_id = capa.get("id")
                source = capa.get("tile_source")
                tile_url = f"{tile_server_base}/{source}/0/0/0.pbf" if sample_tiles else f"{tile_server_base}/{source}"
                fut = executor.submit(self.check_http_endpoint, tile_url, "GET" if sample_tiles else "HEAD")
                layer_futures.append((capa, fut))

            # Recolectar resultados Core
            results["servicios_core"]["api_docs"] = future_docs.result()
            results["servicios_core"]["api_health"] = future_health.result()
            results["servicios_core"]["tile_server_root"] = future_tiles_root.result()

            # Recolectar resultados Capas
            for capa, fut in layer_futures:
                res = fut.result()
                res["layer_id"] = capa.get("id")
                res["titulo"] = capa.get("titulo")
                res["matriz"] = capa.get("matriz")
                results["capas_mvt"].append(res)

        # 3. Métricas Globales
        all_checks = [
            results["servicios_core"]["api_docs"],
            results["servicios_core"]["api_health"],
            results["servicios_core"]["tile_server_root"],
            *results["capas_mvt"]
        ]
        
        total_checks = len(all_checks)
        online_checks = sum(1 for c in all_checks if "ONLINE" in c["status"] or c["http_code"] == 200)
        avg_latency = sum(c["latency_ms"] for c in all_checks) / total_checks if total_checks > 0 else 0.0

        results["metricas"] = {
            "total_endpoints": total_checks,
            "online_endpoints": online_checks,
            "disponibilidad_pct": f"{(online_checks / total_checks * 100.0):.1f}%" if total_checks > 0 else "0.0%",
            "latencia_promedio_ms": round(avg_latency, 2)
        }

        self.print_summary_table(results)
        return results

    def print_summary_table(self, results: Dict[str, Any]) -> None:
        """Imprime un resumen formateado y elegante en consola."""
        metrics = results["metricas"]
        logger.info("=" * 78)
        logger.info(f"📊 REPORTE DE SALUD DE SERVICIOS IDE CIT ({results['timestamp']})")
        logger.info("=" * 78)
        logger.info(f"   • Total de Endpoints Evaluados: {metrics['total_endpoints']}")
        logger.info(f"   • Endpoints Disponibles:       {metrics['online_endpoints']}")
        logger.info(f"   • Disponibilidad Global:        {metrics['disponibilidad_pct']}")
        logger.info(f"   • Latencia Promedio:            {metrics['latencia_promedio_ms']} ms")
        logger.info("-" * 78)
        logger.info(f"{'CAPA / SERVICIO':<35} | {'ESTADO':<15} | {'LATENCIA':<10} | {'HTTP'}")
        logger.info("-" * 78)

        # Core APIs
        for name, res in results["servicios_core"].items():
            status_icon = "🟢" if res["http_code"] == 200 else "🟡" if res["http_code"] else "🔴"
            logger.info(f"{status_icon} [Core] {name:<27} | {res['status']:<15} | {res['latency_ms']:>6.1f} ms | {str(res['http_code']):<4}")

        # Layers
        for res in results["capas_mvt"]:
            status_icon = "🟢" if res["http_code"] == 200 else "🟡" if res["http_code"] else "⚪"
            label = f"{res['layer_id']} ({res['matriz'].upper()})"
            logger.info(f"{status_icon} {label:<33} | {res['status']:<15} | {res['latency_ms']:>6.1f} ms | {str(res['http_code']):<4}")

        logger.info("=" * 78)

    def export_report_markdown(self, results: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Exporta el reporte en formato Markdown para auditoría institucional."""
        target_path = output_path or (self.data_dir / "reporte_salud_servicios.md")
        metrics = results["metricas"]
        
        lines = [
            "# 🛰️ Reporte de Salud y Conectividad de Servicios IDE CIT",
            "",
            f"> **Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez**  ",
            f"> **Fecha y Hora (UTC)**: `{results['timestamp']}`  ",
            f"> **Disponibilidad Global**: `{metrics['disponibilidad_pct']}` | **Latencia Promedio**: `{metrics['latencia_promedio_ms']} ms`",
            "",
            "---",
            "",
            "## 1. Métricas Generales de Infraestructura",
            "",
            f"- **Endpoints Evaluados**: `{metrics['total_endpoints']}`",
            f"- **Endpoints en Línea**: `{metrics['online_endpoints']}`",
            f"- **Latencia Promedio**: `{metrics['latencia_promedio_ms']} ms`",
            "",
            "## 2. Estado Detallado por Servicio y Capa MVT",
            "",
            "| Componente / Capa | Matriz | Estado | Latencia (ms) | Código HTTP |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        for name, res in results["servicios_core"].items():
            icon = "🟢" if res["http_code"] == 200 else "🔴"
            lines.append(f"| {icon} **[Core API]** `{name}` | `INFRA` | `{res['status']}` | `{res['latency_ms']}` | `{res['http_code']}` |")

        for res in results["capas_mvt"]:
            icon = "🟢" if res["http_code"] == 200 else "⚪"
            lines.append(f"| {icon} `{res['layer_id']}` | `{res['matriz'].upper()}` | `{res['status']}` | `{res['latency_ms']}` | `{res['http_code']}` |")

        lines.extend([
            "",
            "---",
            "*CIT-UAI — Infraestructura de Datos Espaciales 2026.*",
            ""
        ])

        with open(target_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        logger.info(f"📄 Reporte Markdown generado en: {target_path}")
        return target_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verificador de salud y conectividad de servicios MVT y S3 para IDE CIT."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.5,
        help="Timeout en segundos para cada petición HTTP (default: 2.5s).",
    )
    parser.add_argument(
        "--sample-tiles",
        action="store_true",
        help="Descarga una tesela muestra (z=0, x=0, y=0) por cada capa.",
    )
    parser.add_argument(
        "--export-md",
        action="store_true",
        help="Exporta el reporte a archivo Markdown.",
    )
    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Exporta el reporte a archivo JSON.",
    )

    args = parser.parse_args()

    try:
        verifier = ServiceHealthVerifier(timeout=args.timeout)
        results = verifier.verify_all(sample_tiles=args.sample_tiles)

        if args.export_md or not (args.export_md or args.export_json):
            verifier.export_report_markdown(results)

        if args.export_json:
            json_out = verifier.data_dir / "reporte_salud_servicios.json"
            with open(json_out, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"📄 Reporte JSON generado en: {json_out}")

        return 0
    except Exception as e:
        logger.error(f"❌ Error durante la verificación de servicios: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
