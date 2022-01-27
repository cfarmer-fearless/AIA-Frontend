
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.platform_vpc.id

  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = "${local.name}-private" })
  )
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.platform_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.network_egress.id
  }

  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = "${local.name}-public" })
  )
}

resource "aws_route" "private" {
  count = local.public_subnet_count

  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.egress_nat_gateway[count.index].id
}

resource "aws_route_table_association" "private" {
  count          = local.private_subnet_count
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "public" {
  count          = local.public_subnet_count
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}