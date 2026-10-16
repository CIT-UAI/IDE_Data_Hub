#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — MONITOR DE APRENDIZAJE ACTIVO Y TELEMETRÍA EN VIVO
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Inspecciona en tiempo real el flujo de consultas ciudadanas, preguntas al
    Copiloto IA, términos buscados, descargas y procedencia de visitantes para
    alimentar el ciclo de auto-entrenamiento continuo del modelo.

Uso:
    python analizar_consultas_y_aprendizaje.py
    o ejecutar VER_PREGUNTAS_Y_TELEMETRIA.bat
===============================================================================
"""

import boto3
import json
import sys
import time
from datetime import datetime, timezone
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

session = boto3.Session(region_name='us-east-1')
s3 = session.client('s3')
BUCKET = 'ide.cit.uai.cl'

def fetch_event(key):
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        return json.loads(obj['Body'].read().decode('utf-8'))
    except:
        return None

def main():
    now = datetime.now(timezone.utc)
    today_prefix = f"telemetry/events/{now.strftime('%Y/%m/%d')}/"
    
    print("=" * 80)
    print("  CIT-UAI · MONITOR DE APRENDIZAJE ACTIVO Y TELEMETRÍA EN TIEMPO REAL")
    print(f"  Fecha: {now.strftime('%d/%m/%Y')} | Bucket: s3://{BUCKET}/{today_prefix}")
    print("=" * 80)

    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=today_prefix):
        for item in page.get('Contents', []):
            keys.append(item['Key'])

    if not keys:
        print(f"\n[*] No hay eventos registrados aún para la fecha {today_prefix}.")
        return

    print(f"[*] Descargando y analizando {len(keys)} eventos de telemetría...")
    events = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = [ex.submit(fetch_event, k) for k in keys]
        for f in as_completed(futures):
            ev = f.result()
            if ev:
                events.append(ev)

    events.sort(key=lambda x: x.get('timestamp', ''))

    copilot_queries = []
    searches = []
    downloads = []
    filter_clicks = Counter()
    ips = Counter()
    devices = Counter()

    for ev in events:
        ip = ev.get('source_ip', 'unknown')
        ua = ev.get('user_agent', 'unknown')
        payload = ev.get('payload', {})
        data = payload.get('data', {})
        evt = payload.get('event', '')
        ts = ev.get('timestamp', '')[11:19]
        
        ips[ip] += 1
        
        # Dispositivo
        if 'iPhone' in ua or 'Android' in ua:
            devices['Móvil (Smartphone)'] += 1
        elif 'Macintosh' in ua:
            devices['Mac (macOS)'] += 1
        elif 'Windows' in ua:
            devices['PC (Windows)'] += 1
        else:
            devices['Otros / Linux'] += 1

        # Preguntas al Copiloto
        if evt == 'copilot_query' or 'query' in data or 'query' in payload:
            q = data.get('query') or payload.get('query')
            if q:
                copilot_queries.append({'ts': ts, 'ip': ip, 'query': q})

        # Búsquedas en catálogo
        if evt == 'search' or 'term' in data or 'term' in payload:
            t = data.get('term') or payload.get('term')
            if t:
                searches.append({'ts': ts, 'ip': ip, 'term': t})

        # Descargas
        if evt == 'download' or 'file' in data or 'file' in payload:
            f = data.get('file') or payload.get('file')
            fmt = data.get('format') or payload.get('format', 'N/D')
            if f:
                downloads.append({'ts': ts, 'ip': ip, 'file': f, 'format': fmt})

        # Filtros aplicados
        if evt == 'filter_click' or 'filter' in data:
            flt = data.get('filter') or payload.get('filter')
            if flt:
                filter_clicks[flt] += 1

    print(f"\n[1] PREGUNTAS REALIZADAS AL COPILOTO IA ({len(copilot_queries)}):")
    if copilot_queries:
        for idx, q in enumerate(copilot_queries, 1):
            print(f"  {idx:2d}. [{q['ts']}] (IP: {q['ip']}) -> \"{q['query']}\"")
    else:
        print("  • Aún no se registran preguntas de texto libre hoy.")

    print(f"\n[2] TÉRMINOS BUSCADOS EN EL CATÁLOGO ({len(searches)}):")
    if searches:
        for s in searches:
            print(f"  • [{s['ts']}] (IP: {s['ip']}) -> \"{s['term']}\"")
    else:
        print("  • No hay términos de búsqueda ingresados en la barra de filtro.")

    print(f"\n[3] DESCARGAS REALIZADAS ({len(downloads)}):")
    if downloads:
        for d in downloads:
            print(f"  • [{d['ts']}] (IP: {d['ip']}) -> {d['file']} ({d['format']})")
    else:
        print("  • No se registran descargas directas de archivos hoy.")

    print(f"\n[4] FILTROS MÁS UTILIZADOS EN EL CATÁLOGO:")
    for flt, cnt in filter_clicks.most_common():
        print(f"  • Ámbito: {flt:<25} ({cnt} clics)")

    print(f"\n[5] DESGLOSE DE VISITANTES (IPs):")
    for ip, cnt in ips.most_common(10):
        print(f"  • IP: {ip:<18} -> {cnt} eventos")

    print(f"\n[6] DISPOSITIVOS:")
    for dev, cnt in devices.most_common():
        print(f"  • {dev:<25} -> {cnt} eventos")

    print("\n" + "=" * 80)
    print("  FIN DEL INFORME DE TELEMETRÍA")
    print("=" * 80)

if __name__ == "__main__":
    main()
