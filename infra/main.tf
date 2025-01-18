provider "aws" {
  region = "ap-southeast-2"
}

variable "home_ip" {
  description = " SSH access"
  type        = string
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.home_ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-0d11f9bfe33cfbe8b" # free tier Amazon Linux 2023 AMI
  instance_type = "t2.micro"
  key_name      = "rsakey"

  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  tags = {
    Name = "AppServer"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              EOF
}

output "instance_public_ip" {
  value = aws_instance.app_server.public_ip
}