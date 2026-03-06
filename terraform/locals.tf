locals {
  env    = terraform.workspace
  prefix = "${var.project}-${local.env}"

  ecr_url = (
    local.env == "dev"
    ? aws_ecr_repository.this[0].repository_url
    : data.aws_ecr_repository.shared[0].repository_url
  )
  ecr_arn = (
    local.env == "dev"
    ? aws_ecr_repository.this[0].arn
    : data.aws_ecr_repository.shared[0].arn
  )

  snowflake_schema = "l0_${local.env}"
}

check "workspace_name" {
  assert {
    condition     = contains(["dev", "prod"], terraform.workspace)
    error_message = "Terraform workspace must be 'dev' or 'prod'."
  }
}
