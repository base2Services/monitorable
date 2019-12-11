import boto3

class Cloudfront:

    def __init__(self,region):
        self.name = 'cloudfront'
        self.region = 'us-east-1'
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('cloudfront', region_name=self.region)
            paginator = client.get_paginator('list_distributions')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                if 'Items' in page['DistributionList']:
                    self.identifiers.extend([item['Id'] for item in page['DistributionList']['Items']])
        except Exception: 
            pass