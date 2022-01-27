locals {
  private_subnet_count = var.private_subnets != "" ? length(flatten(var.private_subnets)) : length(flatten(var.availability_zones))
  public_subnet_count  = var.public_subnets != "" ? length(flatten(var.public_subnets)) : length(flatten(var.availability_zones))
}

data "aws_region" "current" {}

resource "aws_vpc" "platform_vpc" {
  cidr_block = local.cidr_block
  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = local.name })
  )
}

resource "aws_subnet" "private" {
  count             = local.private_subnet_count
  vpc_id            = aws_vpc.platform_vpc.id
  availability_zone = element(var.availability_zones, count.index)

  cidr_block = element(var.private_subnets, count.index)
  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = "${local.name}-private" })
  )
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_subnet" "public" {
  count                   = local.public_subnet_count
  vpc_id                  = aws_vpc.platform_vpc.id
  availability_zone       = element(var.availability_zones, count.index)
  map_public_ip_on_launch = true

  cidr_block = element(var.public_subnets, count.index)
  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = "${local.name}-public" })
  )
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_eip" "nat_gateway_eip" {
  depends_on = [aws_internet_gateway.network_egress]
  vpc        = true
  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = local.name })
  )
}

resource "aws_internet_gateway" "network_egress" {
  vpc_id = aws_vpc.platform_vpc.id
  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = local.name })
  )
}

resource "aws_nat_gateway" "egress_nat_gateway" {
  depends_on    = [aws_internet_gateway.network_egress]
  count         = local.public_subnet_count
  allocation_id = aws_eip.nat_gateway_eip.id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(local.tags,
    var.common_tags,
    tomap({ "Name" = local.name })
  )
}
