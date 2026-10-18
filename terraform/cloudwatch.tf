# Tópico Amazon SNS para Alertas FinOps y de Seguridad
resource "aws_sns_topic" "finops_alerts" {
  name = "${var.project_name}-finops-alerts"
}

# Suscripción por correo electrónico institucional
resource "aws_sns_topic_subscription" "email_sub" {
  topic_arn = aws_sns_topic.finops_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

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

  actions_enabled = true
  alarm_actions   = [aws_sns_topic.finops_alerts.arn]
  ok_actions      = [aws_sns_topic.finops_alerts.arn]

  dimensions = {
    DistributionId = aws_cloudfront_distribution.main.id
    Region         = "Global"
  }
}
