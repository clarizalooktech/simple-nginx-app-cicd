from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    Tags,
    CfnOutput
)
from constructs import Construct

class NginxCicdStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Use the default VPC
        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        # Define the security group
        security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="Allow SSH and HTTP access",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(22), "Allow SSH access")
        security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(80), "Allow HTTP access")

        # Create a role for the EC2 instance with ECR access
        instance_role = iam.Role(self, "InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Add ECR policy to the role
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess")
        )

        # Define the EC2 instance with the custom role
        ec2_instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=security_group,
            key_name="rsakey",
            role=instance_role,  # Assign the role with ECR permissions
            user_data=ec2.UserData.custom(self._get_user_data())
        )

        # Add a Name Tag to EC2 instance
        Tags.of(ec2_instance).add("Name", "NginxInstance")

        # Output the instance ID and public IP
        CfnOutput(self, "InstanceId", value=ec2_instance.instance_id)
        CfnOutput(self, "InstancePublicIp", value=ec2_instance.instance_public_ip)

    def _get_user_data(self):
        return """#!/bin/bash
# Update system packages
yum update -y

# Install Docker
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install AWS CLI v2 if needed
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
./aws/install --update
rm -rf aws awscliv2.zip

# Create a status file to signal instance is ready
touch /tmp/instance_ready

# Log completion
echo "Instance setup complete"
"""