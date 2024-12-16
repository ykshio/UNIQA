# プロバイダの設定
provider "aws" {
  region = "ap-southeast-2"
}

# VPCの作成

# セキュリティグループの作成
resource "aws_security_group" "allow_ssh_http" {
  name        = "allow_ssh_http"
  description = "Allow SSH and HTTP access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2インスタンスの作成
resource "aws_instance" "uniqa" {
  ami           = "ami-0146fc9ad419e2cfd"
  instance_type = "t2.micro"
  key_name      = "MacAWS"
  security_groups = [aws_security_group.allow_ssh_http.name]

  tags = {
    Name = "UNIQA"
  }
  
}
# Elastic IPの作成
