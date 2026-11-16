variable "aws_region" {
  description = "aws region for deployment"
  type        = string
  default     = "ap-south-1"
}
variable "vpc_cidr" {
  description = "CIDR block for the vpc"
  type        = string
  default     = "10.0.0.0/16"

}
variable "public_subnet_cidr" {
  description = "cidr blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]

}
variable "private_subnet_cidr" {
  description = "CIDR for private subnet"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}
variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "employee-management-eks"

}
variable "kubernetes_version" {
  description = "kubernetes version"
  type        = string
  default     = "1.33"
}
variable "node_group_name" {
  description = "EKS managed node group name"
  type        = string
  default     = "employee-management-nodes"
}
variable "instance_types" {
  description = "EC2 instance types for worker nodes"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_size" {
  type    = number
  default = 2
}

variable "min_size" {
  type    = number
  default = 1

}
variable "max_size" {
  type    = number
  default = 3
}
