import boto3

class Asg:

    def __init__(self,region):
        self.name = 'asg'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('autoscaling', region_name=self.region)
            paginator = client.get_paginator('describe_auto_scaling_groups')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['AutoScalingGroupName'] for item in page['AutoScalingGroups']])
        except Exception: 
            pass