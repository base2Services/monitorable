import boto3

class Ecs:

    def __init__(self,region):
        self.name = 'ecs'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('ecs', region_name=self.region)
            paginator = client.get_paginator('list_clusters')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item.split('/')[-1] for item in page['clusterArns']])
        except Exception: 
            pass