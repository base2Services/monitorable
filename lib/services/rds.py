import boto3

class Rds:

    def __init__(self,region):
        self.name = 'rds'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('rds', region_name=self.region)
            paginator = client.get_paginator('describe_db_instances')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['DBInstanceIdentifier'] for item in page['DBInstances'] if "DBClusterIdentifier" not in item])
        except Exception: 
            pass