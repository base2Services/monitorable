import boto3

class Elasticsearchservice:

    def __init__(self, region):
        self.name = 'elasticsearch'
        self.region = region
        self.identifiers = []
        self.templates = {
            'identifier': 'DomainName',
            'cfn-monitor': 'ElasticSearch',
            'cfn-guardian': 'ElasticSearch'
        }
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('es', region_name=self.region)
            get_domains = client.list_domain_names()                    
            for item in get_domains['DomainNames']:     
                list_domains = client.describe_elasticsearch_domains(  
                    DomainNames=[
                        item['DomainName']                      
                    ])
        except Exception as e: 
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
        
        for domain_id in list_domains['DomainStatusList']:
            self.identifiers.extend([{
                    'id': domain_id['DomainName'],
                    'DomainName': "hello"
                }])