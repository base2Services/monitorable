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

                
#   ElasticSearch:
#   - Id: 223829094007/tg-prod-elastic-v6

# self.identifiers.append({
#     'id': {
#         'TargetGroup': tg['arn'].split(':')[-1],
#         'LoadBalancer': lb_arn.split('loadbalancer/')[1]
#     },


# client = boto3.client('elbv2', region_name=self.region)
# paginator = client.get_paginator('describe_target_groups')
# page_iterator = paginator.paginate()
# target_group_arns = []
# for page in page_iterator:
#     target_group_arns.extend([{
#         'arn': item['TargetGroupArn'],
#         'lb': item['LoadBalancerArns']
#     } for item in page['TargetGroups']])

#   ElasticSearch:
#   - DomainName: tg-prod-elastic-v6
#     Id: '123456'