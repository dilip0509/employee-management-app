variable "vpc_cidr" {
  description = "CIDR block for the vpc"
  type        = string
}
variable "public_subnet_cidr" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}
variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = list(string)
}
