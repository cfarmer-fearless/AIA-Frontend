resource "aws_s3_bucket" "mock_data_file_hosting" {
  bucket = "${local.name}-mock-data"
  acl           = "private"
  force_destroy = true # When taking the environment down, delete this bucket even if its not empty
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }
}

resource "aws_s3_bucket_object" "esrd_dialysis_data" {
  bucket = aws_s3_bucket.mock_data_file_hosting.id
  key    = "esrd_dialysis_data.csv"
  source = "${path.module}/esrd_dialysis_data.csv"
}

resource "aws_s3_bucket_object" "beneficiary_data" {
  bucket = aws_s3_bucket.mock_data_file_hosting.id
  key    = "beneficiary_data.csv"
  source = "${path.module}/beneficiary_data.csv"
}