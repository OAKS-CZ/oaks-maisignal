# Terraform — MAiSIGNAL Infrastructure

AWS infrastructure provisioning for MAiSIGNAL using Terraform.

## Resources

- **ECR** — Container registry for the MAiSIGNAL Docker image (immutable tags, scan on push)
- **IAM** — Least-privilege role for ECS/Lambda to pull images from ECR

## Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.5.0
- AWS CLI configured with appropriate credentials
- S3 bucket `oaks-terraform-state` for remote state (create manually or adjust `main.tf`)

## Usage

```bash
cd terraform

# Initialize (downloads providers, configures backend)
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## State Backend

Terraform state is stored in S3:

| Setting | Value |
|---------|-------|
| Bucket | `oaks-terraform-state` |
| Key | `maisignal/terraform.tfstate` |
| Region | `eu-central-1` |

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `project` | `maisignal` | Project name for resource tagging |
| `aws_region` | `eu-central-1` | AWS region |
| `ecr_repo_name` | `maisignal` | ECR repository name |
