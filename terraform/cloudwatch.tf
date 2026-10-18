# Alarma de CloudWatch para Detección de Anomalías de Egress (FinOps & Resiliencia)
resource "aws_cloudwatch_metric_alarm" "high_egress" {
  alarm_name          = "${var.project_name}-cloudfront-high-egress-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "BytesDownloaded"
  namespace           = "AWS/CloudFront"
  period              = 3600
  statistic           = "Sum"
  threshold           = var.cloudwatch_egress_threshold_gb * 1073741824 # 25 GB en bytes
  alarm_description   = "Alerta FinOps/Seguridad: Descarga anómala >${var.cloudwatch_egress_threshold_gb} GB en 1 hora en CloudFront IDE CIT (posible bot o bucle de descarga)"
  treat_missing_data  = "notBreaching"

  dimensions = {
    DistributionId = aws_cloudfront_distribution.main.id
    Region         = "Global"
  }
}
