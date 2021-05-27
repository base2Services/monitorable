import boto3


class Batch:

    def __init__(self, region):
        self.name = 'batch'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'Batch',
            'cfn-guardian': 'Batch'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('batch', region_name=self.region)
            paginator = client.get_paginator('describe_job_queues')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['jobQueueName'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['jobQueues']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
