import boto3


class Glue:

    def __init__(self, region):
        self.name = 'glue'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'Glue',
            'cfn-guardian': 'Glue'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('glue', region_name=self.region)
            paginator = client.get_paginator('get_jobs')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['Name'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['Jobs']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
