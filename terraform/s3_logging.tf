# Bucket S3 Dedicado para Auditoría y Logs de Acceso: ide-cit-access-logs-us-east-1
resource "aws_s3_bucket" "logging" {
  bucket = "${var.project_name}-access-logs-${var.aws_region}"
}

# Control de Propiedad de Objetos: BucketOwnerPreferred para compatibilidad con entrega de logs CloudFront
resource "aws_s3_bucket_ownership_controls" "logging" {
  bucket = aws_s3_bucket.logging.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Bloqueo total de acceso público en el bucket de logs
resource "aws_s3_bucket_public_access_block" "logging" {
  bucket = aws_s3_bucket.logging.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Cifrado en reposo para los registros de auditoría
resource "aws_s3_bucket_server_side_encryption_configuration" "logging" {
  bucket = aws_s3_bucket.logging.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = false
  }
}

# Permisos de ACL para el grupo LogDelivery de AWS
resource "aws_s3_bucket_acl" "logging" {
  depends_on = [aws_s3_bucket_ownership_controls.logging]

  bucket = aws_s3_bucket.logging.id

  access_control_policy {
    grant {
      grantee {
        type = "Group"
        uri  = "http://acs.amazonaws.com/groups/s3/LogDelivery"
      }
      permission = "WRITE"
    }
    grant {
      grantee {
        type = "Group"
        uri  = "http://acs.amazonaws.com/groups/s3/LogDelivery"
      }
      permission = "READ_ACP"
    }
    grant {
      grantee {
        id   = data.aws_canonical_user_id.current.id
        type = "CanonicalUser"
      }
      permission = "FULL_CONTROL"
    }
    owner {
      id = data.aws_canonical_user_id.current.id
    }
  }
}

data "aws_canonical_user_id" "current" {}

# Regla de Ciclo de Vida: Transición a Standard-IA a los 30 días, expiración a los 90 días
resource "aws_s3_bucket_lifecycle_configuration" "logging" {
  bucket = aws_s3_bucket.logging.id

  rule {
    id     = "ExpireLogsAfter90Days"
    status = "Enabled"

    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = var.log_retention_days
    }
  }
}
