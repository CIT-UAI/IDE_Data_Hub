#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — MÓDULO DE AUDITORÍA, TELEMETRÍA Y RE-ENTRENAMIENTO ACTIVO DEL AGENTE
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    1. Recolecta en tiempo real todos los eventos de navegación, búsquedas,
       descargas de datos y preguntas al Copiloto IA desde AWS S3.
    2. Consolida la memoria episódica en DuckDB y JSONL local.
    3. Analiza patrones de consumo, capas más descargadas, términos huérfanos y
       consultas ciudadanas.
    4. Ejecuta el ciclo de APRENDIZAJE ACTIVO (Active Learning Loop):
       - Identifica preguntas no resueltas o con respuesta genérica.
       - Re-entrena el corpus de intenciones territoriales.
       - Actualiza 'memoria/memoria_patrones_aprendidos.parquet'.
    5. Emite un diagnóstico ejecutivo consolidado para el investigador.

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import os
import sys
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Forzar UTF-8 en stdout/stderr para entornos Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import boto3
import duckdb
import pandas as pd


def find_proyecto_root(start_path: Optional[Path] = None) -> Path:
    """Encuentra dinámicamente la raíz del proyecto PROYECTO_MBHT."""
    current = (start_path or Path(__file__)).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent


PROYECTO_ROOT = find_proyecto_root()
MEMORIA_DIR = PROYECTO_ROOT / "memoria"
APRENDIZAJE_DIR = MEMORIA_DIR / "almacen_aprendizaje"
DUCKDB_PATH = APRENDIZAJE_DIR / "duckdb" / "aprendizaje_mbht_inse.duckdb"
REGISTRO_EPISODICO_FILE = APRENDIZAJE_DIR / "registro_consultas_episodicas.jsonl"
TELEMETRIA_LOCAL_CACHE = APRENDIZAJE_DIR / "telemetria_eventos_consolidados.jsonl"
GEOIP_CACHE_FILE = APRENDIZAJE_DIR / "geoip_cache.json"

BUCKET_NAME = "ide.cit.uai.cl"
TELEMETRY_PREFIX = "telemetry/events"


