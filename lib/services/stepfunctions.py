import boto3


class Stepfunctions:

    def __init__(self, region):
        self.name = 'stepfunctions'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'Stepfunctions',
            'cfn-guardian': 'Stepfunctions'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('stepfunctions', region_name=self.region)
            paginator = client.get_paginator('list_state_machines')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['name'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['stateMachines']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
