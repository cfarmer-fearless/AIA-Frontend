variable "environment" {}

variable "project" {}
variable "port" {
  default = 5432
}

variable "public_subnets" {}

variable "private_subnets" {}


variable "ecr_image_tag" {}

variable "rds_master_username" {
  default = "rds_master"
}

variable "availability_zones" {}

variable "cidr_block" {}

variable "common_tags" {}

locals {
  name          = "${var.project}-${var.environment}"
  cidr_block    = lookup(var.cidr_block, var.environment, "10.0.0.0/16")
  ecr_image_tag = lookup(var.ecr_image_tag, var.environment, "LATEST")
  tags = {
    project = var.project
    env     = var.environment
  }
}
