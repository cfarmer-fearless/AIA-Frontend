terraform {
  backend "s3" {
    bucket = "fms-api-terraform"
    key    = "python_lambda_terraform.tfstate"
    region = "us-east-2"
  }
}
