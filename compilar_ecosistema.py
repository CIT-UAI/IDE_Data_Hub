#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDE CIT — Lanzador de Compilación y Certificación del Ecosistema
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
"""
import sys
import subprocess
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent
    script_path = root_dir / "src" / "compilar_y_certificar_ecosistema_ide.py"
    if not script_path.exists():
        print(f"[-] No se encontró el script de compilación en: {script_path}")
        return 1
    return subprocess.run([sys.executable, str(script_path)], cwd=str(root_dir / "src")).returncode

if __name__ == "__main__":
    sys.exit(main())
