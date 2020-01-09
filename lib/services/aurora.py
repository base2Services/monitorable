import boto3

class Aurora:

    def __init__(self,region):
        self.name = 'aurora'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('rds', region_name=self.region)
            paginator = client.get_paginator('describe_db_instances')
            page_iterator = paginator.paginate()
            instances = []
            for page in page_iterator:
                instances.extend([{
                    'id': item['DBInstanceIdentifier'],
                    'arn': item['DBInstanceArn'],
                } for item in page['DBInstances'] if 'DBClusterIdentifier' in item])
            for instance in instances:
                tags = client.list_tags_for_resource(ResourceName=instance['arn'])['TagList']
                self.identifiers.extend([{
                    'id': instance['id'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in tags]
                }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass