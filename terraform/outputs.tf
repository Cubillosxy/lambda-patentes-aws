output "api_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_deployment.api_deployment.invoke_url}/${var.stage_name}/"
}
