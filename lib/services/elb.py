import boto3

class Elb:

    def __init__(self,region):
        self.name = 'elb'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('elb', region_name=self.region)
            paginator = client.get_paginator('describe_load_balancers')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['LoadBalancerName'] for item in page['LoadBalancerDescriptions']])
        except Exception: 
            pass