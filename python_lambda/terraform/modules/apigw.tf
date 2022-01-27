data "template_file" "openapi_yml" {
  template = file("../../docs/openapi.yml")

  vars = {
    auth_lambda_invoke_arn            = aws_lambda_function.cognito_authorization.invoke_arn
    get_beneficiary_lambda_invoke_arn = aws_lambda_function.beneficiary_data.invoke_arn
    cognito_user_pool_arn             = tolist(data.aws_cognito_user_pools.platform_user_pool.arns)[0]
  }
}

resource "aws_api_gateway_rest_api" "platform_rest_api" {
  name = local.name
  body = data.template_file.openapi_yml.rendered
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "platform_rest_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.platform_rest_api.id
  triggers = {
    redeployment = sha1(jsonencode([
      data.template_file.openapi_yml.id,
      aws_api_gateway_rest_api.platform_rest_api.id
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "platform_rest_api_stage" {
  deployment_id = aws_api_gateway_deployment.platform_rest_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.platform_rest_api.id
  stage_name    = var.environment
}
