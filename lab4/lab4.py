import boto3
import requests
import json
import time


ec2 = boto3.resource('ec2', region_name='us-east-1')

print('Starting EC2')
start = time.time()

instance = ec2.create_instances(
        ImageId="ami-02f28876a96187313",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=["launch-wizard-1"]
    )[0]

instance.wait_until_running()

end = time.time()
print('EC2 started in:', end - start)


ec2_client = boto3.client('ec2', region_name='us-east-1')
description = ec2_client.describe_instances(InstanceIds=[instance.id])
ip = description["Reservations"][0]["Instances"][0]["PublicIpAddress"]

address = 'http://' + ip + ':80'
response = requests.get(address)
print('Downloading file')
print(response.text)
with open('index.html', 'w+') as f:
    f.write(response.text)

print('Shuting down EC2')
instance.terminate()
print('Done')
