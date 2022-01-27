resource "aws_security_group" "lambda" {
  name = "${local.name}-lambda-sg"
  vpc_id      = aws_vpc.platform_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, var.common_tags)

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "db" {
  name_prefix = "${local.name}-db-sg"
  vpc_id      = aws_vpc.platform_vpc.id

  tags = merge(local.tags, var.common_tags)

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "lambda_ingress" {
  depends_on = [
    aws_security_group.db
  ]
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.db.id
  security_group_id        = aws_security_group.lambda.id
}

resource "aws_security_group_rule" "db_ingress" {
  depends_on = [
    aws_security_group.lambda
  ]
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lambda.id
  security_group_id        = aws_security_group.db.id
}

resource "aws_security_group_rule" "db_egress" {
  depends_on = [
    aws_security_group.lambda
  ]
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lambda.id
  security_group_id        = aws_security_group.db.id
}