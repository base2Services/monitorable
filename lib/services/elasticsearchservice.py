import boto3

class Elasticsearchservice:

    def __init__(self, region):
        self.name = 'elasticsearch'
        self.region = region
        self.identifiers = []
        self.templates = {
            'identifier': 'Domain',
            'identifier': 'AccountId',
            'cfn-monitor': 'ElasticSearch',
            'cfn-guardian': 'ElasticSearch'
        }
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('es', region_name=self.region)
            get_domains = client.list_domain_names()       
            
            for item in get_domains['DomainNames']:
                account_id = boto3.client("sts").get_caller_identity()["Account"]
                self.identifiers.extend([{
                'id': {
                    'Id': account_id,
                    'AccountId': account_id,
                    'Domain': item['DomainName']
                }
            }])             

        except Exception as e: 
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass