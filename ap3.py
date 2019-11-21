import boto3
from botocore.errorfactory import ClientError
import time

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
ec2_ohio = boto3.resource('ec2', region_name='us-east-2')
client_ohio =boto3.client('ec2', region_name='us-east-2')

def create_KeyPair(ec2, r="n"):
    if r == "n":
        try:
            key_pair = ec2.create_key_pair(
                KeyName='key-leite',
                DryRun=False
            )
            outfile = open('key-leite.pem','w')
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)
            outfile.close()
            print("Created new keypair")

        except ClientError:
            
            print("Keypair already exists")
            key_pair = ec2.KeyPair('key-leite')  
            response = key_pair.delete(
                DryRun=False
            )    
            print("     Deleted existing keypair")
            key_pair = ec2.create_key_pair(
                KeyName='key-leite',
                DryRun=False
            )
            outfile = open('key-leite.pem','w')
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)
            outfile.close()
            print("     Created new keypair")

    if r =="o":
        try:
            key_pair = ec2.create_key_pair(
                KeyName='key-leite-ohio',
                DryRun=False
            )
            outfile = open('key-leite-ohio.pem','w')
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)
            outfile.close()
            print("Created new keypair in ohio")

        except ClientError:
            
            print("Keypair already exists in ohio")
            key_pair = ec2.KeyPair('key-leite-ohio')  
            response = key_pair.delete(
                DryRun=False
            )    
            print("     Deleted existing keypair in ohio")
            key_pair = ec2.create_key_pair(
                KeyName='key-leite-ohio',
                DryRun=False
            )
            outfile = open('key-leite-ohio.pem','w')
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)
            outfile.close()
            print("     Created new keypair in ohio")

