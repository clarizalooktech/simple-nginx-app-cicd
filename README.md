# Nginx App with CI/CD Deployed in AWS EC2

This project demonstrates a simple web application served by an Nginx server, with automated deployment using Docker and AWS EC2. The process involves creating a Docker image from a provided Dockerfile, pushing it to Amazon ECR, and setting up an EC2 instance that pulls and runs the image.

## Overview

The project consists of the following key components:

1.  **Nginx Application:** A basic web application served by Nginx. The HTML content resides in the `src/` directory, and the Nginx configuration is in `nginx/nginx.conf`.
2.  **Dockerization:** The application is containerized using a Dockerfile, which builds an Nginx image with the application's content and configuration.
3.  **ECR Image Storage:** The built Docker image is pushed to Amazon Elastic Container Registry (ECR) for storage and versioning.
4.  **EC2 Infrastructure:** An Amazon EC2 instance is provisioned to run the Docker container.
5.  **Automated Deployment:** The EC2 instance is configured to pull and run the Docker image from ECR upon startup.


```
├── .github/
│   └── workflows
│       └── deploy.yml                   # CICD Pipeline configuration
├── nginx/
│   └── nginx.conf                       # Nginx configuration file
├── infra/
│   └── infra
|       └── infrastructure_stack.py      # EC2 Infrastructure Setup
├── test/
│   └── unit
|       └── test_infra_stack.py          # Unit Test
├── Dockerfile                           # Dockerfile for building the Nginx image
└── README.md                            # This README file
```


## Docker Image

The `Dockerfile` is defined as follows:

```dockerfile
FROM nginx:alpine
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY src/ /usr/share/nginx/html/
```

## EC2 Infrastructure Setup

Refers to `infrastructure_stack.py`. This script performs the following actions:

- Deploys the EC2
- Updates the system packages.
- Installs Docker and starts the Docker service.
- Adds the ec2-user to the docker group.
- Installs AWS CLI v2.
- creates a file to indicate the instance is ready.
- Deployment Process

## Deployment Process

1. Build Docker Image: Build the Docker image using the Dockerfile.
2. Push to ECR: Tag and push the Docker image to Amazon ECR.
3. Provision EC2 Instance: Launch an EC2 instance with the provided user data script.
4. SSH and Docker Run: SSH into the EC2 instance, log into ECR, and run the Docker image.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/[repo]/nginx-app.git
   cd simple-nginx-app-cicd
2. Rebuild and Restart
    After confirming the Dockerfile and nginx.conf, rebuild the image and run the container:
    ```bash
    docker build -t simple-nginx-app-cicd .
    docker run -d -p 8080:80 simple-nginx-app-cicd
3.  Access application

    [http://localhost:8080](http://localhost:8080)


### Screenshots
![Build Docker setup1](https://github.com/clarizalooktech/simple-nginx-app-cicd/blob/feature/build-cicd-pipeline/assets/build-docker-setup-infra-step1.JPG)

![Build Docker setup in the AWS Console](https://github.com/clarizalooktech/simple-nginx-app-cicd/blob/feature/build-cicd-pipeline/assets/build-docker-setup-infra-step2.JPG)

![Successful Deployment in Github Action](https://github.com/clarizalooktech/simple-nginx-app-cicd/blob/main/assets/build-docker-setup-infra-step3.png)