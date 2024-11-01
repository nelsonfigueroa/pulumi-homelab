import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import pulumi_eks as eks
import pulumi_kubernetes as k8s
import json

# Get some values from the Pulumi configuration (or use defaults)
config = pulumi.Config()
min_cluster_size = config.get_int("minClusterSize", 3)
max_cluster_size = config.get_int("maxClusterSize", 6)
desired_cluster_size = config.get_int("desiredClusterSize", 3)
eks_node_instance_type = config.get("eksNodeInstanceType", "t3.medium")
vpc_network_cidr = config.get("vpcNetworkCidr", "10.0.0.0/16")

# Create a VPC for the EKS cluster
eks_vpc = awsx.ec2.Vpc("eks-vpc",
    enable_dns_hostnames=True,
    cidr_block=vpc_network_cidr)

# Create the EKS cluster
eks_cluster = eks.Cluster("eks-cluster",
    # Put the cluster in the new VPC created earlier
    vpc_id=eks_vpc.vpc_id,
    # Public subnets will be used for load balancers
    public_subnet_ids=eks_vpc.public_subnet_ids,
    # Private subnets will be used for cluster nodes
    private_subnet_ids=eks_vpc.private_subnet_ids,
    # Change configuration values to change any of the following settings
    instance_type=eks_node_instance_type,
    desired_capacity=desired_cluster_size,
    min_size=min_cluster_size,
    max_size=max_cluster_size,
    # Do not give worker nodes a public IP address
    node_associate_public_ip_address=False,
    # Change these values for a private cluster (VPN access required)
    endpoint_private_access=False,
    endpoint_public_access=True
)

# IAM Role for EKS Fargate Profile
fargate_iam_role = aws.iam.Role("fargate_iam_role",
    name="eks-fargate-profile-example",
    assume_role_policy=json.dumps({
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "eks-fargate-pods.amazonaws.com",
            },
        }],
        "Version": "2012-10-17",
    })
)

# Pod execution policy for EKS fargate profile
pod_execution_role = aws.iam.RolePolicyAttachment("example-AmazonEKSFargatePodExecutionRolePolicy",
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy",
    role=fargate_iam_role.name)


fargate_profile = aws.eks.FargateProfile("example_fargate_profile",
    cluster_name=eks_cluster.name, # i think this is not working
    fargate_profile_name="fargate-profile",
    pod_execution_role_arn=fargate_iam_role.arn,
    subnet_ids=eks_vpc.private_subnet_ids, # i guess only private subnets work?
    selectors=[{
        "namespace": "default", "labels": { "app.kubernetes.io/name": "workflow-runner" }
    }],
    opts=pulumi.ResourceOptions(depends_on=[eks_cluster])
)


# Apply a Kubernetes YAML manifest after EKS + Fargate has been set up
config_file = k8s.yaml.ConfigFile("raw-deployment-manifest",
    file="raw_deployment.yaml",
    opts=pulumi.ResourceOptions(depends_on=[fargate_profile])
)

# Export values to use elsewhere
# pulumi.export("kubeconfig", eks_cluster.kubeconfig)
# pulumi.export("vpcId", eks_vpc.vpc_id)
# pulumi.export("fargate_profile_name", fargate_profile.fargate_profile_name)