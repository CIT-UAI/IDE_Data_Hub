# Alarma de CloudWatch para Detección de Anomalías de Egress (FinOps & Resiliencia)
resource "aws_cloudwatch_metric_alarm" "high_egress" {
  alarm_name          = "${var.project_name}-cloudfront-high-egress-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "BytesDownloaded"
  namespace           = "AWS/CloudFront"
  period              = 3600
  statistic           = "Sum"
  threshold           = 53687091200 # 50 GB en 1 hora
  alarm_description   = "Alerta FinOps/Seguridad: Descarga masiva de datos en CloudFront IDE CIT (posible scraper o Denial of Wallet)"
  treat_missing_data  = "notBreaching"

  dimensions = {
    DistributionId = aws_cloudfront_distribution.main.id
    Region         = "Global"
  }
}
