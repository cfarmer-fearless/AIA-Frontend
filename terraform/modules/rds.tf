resource "aws_rds_cluster" "lambda_rds" {
  cluster_identifier     = local.name
  db_subnet_group_name   = aws_db_subnet_group.lambda_rds_subnet_group.name
  enable_http_endpoint   = true
  engine                 = "aurora-postgresql"
  engine_mode            = "serverless"
  skip_final_snapshot    = true
  apply_immediately      = true
  availability_zones     = var.availability_zones
  master_username        = var.rds_master_username
  master_password        = aws_ssm_parameter.master.value
  database_name          = var.project
  port                   = var.port
  tags                   = merge(var.common_tags, local.tags)
  vpc_security_group_ids = [aws_security_group.db.id]

  scaling_configuration {
    auto_pause               = true
    max_capacity             = 4
    min_capacity             = 2
    seconds_until_auto_pause = 300
    timeout_action           = "ForceApplyCapacityChange"
  }
}

resource "aws_db_subnet_group" "lambda_rds_subnet_group" {
  name_prefix = local.name
  subnet_ids  = aws_subnet.private.*.id

  tags = merge(local.tags, var.common_tags)
}