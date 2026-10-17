#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — COMPILADOR Y CERTIFICADOR MAESTRO DEL ECOSISTEMA UNIFICADO DE DATOS
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================
"""

import os
import sys
import time
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def main():
    base_dir = Path(__file__).resolve().parent
    print("=" * 80)
    print("🚀 COMPILADOR Y CERTIFICADOR MAESTRO DE LA INFRAESTRUCTURA IDE CIT (CIT-UAI)")
    print("=" * 80)
    
    steps = [
        ("1. Validación y Exportación de Metadatos ISO 19115 / ISO 19139 / XML Schema", "validador_metadatos_iso.py"),
        ("2. Generación de Ejemplos de Conexión Machine-Readable (connection_examples.json)", "generar_connection_examples.py"),
        ("3. Generación de la Ficha Técnica Maestra 17D (ficha-mbht-2017.html)", "generador_ficha_dataset.py"),
        ("4. Generación del Centro de Descargas Territoriales (descargas-2017.html)", "generador_descargas_2017.py"),
        ("5. Generación de la Guía Técnica Metodológica (guia-tecnica.html)", "generador_guia_tecnica.py"),
        ("6. Generación del Directorio de Red de 19 Geoportales SNIT (red-ides.html)", "generador_red_ides.py"),
        ("7. Generación del Portal Principal y Catálogo Abierto (index.html)", "generador_portal_ide_cit.py"),
        ("8. Generación de Catálogo STAC 1.0.0, DCAT-AP y Conectores QGIS / Clean URLs", "generar_recursos_qgis_y_stac.py"),
        ("9. Auditoría Integral de Calidad HTML, Enlaces, Hashes y Accesibilidad", "auditor_calidad_html.py"),
        ("10. Auditoría Adversarial Continua (Higiene de Rutas, Aritmética y Sonda HTTP)", "auditor_adversarial_ide.py")
    ]
    
    t0 = time.time()
    for name, script_name in steps:
        script_path = base_dir / script_name
        print(f"\n[*] Ejecutando: {name}...")
        res = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(base_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode != 0:
            print(f"❌ Error en {script_name}:\n{res.stderr}\n{res.stdout}")
            return 1
        else:
            out = res.stdout or ""
            out_lines = [l for l in out.strip().split("\n") if l.strip()]
            for line in out_lines[-3:]:
                print(f"    {line}")
                
    # Generación automatizada de version.json para auto-detección y bypass de caché
    import json
    build_time = int(time.time())
    version_payload = {
        "build": build_time,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "2026.2",
        "description": "IDE CIT — Infraestructura de Datos Espaciales (CIT-UAI)"
    }
    repo_root = base_dir.parent if base_dir.name == "src" else base_dir
    public_dir = repo_root / "public"
    with open(repo_root / "version.json", "w", encoding="utf-8") as vf:
        json.dump(version_payload, vf, indent=2)
    if public_dir.exists():
        with open(public_dir / "version.json", "w", encoding="utf-8") as vf:
            json.dump(version_payload, vf, indent=2)
    dist_dir = repo_root / "dist"
    if dist_dir.exists():
        with open(dist_dir / "version.json", "w", encoding="utf-8") as vf:
            json.dump(version_payload, vf, indent=2)
    print(f"\n[*] Generado version.json con build ID: {build_time}")

    elapsed = time.time() - t0
    print("\n" + "=" * 80)
    print(f"🎉 CERTIFICACIÓN Y COMPILACIÓN COMPLETA EXITOSA ({elapsed:.2f}s)")
    print("   Fuente Única de Verdad: catalogo_ide_cit.json")
    print("   Cadena Unificada: 100% Validada y Operativa")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
