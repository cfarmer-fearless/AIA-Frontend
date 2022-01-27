variable "region" {
  default = "us-east-2"
}

variable "project" {
  type    = string
  default = "fms"
}

variable "common_tags" {
  type = map(any)
  default = {
    Department = "BD"
    Terraform  = "true"
  }
}

variable "create_prod_infrastructure" {
  type = bool
  default = false
}

locals {
  docker_build_tag = "${var.project}_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
}