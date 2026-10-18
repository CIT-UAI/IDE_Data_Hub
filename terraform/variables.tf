variable "aws_region" {
  description = "Región primaria de AWS para los recursos de la IDE CIT"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Nombre de dominio canónico institucional"
  type        = string
  default     = "ide.cit.uai.cl"
}

variable "project_name" {
  description = "Identificador del proyecto"
  type        = string
  default     = "ide-cit"
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
  default     = "production"
}

variable "enable_waf" {
  description = "Habilitar AWS WAFv2 ($7/mes fijo). Por defecto desactivado para mantener costo plano mínimo ($0 fijo)."
  type        = bool
  default     = false
}

variable "cloudwatch_egress_threshold_gb" {
  description = "Umbral de anomalía de descarga en gigabytes por hora para la alarma gratuita de CloudWatch"
  type        = number
  default     = 25
}

variable "rate_limit_general" {
  description = "Límite de peticiones por IP en 5 minutos para tráfico general (si WAF está activo)"
  type        = number
  default     = 2000
}

variable "rate_limit_downloads" {
  description = "Límite de descargas por IP en 5 minutos en rutas /download/ (si WAF está activo)"
  type        = number
  default     = 500
}

variable "log_retention_days" {
  description = "Días de retención para los logs de acceso antes de su purga automática"
  type        = number
  default     = 90
}
