import boto3

class Elasticsearchservice:

    def __init__(self, region):
        self.name = 'elasticsearch'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'elasticsearch',
            'cfn-guardian': 'elasticsearch'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('es', region_name=self.region)
            page = client.list_domain_names()
            for item in page['DomainNames']:
                self.identifiers.extend([{
                'id': item['DomainName']
                }])

        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass