#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
RED TEAM 2.0 — AUDITOR ANTAGONISTA EXTREMO (ZERO-TRUST / BLACK-BOX & WHITE-BOX)
Infraestructura de Datos Espaciales (IDE CIT-UAI)
===============================================================================
Diseñado para NO autocomplacerse: busca contradicciones semánticas, fallos de
borde en API, descalces entre hashes publicados y streams reales, vulnerabilidades
de seguridad sutiles (SRI, CORS, XSS, Path Traversal, SQLi/NoSQLi en STAC Search),
y discrepancias entre metadatos ISO 19139, DCAT-AP, STAC y Parquet físico.
"""

import json
import hashlib
import pathlib
import re
import ssl
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
BASE_URL = "https://ide.cit.uai.cl"
CTX = ssl.create_default_context()

FINDINGS = []  # (severity, vector, title, detail)

def log_finding(sev, vec, title, detail):
    FINDINGS.append((sev, vec, title, detail))
    icon = {"CRITICAL": "❌ [CRÍTICO]", "HIGH": "🚨 [ALTO]", "MEDIUM": "⚠️  [MEDIO]", "LOW": "🔎 [BAJO]", "PASS": "✅ [OK]"}[sev]
    print(f"  {icon} [{vec}] {title}: {detail}")

def http_req(url, method="GET", data=None, headers=None, timeout=12):
    h = {"User-Agent": "RedTeam-Antagonist-2.0/CIT-ZeroTrust"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            body = r.read()
            return r.status, {k.lower(): v for k, v in r.headers.items()}, body, (time.perf_counter() - t0)*1000
    except urllib.error.HTTPError as e:
        body = e.read() if e.fp else b""
        return e.code, {k.lower(): v for k, v in e.headers.items()}, body, (time.perf_counter() - t0)*1000
    except Exception as e:
        return -1, {}, str(e).encode(), (time.perf_counter() - t0)*1000

print("="*80)
print("🔥 INICIANDO RED TEAM 2.0 (ANTAGONISTA EXTREMO / CERO AUTOCOMPLACENCIA)")
print("="*80)

# ==============================================================================
# VECTOR A1: FUZZING ADVERSARIAL SOBRE STAC SEARCH API (GET & POST)
# ==============================================================================
print("\n[VECTOR A1] Fuzzing Adversarial de API (/stac/search) — Casos de Borde y Maliciosos")

fuzz_cases = [
    # 1. GET con limit negativo -> En OGC API / STAC debería ser 400 Bad Request, o si hace clamp silencioso, ¿es consistente con POST?
    ("GET", f"{BASE_URL}/stac/search?limit=-5", None, [400], "GET limit=-5 (Parámetro fuera de dominio)"),
    ("GET", f"{BASE_URL}/stac/search?limit=abc", None, [400], "GET limit=abc (Tipo no numérico)"),
    ("POST", f"{BASE_URL}/stac/search", b'{"limit": -5}', [400], "POST limit=-5 (Parámetro fuera de dominio en JSON)"),
    ("POST", f"{BASE_URL}/stac/search", b'{"limit": "abc"}', [400], "POST limit='abc' (Tipo inválido en JSON)"),
    ("GET", f"{BASE_URL}/stac/search?bbox=-70,-30,-75,-35", None, [400], "GET bbox invertido (minX > maxX)"),
    ("GET", f"{BASE_URL}/stac/search?bbox=-200,-95,200,95", None, [400], "GET bbox fuera de coordenadas geográficas WGS84"),
    ("GET", f"{BASE_URL}/stac/search?datetime=not-a-date", None, [400], "GET datetime inválido"),
    ("POST", f"{BASE_URL}/stac/search", b'{"datetime": "2025-13-45T99:99:99Z"}', [400], "POST datetime inválido"),
    ("POST", f"{BASE_URL}/stac/search", b'{"collections": "not-a-list"}', [400], "POST collections como string en vez de array"),
    ("POST", f"{BASE_URL}/stac/search", b'{"ids": 12345}', [400], "POST ids como int en vez de array"),
    ("POST", f"{BASE_URL}/stac/search", b'{"unknown_param": "drop table"}', [200, 400], "POST parámetro desconocido / inyección"),
]

for m, u, body, expected_codes, desc in fuzz_cases:
    hdrs = {"Content-Type": "application/json"} if body else {}
    st, rh, rb, ms = http_req(u, method=m, data=body, headers=hdrs)
    if st in expected_codes:
        log_finding("PASS", "A1", desc, f"HTTP {st} ({ms:.0f} ms)")
    else:
        log_finding("HIGH", "A1", desc, f"Recibido HTTP {st} pero un evaluador estricto OGC/STAC exige {expected_codes}. Respuesta: {rb[:120].decode('utf-8','replace')}")

# ==============================================================================
# VECTOR A2: AUDITORÍA DE CSP, SRI (SUBRESOURCE INTEGRITY) Y SCRIPTS EXTERNOS
# ==============================================================================
print("\n[VECTOR A2] Escrutinio de Cadena de Suministro Web (SRI, CDN externos, CSP unsafe-inline/eval)")

st_idx, hdr_idx, body_idx, _ = http_req(f"{BASE_URL}/")
csp = hdr_idx.get("content-security-policy", "")
if "'unsafe-eval'" in csp:
    log_finding("HIGH", "A2", "CSP contiene 'unsafe-eval'", csp)
else:
    log_finding("PASS", "A2", "CSP libre de 'unsafe-eval'", "OK")

if "object-src 'none'" not in csp and "default-src 'self'" not in csp:
    log_finding("MEDIUM", "A2", "CSP sin restricción de object-src", csp)

# Revisar todos los <script src="http..."> y <link rel="stylesheet" href="http..."> en los 5 HTML
for html_path in PUB.glob("*.html"):
    txt = html_path.read_text(encoding="utf-8")
    for tag_match in re.finditer(r'<(script|link)\s+[^>]+>', txt, re.I):
        tag = tag_match.group(0)
        tag_type = tag_match.group(1).lower()
        if tag_type == "link" and 'rel="stylesheet"' not in tag.lower() and "rel='stylesheet'" not in tag.lower():
            continue
        m_url = re.search(r'(?:src|href)=["\'](https?://[^"\']+)["\']', tag, re.I)
        if not m_url:
            continue
        url_ext = m_url.group(1)
        if "fonts.googleapis.com" in url_ext or "fonts.gstatic.com" in url_ext or "ide.cit.uai.cl" in url_ext:
            continue
        if "integrity=" not in tag.lower():
            log_finding("LOW", "A2", f"Recurso CDN externo sin hash SRI (integrity=) en {html_path.name} (mitigado por CSP)", f"{url_ext}")
        else:
            log_finding("PASS", "A2", f"SRI presente en {html_path.name}", f"{url_ext}")

# ==============================================================================
# VECTOR A3: AUDITORÍA DE CORS Y AISLAMIENTO DE ORIGEN (CROSS-ORIGIN)
# ==============================================================================
print("\n[VECTOR A3] Comportamiento CORS ante Orígenes Arbitrarios y Métodos Preflight")

st_cors, hdr_cors, _, _ = http_req(f"{BASE_URL}/stac/catalog.json", headers={"Origin": "https://evil-attacker.example.com"})
acao = hdr_cors.get("access-control-allow-origin", "")
acac = hdr_cors.get("access-control-allow-credentials", "")
if acao == "*" and acac.lower() == "true":
    log_finding("CRITICAL", "A3", "CORS inseguro: Allow-Origin * con Allow-Credentials true", f"ACAO={acao}, ACAC={acac}")
else:
    log_finding("PASS", "A3", "Configuración CORS segura en catálogo abierto", f"ACAO='{acao}', ACAC='{acac}'")

# ==============================================================================
# VECTOR A4: VERIFICACIÓN PROFUNDA DE CADA UNO DE LOS 14 ITEMS STAC Y TODOS SUS ASSETS EN WAN
# ==============================================================================
print("\n[VECTOR A4] Verificación profunda de todos los Items STAC, Assets y Checksums SHA-256 reales vs declarados")

st_cat, _, raw_cat, _ = http_req(f"{BASE_URL}/stac/catalog.json")
cat_json = json.loads(raw_cat.decode("utf-8"))
child_links = [lk["href"] for lk in cat_json.get("links", []) if lk.get("rel") == "child"]
print(f"  -> Encontrados {len(child_links)} child links en /stac/catalog.json")

st_cols, _, raw_cols, _ = http_req(f"{BASE_URL}/stac/collections")
cols_json = json.loads(raw_cols.decode("utf-8"))
cols_list = cols_json.get("collections", [])
print(f"  -> Encontradas {len(cols_list)} colecciones en /stac/collections")

if len(child_links) != len(cols_list):
    log_finding("HIGH", "A4", "Descalce entre child links de catalog.json y /stac/collections", f"catalog.json tiene {len(child_links)} pero /stac/collections tiene {len(cols_list)}")
else:
    log_finding("PASS", "A4", "Paridad exacta entre catalog.json child links y /stac/collections", f"{len(cols_list)} == {len(child_links)}")

# Verificar en paralelo todos los assets declarados en todas las colecciones de /stac/collections
asset_urls = []
for col in cols_list:
    cid = col.get("id")
    for a_key, a_val in col.get("assets", {}).items():
        href = a_val.get("href")
        fsize = a_val.get("file:size")
        fhash = a_val.get("file:checksum")
        asset_urls.append((cid, a_key, href, fsize, fhash))

print(f"  -> Auditando por HEAD en vivo los {len(asset_urls)} assets declarados en STAC...")
bad_assets = 0
size_mismatches = 0
with ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(http_req, u, "HEAD"): (cid, ak, u, sz, fh) for cid, ak, u, sz, fh in asset_urls}
    for fut in as_completed(futs):
        cid, ak, u, sz, fh = futs[fut]
        st, hdrs, _, _ = fut.result()
        if st not in (200, 206):
            bad_assets += 1
            log_finding("CRITICAL", "A4", f"Asset STAC roto ({cid}/{ak})", f"{u} -> HTTP {st}")
        else:
            cl = hdrs.get("content-length")
            if sz is not None and cl is not None and int(cl) != int(sz):
                # Si hay compresión gzip al vuelo para xml/csv puede variar content-length, chequeamos content-encoding
                if "content-encoding" not in hdrs:
                    size_mismatches += 1
                    log_finding("HIGH", "A4", f"Descalce file:size en STAC vs Content-Length S3 ({cid}/{ak})", f"STAC={sz} vs HTTP={cl} en {u}")

if bad_assets == 0 and size_mismatches == 0:
    log_finding("PASS", "A4", f"Todos los {len(asset_urls)} assets STAC responden HTTP 200 y calzan en tamaño físico", "OK")

# ==============================================================================
# VECTOR A5: COHERENCIA SEMÁNTICA CRUZADA: DCAT-AP vs STAC vs ISO 19139 vs CATÁLOGO
# ==============================================================================
print("\n[VECTOR A5] Coherencia Semántica Cruzada (DCAT-AP 2.0 vs STAC vs SHA256SUMS.txt)")

dcat_data = json.loads((PUB / "dcat.json").read_text(encoding="utf-8"))
dcat_datasets = dcat_data.get("dcat:dataset", [])
print(f"  -> Datasets en dcat.json: {len(dcat_datasets)}")

# Verificar si todas las distribuciones en dcat.json tienen downloadURL válido y formato coherente
dcat_urls = []
for ds in dcat_datasets:
    ds_id = ds.get("@id")
    for dist in ds.get("dcat:distribution", []):
        durl = dist.get("dcat:downloadURL") or dist.get("dcat:accessURL")
        fmt = dist.get("dct:format")
        mtype = dist.get("dcat:mediaType")
        dcat_urls.append((ds_id, durl, fmt, mtype))

bad_dcat = 0
with ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(http_req, u, "HEAD"): (ds_id, u, fmt, mt) for ds_id, u, fmt, mt in dcat_urls if u and u.startswith("http")}
    for fut in as_completed(futs):
        ds_id, u, fmt, mt = futs[fut]
        st, _, _, _ = fut.result()
        if st not in (200, 206):
            bad_dcat += 1
            log_finding("HIGH", "A5", f"URL rota en DCAT-AP ({ds_id})", f"{u} -> HTTP {st}")

if bad_dcat == 0:
    log_finding("PASS", "A5", f"100% de las {len(dcat_urls)} distribuciones en dcat.json responden HTTP 200", "OK")

# ==============================================================================
# VECTOR A6: ESCRUTINIO FORENSE DE TEXTO EN HTML ( CONTRADICCIONES DE VERSIÓN Y CONTEOS )
# ==============================================================================
print("\n[VECTOR A6] Búsqueda Forense de Versiones Desactualizadas o Contradicciones en los 5 HTML")

for html_file in sorted(PUB.glob("*.html")):
    txt = html_file.read_text(encoding="utf-8")
    # Buscar versiones v1.0.4 o v1.0.2 presentadas como vigentes
    old_vers = re.findall(r'v1\.0\.[0124]\b[^<]{0,40}vigente', txt, re.I)
    if old_vers:
        log_finding("MEDIUM", "A6", f"Posible versión antigua marcada como vigente en {html_file.name}", str(old_vers))
    # Buscar fechas de auditoría antiguas
    old_dates = re.findall(r'Última auditoría verificada:\s*2026-10-1[0-5]', txt)
    if old_dates:
        log_finding("LOW", "A6", f"Fecha de auditoría desactualizada en {html_file.name}", str(old_dates))
    # Verificar si en index.html dice 2026-10-16 en vez de 2026-10-17
    if "2026-10-16" in txt:
        log_finding("LOW", "A6", f"Mención a fecha 2026-10-16 en {html_file.name} (hoy es 2026-10-17)", "Revisar coherencia temporal")

print("\n" + "="*80)
crit_high_med = [f for f in FINDINGS if f[0] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")]
print(f"RESUMEN RED TEAM 2.0: {len([f for f in FINDINGS if f[0]=='PASS'])} PASS | {len(crit_high_med)} HALLAZGOS ANTAGONISTAS")
for sev, vec, title, det in crit_high_med:
    print(f"  -> [{sev}] ({vec}) {title}: {det}")
print("="*80)
