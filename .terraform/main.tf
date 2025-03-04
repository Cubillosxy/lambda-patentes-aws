provider "aws" {
  region = var.region
}

# IAM Role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM Policy attachment (basic execution permissions)
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function for processing readings
resource "aws_lambda_function" "process_reading" {
  filename         = var.process_reading_zip_path
  function_name    = "process_reading"
  handler          = "handler.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec.arn
  memory_size      = 128
  timeout          = 10

  environment {
    variables = {
      # This path is relative to the Lambda package; remember that /tmp is the only writable folder in Lambda.
      DB_PATH = "./db.db"
    }
  }
}

# Lambda function for metrics
resource "aws_lambda_function" "metrics" {
  filename         = var.metrics_zip_path
  function_name    = "metrics"
  handler          = "handler.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec.arn
  memory_size      = 128
  timeout          = 10

  environment {
    variables = {
      DB_PATH = "./db.db"
    }
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "api" {
  name        = "sqlite-challenge-api"
  description = "API Gateway for SQLite-based Lambda functions"
}

# Resource for /process endpoint
resource "aws_api_gateway_resource" "process" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "process"
}

# POST method for /process endpoint
resource "aws_api_gateway_method" "process_post" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.process.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integration for process_reading Lambda
resource "aws_api_gateway_integration" "process_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.process.id
  http_method = aws_api_gateway_method.process_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.process_reading.invoke_arn
}

# Resource for /metrics endpoint
resource "aws_api_gateway_resource" "metrics" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "metrics"
}

# GET method for /metrics endpoint
resource "aws_api_gateway_method" "metrics_get" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.metrics.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integration for metrics Lambda
resource "aws_api_gateway_integration" "metrics_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.metrics.id
  http_method = aws_api_gateway_method.metrics_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.metrics.invoke_arn
}

# Deployment of the API Gateway
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.process_integration,
    aws_api_gateway_integration.metrics_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = var.stage_name
}
