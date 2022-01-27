variable "region" {
  default = "us-east-2"
}

variable "project" {
  type    = string
  default = "fms"
}

variable "availability_zones" {
  type    = list(any)
  default = ["us-east-2a", "us-east-2b", "us-east-2c"]
}

variable "cidr_block" {
  type = map(any)
  default = {
    dev  = "10.140.0.0/16"
    prod = "10.150.0.0/16"
  }
}

variable "common_tags" {
  type = map(any)
  default = {
    Department = "BD"
    Terraform  = "true"
  }
}

variable "ecr_image_tag" {
  type = map(any)
  default = {
    dev  = "latest"
    prod = "latest"
  }
}

variable "create_prod_infrastructure" {
  type = bool
  default = false
}