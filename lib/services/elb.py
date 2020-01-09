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
            load_balancers = []
            for page in page_iterator:
                load_balancers.extend([item['LoadBalancerName'] for item in page['LoadBalancerDescriptions']])
            tags = client.describe_tags(LoadBalancerNames=load_balancers)
            self.identifiers.extend([{
                'id': item['LoadBalancerName'],
                'tags': [{
                    'key': t['Key'],
                    'value': t['Value']
                } for t in item['Tags']]
            } for item in tags['TagDescriptions']])
        except Exception: 
            pass