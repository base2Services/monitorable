import boto3

class Dynamodb:

    def __init__(self,region):
        self.name = 'dynamodb'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('dynamodb', region_name=self.region)
            paginator = client.get_paginator('list_tables')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item for item in page['TableNames']])
        except Exception: 
            pass