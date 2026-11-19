variable "cluster_name" {
  description = "Name of the EKS Cluster"
  type        = string
}
variable "kubernetes_version" {
  description = "kubernetes version for eks"
  type        = string
}

variable "private_subnet_ids" {
  description = "private subnet IDs for EKS worker nodes"
  type        = list(string)
}

variable "node_group_name" {
  description = "Name of the EKS Managed node group"
  type        = string
}

variable "instance_types" {
  description = "ec2 instance type for worker nodes"
  type        = list(string)
}

variable "desired_size" {
  description = "Desired number of worker nodes"
  type        = number
}

variable "min_size" {
  description = "Minimum number of worker nodes"
  type        = number
}
variable "max_size" {
  description = "Maximum number of worker nodes"
  type        = number
}
