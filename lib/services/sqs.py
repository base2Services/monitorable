import boto3


class Sqs:

    def __init__(self, region):
        self.name = 'sqs'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'SQSQueue',
            'cfn-guardian': 'SQSQueue'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('sqs', region_name=self.region)
            page = client.list_queues()
            queues = []
            if 'QueueUrls' in page:
                queues = [item for item in page['QueueUrls']]
            for queue in queues:
                tags = client.list_queue_tags(QueueUrl=queue)
                self.identifiers.extend([{
                    'id': queue.split('/')[-1],
                    'tags': [{
                        'key': t[0],
                        'value': t[1]
                    } for t in tags.get('Tags', {}).items()]
                }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
