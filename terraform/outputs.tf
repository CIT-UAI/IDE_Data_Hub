output "cloudfront_distribution_id" {
  description = "ID de la distribución CloudFront principal"
  value       = aws_cloudfront_distribution.main.id
}

output "cloudfront_domain_name" {
  description = "Nombre de dominio asignado por CloudFront (d1owm1ug2fpvep.cloudfront.net)"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "s3_storage_bucket_arn" {
  description = "ARN del bucket S3 principal de almacenamiento de datos"
  value       = aws_s3_bucket.main.arn
}

output "s3_logging_bucket_arn" {
  description = "ARN del bucket S3 de logs de acceso y auditoría"
  value       = aws_s3_bucket.logging.arn
}

output "waf_web_acl_arn" {
  description = "ARN del WebACL WAFv2 con Rate Limiting activo"
  value       = aws_wafv2_web_acl.shield.arn
}
