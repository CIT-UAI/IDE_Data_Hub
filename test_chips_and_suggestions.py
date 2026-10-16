import subprocess
import json
import sys
from motor_ia_cit import get_copilot_js_engine

js = get_copilot_js_engine()
harness = '''
const noop = () => {};
const globalObj = {
    __cit_dialog_ctx: null,
    addEventListener: noop,
    removeEventListener: noop
};
global.window = globalObj;
global.sessionStorage = { getItem: () => null, setItem: noop };
global.localStorage = { getItem: () => null, setItem: noop };
global.document = { documentElement: {}, referrer: '', addEventListener: noop, removeEventListener: noop };
fetch = () => Promise.reject(new Error('offline'));
global.fetch = fetch;
global.sendCitTelemetry = noop;
'''

queries = [
    'como impacta la pendiente de tobler en las condes?',
    'a que arquetipo territorial pertenece la pintana?',
    'como es el acceso a salud en puente alto?',
    'como es el acceso a educacion en maipu?',
    'como es el acceso a areas verdes en cerrillos?',
    'cuales son los 8 arquetipos territoriales de chile?',
    'que son los vacios criticos de servicios?',
    'que son los vacios criticos topologicos?',
    'que es la metalogica causal y el operador do(x)?',
    'de que sirve la mbht para proyectos fndr y pmu?',
    'cuales son las normas ISO para vectores y raster?',
    'cual es la politica actual de datos e interoperabilidad?',
    'que es el inse?',
    'que es el SBAP?',
    'que es la FAO y su rol en planificacion marina?',
    'que es darwin core y como se estructuran los registros biologicos?',
    'que es duble core?',
    'son solo 19 IDEs o hay más?',
    '¿Qué superficie mínima debe tener una plaza pública?',
    '¿Cómo se evalúan las multicanchas en el IDEP?',
    '¿Cómo se anonimizan los microdatos censales?',
    '¿Qué es la Matriz Origen-Destino Peatonal?',
    'caminabilidad en providencia',
    'cuanta poblacion tiene aysen',
    'cuanta poblacion tiene coyhaique'
]

test_script = f'''
{harness}
{js}
sendCitTelemetry = noop;

const queries = {json.dumps(queries, ensure_ascii=False)};

async function run() {{
    for (const q of queries) {{
        const res = await resolveCopilotResponse(q);
        const match = res.text.match(/<strong>(.*?)<\\/strong>/);
        const title = match ? match[1] : res.text.substring(0, 60);
        const isFallback = res.text.includes('abre un terreno de análisis interesante');
        console.log((isFallback ? '[FALLBACK FAIL]' : '[OK]') + ' | ' + q + ' ---> ' + title);
    }}
    process.exit(0);
}}
run();
'''

with open('test_chips_probe.js', 'w', encoding='utf-8') as f:
    f.write(test_script)

res = subprocess.run(['node', 'test_chips_probe.js'], capture_output=True, text=True, encoding='utf-8')
print(res.stdout)
if res.stderr:
    print('ERR:', res.stderr)
