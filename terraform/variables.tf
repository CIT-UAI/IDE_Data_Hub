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

variable "rate_limit_general" {
  description = "Límite de peticiones por IP en 5 minutos para tráfico general"
  type        = number
  default     = 2000
}

variable "rate_limit_downloads" {
  description = "Límite de descargas por IP en 5 minutos en rutas /download/ (Cortar antes de pagar)"
  type        = number
  default     = 500
}

variable "log_retention_days" {
  description = "Días de retención para los logs de acceso antes de su purga automática"
  type        = number
  default     = 90
}
