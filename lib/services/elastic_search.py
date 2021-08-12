import boto3

class elastic_search:

    def __init__(self, region):
        self.name = 'elasticsearch'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'ElasticSearch',
            'cfn-guardian': 'ElasticSearch'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('es', region_name=self.region)
            page = client.describe_elasticsearch_domains()
            for item in page['DomainNames']:
                self.identifiers.extend([{
                'DomainName': item['DomainNames'],
                'tags': item['Tags']
                }])

        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
