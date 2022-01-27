resource "aws_cognito_user_pool" "platform_user_pool" {
  name = local.name
}
