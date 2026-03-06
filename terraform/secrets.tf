resource "aws_secretsmanager_secret" "app_credentials" {
  name        = "${local.prefix}-app-credentials"
  description = "Application credentials for MAiSIGNAL (Ecomail API key, Snowflake connection)."
  kms_key_id  = aws_kms_key.this.arn
}

resource "aws_secretsmanager_secret_rotation" "app_credentials" {
  secret_id           = aws_secretsmanager_secret.app_credentials.id
  rotation_lambda_arn = aws_lambda_function.rotate_snowflake_password.arn

  rotation_rules {
    automatically_after_days = var.rotation_schedule_days
  }

  depends_on = [aws_lambda_permission.secretsmanager]
}
