import boto3

class Apigateway:

    def __init__(self,region):
        self.name = 'apigateway'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('apigateway', region_name=self.region)
            paginator = client.get_paginator('get_rest_apis')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['name'] for item in page['items']])
        except Exception: 
            pass

        try:
            client = boto3.client('apigatewayv2', region_name=self.region)
            paginator = client.get_paginator('get_apis')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['Name'] for item in page['Items']])
        except Exception: 
            pass