# AWS WAFv2 WebACL (Scope: CLOUDFRONT) — Protección Proactiva "Cortar antes de pagar"
resource "aws_wafv2_web_acl" "shield" {
  name        = "${var.project_name}-waf-rate-shield"
  description = "WAFv2 Rate-Limiting Shield for IDE CIT - Proactive FinOps Protection"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}
  }

  custom_response_body {
    key          = "RateLimitResponse"
    content_type = "APPLICATION_JSON"
    content      = jsonencode({
      code        = "TooManyRequests"
      description = "Rate limit threshold reached. Access temporarily throttled to protect infrastructure."
    })
  }

  # Regla 1: Rate Limiting específico para descargas pesadas (/download/*)
  rule {
    name     = "RateLimit-Downloads-PerIP"
    priority = 1

    action {
      block {
        custom_response {
          response_code            = 429
          custom_response_body_key = "RateLimitResponse"
        }
      }
    }

    statement {
      rate_based_statement {
        limit              = var.rate_limit_downloads
        aggregate_key_type = "IP"

        scope_down_statement {
          byte_match_statement {
            field_to_match {
              uri_path {}
            }
            positional_constraint = "STARTS_WITH"
            search_string         = "/download/"
            text_transformation {
              priority = 0
              type     = "LOWERCASE"
            }
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitDownloadsPerIP"
      sampled_requests_enabled   = true
    }
  }

  # Regla 2: Rate Limiting general por IP
  rule {
    name     = "RateLimit-General-PerIP"
    priority = 2

    action {
      block {
        custom_response {
          response_code            = 429
          custom_response_body_key = "RateLimitResponse"
        }
      }
    }

    statement {
      rate_based_statement {
        limit              = var.rate_limit_general
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitGeneralPerIP"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.project_name}-waf-rate-shield"
    sampled_requests_enabled   = true
  }
}
