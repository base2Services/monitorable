import boto3

class Ec2:

    def __init__(self,region):
        self.name = 'ec2'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('ec2', region_name=self.region)
            paginator = client.get_paginator('describe_instances')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                for reservation in page['Reservations']:
                    self.identifiers.extend([item['InstanceId'] for item in reservation['Instances']])
        except Exception: 
            pass