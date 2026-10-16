#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación en vivo de la versión online desplegada en CloudFront.
"""
import urllib.request
import json
import ssl
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "https://ide.cit.uai.cl"

endpoints = [
    ("/", "index.html"),
    ("/inicio", "inicio (clean URL)"),
    ("/descargas-2017.html", "descargas-2017.html"),
    ("/descargas", "descargas (clean URL)"),
    ("/guia-tecnica.html", "guia-tecnica.html"),
    ("/guia-tecnica", "guia-tecnica (clean URL)"),
    ("/red-ides.html", "red-ides.html"),
    ("/red-ides", "red-ides (clean URL)"),
    ("/ficha-mbht-2017.html", "ficha-mbht-2017.html"),
    ("/ficha-mbht-2017", "ficha-mbht-2017 (clean URL)"),
    ("/data/catalogo_ide_cit.json", "catalogo_ide_cit.json"),
    ("/connection_examples.json", "connection_examples.json"),
    ("/stac/catalog.json", "stac/catalog.json"),
    ("/stac/collection.json", "stac/collection.json"),
    ("/metadata.xml", "metadata.xml (ISO 19139 raíz)"),
    ("/download/metadata.xml", "download/metadata.xml"),
    ("/data/iso_xml/kpi_mud_2017_iso19139.xml", "ISO 19139 XML (MBHT 2017)"),
    ("/download/iso_xml/auditoria_conformidad_iso.json", "Auditoría Conformidad ISO JSON"),
    ("/download/qgis/CIT_MBHT_2017_Nacional.qlr", "Conector QGIS .qlr (MBHT 2017)"),
    ("/llms.txt", "llms.txt")
]

print("🔍 VERIFICACIÓN DE LA VERSIÓN ONLINE EN CLOUDFRONT")
print("=" * 60)

for path, label in endpoints:
    url = f"{base_url}{path}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VerificationScript/1.0", "Cache-Control": "no-cache"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="ignore")
            size_kb = len(body) / 1024
            
            fao_count = body.count("FAO")
            sbap_count = body.count("SBAP")
            btn_up = "btnScrollTop" in body
            
            print(f"\n[HTTP {status}] {label} ({size_kb:.1f} KB)")
            print(f"   • Ocurrencias 'FAO': {fao_count}")
            print(f"   • Ocurrencias 'SBAP': {sbap_count}")
            if label.endswith(".html"):
                print(f"   • Botón Scroll to Top (btnScrollTop): {'✓ PRESENTE' if btn_up else '❌ FALTA'}")
                
            if label == "catalogo_ide_cit.json":
                data = json.loads(body)
                pem_layers = [c for c in data.get("capas", []) if c.get("matriz") == "pem"]
                print(f"   • Capas PEM encontradas: {len(pem_layers)}")
                for pl in pem_layers:
                    has_fao = "FAO" in pl.get("titulo", "") or "FAO" in pl.get("resumen", "") or any("FAO" in str(f) for f in pl.get("fuentes_institucionales", []))
                    has_sbap = "SBAP" in pl.get("titulo", "") or "SBAP" in pl.get("resumen", "") or any("SBAP" in str(f) for f in pl.get("fuentes_institucionales", []))
                    print(f"     - {pl['id']}: FAO={'✓' if has_fao else '❌'} | SBAP={'✓' if has_sbap else '❌'}")
                    
            if label in ["red-ides.html", "catalogo_ide_cit.json"]:
                has_miratu = "miratuterritorio.ide.cl" in body
                has_calidad = "calidaddevida.minvu.gob.cl" in body
                has_subpesca = "mapas.subpesca.cl/ideviewer" in body
                print(f"   • Visor Territorial (miratuterritorio.ide.cl): {'✓ OK' if has_miratu else '❌'}")
                print(f"   • Observatorio Urbano (calidaddevida.minvu.gob.cl): {'✓ OK' if has_calidad else '❌'}")
                print(f"   • SUBPESCA (mapas.subpesca.cl/ideviewer): {'✓ OK' if has_subpesca else '❌'}")
                
    except Exception as e:
        print(f"\n[ERROR] {label} ({url}): {e}")

print("\n" + "=" * 60)
print("Verificación finalizada.")
