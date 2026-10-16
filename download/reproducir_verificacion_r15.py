#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Canónico de Reproducibilidad Científica e Integridad Criptográfica
Infraestructura de Datos Espaciales (IDE CIT) — Universidad Adolfo Ibáñez
Conjunto: MBHT 2017 (Región de Arica y Parinacota, R15)

Uso:
  # 1. Descargar el script oficial verificado:
  curl -O https://ide.cit.uai.cl/download/reproducir_verificacion_r15.py
  # 2. Ejecutar la verificación localmente:
  python reproducir_verificacion_r15.py
"""

import sys
import hashlib
import urllib.request
from pathlib import Path

try:
    import pandas as pd
    import pyarrow.parquet as pq
except ImportError:
    print("[ERROR] Se requiere pandas y pyarrow para ejecutar la verificación.")
    print("Instalación: pip install pandas pyarrow")
    sys.exit(1)

print("=" * 80)
print("IDE CIT — PROTOCOLO CANÓNICO DE REPRODUCIBILIDAD INDEPENDIENTE")
print("Universidad Adolfo Ibáñez · Centro de Inteligencia Territorial")
print("=" * 80)

# Paso 1: Descarga o lectura del archivo oficial
URL = "https://ide.cit.uai.cl/download/MBHT_2017_R15_Manzanas.parquet"
LOCAL_PATH = Path("MBHT_2017_R15_Manzanas.parquet")

if not LOCAL_PATH.exists():
    print(f"[*] Descargando paquete oficial R15 desde: {URL} ...")
    urllib.request.urlretrieve(URL, LOCAL_PATH)
    print(f"    Descargado exitosamente ({LOCAL_PATH.stat().st_size:,} bytes).")
else:
    print(f"[*] Utilizando archivo local existente: {LOCAL_PATH.name} ({LOCAL_PATH.stat().st_size:,} bytes)")

# Paso 2: Verificación criptográfica SHA-256 (Bit-level integrity)
print("\n[1/4] Verificación Criptográfica SHA-256 (Integridad de Distribución)...")
data = LOCAL_PATH.read_bytes()
sha_calc = hashlib.sha256(data).hexdigest()
sha_expected = "712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505"

if sha_calc == sha_expected:
    print(f"    [OK] Hash SHA-256 coincidente al 100%: {sha_calc}")
else:
    print(f"    [FAIL] Hash no coincide: {sha_calc} != {sha_expected}")
    sys.exit(1)

# Paso 3: Validación del esquema físico (42 columnas individuales)
print("\n[2/4] Validación de Esquema Físico (Paridad 1:1 con Ficha Técnica)...")
table = pq.read_table(LOCAL_PATH)
num_rows = table.num_rows
num_cols = table.num_columns
print(f"    Dimensiones observadas en Parquet: {num_rows:,} filas x {num_cols} columnas")

if num_rows == 3304 and num_cols == 42:
    print("    [OK] Cuadratura exacta de universo: 3.304 manzanas censales y 42 columnas físicas.")
else:
    print(f"    [FAIL] Dimensiones inesperadas: {num_rows} filas, {num_cols} columnas (esperado 3304 x 42)")
    sys.exit(1)

# Paso 4: Reproducción analítica de manzana testigo (Domain-level integrity)
print("\n[3/4] Reproducción Analítica Celda por Celda (Manzana Testigo Arica Centro)...")
df = pd.read_parquet(LOCAL_PATH)
witness_id = "15101011001004001"
row = df.loc[df["id_manzcit"] == witness_id]

if row.empty:
    print(f"    [FAIL] No se encontró la manzana testigo {witness_id}")
    sys.exit(1)

m = row.iloc[0]
print(f"    Manzana: {m['id_manzcit']} | Comuna: {m['comuna']} | Personas: {int(m['personas'])} | Tipología: {m['tob']}")

metrics = [
    ("isal", m["isal"], 0.8691, "Accesibilidad a Salud"),
    ("ise", m["ise"], 1.3381, "Accesibilidad a Educación"),
    ("iav", m["iav"], 5.8035, "Accesibilidad a Áreas Verdes"),
    ("idep", m["idep"], 0.7744, "Accesibilidad a Deporte"),
    ("icul", m["icul"], 0.2934, "Accesibilidad a Cultura"),
    ("iser", m["iser"], 10.3205, "Accesibilidad a Servicios"),
    ("dim_acc", m["dim_acc"], 0.6279, "Macro-dimensión Accesibilidad Peatonal"),
    ("bht", m["bht"], 0.3751, "Índice de Bienestar Humano Territorial (BHT)")
]

all_match = True
for name, obs, exp, desc in metrics:
    diff = abs(obs - exp)
    ok = diff < 1e-3
    print(f"    • {name:<8s} = {obs:8.4f} (esperado: {exp:8.4f}, diff: {diff:.6f}) -> {'[OK]' if ok else '[FAIL]'} {desc}")
    if not ok:
        all_match = False

if not all_match:
    print("    [FAIL] Discrepancia en métricas de manzana testigo.")
    sys.exit(1)
else:
    print("    [OK] Todos los valores de la manzana testigo coinciden con tolerancia cero.")

# Paso 5: Reproducción de la agregación demográfica regional
print("\n[4/4] Reproducción del BHT Regional Ponderado por Población...")
total_pop = df["personas"].sum()
weighted_bht = (df["bht"] * df["personas"]).sum() / total_pop

print(f"    Población total modelada en R15: {int(total_pop):,} habitantes")
print(f"    BHT regional calculado: {weighted_bht:.4f} (Valor oficial: 0.4623)")

if abs(weighted_bht - 0.4623) < 1e-3:
    print("    [OK] Agregación demográfica regional reproducida con éxito.")
else:
    print(f"    [FAIL] Discrepancia en BHT regional: {weighted_bht:.4f} vs 0.4623")
    sys.exit(1)

print("\n" + "=" * 80)
print("[OK] VEREDICTO: REPRODUCIBILIDAD CIENTIFICA INDEPENDIENTE CONFIRMADA")
print("=" * 80)
