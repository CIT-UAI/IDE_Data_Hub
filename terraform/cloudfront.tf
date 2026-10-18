# Origin Access Control (OAC) para S3
resource "aws_cloudfront_origin_access_control" "s3_oac" {
  name                              = "${var.project_name}-s3-oac"
  description                       = "OAC para acceso exclusivo a S3 desde CloudFront IDE CIT"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# Política de Cabeceras de Respuesta Seguras (CSP, HSTS, X-Content-Type)
resource "aws_cloudfront_response_headers_policy" "security" {
  name    = "CIT-IDE-Strict-Security-And-CORS-Policy-v1"
  comment = "Cabeceras de seguridad estrictas, erradicación de unpkg y soporte CORS RFC 7233"

  cors_config {
    access_control_allow_credentials = false
    access_control_max_age_sec       = 86400
    origin_override                  = true

    access_control_allow_headers {
      items = ["Authorization", "Content-Type", "Range", "X-Requested-With", "x-cit-origin-verify"]
    }

    access_control_allow_methods {
      items = ["GET", "HEAD", "OPTIONS"]
    }

    access_control_allow_origins {
      items = ["*"]
    }

    access_control_expose_headers {
      items = ["Content-Length", "Content-Range", "ETag", "Accept-Ranges"]
    }
  }

  security_headers_config {
    content_security_policy {
      content_security_policy = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net data:; img-src 'self' data: blob: https://*.tile.openstreetmap.org https://engine.matrizbht.cl https://*.basemaps.cartocdn.com; connect-src 'self' https://ide.cit.uai.cl https://engine.matrizbht.cl https://*.tile.openstreetmap.org https://*.basemaps.cartocdn.com; object-src 'none'; base-uri 'self'; frame-ancestors 'self';"
      override                = true
    }

    content_type_options {
      override = true
    }

    frame_options {
      frame_option = "SAMEORIGIN"
      override     = true
    }

    referrer_policy {
      referrer_policy = "strict-origin-when-cross-origin"
      override        = true
    }

    strict_transport_security {
      access_control_max_age_sec = 63072000
      include_subdomains         = true
      preload                    = true
      override                   = true
    }
  }
}

# Distribución CloudFront Principal
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = "PriceClass_200" # Edge PoP en Santiago de Chile y Sudamérica
  web_acl_id          = aws_wafv2_web_acl.shield.arn

  aliases = [var.domain_name]

  # Logging Standard hacia el bucket de auditoría
  logging_config {
    bucket          = aws_s3_bucket.logging.bucket_domain_name
    include_cookies = false
    prefix          = "cloudfront/"
  }

  # Origen 1: Bucket S3 de Datos y Portales
  origin {
    domain_name              = aws_s3_bucket.main.bucket_regional_domain_name
    origin_id                = "S3-${var.domain_name}"
    origin_access_control_id = aws_cloudfront_origin_access_control.s3_oac.id
  }

  # Origen 2: Lambda STAC Search (Function URL con Origin Cloaking)
  origin {
    domain_name = "vm3dfibiibax4ciev6e2opsfu40jkzzz.lambda-url.us-east-1.on.aws"
    origin_id   = "Lambda-STAC-Search"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-CIT-Origin-Verify"
      value = "cit-uai-stac-sec-token-2026-auth-prod"
    }
  }

  # Comportamiento por Defecto (S3)
  default_cache_behavior {
    target_origin_id       = "S3-${var.domain_name}"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]

    response_headers_policy_id = aws_cloudfront_response_headers_policy.security.id

    forwarded_values {
      query_string = false
      headers      = ["Range", "Origin", "Access-Control-Request-Headers", "Access-Control-Request-Method"]

      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400
    max_ttl     = 31536000
  }

  # Comportamiento para Búsqueda Espacial Dinámica STAC (/stac/search*)
  ordered_cache_behavior {
    path_pattern           = "/stac/search*"
    target_origin_id       = "Lambda-STAC-Search"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "POST"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      headers      = ["Range", "Origin", "Accept", "Content-Type"]

      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 60
    max_ttl     = 300
  }

  # Respuestas de Error Personalizadas: 404 Sobrio y Ligero (/404.html)
  custom_error_response {
    error_code            = 403
    response_code         = 404
    response_page_path    = "/404.html"
    error_caching_min_ttl = 10
  }

  custom_error_response {
    error_code            = 404
    response_code         = 404
    response_page_path    = "/404.html"
    error_caching_min_ttl = 10
  }

  # Certificado SSL/TLS con ACM en us-east-1
  viewer_certificate {
    acm_certificate_arn      = "arn:aws:acm:us-east-1:192584119994:certificate/ba998f45-0d29-45d2-a7cf-00438ec90b9b"
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
