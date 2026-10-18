# 🏛️ JUSTIFICACIÓN TÉCNICA Y DE GESTIÓN FINANCIERA (FinOps)
## Arquitectura en la Nube de la Infraestructura de Datos Espaciales (IDE CIT)
### Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez

> **Código de Documento**: CIT-UAI-FINOPS-2026-OCT-01  
> **Propósito**: Justificación auditable de diseño arquitectónico, perfil de riesgo y control de costos en AWS.  
> **Destinatarios**: Dirección de Finanzas, Auditoría Interna DTI, Comités Técnicos CIT-UAI.  
> **Fecha de Emisión**: 18 de octubre de 2026  
> **Vigencia**: 2026 – 2027  

---

## 1. Contexto Operativo y Perfil de Demanda Territorial

La **IDE CIT** (`https://ide.cit.uai.cl`) es una plataforma académica y de servicio público diseñada para proveer acceso libre y soberano a la cartografía del **Censo 2024**, la **Matriz de Bienestar Humano Territorial (MBHT 2017/2024)** y la **Planificación Espacial Marina (PEM)** de Chile.

### Perfil de Tráfico de la Plataforma:
- **Naturaleza de la Demanda**: Especializada, analítica e institucional. Sus usuarios principales son profesionales de los 16 Gobiernos Regionales (GORE), 345 municipios, ministerios sectoriales (SUBDERE, MINVU, Medio Ambiente), centros de investigación y universidades.
- **Frecuencia de Uso**: Consultas periódicas profundas. No es un portal de consumo masivo efímero (como redes sociales o prensa digital), sino una infraestructura donde un analista descarga una cobertura cada cierto tiempo y trabaja sobre ella en herramientas de escritorio (QGIS, ArcGIS, Python).
- **Inventario Físico de Archivos en `download/`**:
  - *Navegación Web (HTML, CSS, JS, STAC JSON)*: Entre **2 KB y 875 KB** por recurso. Una sesión completa de navegación consume entre **2 y 4 MB**.
  - *GeoParquet Regional (R15, R13, etc.)*: Entre **2,4 MB y 50 MB**.
  - *GeoParquet Nacional (Censo 2024, MBHT, Red Vial)*: Entre **215 MB y 270 MB**.
  - *GeoPackage Nacional (`.gpkg`)*: Entre **340 MB y 477 MB**.

---

## 2. Matriz de Decisiones Arquitectónicas y Justificación FinOps

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               DECISIONES ARQUITECTÓNICAS AUDITADAS                                │
├───────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┤
│ Decisión de Diseño            │ Justificación de Ciberseguridad │ Justificación FinOps / Costo    │
├───────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ 1. Desactivación de AWS WAF   │ Riesgo DoS bajo en nicho acad.  │ Ahorro directo de $84 USD/año   │
│ 2. Alarma CloudWatch 25 GB/h  │ Detección de bots en ~60 desc.  │ Costo $0 (Capa gratuita AWS)    │
│ 3. S3 Versioning + Expire 30d │ Recuperación ante borrado acc.  │ Sin acumulación residual        │
│ 4. Error 404 Ligero (3,7 KB)  │ Cero falsos 200 en Parquet/QGIS │ Ahorro 99,6% ancho banda error  │
│ 5. S3 Logging + Expire 90d    │ Trazabilidad forense (Athena)   │ Purga automática (< $0,15/mes)  │
│ 6. PriceClass_200 (Chile)     │ Latencia < 25ms en Santiago     │ Diferencia < $0,30 USD/mes      │
└───────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

---

### Decisión 1: Desactivación de AWS WAF y Adopción de Alarma de Egress a Costo Cero ($0)

#### Análisis de Costo-Beneficio:
- El servicio **AWS WAFv2** tiene una tarifa base fija de **\$5,00 USD / mes** por WebACL más **\$1,00 USD / mes** por regla activa. Mantener un WebACL con dos reglas de rate-limiting representa un costo fijo ineludible de **\$7,00 USD / mes** (\$84,00 USD al año).
- El costo operativo de almacenamiento y transferencia normal de la IDE CIT en AWS CloudFront y S3 oscila entre **\$1,50 y \$2,50 USD al mes** (\$18 a \$30 USD al año).
- **Dictamen Financiero**: Pagar \$84 USD anuales de WAF para proteger una plataforma cuyo costo base es de \$25 USD anuales significa **triplicar artificialmente el presupuesto de la universidad** sin que exista una amenaza real de ataques masivos distribuidos que justifiquen ese gasto recurrente.

#### Mitigación Alternativa Adoptada:
- Se implementó la alarma de Amazon CloudWatch **`ide-cit-cloudfront-high-egress-alarm`**, calibrada en **25 GB por hora** (26.843.545.600 bytes) utilizando la métrica `BytesDownloaded`.
- **Cálculo de Sensibilidad**:
  - 25 GB en una hora equivale a que una misma entidad descargue **más de 65 veces consecutivas el GeoPackage nacional más pesado** (400 MB) en 60 minutos.
  - En el uso institucional normal más intenso (ej: 10 analistas descargando coberturas en la misma hora), el consumo no supera los **3 a 4 GB**.
  - **Exposición Financiera Máxima**: En CloudFront para Sudamérica, 25 GB de datos transferidos equivalen a **~\$2,75 USD**. Si un bot o script en bucle descarga datos, la alarma se dispara cuando el incidente apenas ha costado menos de tres dólares, permitiendo intervención técnica inmediata antes de que se genere un cobro significativo.
  - **Costo de la Alarma**: **\$0,00 USD** (cubierto permanentemente por el AWS Free Tier de hasta 10 alarmas CloudWatch).

