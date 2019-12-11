import boto3

class Elasticache:

    def __init__(self,region):
        self.name = 'elasticache'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('elasticache', region_name=self.region)
            paginator = client.get_paginator('describe_replication_groups')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['ReplicationGroupId'] for item in page['ReplicationGroups']])
        except Exception: 
            pass