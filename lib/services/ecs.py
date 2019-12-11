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
            page = client.describe_clusters()
            self.identifiers.extend([item['clusterName'] for item in page['clusters']])
        except Exception: 
            pass