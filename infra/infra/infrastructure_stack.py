from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    Tags
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
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECR-FullAccess")
        )
        
        # Define the EC2 instance with the custom role
        ec2_instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),  
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=security_group,
            key_name="rsakey",
            role=instance_role  # Assign the role with ECR permissions
        )
        
        # Add user data to install Docker
        ec2_instance.add_user_data(
            "yum update -y",
            "amazon-linux-extras install docker -y",
            "service docker start",
            "usermod -a -G docker ec2-user",
            "systemctl enable docker"
        )

        # Add a Name Tag to EC2 instance
        Tags.of(ec2_instance).add("Name", "NginxInstance")