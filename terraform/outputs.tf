output "ecr_repository_url" {
  description = "URL of the ECR repository."
  value       = local.ecr_url
}

output "ecr_pull_role_arn" {
  description = "ARN of the IAM role for pulling images from ECR."
  value       = aws_iam_role.ecr_pull.arn
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster."
  value       = aws_ecs_cluster.this.name
}

output "ecs_task_definition_arn" {
  description = "ARN of the ECS task definition."
  value       = aws_ecs_task_definition.this.arn
}

output "ecs_exec_role_arn" {
  description = "ARN of the ECS execution IAM role."
  value       = aws_iam_role.ecs_exec.arn
}

output "secrets_manager_secret_arn" {
  description = "ARN of the Secrets Manager secret for app credentials."
  value       = aws_secretsmanager_secret.app_credentials.arn
}

output "vpc_id" {
  description = "ID of the VPC."
  value       = aws_vpc.this.id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets."
  value       = aws_subnet.private[*].id
}

output "cloudwatch_log_group" {
  description = "Name of the CloudWatch log group for ECS."
  value       = aws_cloudwatch_log_group.ecs.name
}

output "rotation_lambda_arn" {
  description = "ARN of the Secrets Manager rotation Lambda."
  value       = aws_lambda_function.rotate_snowflake_password.arn
}
