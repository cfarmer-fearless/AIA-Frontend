terraform {
  backend "s3" {
    bucket = "aia-frontend"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
