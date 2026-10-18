# 🏛️ Infraestructura como Código (IaC) — IDE CIT (CIT-UAI)

Este directorio contiene la definición formal y declarativa en **Terraform** de toda la arquitectura en la nube de la **IDE CIT** en Amazon Web Services (AWS), siguiendo las mejores prácticas de seguridad, resiliencia y FinOps.

---

## 📐 Componentes Declarados

1. **Almacenamiento Seguro (`s3_storage.tf`)**:
   - Bucket S3 `ide.cit.uai.cl` con `Block Public Access` al 100%.
   - Cifrado en reposo SSE-S3 (`AES256`).
   - `Versioning: Enabled` para protección contra borrados accidentales.
   - Reglas de ciclo de vida: transición a `INTELLIGENT_TIERING` para descargas >128 KB, purga de multiparts tras 7 días y expiración de versiones no actuales tras 30 días.
   - Política de bucket restringida a CloudFront mediante **Origin Access Control (OAC)** y rechazo obligatorio de peticiones no TLS (`aws:SecureTransport: false`).

2. **Auditoría y Trazabilidad (`s3_logging.tf`)**:
   - Bucket dedicado `ide-cit-access-logs-us-east-1` con expiración automática de logs a los 90 días.
   - S3 Server Access Logging activado (prefijo `s3/`).
   - CloudFront Standard Logging activado (prefijo `cloudfront/`).

3. **Defensa Perimetral Proactiva ("Cortar antes de pagar") (`waf.tf`)**:
   - AWS WAFv2 WebACL con Scope `CLOUDFRONT`.
   - **Regla 1**: Rate limiting en `/download/*` (máximo 500 descargas / 5 min por IP -> bloqueo con HTTP 429).
   - **Regla 2**: Rate limiting general (máximo 2.000 peticiones / 5 min por IP -> bloqueo con HTTP 429).

4. **Distribución Edge CDN (`cloudfront.tf`)**:
   - Clase de precio `PriceClass_200` con presencia directa en el Edge Location de Santiago de Chile (`SCL50-C1`).
   - Orígenes: S3 con OAC + Lambda STAC Search con Origin Cloaking (`X-CIT-Origin-Verify`).
   - Política de cabeceras de seguridad: CSP sin CDNs externas no autorizadas, HSTS de 2 años con preload, X-Content-Type-Options `nosniff`, X-Frame-Options `SAMEORIGIN`.
   - Respuestas de error personalizadas: Códigos 403 y 404 redirigidos a `/404.html` (3,7 KB) devolviendo el código HTTP 404 nativo.

5. **Alertas y Monitoreo FinOps (`cloudwatch.tf`)**:
   - Alarma de CloudWatch en `BytesDownloaded` (>50 GB en 1 hora) para detección temprana de anomalías.

6. **Auditoría Forense con Athena (`athena_queries.sql`)**:
   - Consultas SQL listas para ejecutar en Amazon Athena para inspeccionar scrapers, descargas masivas y bloqueos 429.

---

## 🚀 Despliegue y Gestión

```bash
# 1. Inicializar plugins y proveedores
terraform init

# 2. Validar sintaxis y configuración
terraform validate

# 3. Planificar cambios
terraform plan

# 4. Aplicar en infraestructura (requiere credenciales AWS con permisos IAM adecuados)
terraform apply
```
