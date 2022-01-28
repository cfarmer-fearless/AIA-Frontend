resource "aws_s3_bucket" "front_end_hosting" {
  bucket        = "${local.name}-front-end-hosting-east-2"
  acl           = "public-read"
  force_destroy = true # When taking the environment down, delete this bucket even if its not empty

  # Static website hosting
  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

resource "aws_s3_bucket_policy" "front_end_hosting_bucket_policy" {
  bucket = aws_s3_bucket.front_end_hosting.id
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "public_read_policy"
    Statement = [
      {
        Sid       = "publicaccess"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = ["${aws_s3_bucket.front_end_hosting.arn}/*"]
      },
    ]
  })
}
