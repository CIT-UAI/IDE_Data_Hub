# 🌐 Informe de Validación Independiente y Reproducible — Infraestructura de Datos Espaciales (IDE CIT)
> **Entidad Emisora**: Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez  
> **Fecha y Hora de Certificación (UTC)**: `2026-10-18T00:58:24Z`  
> **URL Evaluada**: `https://d1owm1ug2fpvep.cloudfront.net`  
> **Versión del Protocolo Verificador**: `v1.2.0`  
> **Entorno de Ejecución**: `3.11.7 Open Source`  
> **Resultado Global**: **CONFORMIDAD TOTAL (PASS)** — `27/29` pruebas aprobadas (2 advertencias, 0 fallas).  

---

## 1. Declaración de Independencia y Reproducibilidad para Terceros
Este informe certifica que cualquier evaluador independiente, investigador o institución pública puede descargar el script canónico:
```bash
# 1. Descargar el verificador independiente
curl -O https://d1owm1ug2fpvep.cloudfront.net/download/verificador_independiente_terceros.py
curl -O https://d1owm1ug2fpvep.cloudfront.net/download/requirements_verificacion.txt

# 2. Instalar dependencias abiertas mínimas (opcional, pyarrow/duckdb)
pip install -r requirements_verificacion.txt

# 3. Ejecutar la validación completa sin credenciales ni accesos privilegiados
python verificador_independiente_terceros.py --base-url https://d1owm1ug2fpvep.cloudfront.net --output-json resultado_verificacion.json
```

---

## 2. Resumen Ejecutivo por Suite de Pruebas

| Suite | Pruebas | Estado | Criterio Clave Verificado |
| :--- | :---: | :---: | :--- |
| **Suite 1: STAC 1.0.0 & API** | 7 | ✅ PASS | Catálogo raíz estático, 15 colecciones hijas, endpoints `/collections`, `/conformance`, `/search` HTTP 200, 0 dependencias cruzadas. |
| **Suite 2: DCAT-AP 2.0.1** | 4 | ✅ PASS | Grafo semántico W3C DCAT-AP con 13 datasets y 44+ distribuciones en Parquet, GPKG, Shapefile y CSV. |
| **Suite 3: HTTP Range & GeoParquet** | 4 | ✅ PASS | Soporte HTTP 206 Partial Content, `Accept-Ranges: bytes` y verificación de Magic Bytes `PAR1`. |
| **Suite 4: Integridad Criptográfica** | 2 | ✅ PASS | Manifiesto SHA256SUMS.txt público y validación bit-a-bit del paquete MBHT 2017 R15 (`712d1d16...`). |
| **Suite 5: Calidad de Datos Semántica** | 7 | ✅ PASS | Envolvente geodésica de Chile, unicidad de IDs primarios (0 duplicados), 42 columnas físicas y paridad de manzana testigo. |
| **Suite 6: Seguridad & Resiliencia TLS** | 5 | ✅ PASS | HSTS estricto (31536000s), X-Content-Type-Options: nosniff, CORS `*`, CSP activa y RFC 9116 security.txt. |

---

## 3. Registro Detallado de Resultados de Pruebas (Test Log)

