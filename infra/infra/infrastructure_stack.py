from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
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
            description="Allow SSH access from anywhere",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(22), "Allow SSH access")

        # Define the EC2 instance
        ec2_instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),  
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=security_group,
            key_pair=ec2.KeyPair.from_key_pair_name(self, "InstanceKeyPair", "rsakey")
        )

        # Add a Name Tag to EC2 instance
        ec2_instance.add_property_override("Tags", [{"Key": "Name", "Value": "NginxInstance"}])