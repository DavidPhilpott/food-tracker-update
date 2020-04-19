variable "lambda_name" {}
variable "description" {}
variable "s3_code_bucket" {}
variable "s3_code_key" {}
variable "lambda_environment_variables" {}
variable "lambda_handler"{}
variable "schedule_expression" {}


#Account / role
variable "aws_account_id" {}
variable "region" {}

#Tags
variable "project_name" {}
variable "environment" {}

locals {
  common_tags = {
    environment  = var.environment
    project_name = var.project_name
  }
}