output "apigw_invoke_url" {
  value = aws_api_gateway_deployment.platform_rest_api_deployment.invoke_url
}

output "apigw_stage_name" {
  value = aws_api_gateway_stage.platform_rest_api_stage.stage_name
}