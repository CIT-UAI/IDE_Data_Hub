"""
test_copilot_preguntas.py
Suite de regresión del Copiloto IA Territorial — CIT-UAI
═══════════════════════════════════════════════════════════════════════════════
Modos de ejecución:
  python test_copilot_preguntas.py           → Suite crítica (32 preguntas) — rápida
  python test_copilot_preguntas.py --full    → Suite masiva (3.320 preguntas) — completa
  python test_copilot_preguntas.py --stats   → Solo estadísticas de cobertura (masiva)
═══════════════════════════════════════════════════════════════════════════════
"""
import json
import subprocess
import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from motor_ia_cit import get_copilot_js_engine

# ─────────────────────────────────────────────────────────────────────────────
# SUITE CRÍTICA — 32 preguntas mínimas de regresión (siempre deben pasar)
# ─────────────────────────────────────────────────────────────────────────────
PREGUNTAS_CRITICAS = [
    # Geomorfología marina
    'cuanto mide la fosa de atacama?',
    'un guyot?',
    'un cañon submarino?',
    'que es una dorsal?',
    'que es un monete submarino?',
    'Cuanto mide el maritorio?',
    'que es el oceano? cual es su riqueza y valor para el país?',
    # IDE e historia
    'Cual es la historia de una IDE?',
    'que hace el SNIT?',
    'Que es y que hace la IDE Chile?',
    'son solo 19 IDEs o hay más?',
    'que es el SBAP',
    'qus el la FAO?',
    'qué es el INE?',
    'qués es una cuenca?',
    'es importante para la soberania nacional cartografiar las zonas limitrofes?',
    # Metodología y velocidad
    'cual es la velocidad promedio caminando en ñuñoa?',
    'cuantas avenidas hay en Santiago?',
    # Demografía comunal
    'cuanta población hay en Yumbel?',
    'cuanta gente hay en la comuna de Peñalolen?',
    'cuantas mujeres adultas viven en San Joaquin?',
    'cuantos niños viven en Antofagasta',
    'donde vide la mayor cantidad de adultos mayores',
    'dende viven los más vulnerables en Chile?',
    # Institucional
    'que es UAI?',
    # Topónimos y geomorfología
    'Fosa de Richards ?',
    # Política de datos y estándares
    'cual es la politica actual de datos e interoperabilidad?',
    'que dice la ley de modernizacion y transformacion digital?',
    'que es duble core?',
    'que es darwin core y como se estructuran los registros biologicos?',
    'cuales son las normas ISO para vectores y raster?',
    'que es el EML y un plan de gestion de datos?',
]

# ─────────────────────────────────────────────────────────────────────────────
# HARNESS NODE.JS
# ─────────────────────────────────────────────────────────────────────────────
HARNESS_TEMPLATE = """
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
fetch = () => Promise.reject(new Error('offline'));
global.fetch = fetch;
global.sendCitTelemetry = noop;

{js_code}

sendCitTelemetry = noop;

const FALLBACK_MARKER = 'bitacora de estudio';

async function runTests(tests, statsOnly) {{
    const results = [];
    for (let i = 0; i < tests.length; i++) {{
        const q = tests[i];
        const res = await resolveCopilotResponse(q);
        const textNorm = res.text.toLowerCase().replace(/[áàä]/g,'a').replace(/[éèë]/g,'e').replace(/[íìï]/g,'i').replace(/[óòö]/g,'o').replace(/[úùü]/g,'u');
        const isFallback = textNorm.includes('circunscriben estrictamente') || textNorm.includes('no cuento con la evidencia oficial') || textNorm.includes('bitacora de estudio') || textNorm.includes('abre un terreno de analisis') || textNorm.includes('sobre cual de estas dimensiones');
        const titleMatch = res.text.match(/<strong>(.*?)<\\/strong>/);
        const title = titleMatch ? titleMatch[1] : res.text.substring(0, 80);
        if (!statsOnly) {{
            console.log(`[${{String(i+1).padStart(4)}}] Q: "${{q}}" -> A: ${{title}}`);
        }}
        results.push({{ id: i+1, pregunta: q, titulo: title, es_fallback: isFallback }});
    }}
    const especificas = results.filter(r => !r.es_fallback).length;
    const fallback = results.filter(r => r.es_fallback).length;
    const pct = ((especificas / results.length) * 100).toFixed(2);
    console.log(JSON.stringify({{ status:'OK', total: results.length, especificas, fallback, pct_cobertura: parseFloat(pct) }}));
    process.exit(0);
}}

const tests = {tests_json};
const statsOnly = {stats_only};
runTests(tests, statsOnly);
"""

