import boto3


class Ecs:

    def __init__(self, region):
        self.name = 'ecs'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'ECSCluster',
            'cfn-guardian': 'ECSCluster'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('ecs', region_name=self.region)
            paginator = client.get_paginator('list_clusters')
            page_iterator = paginator.paginate()
            clusterArns = []
            for page in page_iterator:
                clusterArns.extend([item for item in page['clusterArns']])
            if clusterArns:
                clusters = client.describe_clusters(clusters=clusterArns, include=['TAGS'])
                self.identifiers.extend([{
                    'id': item['clusterName'],
                    'tags': item['tags']
                } for item in clusters['clusters']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
