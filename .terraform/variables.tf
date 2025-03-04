variable "region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "stage_name" {
  description = "API Gateway stage name"
  default     = "dev"
}

variable "process_reading_zip_path" {
  description = "Path to the process_reading Lambda zip file"
  default     = "../process_reading.zip"
}

variable "metrics_zip_path" {
  description = "Path to the metrics Lambda zip file"
  default     = "../metrics.zip"
}
