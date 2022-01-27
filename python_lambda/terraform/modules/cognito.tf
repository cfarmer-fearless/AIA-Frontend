resource "aws_cognito_user_pool_client" "platform_user_pool_client" {
  name                         = local.name
  user_pool_id                 = tolist(data.aws_cognito_user_pools.platform_user_pool.ids)[0]
  explicit_auth_flows          = ["USER_PASSWORD_AUTH"]
  supported_identity_providers = ["COGNITO"]
}