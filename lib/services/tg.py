import boto3

class Tg:

    def __init__(self,region):
        self.name = 'tg'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('elbv2', region_name=self.region)
            paginator = client.get_paginator('describe_target_groups')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['TargetGroupName'] for item in page['TargetGroups']])
        except Exception: 
            pass