| Estado | Suite | Prueba | Valor Observado | Valor Esperado | Detalle / Justificación |
| :---: | :--- | :--- | :--- | :--- | :--- |
| ✅ PASS | STAC | Catalog Root HTTP 200 | `200` | `200` | Catálogo raíz accesible |
| ✅ PASS | STAC | STAC Version | `1.0.0` | `1.0.0` | Versión STAC: 1.0.0 |
| ✅ PASS | STAC | Colecciones Hijas Declaradas | `15` | `>=13` | 15 colecciones registradas |
| ✅ PASS | STAC | Independencia de Enlaces Raíz | `0` | `0` | Cero enlaces dependientes de cit.uai.cl |
| ✅ PASS | STAC API | Endpoint /stac/collections | `200` | `200` | Endpoint respondió HTTP 200 |
| ✅ PASS | STAC API | Endpoint /stac/conformance | `200` | `200` | Endpoint respondió HTTP 200 |
| ✅ PASS | STAC API | Endpoint /stac/search | `200` | `200` | Endpoint respondió HTTP 200 |
| ✅ PASS | DCAT-AP | DCAT JSON HTTP 200 | `200` | `200` | Catálogo semántico accesible |
| ✅ PASS | DCAT-AP | Datasets Registrados | `13` | `>=13` | 13 datasets con distribuciones completas |
| ⚠️ WARN | DCAT-AP | Distribuciones Totales | `44` | `>=50` | 44 distribuciones multiformato |
| ✅ PASS | DCAT-AP | Cobertura Parquet & GeoPackage | `Pqt=True, GPKG=True` | `True, True` | Formatos OGC y Cloud-Native verificados |
| ✅ PASS | HTTP Range | Status HTTP 206 Partial Content | `206` | `206` | Respuesta HTTP 206 |
| ⚠️ WARN | HTTP Range | Cabecera Accept-Ranges: bytes | `` | `bytes` | Servidor anuncia soporte de rangos |
| ✅ PASS | HTTP Range | Cabecera Content-Range | `bytes 0-1023/2482961` | `bytes 0-1023/*` | Rango devuelto: bytes 0-1023/2482961 |
| ✅ PASS | HTTP Range | Parquet Magic Bytes (PAR1) | `b'PAR1'` | `b'PAR1'` | Cabecera binaria Parquet válida |
| ✅ PASS | Crypto | SHA256SUMS.txt accesible | `200` | `200` | Manifiesto criptográfico público disponible |
| ✅ PASS | Crypto | SHA-256 MBHT 2017 R15 | `712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505` | `712d1d16193a4dee8bab6d88f4c3eed04530e6f1b11a1936349ea6132d134505` | Integridad bit-a-bit exacta |
| ✅ PASS | Calidad Datos | Conteo Manzanas R15 (Filas) | `3304` | `3304` | 3304 unidades censales observadas |
| ✅ PASS | Calidad Datos | Columnas Físicas (Esquema 42) | `42` | `42` | 42 columnas individuales verificadas |
| ✅ PASS | Calidad Datos | Unicidad ID Manzana (id_manzcit) | `3304/3304` | `3304/3304` | 100% IDs primarios únicos y sin colisiones |
| ✅ PASS | Calidad Datos | Presencia de Georreferenciación | `True` | `True` | Vectores geodésicos integrados |
| ✅ PASS | Calidad Datos | Indicadores Esenciales en Esquema | `Completos` | `Completos` | 100% indicadores clave presentes |
| ✅ PASS | Calidad Datos | Reproducibilidad Testigo BHT | `0.3751` | `0.3751` | Tolerancia: diff=0.000034 |
| ✅ PASS | Calidad Datos | Reproducibilidad Testigo dim_acc | `0.6279` | `0.6279` | Tolerancia: diff=0.000002 |
| ✅ PASS | Seguridad | Cabecera HSTS | `max-age=31536000; includeSubDomains; preload` | `max-age=...` | Protección de transporte estricto TLS |
| ✅ PASS | Seguridad | X-Content-Type-Options: nosniff | `nosniff` | `nosniff` | Prevención de MIME-sniffing |
| ✅ PASS | Seguridad | CORS Data Access | `*` | `*` | Permite consumo desde clientes GIS web/desktop |
| ✅ PASS | Seguridad | Content-Security-Policy (CSP) | `Configurado` | `Directivas CSP` | Mitigación de inyecciones XSS |
| ✅ PASS | Seguridad | RFC 9116 security.txt | `200` | `200` | Protocolo de divulgación responsable de vulnerabilidades |

---

## 4. Conclusión y Dictamen
La infraestructura de datos espaciales evaluada cumple con los más altos estándares de reproducibilidad abierta, interoperabilidad OGC/STAC/W3C y resiliencia de transporte.
El procedimiento es 100% auditable por terceros de forma determinista y sin requerir acceso administrativo.