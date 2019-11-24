import boto3

def delete_instances(ec2,client):
    
    response = client.describe_addresses()

    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']},
        {"Name": "tag:Owner",
        "Values": ["guilhermepl3"]}])

    
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']},
        {"Name": "tag:Owner",
        "Values": ["guilhermepl3"]}])

    for instance in running_instances:
        for addr in response['Addresses']:
            if addr['PublicIp']==instance.public_ip_address:
                client.release_address(
                    AllocationId=addr['AllocationId'],
                    DryRun=False
                )
        ec2.instances.filter(InstanceIds=[instance.id]).terminate()
        print("Terminating instances...")
        time.sleep(40)
        #print (shuttingDown)
    else:
        print ("No running instance with this tag")
        time.sleep(10)

def nuke():
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    ec2_ohio = boto3.resource('ec2', region_name='us-east-2')
    client_ohio =boto3.client('ec2', region_name='us-east-2')
    elastic_client = boto3.client('elbv2', region_name='us-east-2')
    elb_client = boto3.client('elb',region_name='us-east-2')
    auto_client = boto3.client('autoscaling', region_name='us-east-2')

    try:
        delete_instances(ec2,client)
    except:
        print("a")
    try:
        delete_instances(ec2_ohio,client_ohio)
    except:
        print("a")

    try:
        response = auto_client.delete_auto_scaling_group(
                    AutoScalingGroupName='AutoScaling-gpl',
                    ForceDelete=True
                    )
    except:
        print("a")
    response = elastic_client.describe_target_groups(Names=['TargetGroup-gpl'])
    response = elastic_client.delete_target_group(TargetGroupArn=response['TargetGroups'][0]['TargetGroupArn'])
    response = elb_client.delete_load_balancer(LoadBalancerName='LoadBalancer-gpl')
    response = auto_client.delete_launch_configuration(LaunchConfigurationName='LaunchConfig-gpl')
    response = client_ohio.describe_images(Filters=[{'Name': 'name','Values': ['fowarder_image']}])
    image_id = response['Images'][0]['ImageId']
    client_ohio.deregister_image(ImageId = image_id)
    response = client_ohio.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-lb'])])
    group_id = response['SecurityGroups'][0]['GroupId']
    secgroup = ec2_ohio.SecurityGroup(group_id)  
    response = secgroup.delete(
        DryRun=False
        )     
    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-WS'])])
    group_id = response['SecurityGroups'][0]['GroupId']
    secgroup = ec2.SecurityGroup(group_id)  
    response = secgroup.delete(
        DryRun=False
        )     
    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-DB'])])
    group_id = response['SecurityGroups'][0]['GroupId']
    secgroup = ec2.SecurityGroup(group_id)  
    response = secgroup.delete(
        DryRun=False
        )  
    print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM")   

nuke()