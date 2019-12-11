import boto3

class Mq:

    def __init__(self,region):
        self.name = 'mq'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('mq', region_name=self.region)
            paginator = client.get_paginator('list_brokers')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend(item['BrokerId'] for item in page['BrokerSummaries'])
        except Exception: 
            pass