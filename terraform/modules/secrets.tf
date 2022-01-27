resource "random_password" "master" {
  length           = 16
  special          = true
  override_special = "!#$%^&*()_-+="
}

resource "aws_ssm_parameter" "master" {
  name      = "/${var.environment}/${var.project}/rds/master/password"
  type      = "SecureString"
  overwrite = true
  value     = random_password.master.result
}