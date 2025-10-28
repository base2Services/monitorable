import boto3

class Docdb:

    def __init__(self, region):
        self.name = 'docdb'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'DocumentDBCluster',
            'cfn-guardian': 'DocumentDBCluster'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('docdb', region_name=self.region)
            paginator = client.get_paginator('describe_db_clusters')
            page_iterator = paginator.paginate()
            clusters = []
            for page in page_iterator:
                clusters.extend([{
                    'id': item['DBClusterIdentifier'],
                    'arn': item['DBClusterArn'],
                } for item in page['DBClusters'] if 'DBClusterIdentifier' in item and item['Engine'] == 'docdb'])
            for cluster in clusters:
                tags = client.list_tags_for_resource(ResourceName=cluster['arn'])['TagList']
                self.identifiers.extend([{
                    'id': cluster['id'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in tags]
                }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