def create_SecGroup(ec2,client,vpc,r,eipDB,eipWS,eipFW):
    if r == "o":
        vpc = "vpc-08f8c860"

        try:
            response = ec2.create_security_group(GroupName='SEC-leite',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response.authorize_ingress(
                GroupName='SEC-leite',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',#####
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, 
                ],
                DryRun=False
            )
            print("Created new FW SecurityGroup")

        except ClientError:

            print("FW SecurityGroup already exists")
            group_name = 'SEC-leite' ###

            response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=[group_name])])
            group_id = response['SecurityGroups'][0]['GroupId']
            print(group_id)
            secgroup = ec2.SecurityGroup(group_id)  
            response = secgroup.delete(
                DryRun=False
                )    

            print("     Deleted existing FW SecurityGroup")
            
            response = ec2.create_security_group(GroupName='SEC-leite', ####
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response.authorize_ingress(
                GroupName='SEC-leite',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',#####
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, 
                ],
                DryRun=False
            )
            print("     Created new FW SecurityGroup")

        try:
            response = ec2.create_security_group(GroupName='SEC-leite-lb',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response.authorize_ingress(
                GroupName='SEC-leite-lb',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',#####
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, 
                    {'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ],
                DryRun=False
            )
            print("Created new LB SecurityGroup")

        except ClientError:
            print("LB SecurityGroup already exists")

            try:
                print("     Deleting Load Balancer")
                elb_client = boto3.client('elb',region_name='us-east-2')
                response = elb_client.delete_load_balancer(LoadBalancerName='LoadBalancer-gpl')
                time.sleep(10)
                print("     Load Balancer deleted")
            except:
                print("\n +++++++++++++++")
            try:
                auto_client = boto3.client('autoscaling', region_name='us-east-2')
                response = auto_client.delete_auto_scaling_group(
                            AutoScalingGroupName='AutoScaling-gpl',
                            ForceDelete=True
                            )
                print("     Auto Scaling Group already exists")
                print("     Auto Scaling Group deleted")
                time.sleep(60)
            except:
                print("\n ===============")

            response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-lb'])])
            group_id = response['SecurityGroups'][0]['GroupId']
            secgroup = ec2.SecurityGroup(group_id)  
            response = secgroup.delete(
                DryRun=False
                )    
        
            print("     Deleted existing LB SecurityGroup")
            
            response = ec2.create_security_group(GroupName='SEC-leite-lb',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response.authorize_ingress(
                GroupName='SEC-leite-lb',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',#####
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, 
                    {'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ],
                DryRun=False
            )
            print("     Created new LB SecurityGroup")

    else:
        vpc = "vpc-ec925f96"

        try:
            response1 = ec2.create_security_group(GroupName='SEC-leite-WS',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response1.authorize_ingress(
                GroupName='SEC-leite-WS',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp':eipFW["PublicIp"]+"/32"}]},## IP DO FOWARDer
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ],
                DryRun=False
            )

            response2 = ec2.create_security_group(GroupName='SEC-leite-DB',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )
            response2.authorize_ingress(
                GroupName='SEC-leite-DB',
                IpPermissions=[
                    
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 27017,
                    'ToPort': 27017,
                    'IpRanges': [{'CidrIp': eipWS["PublicIp"]+"/32"}]} ## IP DO WS
                ],
                DryRun=False
            )
            print("Created new SecurityGroups")

        except ClientError:

            print("SecurityGroups already exists")
            
            response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-WS'])])
            group_id = response['SecurityGroups'][0]['GroupId']
            secgroup = ec2.SecurityGroup(group_id)  
            response = secgroup.delete(
                DryRun=False
                )    
            try:
                time.sleep(10)
                response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-DB'])])
                group_id = response['SecurityGroups'][0]['GroupId']
                secgroup = ec2.SecurityGroup(group_id)  
                response = secgroup.delete(
                    DryRun=False
                    )  
            except ClientError:
                    print("hmm")

        
            print("     Deleted existing SecurityGroups")
            
            response1 = ec2.create_security_group(GroupName='SEC-leite-WS',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response2 = ec2.create_security_group(GroupName='SEC-leite-DB',
                                                Description='DESCRIPTION',
                                                VpcId=vpc,
                                                DryRun=False
                                                )

            response1.authorize_ingress(
                GroupName='SEC-leite-WS',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': eipFW["PublicIp"]+"/32"}]},## IP DO FOWARD
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ],
                DryRun=False
            )

            response2.authorize_ingress(
                GroupName='SEC-leite-DB',
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 27017,
                    'ToPort': 27017,
                    'IpRanges': [{'CidrIp':eipWS["PublicIp"]+"/32"}]} ## IP DO WS
                ],
                DryRun=False
            )
            print("     Created new SecurityGroups")

def delete_instances(ec2):

    instances = ec2.instances.filter(Filters=[{"Name": "tag:Owner", "Values": ["guilhermepl3"]}])

    RunningInstances = [instance.id for instance in instances if instance.state['Name'] == 'running']

    if len(RunningInstances) > 0:

        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).terminate()
        #print (shuttingDown)
    else:
        print ("No running instance with this tag")

    time.sleep(2)
    if len([instance.id for instance in instances if instance.state['Name'] == 'shutting-down'])>0:
        print("Terminating instances...")
        time.sleep(30)

    if len([instance.id for instance in instances if instance.state['Name'] == 'shutting-down'])>0:
        print("Terminating instances....")
        time.sleep(20)

def create_Instance(ec2,client,eipWS,eipDB):  # =~ 2 min pra subir o servidor

    ami = "ami-04763b3055de4860b" # Imagem
    tag_owner = {"Key": "Owner", "Value": "guilhermepl3"}
    tag_name = {"Key": "Name", "Value": "Webserver-gpl"}
    instance_type = "t2.micro"
    key_name = 'key-leite' # Nome do key pair

    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-WS'])]) # Pega o id do security group
    group_id = response['SecurityGroups'][0]['GroupId']
    commands = '''#!/bin/bash
sudo su
git clone https://github.com/guipleite/Spark_REST.git
sudo chmod +x /Spark_REST/installer.sh
sudo /Spark_REST/installer.sh
echo "export serv_addr={}" >> ~/.bashrc
export serv_addr={}
python3 /Spark_REST/aps1.py
'''.format(eipDB["PublicIp"],eipDB["PublicIp"])#python3 /Spark_REST/aps1.py

    instance = ec2.create_instances(ImageId=ami,
                        MinCount=1,MaxCount=1,    
                        InstanceType=instance_type, 
                        KeyName=key_name,
                        SecurityGroupIds=['SEC-leite-WS'],
                        TagSpecifications=[{'ResourceType': 'instance','Tags': [tag_owner,tag_name]}],
                        UserData=commands
                        )
    print("Creating new instance: Webserver")
    instance[0].wait_until_running()

    client.associate_address(
     DryRun = False,
     InstanceId = instance[0].id,
     AllocationId = eipWS["AllocationId"])

    print("     Done!")


