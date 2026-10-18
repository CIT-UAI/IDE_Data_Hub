#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDE CIT — Test de Independencia Real del CDN (CloudFront Alternate Domain)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez

Criterio de Cierre (Prioridad 1):
Una prueba automatizada debe recorrer todo el catálogo utilizando exclusivamente
el dominio alternativo (d1owm1ug2fpvep.cloudfront.net), sin depender de solicitudes
a cit.uai.cl.
"""

from urllib.parse import urljoin, urlparse
import urllib.request
import argparse
import json
import ssl
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_BASE = "https://d1owm1ug2fpvep.cloudfront.net"

def main():
    parser = argparse.ArgumentParser(description="Test de Independencia Real del CDN para IDE CIT")
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="Dominio base a testear (por defecto CloudFront)")
    parser.add_argument("--verbose", action="store_true", help="Imprimir detalle de cada URL")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    base_domain = urlparse(base_url).netloc
    
    print("=" * 80)
    print("🧪 TEST DE INDEPENDENCIA REAL DEL CDN (CLOUDFRONT / DOMINIO ALTERNATIVO)")
    print(f"   Dominio Base a Evaluar: {base_url} ({base_domain})")
    print("   Objetivo: CERO dependencia y CERO llamadas cruzadas a cit.uai.cl")
    print("=" * 80)

    ctx = ssl.create_default_context()
    visited_urls = set()
    cross_origin_violations = []
    failed_requests = []
    tested_count = 0

    def check_url(target_url, expected_code=200, is_range=False):
        nonlocal tested_count
        if target_url in visited_urls:
            return True
        visited_urls.add(target_url)
        tested_count += 1

        parsed = urlparse(target_url)
        # Ignorar recursos de terceras partes expresamente externos (licencias Creative Commons, esquemas STAC, plataformas hermanas externas)
        if parsed.netloc in ["creativecommons.org", "stac-extensions.github.io", "api.stacspec.org", "www.opengis.net", "matrizbht.cl", "censo2024.ine.gob.cl"]:
            if args.verbose:
                print(f"  [EXTERNO] {target_url}")
            return True

        # Verificar independencia: no debe apuntar a cit.uai.cl ni uai.cl
        if "cit.uai.cl" in parsed.netloc or (parsed.netloc.endswith("uai.cl") and parsed.netloc != base_domain):
            cross_origin_violations.append({
                "url": target_url,
                "reason": f"Violación de independencia: apunta a dominio primario ({parsed.netloc}) en vez de ({base_domain})"
            })
            print(f"  ❌ VIOLACIÓN CDN: {target_url}")
            return False

        # Comprobar que resuelve estrictamente en el dominio base
        if parsed.netloc != base_domain:
            cross_origin_violations.append({
                "url": target_url,
                "reason": f"Dominio inesperado: {parsed.netloc} != {base_domain}"
            })
            print(f"  ❌ DOMINIO INESPERADO: {target_url}")
            return False

        headers = {'User-Agent': 'CDN-Independence-Tester/1.0'}
        if is_range:
            headers['Range'] = 'bytes=0-4095'

        try:
            req = urllib.request.Request(target_url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                code = resp.status
                if is_range and code == 206:
                    if args.verbose:
                        print(f"  ✅ 206 (Range OK) | {target_url}")
                    return True
                elif code == expected_code:
                    if args.verbose:
                        print(f"  ✅ {code} OK | {target_url}")
                    return True
                else:
                    failed_requests.append({"url": target_url, "code": code})
                    print(f"  ⚠️ Código inesperado: {code} en {target_url}")
                    return False
        except Exception as e:
            failed_requests.append({"url": target_url, "error": str(e)})
            print(f"  ❌ Error HTTP en {target_url}: {e}")
            return False

    t0 = time.time()

    # 1. Probar Catálogo Raíz STAC
    catalog_url = f"{base_url}/stac/catalog.json"
    print("\n[*] 1. Validando Catálogo Raíz STAC 1.0.0...")
    req = urllib.request.Request(catalog_url, headers={'User-Agent': 'CDN-Independence-Tester/1.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        cat_data = json.loads(r.read().decode('utf-8'))
    
    # Evaluar enlaces del catálogo raíz
    for lk in cat_data.get("links", []):
        href = lk.get("href", "")
        resolved = urljoin(catalog_url, href)
        check_url(resolved)

    # 2. Probar Colecciones Hijas STAC
    child_links = [lk for lk in cat_data.get("links", []) if lk.get("rel") == "child"]
    print(f"\n[*] 2. Validando {len(child_links)} Colecciones STAC hijas...")
    
    for cl in child_links:
        col_url = urljoin(catalog_url, cl.get("href", ""))
        if not check_url(col_url):
            continue
        try:
            req = urllib.request.Request(col_url, headers={'User-Agent': 'CDN-Independence-Tester/1.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                col_data = json.loads(r.read().decode('utf-8'))
            
            # Validar enlaces de la colección
            for clink in col_data.get("links", []):
                chref = clink.get("href", "")
                check_url(urljoin(col_url, chref))

            # Validar activos de la colección (GeoParquet, GPKG, SHP, CSV, ISO XML)
            for akey, asset in col_data.get("assets", {}).items():
                ahref = asset.get("href", "")
                resolved_asset = urljoin(col_url, ahref)
                # Para parquet, probar lectura eficiente HTTP Range
                is_pqt = ahref.endswith(".parquet")
                check_url(resolved_asset, is_range=is_pqt)
        except Exception as e:
            failed_requests.append({"url": col_url, "error": f"Error parseando colección: {e}"})

    # 3. Probar Endpoints STAC API
    print("\n[*] 3. Validando Endpoints STAC API (/collections, /conformance, /search)...")
    check_url(f"{base_url}/stac/collections")
    check_url(f"{base_url}/stac/collections/")
    check_url(f"{base_url}/stac/conformance")
    check_url(f"{base_url}/stac/conformance/")
    check_url(f"{base_url}/stac/search")
    check_url(f"{base_url}/stac/search/")
    check_url(f"{base_url}/stac/search?limit=5")

    # 4. Probar Catálogo Semántico W3C DCAT-AP
    print("\n[*] 4. Validando Catálogo Semántico W3C DCAT-AP 2.0.1 (/dcat.json)...")
    dcat_url = f"{base_url}/dcat.json"
    if check_url(dcat_url):
        try:
            req = urllib.request.Request(dcat_url, headers={'User-Agent': 'CDN-Independence-Tester/1.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                dcat_data = json.loads(r.read().decode('utf-8'))
            for ds in dcat_data.get("dcat:dataset", []):
                for dist in ds.get("dcat:distribution", []):
                    acc_url = dist.get("dcat:accessURL") or dist.get("dcat:downloadURL", "")
                    if acc_url:
                        check_url(urljoin(dcat_url, acc_url), is_range=acc_url.endswith(".parquet"))
        except Exception as e:
            failed_requests.append({"url": dcat_url, "error": f"Error parseando DCAT: {e}"})

    # 5. Probar Páginas HTML y Recursos Clave
    print("\n[*] 5. Validando Páginas y Recursos Documentales...")
    for doc in ["/guia-tecnica", "/ficha-mbht-2017", "/descargas", "/red-ides", "/conformance_report.json"]:
        check_url(f"{base_url}{doc}")

    elapsed = time.time() - t0

    print("\n" + "=" * 80)
    print("📊 RESULTADOS DE LA AUDITORÍA DE INDEPENDENCIA CDN")
    print(f"   URLs Auditadas: {tested_count}")
    print(f"   Violaciones de Dependencia Cross-Origin: {len(cross_origin_violations)}")
    print(f"   Peticiones Fallidas (Errores HTTP): {len(failed_requests)}")
    print(f"   Tiempo Total de Evaluación: {elapsed:.2f} s")
    print("=" * 80)

    if cross_origin_violations:
        print("\n❌ SE ENCONTRARON VIOLACIONES DE INDEPENDENCIA CDN:")
        for v in cross_origin_violations:
            print(f"   - {v['url']}: {v['reason']}")

    if failed_requests:
        print("\n❌ SE ENCONTRARON PETICIONES FALLIDAS:")
        for fr in failed_requests:
            print(f"   - {fr}")

    if not cross_origin_violations and not failed_requests:
        print("\n🏆 CERTIFICACIÓN EXITOSA: 100% INDEPENDENCIA CDN VERIFICADA.")
        print(f"   Todos los recursos se consumen de manera autónoma desde: {base_domain}")
        print("   CERO solicitudes dirigidas o dependientes de cit.uai.cl.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
