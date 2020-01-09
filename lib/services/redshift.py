import boto3

class Redshift:

    def __init__(self,region):
        self.name = 'redshift'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('redshift', region_name=self.region)
            paginator = client.get_paginator('describe_clusters')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['ClusterIdentifier'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['Clusters']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass