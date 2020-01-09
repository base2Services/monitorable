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
            tables = []
            for page in page_iterator:
                tables.extend([item for item in page['TableNames']])
            for table in tables:
                arn = client.describe_table(TableName=table)['Table']['TableArn']
                tags = client.list_tags_of_resource(ResourceArn=arn)['Tags']
                self.identifiers.extend([{
                    'id': table,
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in tags]
                }])
        except Exception: 
            pass