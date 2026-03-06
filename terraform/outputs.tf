output "ecr_repository_url" {
  description = "URL of the ECR repository."
  value       = aws_ecr_repository.this.repository_url
}

output "ecr_pull_role_arn" {
  description = "ARN of the IAM role for pulling images from ECR."
  value       = aws_iam_role.ecr_pull.arn
}
