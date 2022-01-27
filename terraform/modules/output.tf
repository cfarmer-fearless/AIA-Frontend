output "database_cluster_id" {
  value = aws_rds_cluster.lambda_rds.id
}

output "database_endpoint" {
  value = aws_rds_cluster.lambda_rds.endpoint
}

output "database_cluster_members" {
  value = aws_rds_cluster.lambda_rds.cluster_members
}

output "database_name" {
  value = aws_rds_cluster.lambda_rds.database_name
}

output "ecr_repository_uri" {
  value = aws_ecr_repository.platform_ecr_repo.repository_url
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.front_end.domain_name
}