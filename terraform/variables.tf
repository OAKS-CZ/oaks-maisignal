variable "project" {
  description = "Project name used for tagging resources."
  type        = string
  default     = "maisignal"
}

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "eu-central-1"
}

variable "ecr_repo_name" {
  description = "Name of the ECR repository."
  type        = string
  default     = "maisignal"
}
