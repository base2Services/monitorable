import boto3

class Sqs:

    def __init__(self,region):
        self.name = 'sqs'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('sqs', region_name=self.region)
            page = client.list_queues()
            if 'QueueUrls' in page:
                self.identifiers = [item.split('/')[-1] for item in page['QueueUrls']]
        except Exception: 
            pass