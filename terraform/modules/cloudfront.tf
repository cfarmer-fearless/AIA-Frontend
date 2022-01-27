resource "aws_cloudfront_distribution" "front_end" {
  origin {
    domain_name = aws_s3_bucket.front_end_hosting.website_endpoint
    origin_id   = aws_s3_bucket.front_end_hosting.website_endpoint

    custom_origin_config {
      http_port              = "80"
      https_port             = "443"
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  comment = "${local.name} cloudfront distribution"

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
        allowed_methods  = ["GET", "HEAD"]
        cached_methods   = ["GET", "HEAD"]
        target_origin_id = aws_s3_bucket.front_end_hosting.website_endpoint

    forwarded_values {
        query_string = false

        cookies {
            forward = "none"
        }
    }

        viewer_protocol_policy = "allow-all"
        default_ttl            = 3600
        max_ttl                = 86400
    }

    restrictions {
        geo_restriction {
            restriction_type = "none"
        }
    }

    viewer_certificate {
        cloudfront_default_certificate = true
    }

    custom_error_response {
        error_caching_min_ttl = 0
        error_code            = 403
        response_code         = 200
        response_page_path    = "/index.html"
    }

}