import boto3


class Ecs_services:

    def __init__(self, region):
        self.name = 'ecsservices'
        self.region = region
        self.identifiers = []
        self.templates = {
            'identifier': 'ServiceName',
            'cfn-monitor': 'ECSService',
            'cfn-guardian': 'ECSService'
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
                clusters = client.describe_clusters(clusters=clusterArns)
                for cluster in clusters['clusters']:
                    serviceArns = []
                    clusterName = cluster['clusterName']
                    paginator = client.get_paginator('list_services')
                    page_iterator = paginator.paginate(cluster=clusterName)
                    
                    for page in page_iterator:
                        serviceArns.extend([item for item in page['serviceArns']])
                    
                    if serviceArns:
                        if len(serviceArns) > 10:
                            split = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
                            splitServiceArns = split(serviceArns, 10)
                            for array in splitServiceArns:
                                self.identifiers.extend({
                                    'id': {
                                        'ServiceName': item['serviceName'],
                                        'Cluster': clusterName
                                    },
                                    'tags': item['tags']
                                } for item in client.describe_services(cluster=clusterName, services=array, include=['TAGS'])['services'])
                        else:
                            self.identifiers.extend({
                                    'id': {
                                        'ServiceName': item['serviceName'],
                                        'Cluster': clusterName
                                    },
                                    'tags': item['tags']
                                } for item in client.describe_services(cluster=clusterName, services=serviceArns, include=['TAGS'])['services'])

        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
