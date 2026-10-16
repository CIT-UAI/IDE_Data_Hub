#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conversacion_con_agente.py
===============================================================================
Script de interacción y conversación profunda con el Copiloto IA Territorial (CIT-UAI).
Mantiene un diálogo estructurado, humano y continuo de más de 3.300 preguntas
recorriendo el territorio nacional (345 comunas), sus métodos espaciales, coberturas,
manzanas, población y equipamientos de la MBHT.
===============================================================================
"""

import json
import subprocess
import sys
import time
from pathlib import Path

# Configurar encoding UTF-8 en consola
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from motor_ia_cit import get_copilot_js_engine
from test_masivo.generar_preguntas_masivas import generar_preguntas

def ejecutar_conversacion_con_agente():
    print("=" * 80)
    print("  INICIANDO CONVERSACIÓN PROFUNDA CON EL COPILOTO IA TERRITORIAL CIT-UAI")
    print("=" * 80)
    print("[*] Preparando temas de diálogo territorial, métodos y coberturas...")

    # Cargar o generar el dataset de preguntas territoriales (3.320 preguntas)
    preguntas_masivas_path = BASE_DIR / "test_masivo" / "preguntas_masivas.json"
    if not preguntas_masivas_path.exists():
        preguntas = generar_preguntas()
        preguntas_masivas_path.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        preguntas = json.loads(preguntas_masivas_path.read_text(encoding="utf-8"))
    
    print(f"[*] Universo conversacional disponible: {len(preguntas)} preguntas territoriales.")

    # Diseñar hilos conversacionales profundos de diálogo temático (mínimo 5 preguntas hiladas cada uno)
    hilos_conversacionales = [
        {
            "tema": "Hilo 1: Acceso a Salud y Decaimiento Espacial en la Región Metropolitana",
            "turnos": [
                "¿Cómo se mide el acceso a equipamientos de salud en la MBHT?",
                "¿Qué función de decaimiento espacial se utiliza para el cálculo peatonal?",
                "¿Cómo se modela la velocidad de caminata según la pendiente de Tobler?",
                "¿Cuál es la dotación de CESFAM y centros de salud en la comuna de La Pintana?",
                "¿Cómo se compara la accesibilidad a salud de La Pintana con Providencia o Las Condes?",
                "¿Qué recomendaciones surgen para reducir las brechas de atención primaria en estas manzanas?"
            ]
        },
        {
            "tema": "Hilo 2: Cobertura de Áreas Verdes y Calidad de Vida en el Biobío",
            "turnos": [
                "¿Qué indicador evalúa la presencia de parques y plazas públicas en la MBHT?",
                "¿Cuál es el umbral de distancia o tiempo de caminata recomendado para plazas de barrio?",
                "¿Cuántas plazas y áreas verdes tiene registradas la comuna de Concepción?",
                "¿Cómo se distribuye la población y las manzanas censales en Coronel y Lota?",
                "¿Cómo influyen las quebradas y la topografía en la accesibilidad peatonal a espacios públicos?",
                "¿Qué datos de la IDE permiten priorizar nuevas inversiones de parques urbanos?"
            ]
        },
        {
            "tema": "Hilo 3: Demografía, Envejecimiento y Censo 2024 en el Norte Grande",
            "turnos": [
                "¿Cuánta población total reside en la comuna de Arica según el Censo 2024?",
                "¿Cuántos adultos mayores y niños viven en Iquique y Alto Hospicio?",
                "¿Cuántas manzanas censales componen el área urbana de Antofagasta?",
                "¿Cómo se evalúa la caminabilidad de las personas mayores en zonas de alta pendiente?",
                "¿Qué estándares de datos geográficos (ISO 19115, OGC) aseguran la interoperabilidad de estas coberturas?"
            ]
        },
        {
            "tema": "Hilo 4: Metodología E2SFCA y Matriz de Bienestar Humano Territorial",
            "turnos": [
                "¿En qué consiste el método de las Dos Áreas de Captación Flotantes Mejoradas (E2SFCA)?",
                "¿Cómo se equilibra la oferta de servicios con la demanda de los hogares en cada manzana?",
                "¿Qué dimensiones componen la Matriz de Bienestar Humano Territorial?",
                "¿Qué representan los indicadores ISAL, ISE, IAV, IDEP, ICUL e ISER?",
                "¿Cómo se integran las 345 comunas de Chile en la base de datos DuckDB y GeoParquet?"
            ]
        },
        {
            "tema": "Hilo 5: Maritorio, Zonas Extremas e Integración Austral",
            "turnos": [
                "¿Qué dimensiones abarca el concepto de Maritorio en la cartografía del CIT?",
                "¿Qué características geomorfológicas destacan en la Fosa de Atacama y los cañones submarinos?",
                "¿Cuántos habitantes y viviendas censadas tiene la comuna de Cabo de Hornos y Puerto Williams?",
                "¿Cómo se abordan las singularidades de aislamiento en Aysén y Magallanes?",
                "¿Qué rol cumple la IDE CIT en el fortalecimiento de la soberanía y la equidad territorial?"
            ]
        }
    ]

    hilos_path = BASE_DIR / "test_masivo" / "_temp_hilos.json"
    hilos_path.write_text(json.dumps(hilos_conversacionales, ensure_ascii=False, indent=2), encoding="utf-8")

    hilos_path_js = str(hilos_path).replace("\\", "/")
    preguntas_path_js = str(preguntas_masivas_path).replace("\\", "/")

    # Ejecución del motor JS en Node.js para mantener la conversación
    js_engine = get_copilot_js_engine()

    harness_code = f"""
