#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.infrastructure_stack import NginxCicdStack

app = cdk.App()

# Specify the environment (account and region)
env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
    region=os.getenv('CDK_DEFAULT_REGION'))

NginxCicdStack(app, 
    "nginx-cicd-stack", 
    env=env, 
    description="Stack for deploying Nginx with CI/CD pipeline"
)

app.synth()