import boto3

class Lambda:

    def __init__(self,region):
        self.name = 'lambda'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('lambda', region_name=self.region)
            paginator = client.get_paginator('list_functions')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['FunctionName'] for item in page['Functions']])
        except Exception: 
            pass