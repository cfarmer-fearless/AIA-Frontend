terraform {
  backend "s3" {
    bucket = "aia-terraform-backend"
    key    = "aia-frontend.terraform.tfstate"
    region = "us-east-1"
  }
}
