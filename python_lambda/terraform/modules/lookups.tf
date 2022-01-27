
data "aws_ecr_repository" "platform_ecr_repo" {
  name = local.name
}

data "aws_ecr_authorization_token" "ecr_token" {}

data "aws_ssm_parameter" "master" {
  name = "/${var.environment}/${var.project}/rds/master/password"
}

data "aws_cognito_user_pools" "platform_user_pool" {
  name = local.name
}

data "aws_rds_cluster" "lambda_rds" {
  cluster_identifier = local.name
}

data "aws_vpc" "platform_vpc" {
  filter {
    name   = "tag:Name"
    values = [local.name]
  }
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.platform_vpc.id

  tags = {
    Name = "${local.name}-private"
  }
}

data "aws_security_group" "lambda" {
  name = "${local.name}-lambda-sg"
}