const fs = require('fs');

const noop = () => {{}};
const globalObj = {{
    __cit_dialog_ctx: null,
    addEventListener: noop,
    removeEventListener: noop
}};
global.window = globalObj;
global.sessionStorage = {{ getItem: () => null, setItem: noop }};
global.localStorage = {{ getItem: () => null, setItem: noop }};
global.document = {{ documentElement: {{}}, referrer: '', addEventListener: noop, removeEventListener: noop }};
global.fetch = () => Promise.reject(new Error('offline'));
global.sendCitTelemetry = noop;
global.setTimeout = (fn, ms) => 0;
global.clearTimeout = () => {{}};

{js_engine}

sendCitTelemetry = noop;

async function runFullConversation() {{
    const hilos = JSON.parse(fs.readFileSync('{hilos_path_js}', 'utf-8'));
    const massPreguntas = JSON.parse(fs.readFileSync('{preguntas_path_js}', 'utf-8'));

    const logConversacion = [];

    // 1. Ejecutar diálogos hilados en profundidad
    for (let h = 0; h < hilos.length; h++) {{
        const hilo = hilos[h];
        const respuestasHilo = [];
        for (let t = 0; t < hilo.turnos.length; t++) {{
            const preg = hilo.turnos[t];
            const res = await resolveCopilotResponse(preg);
            const textLimpio = (res && res.text) ? res.text.replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim() : '';
            respuestasHilo.push({{
                turno: t + 1,
                pregunta: preg,
                respuesta_corta: textLimpio.substring(0, 220) + (textLimpio.length > 220 ? '...' : '')
            }});
        }}
        logConversacion.push({{
            hilo_id: h + 1,
            tema: hilo.tema,
            interacciones: respuestasHilo
        }});
    }}

    // 2. Ejecutar conversación masiva de cobertura nacional (3.320 preguntas)
    let respondidasEspecificas = 0;
    let respuestasFallback = 0;

    for (let i = 0; i < massPreguntas.length; i++) {{
        const item = massPreguntas[i];
        const res = await resolveCopilotResponse(item.pregunta);
        const text = (res && res.text) ? res.text.toLowerCase() : '';
        if (text.includes('abre un terreno de analisis') || text.includes('sobre cual de estas dimensiones') || text.includes('tu consulta sobre')) {{
            respuestasFallback++;
        }} else {{
            respondidasEspecificas++;
        }}
    }}

    const salida = {{
        status: 'OK',
        total_preguntas_conversadas: massPreguntas.length + hilos.reduce((acc, h) => acc + h.turnos.length, 0),
        hilos_profundos: logConversacion,
        resumen_cobertura: {{
            total: massPreguntas.length,
            especificas: respondidasEspecificas,
            fallback: respuestasFallback,
            pct_exito: ((respondidasEspecificas / massPreguntas.length) * 100).toFixed(2)
        }}
    }};

    console.log("===JSON_START===");
    console.log(JSON.stringify(salida));
    console.log("===JSON_END===");
    process.exit(0);
}}

runFullConversation();
"""

    temp_js = BASE_DIR / "temp_conversacion_runner.js"
    temp_js.write_text(harness_code, encoding="utf-8")

    try:
        print("[*] Conversando con el agente a través de los 5 hilos temáticos y el corpus nacional de 345 comunas...")
        t0 = time.time()
        proc = subprocess.run(
            ["node", str(temp_js)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60
        )
        t1 = time.time()

        if proc.returncode != 0:
            print(f"[!] Error ejecutando conversación en Node: {proc.stderr}")
            return False

        # Extraer JSON de salida
        stdout = proc.stdout
        if "===JSON_START===" in stdout and "===JSON_END===" in stdout:
            json_str = stdout.split("===JSON_START===")[1].split("===JSON_END===")[0].strip()
            data = json.loads(json_str)

            print(f"\n[OK] Conversación completada exitosamente en {t1 - t0:.2f} segundos.")
            print(f"[*] Total de preguntas conversadas y respondidas: {data['total_preguntas_conversadas']:,}")
            print(f"[*] Cobertura territorial específica lograda: {data['resumen_cobertura']['pct_exito']}%\n")

            print("--- EXTRACTO DE DIÁLOGOS HILADOS SOSTENIDOS CON EL AGENTE ---")
            for hilo in data["hilos_profundos"]:
                print(f"\n📖 {hilo['tema']}")
                for turno in hilo["interacciones"]:
                    print(f"  👤 Usuario : {turno['pregunta']}")
                    print(f"  🤖 Agente  : {turno['respuesta_corta']}\n")

            # Guardar registro de la conversación
            log_path = BASE_DIR / "test_masivo" / "bitacora_conversacion_agente.json"
            log_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[*] Bitácora completa de la conversación guardada en: {log_path}")
            return True
        else:
            print("[!] No se encontró el bloque de datos JSON en la salida:")
            print(stdout[:500])
            return False

    finally:
        if temp_js.exists():
            temp_js.unlink(missing_ok=True)
        if hilos_path.exists():
            hilos_path.unlink(missing_ok=True)

if __name__ == "__main__":
    exito = ejecutar_conversacion_con_agente()
    print("=" * 80)
    if exito:
        print("Conversación con el agente: SÍ")
    else:
        print("Conversación con el agente: NO")
    print("=" * 80)
