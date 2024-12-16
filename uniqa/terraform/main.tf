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

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y

              # gitのインストール
              sudo yum install -y git

              # python3のインストール
              sudo yum install -y python3

              # pipのインストール 
              sudo yum install -y python3-pip

              # Nginxのインストール
              sudo yum install -y nginx

              # GitHubからソースコードを取得
              git clone https://github.com/ykshio/UNIQA.git /home/ec2-user/uniqa

              # 必要なPythonライブラリのインストール
              cd /home/ec2-user/uniqa
              pip3 install -r requirements.txt

              # Nginxの起動
              systemctl start nginx
              systemctl enable nginx

              # その他、UNIQA用のセットアップを実行（例: Djangoのマイグレーションなど）
              cd /home/ec2-user/uniqa
              python3 manage.py migrate
              python3 manage.py collectstatic --noinput

              EOF
  tags = {
    Name = "UNIQA"
  }
  
}

# Elastic IPの作成
resource "aws_eip" "uniqa_eip" {
  instance = aws_instance.uniqa.id
}

