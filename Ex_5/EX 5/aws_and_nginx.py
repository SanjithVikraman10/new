import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')
user_data_script = '''#!/bin/bash
sudo yum update -y
sudo yum install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
echo "<h1>Welcome to Web Server</h1>" > /usr/share/nginx/html/index.html
'''

instances = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0',
    MinCount=2,
    MaxCount=2,
    InstanceType='t2.micro',
    KeyName='KeyPairName',
    SecurityGroupIds=['SecurityGroupId'],
    UserData=user_data_script
)

for instance in instances:
    instance.wait_until_running()
    print(f"Instance {instance.id} created and running.")

elb = boto3.client('elbv2', region_name='us-east-1')

response = elb.create_target_group(
    Name='web-target-group',
    Protocol='HTTP',
    Port=80,
    VpcId='YourVpcId'
)
target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

instance_ids = [instance.id for instance in instances]
elb.register_targets(TargetGroupArn=target_group_arn, Targets=[{'Id': id} for id in instance_ids])

response = elb.create_load_balancer(
    Name='web-load-balancer',
    Subnets=['SubnetId1', 'SubnetId2'],
    SecurityGroups=['SecurityGroupId'],
    Scheme='internet-facing',
    Type='application'
)
load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']

elb.create_listener(
    LoadBalancerArn=load_balancer_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}]
)
print("Load balancer set up successfully.")

autoscaling = boto3.client('autoscaling', region_name='us-east-1')

autoscaling.create_launch_configuration(
    LaunchConfigurationName='web-launch-config',
    ImageId='ami-0c55b159cbfafe1f0',
    InstanceType='t2.micro',
    SecurityGroups=['YourSecurityGroupId'],
    UserData=user_data_script
)

autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='web-auto-scaling-group',
    LaunchConfigurationName='web-launch-config',
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=2,
    VPCZoneIdentifier='SubnetId1,SubnetId2',
    TargetGroupARNs=[target_group_arn]
)

autoscaling.enable_metrics_collection(
    AutoScalingGroupName='web-auto-scaling-group',
    Granularity='1Minute'
)
print("Auto-scaling group with fault tolerance set up.")
