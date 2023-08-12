terraform {
 required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.9.0"
    }
  }
  cloud {
    organization = "Cataprato"

    workspaces {
      name = "cataprato-auth"
    }
  }
}
provider "aws" {
  region = "us-east-1"
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}


data "aws_caller_identity" "current" {}

data "aws_organizations_organization" "this" {}


module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "5.3.0"

  function_name          = "cataprato-auth-lambda"
  description            = "Cataprato auth"
  handler                = "main.handler"
  runtime                = "python3.10"
  ephemeral_storage_size = 512
  architectures          = ["x86_64"]
  publish                = true

  source_path            = "${path.module}/src"


  store_on_s3 = true
  s3_bucket   = module.s3_bucket.s3_bucket_id
  s3_prefix   = "lambda-builds/"

  artifacts_dir = "${path.root}/.terraform/lambda-builds/"

  layers = [
    module.lambda_layer_s3.lambda_layer_arn,
  ]

 /*  environment_variables = {
    Hello      = "World"
    Serverless = "Terraform"
  } */

  role_path   = "/tf-managed/"
  policy_path = "/tf-managed/"



  allowed_triggers = {
    APIGatewayAny = {
      service    = "apigateway"
      source_arn = "arn:aws:execute-api:us-east-1:${data.aws_caller_identity.current.account_id}:${one(data.aws_apigatewayv2_apis.cataprato.ids)}/*/*"
    }
  }


  create_lambda_function_url = true
  authorization_type         = "AWS_IAM"
  cors = {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
  invoke_mode = "RESPONSE_STREAM"

  policy_statements = {
    dynamodb = {
      effect    = "Allow",
      actions   = ["dynamodb:BatchWriteItem"],
      resources = ["arn:aws:dynamodb:us-east-1:`${data.aws_caller_identity.current.account_id}`:table/Test"]
    },
    s3_read = {
      effect    = "Deny",
      actions   = ["s3:HeadObject", "s3:GetObject"],
      resources = ["arn:aws:s3:::my-bucket/*"]
    }
  }

  timeouts = {
    create = "20m"
    update = "20m"
    delete = "20m"
  }

   tags = {
    Deployment = "terraform"
  } 
}

module "lambda_layer_s3" {
   source  = "terraform-aws-modules/lambda/aws"
  version = "5.3.0"

  create_layer = true

  layer_name          = "cataprato-auth-layer-s3"
  description         = "Pip layer"
  compatible_runtimes = ["python3.10"]

  create_package = true
  source_path = "dist"

  store_on_s3 = true
  s3_bucket   = module.s3_bucket.s3_bucket_id
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.14.1"

  bucket_prefix = "cataprato-auth-"
  force_destroy = true

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning = {
    enabled = true
  }
}

data "aws_apigatewayv2_apis" "cataprato"{
  protocol_type  = "HTTP"
}