resource "aws_ecr_repository" "this" {
  count                = local.env == "dev" ? 1 : 0
  name                 = var.ecr_repo_name
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.this.arn
  }
}

data "aws_ecr_repository" "shared" {
  count = local.env == "prod" ? 1 : 0
  name  = var.ecr_repo_name
}
