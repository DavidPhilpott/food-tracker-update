resource "aws_lambda_function" "lambda" {
  depends_on    = [data.aws_iam_policy_document.lambda]
  s3_bucket     = var.s3_code_bucket
  s3_key        = var.s3_code_key
  function_name = var.lambda_name
  role          = aws_iam_role.lambda.arn
  handler       = var.lambda_handler

  runtime     = "python3.6"
  memory_size = 1024
  timeout     = 900

  environment {
    variables = var.lambda_environment_variables
  }

  tags = merge(
    {
      "Name" = var.lambda_name
    },
    local.common_tags
  )
}


data "aws_iam_policy_document" "lambda" {
  statement {
    actions = [
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DeleteNetworkInterface"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:${var.region}:${var.aws_account_id}:*"
    ]
  }

  statement {
    actions = [
      "ssm:*"
    ]
    resources = [
      "arn:aws:ssm:${var.region}:${var.aws_account_id}:*"
    ]
  }
}

resource "aws_iam_role" "lambda" {
  name  = "${var.lambda_name}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}
resource "aws_iam_role_policy" "lambda" {
  role   = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.lambda.json
}
