lambda_name = "food-tracker-lambda"
description   = "Moves data from daily food tracker to historical tracker."
s3_code_bucket = "dphilpott-dev-code-bucket"
s3_code_key = "food-tracker/dev/food-tracker.zip"
lambda_handler = "app.foodDailyUpdate.lambda_handler"
aws_account_id = "020968065558"
region = "eu-west-1"
project_name = "food-tracker"
environment = "prod"

lambda_environment_variables =  {
  "google_auth_type": "service_account",
  "google_auth_project_id": "secret_google_auth_project_id",
  "google_auth_private_key_id": "secret_secure_google_auth_private_key_id",
  "google_auth_private_key": "secret_pem_google_auth_private_key",
  "google_auth_client_email": "secret_secure_ghseet_google_auth_client_email",
  "google_auth_client_id": "secret_google_auth_client_id",
  "google_auth_auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "google_auth_token_uri": "https://oauth2.googleapis.com/token",
  "google_auth_auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "google_auth_client_x509_cert_url": "secret_google_auth_client_x509_cert_url",
  "spreadsheet_key_FoodDaily": "1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU",
  "spreadsheet_key_FoodCore": "1QDq6rDSosVcLE-TekFcxGDLqvbn_leVa5vUo8uJMTSI",
  "daily_auto_spreadsheet_name": "FoodDaily",
  "daily_manual_spreadsheet_name": "FoodDaily",
  "daily_auto_worksheet_name": "Auto",
  "daily_manual_worksheet_name": "Manual",
  "date_index": "C2",
  "date_spreadsheet": "FoodDaily",
  "date_worksheet": "Info",
  "core_spreadsheet_name": "FoodCore",
  "core_worksheet_name": "Historical Food Tracker",
  "DEFAULT_AWS_REGION": "eu-west-1",
  "LOG_LEVEL": "DEBUG"
}