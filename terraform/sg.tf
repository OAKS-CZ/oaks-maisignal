resource "aws_security_group" "ecs_task" {
  name        = "${local.prefix}-ecs-task"
  description = "Allow HTTPS egress only for ECS Fargate tasks."
  vpc_id      = aws_vpc.this.id

  egress {
    description = "HTTPS to external services"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${local.prefix}-ecs-task" }
}
