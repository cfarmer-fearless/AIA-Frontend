output "invocation_url_dev" {
  value = join("", [module.dev.apigw_invoke_url, module.dev.apigw_stage_name])
}

output "invocation_url_prod" {
  value = var.create_prod_infrastructure ? join("", [module.prod[0].apigw_invoke_url, module.prod[0].apigw_stage_name]) : ""
}