def run_harness(preguntas: list, stats_only: bool = False) -> dict:
    """Ejecuta las preguntas en Node.js y retorna estadísticas."""
    js_code = get_copilot_js_engine()
    script = HARNESS_TEMPLATE.format(
        js_code=js_code,
        tests_json=json.dumps(preguntas, ensure_ascii=False),
        stats_only='true' if stats_only else 'false'
    )
    tmp = Path("test_copilot_temp.js")
    tmp.write_text(script, encoding="utf-8")
    try:
        res = subprocess.run(
            ["node", "test_copilot_temp.js"],
            capture_output=True, text=True, encoding="utf-8", timeout=300
        )
        if res.stderr and 'Error' in res.stderr:
            print("ERRORS:", res.stderr[:500], file=sys.stderr)
        # Última línea = JSON de estadísticas
        lines = [l for l in res.stdout.strip().splitlines() if l.strip()]
        if not stats_only:
            for line in lines[:-1]:
                print(line)
        stats_line = lines[-1] if lines else '{}'
        return json.loads(stats_line)
    finally:
        tmp.unlink(missing_ok=True)


def cargar_preguntas_masivas() -> list:
    """Carga la suite masiva de 3.320 preguntas."""
    p = Path("test_masivo/preguntas_masivas.json")
    if not p.exists():
        print("[!] No se encontró test_masivo/preguntas_masivas.json")
        print("    Ejecuta primero: python test_masivo/generar_preguntas_masivas.py")
        sys.exit(1)
    datos = json.loads(p.read_text(encoding="utf-8"))
    return [item["pregunta"] for item in datos]


def banner(titulo: str):
    w = 72
    print("=" * w)
    print(f"  {titulo}")
    print("=" * w)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Detect flags and optional custom question file
    modo_full  = "--full"  in sys.argv
    modo_stats = "--stats" in sys.argv
    custom_path = None
    if "--custom" in sys.argv:
        idx = sys.argv.index("--custom")
        if idx + 1 < len(sys.argv):
            custom_path = sys.argv[idx + 1]
        else:
            print("[!] Flag --custom requires a path to a JSON file of questions.")
            sys.exit(1)

    if modo_full or modo_stats:
        banner("SUITE MASIVA — 3.320 PREGUNTAS | Copiloto IA Territorial CIT-UAI")
        if custom_path:
            p = Path(custom_path)
            if not p.exists():
                print(f"[!] No se encontró el archivo de preguntas: {custom_path}")
                sys.exit(1)
            datos = json.loads(p.read_text(encoding="utf-8"))
            preguntas = [item["pregunta"] for item in datos]
            print(f"[*] Cargadas {len(preguntas)} preguntas desde {custom_path}")
        else:
            preguntas = cargar_preguntas_masivas()
            print(f"[*] Cargadas {len(preguntas)} preguntas desde test_masivo/preguntas_masivas.json")
        if modo_stats:
            print("[*] Modo estadísticas (sin imprimir cada pregunta)...")
        # Run harness; stats_only=False will print each Q&A, stats_only=True suppresses output
        stats = run_harness(preguntas, stats_only=modo_stats)
        print()
        print(f"{'TOTAL EVALUADAS':<30}: {stats.get('total', 0):,}")
        print(f"{'CON RESPUESTA ESPECÍFICA':<30}: {stats.get('especificas', 0):,}  ({stats.get('pct_cobertura', 0):.2f}%)")
        print(f"{'FALLBACK (sin cobertura)':<30}: {stats.get('fallback', 0):,}")
        cobertura = stats.get('pct_cobertura', 0)
        if cobertura >= 96:
            print(f"\n  Cobertura: {cobertura:.2f}% — EXCELENTE")
        elif cobertura >= 90:
            print(f"\n  Cobertura: {cobertura:.2f}% — BUENA")
        else:
            print(f"\n  Cobertura: {cobertura:.2f}% — REVISAR GAPS")
        print("=" * 72)

    else:
        # Default mode: run critical suite (prints each Q&A)
        stats = run_harness(PREGUNTAS_CRITICAS, stats_only=False)
        total   = stats.get('total', len(PREGUNTAS_CRITICAS))
        ok      = stats.get('especificas', total)
        fallback = stats.get('fallback', 0)
        print()
        if fallback == 0:
            print(f"  [{ok}/{total}] Suite crítica OK — todos los tests respondidos correctamente.")
        else:
            print(f"  [{ok}/{total}] Suite crítica — {fallback} preguntas sin respuesta específica. Revisar motor.")
        print()