def create_database(ec2,client,eipDB,eipWS): # =~ 2min? pra subir 
 
    ami = "ami-04763b3055de4860b" # Imagem
    tag_owner = {"Key": "Owner", "Value": "guilhermepl3"}
    tag_name = {"Key": "Name", "Value": "Database-gpl"}
    instance_type = "t2.micro"
    key_name = 'key-leite' # Nome do key pair

    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-DB'])]) # Pega o id do security group
    group_id = response['SecurityGroups'][0]['GroupId']
    commands = '''#!/bin/bash
git clone https://github.com/guipleite/Spark_REST.git
sudo chmod +x /Spark_REST/dbinstaller.sh
sudo /Spark_REST/dbinstaller.sh
sudo mongod --port 27017 --dbpath /data/db --bind_ip_all
'''#sudo mongod --port 27017 --dbpath /data/db --bind_ip_all

    instance = ec2.create_instances(ImageId=ami,
                        MinCount=1,MaxCount=1,    
                        InstanceType=instance_type, 
                        KeyName=key_name,
                        SecurityGroupIds=['SEC-leite-DB'],
                        TagSpecifications=[{'ResourceType': 'instance','Tags': [tag_owner,tag_name]}],
                        UserData=commands
                        )
                         
    print("Creating new instance: Database")
    print("     Setting up Database ...")
    instance[0].wait_until_running()

    client.associate_address(
     DryRun = False,
     InstanceId = instance[0].id,
     AllocationId = eipDB["AllocationId"])

    print("     Done!")

