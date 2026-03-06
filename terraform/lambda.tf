resource "null_resource" "lambda_deps" {
  triggers = {
    handler = filemd5("${path.module}/lambda/rotate_snowflake_password.py")
  }

  provisioner "local-exec" {
    command = <<-EOT
      pip install snowflake-connector-python -t ${path.module}/lambda/package/ --upgrade --quiet
      cp ${path.module}/lambda/rotate_snowflake_password.py ${path.module}/lambda/package/
    EOT
  }
}

data "archive_file" "rotate_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/package"
  output_path = "${path.module}/lambda/rotate_snowflake_password.zip"

  depends_on = [null_resource.lambda_deps]
}

resource "aws_cloudwatch_log_group" "lambda_rotate" {
  name              = "/aws/lambda/${local.prefix}-rotate-snowflake-password"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.this.arn
}

resource "aws_iam_role" "lambda_rotate" {
  name = "${local.prefix}-lambda-rotate"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "lambda_rotate" {
  name = "${local.prefix}-lambda-rotate"
  role = aws_iam_role.lambda_rotate.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:PutSecretValue",
          "secretsmanager:UpdateSecretVersionStage",
          "secretsmanager:DescribeSecret",
        ]
        Resource = aws_secretsmanager_secret.app_credentials.arn
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
        ]
        Resource = aws_kms_key.this.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "${aws_cloudwatch_log_group.lambda_rotate.arn}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
        ]
        Resource = "*"
      },
    ]
  })
}

resource "aws_lambda_function" "rotate_snowflake_password" {
  function_name    = "${local.prefix}-rotate-snowflake-password"
  role             = aws_iam_role.lambda_rotate.arn
  handler          = "rotate_snowflake_password.lambda_handler"
  runtime          = "python3.12"
  timeout          = 60
  memory_size      = 256
  filename         = data.archive_file.rotate_lambda.output_path
  source_code_hash = data.archive_file.rotate_lambda.output_base64sha256

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.ecs_task.id]
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_rotate,
    aws_iam_role_policy.lambda_rotate,
  ]
}

resource "aws_lambda_permission" "secretsmanager" {
  statement_id  = "AllowSecretsManagerInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rotate_snowflake_password.function_name
  principal     = "secretsmanager.amazonaws.com"
  source_arn    = aws_secretsmanager_secret.app_credentials.arn
}
