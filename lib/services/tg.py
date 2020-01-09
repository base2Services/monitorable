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
            target_group_arns = []
            for page in page_iterator:
                # self.identifiers.extend([item['TargetGroupArn'].split(':')[-1] for item in page['TargetGroups']])
                target_group_arns.extend([item['TargetGroupArn'] for item in page['TargetGroups']])
            tags = client.describe_tags(ResourceArns=target_group_arns)
            self.identifiers.extend([{
                'id': item['ResourceArn'].split(':')[-1],
                'tags': [{
                    'key': t['Key'],
                    'value': t['Value']
                } for t in item['Tags']]
            } for item in tags['TagDescriptions']])
        except Exception: 
            pass