def create_Fowarder(ec2,client, eipws,eipFW):  # =~ 2 min pra subir o servidor

    ami = "ami-0d03add87774b12c5" # Imagem
    tag_owner = {"Key": "Owner", "Value": "guilhermepl3"}
    tag_name = {"Key": "Name", "Value": "Fowarder-gpl"}
    instance_type = "t2.micro"
    group_name = 'SEC-leite-lb' # Nome do Security group
    key_name = 'key-leite-ohio' # Nome do key pair

    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=[group_name])]) # Pega o id do security group
    group_id = response['SecurityGroups'][0]['GroupId']
    commands = '''#!/bin/bash
sudo su
git clone https://github.com/guipleite/Spark_REST.git
sudo chmod +x /Spark_REST/installer.sh
sudo /Spark_REST/installer.sh
echo "export serv_addr={}" >> ~/.bashrc
export serv_addr={}
python3 /Spark_REST/fowarder.py
'''.format(eipws["PublicIp"],eipws["PublicIp"])#python3 /Spark_REST/fowarder.py
    print("Created new instance: Fowarder")
    instance = ec2.create_instances(ImageId=ami,
                        MinCount=1,MaxCount=1,    
                        InstanceType=instance_type, 
                        KeyName=key_name,
                        SecurityGroupIds=[group_id],
                        TagSpecifications=[{'ResourceType': 'instance','Tags': [tag_owner,tag_name]}],
                        UserData=commands
                        )
    instance[0].wait_until_running()
    client.associate_address(
     DryRun = False,
     InstanceId = instance[0].id,
     AllocationId = eipFW["AllocationId"])
    print("     Done !")

    commands = '''#!/bin/bash
sudo su
git clone https://github.com/guipleite/Spark_REST.git
sudo chmod +x /Spark_REST/installer.sh
sudo /Spark_REST/installer.sh
echo "export serv_addr={}" >> ~/.bashrc
export serv_addr={}
python3 /Spark_REST/fowarder.py
'''.format(eipFW["PublicIp"],eipFW["PublicIp"])#python3 /Spark_REST/fowarder.py

    instance = ec2.create_instances(ImageId=ami,
                        MinCount=1,MaxCount=1,    
                        InstanceType=instance_type, 
                        KeyName=key_name,
                        SecurityGroupIds=[group_id],
                        TagSpecifications=[{'ResourceType': 'instance','Tags': [tag_owner,{"Key": "Name", "Value": "Fowarder-LB-gpl"}]}],
                        UserData=commands
                        )

    print("Creating new instance: LB-fowarder")
    instance[0].wait_until_running()

    print("     Done!")
    print("Creating Image")
    time.sleep(150)

    try:
        print("Creating Image...")
        res = client.create_image(InstanceId=instance[0].id, NoReboot=True, Name="fowarder_image")
        print("Image created")

    except:
        print("Image already exists")
        response = client.describe_images(Filters=[{'Name': 'name','Values': ['fowarder_image']}])
        image_id = response['Images'][0]['ImageId']

        client.deregister_image(ImageId = image_id)
        print("     Image deleted")
        res = client.create_image(InstanceId=instance[0].id, NoReboot=True, Name="fowarder_image")
        print("     New Image created")
        ami_id = res['ImageId']
    print("     Image id: "+ami_id)

    print("Creating Launch Confuguration...")
    auto_client = boto3.client('autoscaling', region_name='us-east-2')
    time.sleep(90)

    try:
        response = auto_client.create_launch_configuration(
        LaunchConfigurationName='LaunchConfig-gpl',
        ImageId=ami_id,
        KeyName=key_name,
        SecurityGroups=[group_name],
        InstanceType=instance_type,
        )
    except:
        print("     Launch Confuguration already exists")
        response = auto_client.delete_launch_configuration(LaunchConfigurationName='LaunchConfig-gpl')
        print("     Launch Confuguration deleted")
        response = auto_client.create_launch_configuration(
        LaunchConfigurationName='LaunchConfig-gpl',
        ImageId=ami_id,
        KeyName=key_name,
        SecurityGroups=[group_name],
        InstanceType=instance_type,
        )
    print("     New Launch Confuguration created")
       
    print("Creating Target Group...")

    elastic_client = boto3.client('elbv2', region_name='us-east-2')

    try:
        response = elastic_client.create_target_group(
                    Name='TargetGroup-gpl',
                    Protocol='HTTP',
                    Port=80,
                    VpcId="vpc-08f8c860",
                    HealthCheckProtocol='HTTP',
                    HealthCheckPort='5000',
                    HealthCheckEnabled=True,
                    HealthCheckPath='/healthcheck/',
                    HealthCheckIntervalSeconds=30,
                    HealthCheckTimeoutSeconds=5,
                    HealthyThresholdCount=5,
                    UnhealthyThresholdCount=2,
                    Matcher={
                        'HttpCode': '200'
                    },
                    TargetType='instance'
                    )
    except:
        print("    Target Group already exists")
        response = elastic_client.describe_target_groups(Names=['TargetGroup-gpl'])

        response = elastic_client.delete_target_group(TargetGroupArn=response['TargetGroups'][0]['TargetGroupArn'])
        print("     Target Group deleted")
        response = elastic_client.create_target_group(
                    Name='TargetGroup-gpl',
                    Protocol='HTTP',
                    Port=80,
                    VpcId="vpc-08f8c860",
                    HealthCheckProtocol='HTTP',
                    HealthCheckPort='5000',
                    HealthCheckEnabled=True,
                    HealthCheckPath='/healthcheck/',
                    HealthCheckIntervalSeconds=30,
                    HealthCheckTimeoutSeconds=5,
                    HealthyThresholdCount=5,
                    UnhealthyThresholdCount=2,
                    Matcher={
                        'HttpCode': '200'
                    },
                    TargetType='instance'
                    )

    print("     New Target Group created")

    print("Creating Load Balancer...")

    elb_client = boto3.client('elb',region_name='us-east-2')
    response = client.describe_security_groups(Filters=[dict(Name='group-name', Values=['SEC-leite-lb'])])
    group_id = response['SecurityGroups'][0]['GroupId']

    try:
        response = elb_client.create_load_balancer(
            LoadBalancerName='LoadBalancer-gpl',
            SecurityGroups=[group_id],
            Listeners=[
            {
            'Protocol': 'tcp',
            'LoadBalancerPort': 8080,
            'InstanceProtocol': 'tcp',
            'InstancePort': 5000    
            },
            ],
            AvailabilityZones=[
                'us-east-2a','us-east-2b','us-east-2c'
            ],
            Scheme='internet-facing',
        )

    except:
        print("    Load Balancer already exists")
        response = elb_client.delete_load_balancer(LoadBalancerName='LoadBalancer-gpl')
        print("     Load Balancer deleted")
        response = elb_client.create_load_balancer(
            LoadBalancerName='LoadBalancer-gpl',
            SecurityGroups=[group_id],
            Listeners=[
            {
            'Protocol': 'tcp',
            'LoadBalancerPort': 80,
            'InstanceProtocol': 'tcp',
            'InstancePort': 5000    
            },
            ],
            AvailabilityZones=[
                'us-east-2a','us-east-2b','us-east-2c'
            ],
            Scheme='internet-facing',
        )

    print("     Load Balancer created")

    print("Creting Auto Scaling Group")
    Arnresponse = elastic_client.describe_target_groups(Names=['TargetGroup-gpl'])
    Arn = Arnresponse['TargetGroups'][0]['TargetGroupArn']

    try:
        response = auto_client.delete_auto_scaling_group(
                    AutoScalingGroupName='AutoScaling-gpl',
                    ForceDelete=True
                    )
        print("     Auto Scaling Group already exists")
        print("     Auto Scaling Group deleted")

    except:
        print("hmmm")
    
    response = auto_client.create_auto_scaling_group(
            AutoScalingGroupName='AutoScaling-gpl',
            LaunchConfigurationName='LaunchConfig-gpl',
            MinSize=1,
            MaxSize=3,
            DesiredCapacity=1,
            DefaultCooldown=300,
            AvailabilityZones=['us-east-2a','us-east-2b','us-east-2c'],
            LoadBalancerNames=['LoadBalancer-gpl'],
            TargetGroupARNs=[Arn],
            HealthCheckType='EC2',
            HealthCheckGracePeriod=0,
        )
    print("Creted new Auto Scaling Group")


    print("     Done!")


