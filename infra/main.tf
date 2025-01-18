provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0d11f9bfe33cfbe8b" # free tier Amazon Linux 2023 AMI
  instance_type = "t2.micro"

  tags = {
    Name = "NginxAppServer"
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