resource "aws_vpc_endpoint" "ssm" {
  vpc_id            = aws_vpc.platform_vpc.id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.ssm"
  vpc_endpoint_type = "Interface"

  security_group_ids = [
    aws_security_group.lambda.id,
  ]
}

resource "aws_vpc_endpoint_subnet_association" "ssm" {
  count           = local.private_subnet_count
  vpc_endpoint_id = aws_vpc_endpoint.ssm.id
  subnet_id       = element(aws_subnet.private.*.id, count.index)
}