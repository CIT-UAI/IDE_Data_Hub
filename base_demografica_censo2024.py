#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — BASE DE CONOCIMIENTO DEMOGRÁFICA Y DE GÉNERO CENSO 2024 (CIT-UAI)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Compila el diccionario maestro de datos oficiales del Censo 2024, con
desagregación de sexo/género (Hombres, Mujeres, IFE 60+, IFE 80+, Mujeres en edad fértil),
estructura etaria completa, tiempos de caminata de Tobler e integración de todas
las capacidades, capas y coberturas cargadas en la IDE CIT.
"""

from __future__ import annotations
import json
import unicodedata
from pathlib import Path
import duckdb


def norm_key(s: str) -> str:
    """Normaliza texto para búsqueda sin tildes ni mayúsculas."""
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.strip()


def get_censo_2024_js_data(duckdb_path: Path, parquet_maestro_path: Path = None) -> str:
    """
    Lee `libro_digital_mbht_experto.duckdb` y `MBHT_MAESTRO_2024_NACIONAL.parquet`
    para compilar las constantes JavaScript con desagregación total por género/sexo
    y catálogo completo de la IDE CIT.
    """
    if not duckdb_path.exists():
        return "// DuckDB demografico no encontrado\nconst CIT_CENSO_2024_COMUNAS = {};\nconst CIT_CENSO_2024_REGIONES = {};\nconst CIT_CENSO_2024_NACIONAL = {};"

    conn = duckdb.connect(str(duckdb_path), read_only=True)

    # 1. Base comunal desde duckdb (345 comunas)
    rows_comunas = conn.execute("""
    SELECT 
        COD_REG, REGION, COD_COM, COMUNA,
        total_manzanas,
        round(poblacion_total, 0) as poblacion,
        total_nna, total_lactantes, total_parvulos,
        total_mayores_60, total_cuarta_edad,
        round(bht_promedio_ponderado, 3) as bht,
        round(sobrecarga_cuidados_prom, 1) as sobrecarga,
        round(prop_mayores_60_pct, 1) as pct_60,
        round(prop_nna_pct, 1) as pct_nna,
        round(indice_envejecimiento, 1) as ind_env,
        round(t_salud_min_prom, 1) as t_salud,
        round(t_salacuna_min_prom, 1) as t_salacuna,
        round(t_educacion_min_prom, 1) as t_educ,
        round(t_areasverdes_min_prom, 1) as t_av
    FROM resumen_comunal
    ORDER BY COMUNA
    """).fetchall()

    # 1.1 Cargar catálogo maestro 345 comunas entrenado con CUDA
    cat_345 = {}
    cat_path_local = duckdb_path.parent / "catalogo_nacional_345_entrenado_cuda.json"
    if not cat_path_local.exists():
        cat_path_local = duckdb_path.parent.parent / "memoria" / "catalogo_nacional_345_entrenado_cuda.json"
    if cat_path_local.exists():
        try:
            with open(cat_path_local, "r", encoding="utf-8") as fc:
                cat_345 = json.load(fc)
        except Exception:
            pass

    # 2. Desglose de Género/Sexo desde Parquet Maestro 2024 (si está disponible)
    sexo_comunal = {}
    if parquet_maestro_path and parquet_maestro_path.exists():
        try:
            p_str = str(parquet_maestro_path).replace("\\", "/")
            df_sexo = duckdb.query(f"""
            SELECT COD_COM,
                   round(sum(HOMBRES_x), 0) as hombres,
                   round(sum(MUJERES_x), 0) as mujeres,
                   round(sum(H0A17), 0) as hombres_nna,
                   round(sum(M0A17), 0) as mujeres_nna,
                   round(sum(H60AMAS), 0) as hombres_60,
                   round(sum(M60AMAS), 0) as mujeres_60,
                   round(sum(H80AMAS), 0) as hombres_80,
                   round(sum(M80AMAS), 0) as mujeres_80,
                   round(sum(M15A49), 0) as mujeres_edad_fertil,
                   round(avg(IFE_60), 1) as ife_60,
                   round(avg(IFE_80), 1) as ife_80
            FROM '{p_str}'
            GROUP BY COD_COM
            """).df()
            for _, row in df_sexo.iterrows():
                sexo_comunal[str(row["COD_COM"])] = row
        except Exception as e:
            pass

    comunas = {}
    for r in rows_comunas:
        c_reg, reg, c_com, com, mz, pob, nna, lac, parv, m60, c80, bht, sobre, p60, pnna, ienv, tsal, tsala, ted, tav = r
        k = norm_key(com)
        s_data = sexo_comunal.get(str(c_com))

        pob_val = int(pob) if pob else 0
        raw_h = float(s_data["hombres"]) if (s_data is not None and "hombres" in s_data) else 0.0
        raw_m = float(s_data["mujeres"]) if (s_data is not None and "mujeres" in s_data) else 0.0

        if (raw_h + raw_m) > 0 and (raw_h + raw_m) >= pob_val * 0.7:
            # Escalamiento estricto de conservación matricial
            factor = pob_val / (raw_h + raw_m)
            hombres_val = int(round(raw_h * factor))
            mujeres_val = pob_val - hombres_val
        elif (raw_h + raw_m) > 0:
            ratio_h = raw_h / (raw_h + raw_m)
            hombres_val = int(round(pob_val * ratio_h))
            mujeres_val = pob_val - hombres_val
        else:
            # Proporción oficial INE Censo 2024 (48.8% hombres, 51.2% mujeres)
            hombres_val = int(round(pob_val * 0.488))
            mujeres_val = pob_val - hombres_val

        h_nna = int(s_data["hombres_nna"]) if (s_data is not None and "hombres_nna" in s_data and s_data["hombres_nna"] > 0) else int(round((nna or 0) * 0.512))
        m_nna = max(0, (int(nna) if nna else 0) - h_nna)
        
        m60_val = int(m60) if m60 else 0
        h_60 = int(s_data["hombres_60"]) if (s_data is not None and "hombres_60" in s_data and s_data["hombres_60"] > 0) else int(round(m60_val * 0.445))
        m_60 = max(0, m60_val - h_60)
        
        c80_val = int(c80) if c80 else 0
        h_80 = int(s_data["hombres_80"]) if (s_data is not None and "hombres_80" in s_data and s_data["hombres_80"] > 0) else int(round(c80_val * 0.355))
        m_80 = max(0, c80_val - h_80)
        
        m_ef = int(s_data["mujeres_edad_fertil"]) if (s_data is not None and "mujeres_edad_fertil" in s_data and s_data["mujeres_edad_fertil"] > 0) else int(round(mujeres_val * 0.478))
        ife_60_val = round((m_60 / max(1, h_60)) * 100, 1)
        ife_80_val = round((m_80 / max(1, h_80)) * 100, 1)

        pct_h = round((hombres_val / max(1, pob_val)) * 100, 1)
        pct_m = round((mujeres_val / max(1, pob_val)) * 100, 1)

        c_code_5 = str(c_com).zfill(5)
        cat_info = cat_345.get(c_code_5, {})

        comunas[k] = {
            "comuna": com,
            "cod_com": str(c_com),
            "cod_reg": str(c_reg),
            "region": reg,
            "manzanas": int(mz) if mz else 0,
            "poblacion": pob_val,
            # Desglose de Sexo / Género
            "hombres": hombres_val,
            "mujeres": mujeres_val,
            "pct_hombres": pct_h,
            "pct_mujeres": pct_m,
            "mujeres_edad_fertil": m_ef,
            "ife_60": ife_60_val,
            "ife_80": ife_80_val,
            # Niñez y Juventud
            "nna": int(nna) if nna else 0,
            "hombres_nna": h_nna,
            "mujeres_nna": m_nna,
            "lactantes": int(lac) if lac else 0,
            "parvulos": int(parv) if parv else 0,
            # Vejez y Cuarta Edad
            "mayores_60": int(m60) if m60 else 0,
            "hombres_60": h_60,
            "mujeres_60": m_60,
            "cuarta_edad_80": int(c80) if c80 else 0,
            "hombres_80": h_80,
            "mujeres_80": m_80,
            # Vivienda y Hogares
            "hogares": int(cat_info.get("hogares", 0)) if cat_info.get("hogares") else int(round(pob_val / 2.8)),
            "viviendas": int(cat_info.get("viviendas", 0)) if cat_info.get("viviendas") else int(round(pob_val / 2.4)),
            # Indicadores Territoriales Oficiales
            "bht": float(cat_info.get("bht", bht or 0.0)),
            "sobrecarga": float(sobre) if sobre else 0.0,
            "pct_mayores_60": float(p60) if p60 else 0.0,
            "pct_nna": float(pnna) if pnna else 0.0,
            "indice_envejecimiento": float(ienv) if ienv else 0.0,
            "t_salud_min": float(tsal) if tsal else 0.0,
            "t_salacuna_min": float(tsala) if tsala else 0.0,
            "t_educacion_min": float(ted) if ted else 0.0,
            "t_areasverdes_min": float(tav) if tav else 0.0,
            # Dimensiones MBHT Desagregadas
            "dim_acc": float(cat_info.get("dim_acc", 0.0)),
            "dim_soc": float(cat_info.get("dim_soc", 0.0)),
            "dim_seg": float(cat_info.get("dim_seg", 0.0)),
            "dim_amb": float(cat_info.get("dim_amb", 0.0)),
            # Indicadores Elementales MBHT (0.0000 a 1.0000)
            "isal": float(cat_info.get("isal", 0.0)),
            "ise": float(cat_info.get("ise", 0.0)),
            "iav": float(cat_info.get("iav", 0.0)),
            "idep": float(cat_info.get("idep", 0.0)),
            "icul": float(cat_info.get("icul", 0.0)),
            "iser": float(cat_info.get("iser", 0.0)),
            # Análisis Cualitativo y Arquetipos
            "dim_fuerte": cat_info.get("dim_fuerte", ""),
            "dim_rezagada": cat_info.get("dim_rezagada", ""),
            "prioridad_inversion": cat_info.get("prioridad_inversion", ""),
            "arquetipo": cat_info.get("arquetipo", ""),
            "comunas_gemelas": cat_info.get("comunas_gemelas", []),
            "lat": cat_info.get("centro", {}).get("lat", 0.0) if isinstance(cat_info.get("centro"), dict) else 0.0,
            "lon": cat_info.get("centro", {}).get("lon", 0.0) if isinstance(cat_info.get("centro"), dict) else 0.0,
        }

    # Aliases y variantes fonéticas frecuentes de comunas
    if "aisen" in comunas:
        comunas["aysen"] = dict(comunas["aisen"], comuna="Aysén")
        comunas["puerto aysen"] = dict(comunas["aisen"], comuna="Puerto Aysén")
    if "coihaique" in comunas:
        comunas["coyhaique"] = dict(comunas["coihaique"], comuna="Coyhaique")
    if "calera" in comunas:
        comunas["la calera"] = dict(comunas["calera"], comuna="La Calera")
    if "llaillay" in comunas:
        comunas["llayllay"] = dict(comunas["llaillay"], comuna="Llay-Llay")

    # 3. Regiones (16 regiones)
    rows_reg = conn.execute("""
    SELECT 
        COD_REG, REGION,
        count(*) as total_comunas,
        sum(total_manzanas) as total_manzanas,
        round(sum(poblacion_total), 0) as poblacion,
        sum(total_nna) as total_nna,
        sum(total_mayores_60) as total_mayores_60,
        sum(total_cuarta_edad) as total_cuarta_edad,
        round(avg(bht_promedio_ponderado), 3) as bht,
        round(avg(indice_envejecimiento), 1) as ind_env
    FROM resumen_comunal
    GROUP BY COD_REG, REGION
    ORDER BY COD_REG
    """).fetchall()

    regiones = {}
    for r in rows_reg:
        c_reg, reg, tcom, tmz, tpob, tnna, tm60, tc80, bht, ienv = r
        k = norm_key(reg)
        reg_coms = [v for v in comunas.values() if v["cod_reg"] == str(c_reg)]
        h_reg = sum(c["hombres"] for c in reg_coms)
        m_reg = sum(c["mujeres"] for c in reg_coms)
        m_ef_reg = sum(c["mujeres_edad_fertil"] for c in reg_coms)
        h_80_reg = sum(c["hombres_80"] for c in reg_coms)
        m_80_reg = sum(c["mujeres_80"] for c in reg_coms)
        ife_80_reg = round((m_80_reg / max(1, h_80_reg)) * 100, 1)

        regiones[k] = {
            "cod_reg": str(c_reg),
            "region": reg,
            "comunas": int(tcom),
            "manzanas": int(tmz) if tmz else 0,
            "poblacion": int(tpob) if tpob else 0,
            "hombres": h_reg,
            "mujeres": m_reg,
            "mujeres_edad_fertil": m_ef_reg,
            "hombres_80": h_80_reg,
            "mujeres_80": m_80_reg,
            "ife_80": ife_80_reg,
            "nna": int(tnna) if tnna else 0,
            "mayores_60": int(tm60) if tm60 else 0,
            "cuarta_edad_80": int(tc80) if tc80 else 0,
            "bht": float(bht) if bht else 0.0,
            "indice_envejecimiento": float(ienv) if ienv else 0.0,
        }

    # 4. Consolidado Nacional
    h_nac = sum(c["hombres"] for c in comunas.values())
    m_nac = sum(c["mujeres"] for c in comunas.values())
    h_80_nac = sum(c["hombres_80"] for c in comunas.values())
    m_80_nac = sum(c["mujeres_80"] for c in comunas.values())
    m_ef_nac = sum(c["mujeres_edad_fertil"] for c in comunas.values())

    nacional = {
        "pais": "Chile",
        "regiones": 16,
        "comunas": 346,
        "municipios": 345,
        "manzanas": 254268,
        "poblacion": 18480377,
        # Género Nacional
        "hombres": h_nac,
        "mujeres": m_nac,
        "pct_hombres": round((h_nac / 18480377) * 100, 1),
        "pct_mujeres": round((m_nac / 18480377) * 100, 1),
        "mujeres_edad_fertil": m_ef_nac,
        "hombres_cuarta_edad_80": h_80_nac,
        "mujeres_cuarta_edad_80": m_80_nac,
        "ife_80_cuarta_edad": round((m_80_nac / max(1, h_80_nac)) * 100, 1),
        # Edades
        "nna": 6138236,
        "mayores_60": 3436578,
        "cuarta_edad_80": 538603,
        "bht_promedio": 0.668,
        "indice_envejecimiento": 52.1,
        # Infraestructura Censal
        "viviendas_censo_2024": 7664466,
        "hogares_censo_2024": 6622597,
        "zonas_censales": 15006,
        "equipamientos_auditados": 202418,
    }

    # 5. Catálogo Integral de lo cargado en la IDE CIT
    catalogo_ide = {
        "capas_oficiales": [
            {"id": "kpi_mud_2017", "nombre": "MBHT 2017 (Matriz Urbana de Destinos)", "tipo": "Acceso Peatonal Continuo"},
            {"id": "censo_imputaciones_2024", "nombre": "Censo 2024 — Imputaciones Micro-espaciales", "tipo": "Demografía Manzanal"},
            {"id": "subdere_limites_comunales", "nombre": "Límites Político-Administrativos SUBDERE", "tipo": "Límites Oficiales"},
            {"id": "sii_areas_homogeneas", "nombre": "Áreas Homogéneas SII (VGT Fiscal)", "tipo": "Economía del Suelo"},
            {"id": "pem_maritorio_nacional", "nombre": "Planificación Marina Nacional (FAO / SBAP / ZEE)", "tipo": "Maritorio Tricontinental"},
            {"id": "pem_cuencas_oceanicas", "nombre": "Cuencas Oceánicas y Ecosistemas Marinos", "tipo": "Conservación Marina"},
            {"id": "inse_socioeconomico", "nombre": "Nivel Socioeconómico y Habitacional (INSE)", "tipo": "Estratificación Social"},
            {"id": "kpi_isal", "nombre": "ISAL — Dimensión Salud Primaria y Hospitalaria", "tipo": "Acceso Asistencial"},
            {"id": "kpi_ise", "nombre": "ISE — Dimensión Educación Inicial, Básica y Media", "tipo": "Acceso Formativo"},
            {"id": "kpi_iav", "nombre": "IAV — Dimensión Parques y Plazas Públicas", "tipo": "Espacio Público"},
            {"id": "kpi_idep", "nombre": "IDEP — Dimensión Deporte y Canchas Polideportivas", "tipo": "Infraestructura Deportiva"},
            {"id": "kpi_icul", "nombre": "ICUL — Dimensión Cultura, Bibliotecas y Museos", "tipo": "Patrimonio y Creación"},
            {"id": "kpi_iser", "nombre": "ISER — Dimensión Servicios Cívicos y Bancarios", "tipo": "Trámites Ciudadanos"},
            {"id": "tob_oportunidad", "nombre": "TOB — Territorios de Oportunidad de Bienestar", "tipo": "Focalización de Inversión"}
        ],
        "formatos_descarga": ["GeoParquet 1.1", "GeoPackage (.gpkg)", "Shapefile (.zip)", "CSV"],
        "coberturas_descargas": ["Manzanas Censales Nacionales", "Equipamientos Georreferenciados", "Red Vial Caminable"],
        "geoportales_red_ides": 19,
        "interoperabilidad": ["QGIS (WMS / WFS / OGC)", "ArcGIS Pro", "Python (GeoPandas / DuckDB)", "R (sf / terra)"]
    }

    conn.close()

    js_comunas = json.dumps(comunas, ensure_ascii=False)
    js_regiones = json.dumps(regiones, ensure_ascii=False)
    js_nacional = json.dumps(nacional, ensure_ascii=False)
    js_catalogo = json.dumps(catalogo_ide, ensure_ascii=False)

    return f"""
        // BASE DE DATOS DEMOGRÁFICA, DE GÉNERO Y CATÁLOGO TOTAL IDE CIT (CENSO 2024)
        const CIT_CENSO_2024_COMUNAS = {js_comunas};
        const CIT_CENSO_2024_REGIONES = {js_regiones};
        const CIT_CENSO_2024_NACIONAL = {js_nacional};
        const CIT_CATALOGO_IDE_TOTAL = {js_catalogo};
    """


if __name__ == "__main__":
    from motor_ia_cit import find_proyecto_root
    root = find_proyecto_root()
    db_file = root / "memoria" / "libro_digital_mbht_experto.duckdb"
    pq_maestro = root / "03_Resultados" / "2024" / "Coberturas_Maestras_Consolidadas_2024" / "geoparquet" / "MBHT_MAESTRO_2024_NACIONAL.parquet"
    res = get_censo_2024_js_data(db_file, pq_maestro)
    print("Longitud JS Demografía + Género + Catálogo:", len(res), "bytes")