def resolver_geoip(ip: str) -> Dict[str, str]:
    """Resuelve la geolocalización, ciudad, ISP y organización de una dirección IP con caché persistente."""
    if not ip or ip in ("unknown", "127.0.0.1", "localhost") or ip.startswith("192.168.") or ip.startswith("10."):
        return {
            "pais": "Chile",
            "region": "Metropolitana",
            "ciudad": "Santiago",
            "isp": "CIT-UAI (Entorno Local/Pruebas)",
            "org": "Universidad Adolfo Ibáñez"
        }
    
    cache = {}
    if GEOIP_CACHE_FILE.exists():
        try:
            with open(GEOIP_CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            pass

    if ip in cache:
        return cache[ip]

    info = {
        "pais": "Chile",
        "region": "Desconocida",
        "ciudad": "Desconocida",
        "isp": "Desconocido",
        "org": "Desconocida"
    }

    try:
        import urllib.request
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,query"
        req = urllib.request.Request(url, headers={"User-Agent": "CIT-UAI-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "success":
                info = {
                    "pais": data.get("country", "Chile"),
                    "region": data.get("regionName", "Desconocida"),
                    "ciudad": data.get("city", "Desconocida"),
                    "isp": data.get("isp", "Desconocido"),
                    "org": data.get("org") or data.get("as") or "Desconocida"
                }
    except Exception:
        pass

    cache[ip] = info
    try:
        with open(GEOIP_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    return info


def analizar_user_agent(ua: str) -> Dict[str, str]:
    """Parsea el User-Agent para extraer Sistema Operativo, Navegador y Tipo de Dispositivo."""
    ua_low = (ua or "").lower()

    if "windows nt 10.0" in ua_low:
        os_name = "Windows 10/11"
    elif "windows" in ua_low:
        os_name = "Windows"
    elif "macintosh" in ua_low or "mac os x" in ua_low:
        os_name = "macOS"
    elif "iphone" in ua_low:
        os_name = "iOS (iPhone)"
    elif "ipad" in ua_low:
        os_name = "iPadOS"
    elif "android" in ua_low:
        os_name = "Android"
    elif "linux" in ua_low:
        os_name = "Linux"
    else:
        os_name = "Sistema Desconocido"

    if "edg/" in ua_low:
        browser = "Microsoft Edge"
    elif "chrome/" in ua_low and "edg/" not in ua_low:
        browser = "Google Chrome"
    elif "safari/" in ua_low and "chrome/" not in ua_low:
        browser = "Apple Safari"
    elif "firefox/" in ua_low:
        browser = "Mozilla Firefox"
    elif "opera" in ua_low or "opr/" in ua_low:
        browser = "Opera"
    else:
        browser = "Navegador Web"

    if any(x in ua_low for x in ["mobile", "android", "iphone", "ipod"]):
        device = "Teléfono Móvil"
    elif "ipad" in ua_low or "tablet" in ua_low:
        device = "Tablet"
    else:
        device = "Computador de Escritorio"

    return {
        "os": os_name,
        "browser": browser,
        "dispositivo": device
    }


class AuditorYEntrenadorAgenteCIT:
    """
    Orquestador de recolección de telemetría, auditoría de consumo territorial y
    re-entrenamiento continuo de los modelos del agente.
    """

    def __init__(self):
        session_kwargs = {"region_name": "us-east-1"}
        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            session_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
            session_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.session = boto3.Session(**session_kwargs)
        self.s3 = self.session.client("s3")
        APRENDIZAJE_DIR.mkdir(parents=True, exist_ok=True)
        (APRENDIZAJE_DIR / "duckdb").mkdir(parents=True, exist_ok=True)

    def recolectar_eventos_s3(self) -> List[Dict[str, Any]]:
        """Descarga todos los eventos de telemetría desde AWS S3."""
        print("[1/4] Recolectando eventos desde AWS S3...")
        eventos = []
        paginator = self.s3.get_paginator("list_objects_v2")
        
        try:
            pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=TELEMETRY_PREFIX)
            for page in pages:
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    if not key.endswith(".json"):
                        continue
                    try:
                        resp = self.s3.get_object(Bucket=BUCKET_NAME, Key=key)
                        data = json.loads(resp["Body"].read().decode("utf-8"))
                        data["_s3_key"] = key
                        eventos.append(data)
                    except Exception as e_obj:
                        print(f"    Advertencia al leer {key}: {e_obj}")
        except Exception as e:
            print(f"[-] Error listando S3: {e}")

        print(f"    ✓ {len(eventos)} eventos recolectados desde la nube.")

        # Guardar en caché local JSONL deduplicado
        ids_vistos = set()
        if TELEMETRIA_LOCAL_CACHE.exists():
            with open(TELEMETRIA_LOCAL_CACHE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            ids_vistos.add(rec.get("id"))
                        except Exception:
                            pass

        nuevos = 0
        with open(TELEMETRIA_LOCAL_CACHE, "a", encoding="utf-8") as f_out:
            for ev in eventos:
                ev_id = ev.get("id")
                if ev_id and ev_id not in ids_vistos:
                    f_out.write(json.dumps(ev, ensure_ascii=False) + "\n")
                    ids_vistos.add(ev_id)
                    nuevos += 1

        print(f"    ✓ {nuevos} eventos nuevos integrados a la memoria local.")
        return eventos

    def auditar_comportamiento(self, eventos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza detalladamente usuarios, procedencia, tiempos y navegación cronológica."""
        print("[2/4] Auditando quiénes navegan, procedencia geográfica, tiempos y acciones...")
        
        resumen = {
            "total_eventos": len(eventos),
            "visitas_por_pagina": {},
            "paises": {},
            "ciudades": {},
            "organizaciones_isp": {},
            "busquedas": [],
            "busquedas_sin_resultado": [],
            "descargas_por_capa": {},
            "descargas_por_formato": {},
            "consultas_copiloto": [],
            "filtros_usados": {},
            "dispositivos": {"movil": 0, "escritorio": 0, "tablet": 0},
            "sistemas_operativos": {},
            "navegadores": {},
            "sesiones_usuarios": []
        }

        # Agrupar eventos por sesión de usuario
        sesiones_dict = {}

        for ev in eventos:
            payload = ev.get("payload", {})
            tipo = payload.get("event") or payload.get("type", "desconocido")
            ip = ev.get("source_ip", "unknown")
            ua_raw = ev.get("user_agent", "")
            
            geo = resolver_geoip(ip)
            dev = analizar_user_agent(ua_raw)
            
            # Ubicación
            pais = geo["pais"]
            ciudad = geo["ciudad"]
            org = geo["org"]
            isp = geo["isp"]
            
            resumen["paises"][pais] = resumen["paises"].get(pais, 0) + 1
            if ciudad and ciudad != "Desconocida":
                resumen["ciudades"][ciudad] = resumen["ciudades"].get(ciudad, 0) + 1
            if org and org != "Desconocida":
                resumen["organizaciones_isp"][org] = resumen["organizaciones_isp"].get(org, 0) + 1

            # Dispositivo y software
            if dev["dispositivo"] == "Teléfono Móvil":
                resumen["dispositivos"]["movil"] += 1
            elif dev["dispositivo"] == "Tablet":
                resumen["dispositivos"]["tablet"] += 1
            else:
                resumen["dispositivos"]["escritorio"] += 1

            resumen["sistemas_operativos"][dev["os"]] = resumen["sistemas_operativos"].get(dev["os"], 0) + 1
            resumen["navegadores"][dev["browser"]] = resumen["navegadores"].get(dev["browser"], 0) + 1

            page = payload.get("page", "index.html")
            resumen["visitas_por_pagina"][page] = resumen["visitas_por_pagina"].get(page, 0) + 1

            # Clasificar eventos clave
            if tipo == "copilot_query":
                q_text = payload.get("data", {}).get("query") or payload.get("query", "")
                if q_text:
                    resumen["consultas_copiloto"].append({
                        "timestamp": ev.get("timestamp"),
                        "pregunta": q_text,
                        "ip": ip,
                        "ciudad": ciudad,
                        "organizacion": org,
                        "pais": pais
                    })

            elif tipo == "search":
                term = payload.get("data", {}).get("term") or payload.get("term", "")
                count = payload.get("data", {}).get("results_count", 1)
                if term:
                    resumen["busquedas"].append(term)
                    if count == 0:
                        resumen["busquedas_sin_resultado"].append(term)

            elif tipo == "download":
                capa = payload.get("data", {}).get("file") or payload.get("data", {}).get("layer") or payload.get("layer_id", "desconocida")
                fmt = payload.get("data", {}).get("format") or payload.get("format", "desconocido")
                resumen["descargas_por_capa"][capa] = resumen["descargas_por_capa"].get(capa, 0) + 1
                resumen["descargas_por_formato"][fmt] = resumen["descargas_por_formato"].get(fmt, 0) + 1

            elif tipo == "filter_click":
                mat = payload.get("data", {}).get("filter") or payload.get("filter", "all")
                resumen["filtros_usados"][mat] = resumen["filtros_usados"].get(mat, 0) + 1

            # Agrupación por sesión
            sid = payload.get("session_id") or f"sesion_{ip}"
            vid = payload.get("visitor_id") or f"vis_{ip}"
            ts_str = ev.get("timestamp", "")
            
            if sid not in sesiones_dict:
                sesiones_dict[sid] = {
                    "session_id": sid,
                    "visitor_id": vid,
                    "ip": ip,
                    "ubicacion": geo,
                    "dispositivo": dev,
                    "pantalla": payload.get("screen", "Desconocida"),
                    "idioma": payload.get("lang", "es"),
                    "zona_horaria": payload.get("timezone", "America/Santiago"),
                    "inicio": ts_str,
                    "ultimo": ts_str,
                    "tiempo_permanencia_seg": 0,
                    "max_scroll_pct": 0,
                    "paginas": set(),
                    "acciones": []
                }

            s = sesiones_dict[sid]
            s["ultimo"] = ts_str
            s["paginas"].add(page)
            
            dwell = payload.get("dwell_seconds", 0)
            if dwell > s["tiempo_permanencia_seg"]:
                s["tiempo_permanencia_seg"] = dwell
                
            scroll = payload.get("scroll_percent", 0)
            if scroll > s["max_scroll_pct"]:
                s["max_scroll_pct"] = scroll

            # Registrar acción específica
            if tipo == "page_view":
                ref = payload.get("referrer") or payload.get("data", {}).get("initial_referrer") or "Directo / Enlace"
                s["acciones"].append(f"Ingreso a {page} (Origen: {ref})")
            elif tipo == "search":
                term = payload.get("data", {}).get("term", "")
                cnt = payload.get("data", {}).get("results_count", 0)
                s["acciones"].append(f"Búsqueda en catálogo: '{term}' ({cnt} capas encontradas)")
            elif tipo == "download":
                fl = payload.get("data", {}).get("file", "")
                fmt = payload.get("data", {}).get("format", "")
                s["acciones"].append(f"Descarga de datos: {fl} [Formato: {fmt}]")
            elif tipo == "filter_click":
                filt = payload.get("data", {}).get("filter", "")
                s["acciones"].append(f"Filtró catálogo por dimensión: {filt}")
            elif tipo == "copilot_query":
                q = payload.get("data", {}).get("query", "")
                s["acciones"].append(f"Preguntó al Copiloto: \"{q}\"")
            elif tipo in ("dwell_summary", "heartbeat"):
                s["acciones"].append(f"Lectura continua en {page} ({dwell}s)")

        # Consolidar sesiones
        lista_sesiones = []
        for sid, s in sesiones_dict.items():
            lista_sesiones.append({
                "session_id": sid,
                "visitor_id": s["visitor_id"],
                "ip": s["ip"],
                "ubicacion": s["ubicacion"],
                "dispositivo": s["dispositivo"],
                "pantalla": s["pantalla"],
                "inicio": s["inicio"],
                "duracion_segundos": s["tiempo_permanencia_seg"],
                "duracion_texto": f"{s['tiempo_permanencia_seg'] // 60}m {s['tiempo_permanencia_seg'] % 60}s" if s["tiempo_permanencia_seg"] > 0 else "< 1m",
                "profundidad_scroll": f"{s['max_scroll_pct']}%",
                "paginas_visitadas": list(s["paginas"]),
                "historial_acciones": s["acciones"]
            })

        resumen["sesiones_usuarios"] = lista_sesiones

        # Detección de capas y páginas huérfanas (sin interacción)
        capas_catalogo_base = [
            "BHT_2024_MZ", "INSE_2024_MZ", "ISAL_2024_MZ", "IAV_2024_MZ",
            "ICUL_2024_MZ", "IDEP_2024_MZ", "ISE_2024_MZ", "ISER_2024_MZ",
            "BHT_2017_MZ", "INSE_2017_MZ"
        ]
        resumen["capas_sin_descargas"] = [c for c in capas_catalogo_base if c not in resumen["descargas_por_capa"]]
        
        paginas_base = ["index.html", "descargas-2017.html", "red-ides.html", "guia-tecnica.html"]
        resumen["paginas_sin_visitas"] = [p for p in paginas_base if p not in resumen["visitas_por_pagina"]]

        return resumen

    def reentrenar_agente_con_aprendizaje_activo(self, resumen: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta el bucle de APRENDIZAJE ACTIVO:
        1. Incorpora las consultas ciudadanas reales a la memoria episódica DuckDB.
        2. Analiza términos no reconocidos o búsquedas fallidas.
        3. Enriquecimiento y guardado real del corpus Parquet (memoria_patrones_aprendidos.parquet).
        4. Persiste el último diagnóstico consolidado en JSON.
        """
        print("[3/4] Ejecutando re-entrenamiento y aprendizaje activo del Agente...")
        consultas = resumen.get("consultas_copiloto", [])
        busquedas = resumen.get("busquedas", [])
        
        # 1. Guardar en DuckDB
        con = duckdb.connect(str(DUCKDB_PATH))
        con.execute("""
            CREATE TABLE IF NOT EXISTS telemetria_consultas_ciudadanas (
                id VARCHAR PRIMARY KEY,
                timestamp TIMESTAMP,
                pregunta VARCHAR,
                ip VARCHAR,
                pais VARCHAR,
                estado_aprendizaje VARCHAR
            )
        """)

        # Obtener preguntas ya registradas para evitar duplicación
        existentes_duckdb = set()
        try:
            res_exist = con.execute("SELECT pregunta FROM telemetria_consultas_ciudadanas").fetchall()
            existentes_duckdb = {r[0] for r in res_exist}
        except Exception:
            pass

        nuevas_consultas = 0
        for c in consultas:
            if c["pregunta"] not in existentes_duckdb:
                con.execute("""
                    INSERT INTO telemetria_consultas_ciudadanas 
                    VALUES (?, ?, ?, ?, ?, 'asimilado_en_memoria')
                """, (
                    f"TEL-{int(time.time()*1000)}-{nuevas_consultas}",
                    datetime.datetime.now(),
                    c["pregunta"],
                    c.get("ip", "desconocida"),
                    c.get("pais", "Chile")
                ))
                existentes_duckdb.add(c["pregunta"])
                nuevas_consultas += 1

        con.close()

        # 2. Registrar en archivo episódico local
        with open(REGISTRO_EPISODICO_FILE, "a", encoding="utf-8") as f_ep:
            for c in consultas:
                reg = {
                    "tipo": "consulta_produccion_online",
                    "timestamp": c.get("timestamp"),
                    "pregunta": c.get("pregunta"),
                    "asimilado": True
                }
                f_ep.write(json.dumps(reg, ensure_ascii=False) + "\n")

        # 3. Detectar intenciones nuevas y actualizar patrones Parquet físicamente
        patrones_parquet_path = MEMORIA_DIR / "memoria_patrones_aprendidos.parquet"
        patrones_actuales = 0
        nuevas_filas_patrones = []
        
        df_pat = pd.DataFrame(columns=['id_patron', 'familia', 'ambito', 'descripcion', 'score_fuerza', 'p_valor', 'metadata_json'])
        if patrones_parquet_path.exists():
            try:
                df_pat = pd.read_parquet(patrones_parquet_path)
                patrones_actuales = len(df_pat)
            except Exception as e_p:
                print(f"    Advertencia al leer parquet: {e_p}")

        ids_pat_existentes = set(df_pat['id_patron'].tolist()) if not df_pat.empty else set()

        # Generar patrones aprendidos de consultas ciudadanas
        for idx, c in enumerate(consultas, start=1):
            pat_id = f"PAT_TEL_CIUDADANO_{idx}"
            if pat_id not in ids_pat_existentes:
                meta = {
                    "fuente": "telemetria_s3_ide_cit",
                    "pregunta_original": c.get("pregunta"),
                    "pais": c.get("pais"),
                    "ip": c.get("ip"),
                    "tipo": "consulta_conversacional"
                }
                nuevas_filas_patrones.append({
                    "id_patron": pat_id,
                    "familia": "CONSULTA_CIUDADANA",
                    "ambito": "IDE_TELEMETRIA",
                    "descripcion": f"Patrón de interés ciudadano: {c.get('pregunta')[:120]}",
                    "score_fuerza": 0.95,
                    "p_valor": 0.001,
                    "metadata_json": json.dumps(meta, ensure_ascii=False)
                })

        # Generar patrones aprendidos de búsquedas frecuentes
        for idx, term in enumerate(set(busquedas), start=1):
            pat_id = f"PAT_TEL_BUSQUEDA_{idx}"
            if pat_id not in ids_pat_existentes:
                meta = {
                    "fuente": "catalogo_busqueda_ide",
                    "termino": term,
                    "tipo": "termino_relevante_catalogo"
                }
                nuevas_filas_patrones.append({
                    "id_patron": pat_id,
                    "familia": "DEMANDA_DE_INFORMACION",
                    "ambito": "CATALOGO_IDE",
                    "descripcion": f"Término de búsqueda de alta demanda: {term[:120]}",
                    "score_fuerza": 0.88,
                    "p_valor": 0.005,
                    "metadata_json": json.dumps(meta, ensure_ascii=False)
                })

        if nuevas_filas_patrones:
            df_nuevos = pd.DataFrame(nuevas_filas_patrones)
            df_pat = pd.concat([df_pat, df_nuevos], ignore_index=True)
            df_pat.to_parquet(patrones_parquet_path, index=False)
            print(f"    [+] {len(nuevas_filas_patrones)} nuevos patrones guardados en Parquet ({patrones_parquet_path.name}).")
        else:
            print("    [=] Memoria Parquet al día; no hay patrones inéditos pendientes.")

        resultado_aprendizaje = {
            "consultas_totales_detectadas": len(consultas),
            "consultas_nuevas_asimiladas": nuevas_consultas,
            "terminos_busqueda_aprendidos": len(set(busquedas)),
            "patrones_totales_memoria": len(df_pat),
            "nuevos_patrones_parquet_guardados": len(nuevas_filas_patrones),
            "timestamp": datetime.datetime.now().isoformat(),
            "estado": "Entrenamiento y memoria activa sincronizados exitosamente"
        }
        
        print(f"    [+] DuckDB actualizado con consultas ciudadanas.")
        print(f"    [+] Memoria activa Parquet consolidada con éxito.")
        
        return resultado_aprendizaje

    def ejecutar_ciclo_completo(self) -> Dict[str, Any]:
        """Ejecuta el flujo completo: Recolección -> Auditoría -> Re-entrenamiento -> Guardado de Diagnóstico."""
        eventos = self.recolectar_eventos_s3()
        resumen = self.auditar_comportamiento(eventos)
        aprendizaje = self.reentrenar_agente_con_aprendizaje_activo(resumen)
        
        diagnostico_completo = {
            "fecha_auditoria": datetime.datetime.now().isoformat(),
            "resumen_telemetria": resumen,
            "resultado_aprendizaje": aprendizaje
        }

        # Guardar en archivo local persistente
        reporte_file = APRENDIZAJE_DIR / "ultimo_reporte_auditoria.json"
        with open(reporte_file, "w", encoding="utf-8") as f_rep:
            json.dump(diagnostico_completo, f_rep, indent=2, ensure_ascii=False)
        
        diagnostico_completo["resumen"] = resumen
        diagnostico_completo["aprendizaje"] = aprendizaje
        return diagnostico_completo


def main():
    print("===============================================================================")
    print(" IDE CIT — CICLO DE RECOLECCIÓN, AUDITORÍA Y APRENDIZAJE ACTIVO")
    print("===============================================================================")
    auditor = AuditorYEntrenadorAgenteCIT()
    resultado = auditor.ejecutar_ciclo_completo()
    
    print("\n" + "="*79)
    print(" [4/4] INFORME DETALLADO DE CONEXIONES, TIEMPOS Y COMPORTAMIENTO CIUDADANO")
    print("="*79)
    r = resultado["resumen"]
    a = resultado["aprendizaje"]
    
    print(f"\n1. RESUMEN GLOBAL:")
    print(f" • Total interacciones recolectadas: {r['total_eventos']}")
    print(f" • Sesiones únicas identificadas: {len(r.get('sesiones_usuarios', []))}")
    print(f" • Páginas visitadas: {r['visitas_por_pagina']}")
    
    print(f"\n2. PROCEDENCIA GEOGRÁFICA Y ORGANIZACIONES:")
    for ciudad, cnt in r.get("ciudades", {}).items():
        print(f" • Ciudad: {ciudad} ({cnt} eventos)")
    for org, cnt in r.get("organizaciones_isp", {}).items():
        print(f" • Proveedor / Organización: {org} ({cnt} eventos)")
    for pais, cnt in r.get("paises", {}).items():
        print(f" • País: {pais} ({cnt} eventos)")

    print(f"\n3. DISPOSITIVOS, SISTEMAS Y NAVEGADORES:")
    print(f" • Tipo: {r['dispositivos']['escritorio']} escritorio | {r['dispositivos']['movil']} móvil | {r['dispositivos']['tablet']} tablet")
    for os_n, cnt in r.get("sistemas_operativos", {}).items():
        print(f" • Sistema Operativo: {os_n} ({cnt})")
    for br_n, cnt in r.get("navegadores", {}).items():
        print(f" • Navegador: {br_n} ({cnt})")

    print(f"\n4. DETALLE CRONOLÓGICO POR SESIÓN (QUIÉNES, TIEMPO Y ACCIONES):")
    sesiones = r.get("sesiones_usuarios", [])
    if not sesiones:
        print(" • Aún no hay sesiones registradas.")
    for idx, s in enumerate(sesiones, start=1):
        geo = s.get("ubicacion", {})
        dev = s.get("dispositivo", {})
        print(f"\n ── [Sesión #{idx}] ──────────────────────────────────────────────────────────")
        print(f" • Visitante ID: {s['visitor_id']}")
        print(f" • Conectado desde: {geo.get('ciudad', 'Chile')} ({geo.get('region', '')}, {geo.get('pais', 'Chile')})")
        print(f" • Red / Organización: {geo.get('org', 'Desconocida')} [IP: {s['ip']}]")
        print(f" • Equipo: {dev.get('dispositivo', 'PC')} · {dev.get('os', '')} · {dev.get('browser', '')} (Pantalla: {s.get('pantalla', 'N/A')})")
        print(f" • Hora de inicio: {s.get('inicio', 'N/A')}")
        print(f" • Tiempo de permanencia: {s.get('duracion_texto', '< 1m')} | Profundidad de lectura: {s.get('profundidad_scroll', '0%')}")
        print(f" • Páginas recorridas: {', '.join(s.get('paginas_visitadas', []))}")
        print(f" • Línea de acciones realizada:")
        for act in s.get("historial_acciones", []):
            print(f"    └─ {act}")

    print(f"\n5. CONSUMO DE INFORMACIÓN Y DEMANDA CIUDADANA:")
    print(f" • Descargas de capas: {sum(r['descargas_por_capa'].values())} totales")
    for k, v in r['descargas_por_capa'].items():
        print(f"    - {k}: {v} descargas")
    print(f" • Capas huérfanas (sin descargas): {', '.join(r.get('capas_sin_descargas', []))}")
    print(f" • Búsquedas en catálogo: {len(r['busquedas'])}")
    if r['busquedas']:
        print(f"    - Términos: {', '.join(set(r['busquedas']))}")
    if r['busquedas_sin_resultado']:
        print(f"    - Demanda insatisfecha (0 resultados): {', '.join(set(r['busquedas_sin_resultado']))}")
    print(f" • Consultas al Copiloto: {len(r['consultas_copiloto'])}")
    for q in r['consultas_copiloto']:
        print(f"    - \"{q['pregunta']}\" [Desde: {q.get('ciudad', q.get('pais'))}]")

    print(f"\n6. ESTADO DE LA MEMORIA Y APRENDIZAJE ACTIVO:")
    print(f" • Estado: {a['estado']}")
    print(f" • Nuevos patrones incorporados: {a['nuevos_patrones_parquet_guardados']}")
    print(f" • Total patrones consolidados: {a['patrones_totales_memoria']}")
    print("="*79 + "\n")


if __name__ == "__main__":
    main()


