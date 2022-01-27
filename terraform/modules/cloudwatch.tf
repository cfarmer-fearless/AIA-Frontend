resource "aws_cloudwatch_log_group" "platform_cloudwatch" {
  name              = "/aws/lambda/${var.project}/${var.environment}"
  retention_in_days = 14
}