---

### Decisión 2: S3 Bucket Versioning con Purga Automática de Versiones Previas (30 Días)

#### Justificación Técnica:
- La plataforma custodia datos oficiales del Censo 2024. Un error humano en un script de despliegue (`aws s3 sync --delete`) o una instrucción errónea podría eliminar coberturas críticas.
- El versionamiento (`Versioning: Enabled`) garantiza que cualquier archivo eliminado o sobreescrito conserve su versión histórica recuperable.

#### Control FinOps:
- Sin una regla de ciclo de vida, cada actualización de un archivo de 270 MB acumularía versiones anteriores de forma indefinida en S3 Standard (\$0,023/GB-mes).
- Se configuró la regla **`ExpireNoncurrentVersionsAfter30Days`**: las versiones anteriores se eliminan de forma automática e irreversible a los **30 días**, brindando una ventana de recuperación suficiente sin generar pasivos de almacenamiento a largo plazo.

---

### Decisión 3: Corrección de Respuestas 404 (De 875 KB a 3,7 KB)

#### Justificación Técnica y de Red:
- Anteriormente, ante cualquier petición a un archivo inexistente, CloudFront devolvía `index.html` (875 KB) con código 404.
- Si un script de Python o un usuario en QGIS solicitaba una capa inexistente, recibía 875 KB de código HTML que intentaba procesar, generando errores crípticos y consumiendo ancho de banda innecesario.
- Se implementó la página dedicada `public/404.html` de solo **3,7 KB**.
- **Impacto FinOps**: Reducción del **99,6%** en la transferencia de datos por cada error 404, mitigando el costo de escaneos automáticos de vulnerabilidades o rutas obsoletas.

---

### Decisión 4: Clase de Precio CloudFront (`PriceClass_200` — Sudamérica)

#### Justificación de Servicio Público:
- `PriceClass_100` excluía los Edge Locations de Sudamérica, forzando a que todo el tráfico chileno fuera atendido desde Miami o Virginia (latencia RTT: ~140 ms).
- Al actualizar a **`PriceClass_200`**, las peticiones son resueltas en el Edge PoP de **Santiago de Chile (`SCL50-C1`)**, reduciendo la latencia percibida a **< 25 ms**.

#### Impacto FinOps:
- La tarifa de transferencia en Sudamérica es de \$0,110 / GB frente a \$0,085 / GB en Norteamérica (diferencia de \$0,025 / GB).
- Para un consumo proyectado de 20 GB mensuales, el costo adicional es de **\$0,50 USD al mes** (cincuenta centavos de dólar), plenamente justificado por la velocidad de acceso para las instituciones chilenas.

---

### Decisión 5: Trazabilidad y Logs en Frío con Retención a 90 Días

#### Justificación de Cumplimiento:
- Para auditorías de seguridad y requerimientos de la DTI de la UAI, es indispensable registrar qué IPs acceden y descargan coberturas.
- Se habilitó el logging hacia el bucket dedicado **`ide-cit-access-logs-us-east-1`**.

#### Control FinOps:
- Los logs se transfieren comprimidos (`.gz`).
- Se implementó la regla **`ExpireLogsAfter90Days`**: pasan a `STANDARD_IA` a los 30 días y se purgan a los 90 días.
- Costo estimado de almacenamiento de logs: **inferior a \$0,15 USD al mes**.

---

## 3. Presupuesto Mensual Proyectado (Línea Base Plana)

```
┌────────────────────────────────────────────────────────┬──────────────────────┐
│ Concepto de Infraestructura en AWS                     │ Costo Mensual Est.   │
├────────────────────────────────────────────────────────┼──────────────────────┤
│ 1. Almacenamiento S3 (Datos Oficiales ~5 GB)           │ $0,12 USD            │
│ 2. Almacenamiento S3 Versionado (Retención 30 días)    │ $0,05 USD            │
│ 3. Transferencia de Datos CloudFront Egress (10-25 GB) │ $1,10 - $2,75 USD    │
│ 4. Peticiones HTTPS CloudFront (~50.000 req/mes)       │ $0,05 USD            │
│ 5. Almacenamiento de Logs de Acceso (90 días)          │ $0,10 USD            │
│ 6. Alarma de Monitoreo CloudWatch (25 GB/h)            │ $0,00 USD (Free Tier)│
│ 7. Lambda STAC Search (Consultas dinámicas < 10.000)   │ $0,00 USD (Free Tier)│
├────────────────────────────────────────────────────────┼──────────────────────┤
│ TOTAL MENSUAL ESTIMADO                                 │ $1,42 – $3,07 USD    │
└────────────────────────────────────────────────────────┴──────────────────────┘
```

---

## 4. Conclusión para Auditorías

La arquitectura implementada no presenta sobreingeniería ni gastos fijos desproporcionados. Aplica el estándar de **máxima austeridad institucional con resiliencia activa**:
1. El bucket está cerrado por OAC y cifrado por defecto.
2. Los datos censales están protegidos contra borrado accidental mediante Versioning temporal.
3. La universidad está protegida financieramente ante descargas anómalas mediante la alarma de 25 GB.
4. Los costos se mantienen en una **línea base plana de menos de \$3,50 USD al mes**, asegurando estabilidad presupuestaria y trazabilidad forense completa.
