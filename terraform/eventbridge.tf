resource "aws_cloudwatch_event_rule" "daily_alert" {
  name                = "${local.prefix}-daily-alert"
  description         = "Trigger MAiSIGNAL alert task daily."
  schedule_expression = var.ecs_schedule_expression
}

resource "aws_cloudwatch_event_target" "ecs" {
  rule     = aws_cloudwatch_event_rule.daily_alert.name
  arn      = aws_ecs_cluster.this.arn
  role_arn = aws_iam_role.eventbridge_ecs.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.this.arn_without_revision
    task_count          = 1
    launch_type         = "FARGATE"

    network_configuration {
      subnets          = aws_subnet.private[*].id
      security_groups  = [aws_security_group.ecs_task.id]
      assign_public_ip = false
    }
  }
}