eipWS = client.allocate_address(DryRun=False, Domain='vpc')
eipDB = client.allocate_address(DryRun=False, Domain='vpc')
eipFW = client_ohio.allocate_address(DryRun=False, Domain='vpc')

print("   eipWS:"+eipWS["PublicIp"])
print("   eipDB:"+eipDB["PublicIp"])
print("   eipFW:"+eipFW["PublicIp"])

print("\n N. Virginia")

delete_instances(ec2)
vpc = "vpc-ec925f96"
try:
    create_SecGroup(ec2,client,vpc,"n",eipDB,eipWS,eipFW)
except:
    print("Instances weren't terminated correctly, trying again")
    delete_instances(ec2)
    time.sleep(30)
    create_SecGroup(ec2,client,vpc,"n",eipDB,eipWS,eipFW)

create_KeyPair(ec2)
create_database(ec2,client,eipDB,eipWS)
create_Instance(ec2,client,eipWS,eipDB)

print("\n Ohio")

vpc = "vpc-08f8c860"

delete_instances(ec2_ohio)
try:
    create_SecGroup(ec2_ohio,client_ohio,vpc,"o",eipDB,eipWS,eipFW)
except:
    print("Instances in Ohio weren't terminated correctly, trying again")
    delete_instances(ec2_ohio)
    time.sleep(30)
    create_SecGroup(ec2_ohio,client_ohio,vpc,"o",eipDB,eipWS,eipFW)
create_KeyPair(ec2_ohio,"o")
#eipWS = "34.198.234.225"
create_Fowarder(ec2_ohio,client_ohio,eipWS,eipFW)


