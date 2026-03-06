resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${local.prefix}"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.this.arn
}

resource "aws_ecs_cluster" "this" {
  name = "${local.prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "this" {
  family                   = "${local.prefix}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_exec.arn

  container_definitions = jsonencode([
    {
      name                   = var.project
      image                  = "${local.ecr_url}:${var.container_image_tag}"
      essential              = true
      readonlyRootFilesystem = true

      environment = [
        {
          name  = "SNOWFLAKE_SCHEMA"
          value = local.snowflake_schema
        },
      ]

      secrets = [
        {
          name      = "ECOMAIL_API_KEY"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:ECOMAIL_API_KEY::"
        },
        {
          name      = "SNOWFLAKE_ACCOUNT"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:SNOWFLAKE_ACCOUNT::"
        },
        {
          name      = "SNOWFLAKE_USER"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:SNOWFLAKE_USER::"
        },
        {
          name      = "SNOWFLAKE_PASSWORD"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:SNOWFLAKE_PASSWORD::"
        },
        {
          name      = "SNOWFLAKE_ROLE"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:SNOWFLAKE_ROLE::"
        },
        {
          name      = "SNOWFLAKE_WAREHOUSE"
          valueFrom = "${aws_secretsmanager_secret.app_credentials.arn}:SNOWFLAKE_WAREHOUSE::"
        },
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
  ])
}
