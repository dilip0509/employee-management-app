output "vpc_id" {
  description = "ID of VPC"
  value       = module.vpc.vpc_id
}
output "public_subnet_id" {
  description = "ID od public subnet"
  value       = module.vpc.public_subnet_id
}
output "private_subnet_id" {
  description = "ID of private subnet"
  value       = module.vpc.private_subnet_id
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name

}
output "eks_cluster_endpoint" {
  description = "EKS cluster API endpoint"
  value       = module.eks.cluster_endpoint
}
output "eks_cluster_security_group_id" {
  description = "EKS Cluster security group ID"
  value       = module.eks.cluster_security_group_id
}
output "eks_node_group_name" {
  description = "EKS Managed node group name"
  value       = module.eks.node_group_name
}
