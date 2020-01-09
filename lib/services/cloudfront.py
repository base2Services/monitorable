import boto3

class Cloudfront:

    def __init__(self,region):
        self.name = 'cloudfront'
        self.region = 'us-east-1'
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('cloudfront', region_name=self.region)
            paginator = client.get_paginator('list_distributions')
            page_iterator = paginator.paginate()
            distributions = []
            for page in page_iterator:
                if 'Items' in page['DistributionList']:
                    distributions.extend([{
                        'id': item['Id'],
                        'arn': item['ARN']
                    } for item in page['DistributionList']['Items']])
            for distribution in distributions:
                tags = client.list_tags_for_resource(Resource=distribution['arn'])['Tags']['Items']
                self.identifiers.extend([{
                    'id': distribution['id'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in tags]
                }])
        except Exception:
            pass