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
            if load_balancers:
                for i in range(0, len(load_balancers), 20):
                    tags = client.describe_tags(LoadBalancerNames=load_balancers[i:i + 20])
                    self.identifiers.extend([{
                        'id': item['LoadBalancerName'],
                        'tags': [{
                            'key': t['Key'],
                            'value': t['Value']
                        } for t in item['Tags']]
                    } for item in tags['TagDescriptions']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass