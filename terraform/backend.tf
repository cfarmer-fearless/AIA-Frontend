terraform {
  backend "s3" {
    bucket = "fms-api-terraform"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}
