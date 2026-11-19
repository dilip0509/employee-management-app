output "vpc_id" {
  description = "ID of the vpc"
  value       = aws_vpc.main.id
}
output "public_subnet_id" {
  description = "ID of Public subnet"
  value       = aws_subnet.public[*].id
}

output "private_subnet_id" {
  description = "ID of Private subnet"
  value       = aws_subnet.private[*].id
}
output "private_route_table_id" {
  description = "ID of private route table"
  value       = aws_route_table.private.id
}
