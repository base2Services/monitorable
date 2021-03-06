import boto3


class Asg:

    def __init__(self, region):
        self.name = 'asg'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'AutoScalingGroup',
            'cfn-guardian': 'AutoScalingGroup'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('autoscaling', region_name=self.region)
            paginator = client.get_paginator('describe_auto_scaling_groups')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['AutoScalingGroupName'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['AutoScalingGroups']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
