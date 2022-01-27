## DEV
output "database_cluster_id_dev" {
  value = module.dev.database_cluster_id
}

output "database_endpoint_dev" {
  value = module.dev.database_endpoint
}

output "ecr_repository_uri_dev" {
  value = module.dev.ecr_repository_uri
}

output "cloudfront_domain_name_dev" {
  value = module.dev.cloudfront_domain_name
}

## PROD
output "database_cluster_id_prod" {
  value = var.create_prod_infrastructure ? module.prod[0].database_cluster_id : ""
}

output "database_endpoint_prod" {
  value = var.create_prod_infrastructure ? module.prod[0].database_endpoint : ""
}

output "ecr_repository_uri_prod" {
  value = var.create_prod_infrastructure ? module.prod[0].ecr_repository_uri : ""
}

output "cloudfront_domain_name_prod" {
  value = var.create_prod_infrastructure ? module.prod[0].cloudfront_domain_name : ""
}