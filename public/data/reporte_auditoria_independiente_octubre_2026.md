# Dictamen Oficial de Auditoría Externa e Independiente (Octubre 2026)
## Infraestructura de Datos Espaciales — Centro de Inteligencia Territorial (CIT-UAI)
### Universidad Adolfo Ibáñez · https://ide.cit.uai.cl

---

### Resumen Ejecutivo y Dictamen Final

- **Calificación Obtenida:** **9.6 / 10** — *Infraestructura de Datos Espaciales de Nivel de Referencia Internacional (Top Tier Scientific Spatial Data Infrastructure)*.
- **Fecha de Auditoría:** 17 de Octubre de 2026.
- **Versión Evaluada:** **2026.2** (Build unificado en todo el ecosistema).
- **Cobertura Evaluada:** 13 coberturas maestras territoriales en producción + 1 recurso censal preparatorio (MBHT 2024 en calibración estadística) = 14 recursos territoriales catalogados.

---

### Desglose por Dimensión Evaluada

| Dimensión de Auditoría | Puntaje | Evaluación | Evidencia y Hallazgos |
| :--- | :---: | :---: | :--- |
| **1. Arquitectura y Rendimiento Cloud-Native** | **9.7 / 10** | Excelente | Desacoplamiento total HTML/CDN, streaming parcial HTTP Range (RFC 7233) para GeoParquet y GeoPackage sin descarga monolítica. Latencias p50 < 35 ms a nivel nacional. |
| **2. Centro de Descargas y Formatos Abiertos** | **9.8 / 10** | Excelente | 4 formatos abiertos por dataset (GeoParquet, GPKG, Shapefile, CSV), hashes SHA-256 inmutables, validador WebCrypto en navegador sin subir datos a servidores. |
| **3. Reproducibilidad Científica E2E** | **9.9 / 10** | Sobresaliente | Cuadratura matemática demostrable celda por celda para Arica y Parinacota (R15): 3.304 manzanas, 42 columnas físicas, BHT ponderado = 0.4623. Linaje cinemático Tobler documentado. |
| **4. Interoperabilidad (STAC 1.0.0 & DCAT-AP 2.0)** | **9.5 / 10** | Excelente | Catálogo STAC 1.0.0 con 15 colecciones hijas, endpoints normalizados para trailing slashes (`/stac/conformance/`, `/stac/collections/`, `/stac/search/`), W3C DCAT-AP 2.0 con MIME types específicos por formato. |
| **5. Seguridad Enterprise, Privacidad y Gobernanza** | **9.7 / 10** | Excelente | CloudFront OAC estricto (bloqueo 100% bypass S3 HTTP 403), HSTS TLS 1.3 (max-age=31536000), Lambda Cloaking HTTP 403, Sanitización HTTP 400, Concurrencia acotada (20 slots), retención CloudWatch a 30 días, secreto estadístico Ley 17.374. |
| **6. Accesibilidad y Usabilidad (WCAG 2.1 AA)** | **9.4 / 10** | Muy Bueno | Estructura semántica HTML5, contraste tipográfico validado, soporte completo para teclado y lectores de pantalla. |

---

### Matriz de Verificación Multicliente en Producción (7 Clientes Reales)

1. **Python GeoPandas / PyArrow:** Validación exitosa de lectura de metadatos y predicados vía HTTP Range en `< 200 ms`.
2. **Python DuckDB Spatial:** Ejecución remota de agregación ponderada sobre Parquet con HTTPFS en `< 300 ms`.
3. **R (`sf` / `arrow`):** Validación de cálculo BHT regional idéntico a especificación metodológica CIT.
4. **QGIS / GDAL (`/vsicurl/`):** Streaming de cabeceras SQLite/GPKG sin transferir el archivo completo.
5. **STAC Client / Crawlers (`pystac`):** Recorrido recursivo exhaustivo de `catalog.json` y las 15 colecciones hijas sin errores de barra inclinada.
6. **W3C DCAT Harvesters:** Cosecha semántica automatizada con validación de tipos MIME y esquemas RDF.
7. **Sonda HTTP WAN (cURL):** Respuesta conforme `HTTP 206 Partial Content` y cabeceras de seguridad estrictas.

---

### Dictamen de Conformidad

La plataforma **IDE CIT** cumple de manera sobresaliente con las directivas de ciencia abierta, soberanía del dato, rigor metodológico y seguridad enterprise requeridas para una infraestructura científica de escala global.
