import random
import json
from typing import List

# Pools of phrasing for different IDE topics (catalog, standards, APIs, coverage, open data, interoperability, metadata, governance)
_TOPICS = {
    "catalog": [
        "¿Qué formato de intercambio se sugiere para los recursos vectoriales en la IDE?",
        "¿Cómo se mantiene actualizado el catálogo de datos en la IDE?",
        "¿Qué criterios de calidad se aplican al registro de nuevos datasets?",
        "¿Cuál es la política de versionado del catálogo nacional?",
    ],
    "standards": [
        "¿Qué estándares de metadatos recomienda la IDE (por ejemplo ISO 19115, DCAT)?",
        "¿Cómo se garantiza la interoperabilidad mediante OGC en la IDE?",
        "¿Qué normas de codificación se usan para códigos territoriales?",
        "¿Cuál es la estrategia de adopción de GeoParquet en la IDE?",
    ],
    "apis": [
        "¿Qué APIs REST están disponibles para acceder a los datos de salud?",
        "¿Cómo se autentica un usuario en la API de la IDE?",
        "¿Qué límites de uso (rate‑limit) tiene la API pública?",
        "¿Cuál es el formato de respuesta estándar de la API (JSON, GeoJSON)?",
    ],
    "coverage": [
        "¿Cómo se mide la cobertura geográfica de los equipamientos en la IDE?",
        "¿Qué indicadores de accesibilidad se calculan a nivel de manzana?",
        "¿Cómo se actualizan los datos de cobertura de redes de transporte?",
        "¿Qué metodologías (E2SFCA, isocronas Tobler) se usan para la evaluación territorial?",
    ],
    "open_data": [
        "¿Qué datasets están bajo licencia Creative Commons en la IDE?",
        "¿Cómo se publica la información de salud en datos abiertos?",
        "¿Cuál es el proceso para solicitar la inclusión de un nuevo recurso abierto?",
        "¿Qué políticas de privacidad se aplican a los datos personales?",
    ],
    "interoperability": [
        "¿Cómo se integran servicios WMS y WFS en la infraestructura?",
        "¿Qué mecanismos de descubrimiento (catalogue service) se utilizan?",
        "¿Cómo se asegura la consistencia entre diferentes fuentes de datos?",
        "¿Qué papel juega la arquitectura de microservicios en la IDE?",
    ],
    "metadata": [
        "¿Qué atributos de metadatos son obligatorios para cada capa?",
        "¿Cómo se gestiona la actualización automática de metadatos?",
        "¿Qué herramienta se usa para validar la conformidad con ISO 19115?",
        "¿Cómo se documenta la procedencia de los datos (provenance)?",
    ],
    "governance": [
        "¿Cuál es la estructura de gobernanza de la IDE dentro del CIT‑UAI?",
        "¿Qué comités revisan la calidad de los datos publicados?",
        "¿Cómo se gestiona el ciclo de vida de los datasets (retención, archivo)?",
        "¿Qué normas legales regulan el intercambio de datos territoriales?",
    ],
}

def generate_ide_questions(num_questions: int = 1200, seed: int = 42) -> List[str]:
    """Generate a list of varied, human‑like questions about the IDE.

    The function draws randomly from the predefined topic pools, mixing topics
    and applying light phrasing variations so that the output resembles a natural
    conversational flow rather than a repetitive list.
    """
    random.seed(seed)
    all_qs: List[str] = []
    pool_names = list(_TOPICS.keys())
    while len(all_qs) < num_questions:
        pool = random.choice(pool_names)
        base = random.choice(_TOPICS[pool])
        # Small variations to avoid exact duplicates
        variations = [
            base,
            base.replace("¿", "").replace("?", "").capitalize() + "?",
            "Me gustaría saber: " + base[1:].lower(),
            "Podrías indicarme " + base[1:].lower(),
        ]
        all_qs.append(random.choice(variations))
    return all_qs[:num_questions]

if __name__ == "__main__":
    # Simple test: generate a few questions and print as JSON
    sample = generate_ide_questions(10)
    print(json.dumps(sample, ensure_ascii=False, indent=2))
