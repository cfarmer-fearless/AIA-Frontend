locals {
  ecr_image = "${data.aws_ecr_repository.platform_ecr_repo.repository_url}:${local.environment_docker_build_tag}"
}

resource "null_resource" "push_image" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    working_dir = "../"
    command = <<-EOS
    docker tag ${var.docker_build_tag} ${local.ecr_image}
    docker login --username AWS --password ${data.aws_ecr_authorization_token.ecr_token.password} ${data.aws_ecr_repository.platform_ecr_repo.repository_url}
    docker push ${local.ecr_image}
    EOS
  }
}

resource "aws_lambda_function" "cognito_authorization" {
  function_name = "${local.name}-cognito-authorization"
  role          = aws_iam_role.lambda_role.arn
  image_uri     = local.ecr_image
  image_config {
    command = ["cognito_authorization.lambda_handler"]
  }
  package_type = "Image"

  environment {
    variables = {
      APP_CLIENT_ID = aws_cognito_user_pool_client.platform_user_pool_client.id
    }
  }
  depends_on = [null_resource.push_image]
}

resource "aws_lambda_function" "beneficiary_data" {
  function_name = "${local.name}-get-beneficiary-data"
  role          = aws_iam_role.lambda_role.arn
  image_uri     = local.ecr_image
  timeout       = 15
  image_config {
    command = ["get_beneficiary_data.lambda_handler"]
  }

  environment {
    variables = {
      POSTGRES_DB            = data.aws_rds_cluster.lambda_rds.database_name
      POSTGRES_USER          = data.aws_rds_cluster.lambda_rds.master_username
      PARAMETER_STORE_PG_KEY = data.aws_ssm_parameter.master.name
      POSTGRES_HOSTNAME      = data.aws_rds_cluster.lambda_rds.endpoint
    }
  }
  vpc_config {
    subnet_ids         = data.aws_subnet_ids.private.ids
    security_group_ids = [data.aws_security_group.lambda.id]
  }

  package_type = "Image"

  depends_on = [null_resource.push_image]
}

resource "aws_lambda_function" "data_load" {
  depends_on = [aws_iam_role_policy_attachment.AWSLambdaVPCAccessExecutionRole, null_resource.push_image]

  function_name = "${local.name}-data-load"
  role          = aws_iam_role.lambda_role.arn
  image_uri     = local.ecr_image
  image_config {
    command = ["data_load_lambda.load_data"]
  }
  timeout = 30
  environment {
    variables = {
      POSTGRES_DB            = data.aws_rds_cluster.lambda_rds.database_name
      DATA_BUCKET            = aws_s3_bucket.mock_data_file_hosting.id
      BENEFICIARY_DATA       = aws_s3_bucket_object.beneficiary_data.key
      ESRD_DIALYSIS_DATA     = aws_s3_bucket_object.esrd_dialysis_data.key
      POSTGRES_USER          = data.aws_rds_cluster.lambda_rds.master_username
      PARAMETER_STORE_PG_KEY = data.aws_ssm_parameter.master.name
      POSTGRES_HOSTNAME      = data.aws_rds_cluster.lambda_rds.endpoint
    }
  }

  vpc_config {
    subnet_ids         = data.aws_subnet_ids.private.ids
    security_group_ids = [data.aws_security_group.lambda.id]
  }
  package_type = "Image"
}

## Lambda Permissions
resource "aws_lambda_permission" "cognito_authorization" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cognito_authorization.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.platform_rest_api.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "beneficiary_data" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.beneficiary_data.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.platform_rest_api.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "data_load" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_load.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.platform_rest_api.execution_arn}/*/*/*"
}
