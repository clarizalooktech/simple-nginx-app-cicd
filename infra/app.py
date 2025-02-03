#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.infrastructure_stack import NginxCicdStack

app = cdk.App()
NginxCicdStack(app, "nginx-cicd-stack")

app.synth()
