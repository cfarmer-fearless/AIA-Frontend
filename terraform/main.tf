module "dev" {
  source = "./modules"

  environment        = "dev"
  project            = var.project
  availability_zones = var.availability_zones
  private_subnets    = ["10.140.0.0/22", "10.140.4.0/22", "10.140.8.0/21"]
  public_subnets     = ["10.140.16.0/20"]
  common_tags        = var.common_tags
  cidr_block         = var.cidr_block
  ecr_image_tag      = var.ecr_image_tag
}

module "prod" {
  source = "./modules"
  count = var.create_prod_infrastructure ? 1 : 0

  environment        = "prod"
  project            = var.project
  availability_zones = var.availability_zones
  private_subnets    = ["10.150.0.0/22", "10.150.4.0/22", "10.150.8.0/21"]
  public_subnets     = ["10.150.16.0/20"]
  common_tags        = var.common_tags
  cidr_block         = var.cidr_block
  ecr_image_tag      = var.ecr_image_tag
}
