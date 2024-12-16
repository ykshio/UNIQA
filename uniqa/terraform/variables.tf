# AWSのリージョン
variable "aws_region" {
  description = "AWSのリージョン"
  type = string
  default = "ap-northeast-1"
}

# EC2インスタンスのタイプ
variable "instance_type" {
  description = "EC2インスタンスのタイプ"
  type = string
  default = "t2.micro"
}

# EC2インスタンスのAMI
variable "ami_id" {
  description = "EC2インスタンスのAMI ID"
  type = string
}