variable "project" {
  type    = string
}

variable "environment" {
  type    = string
}

variable "docker_build_tag" {
  type    = string
}

locals {
  name = "${var.project}-${var.environment}"
  environment_docker_build_tag = "${var.project}_${var.environment}_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
}