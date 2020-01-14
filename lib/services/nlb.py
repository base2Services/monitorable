import boto3

class Nlb:

    def __init__(self,region):
        self.name = 'nlb'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('elbv2', region_name=self.region)
            paginator = client.get_paginator('describe_target_groups')
            page_iterator = paginator.paginate()
            target_group_arns = []
            for page in page_iterator:
                target_group_arns.extend([{
                    'arn': item['TargetGroupArn'],
                    'lb': item['LoadBalancerArns']
                } for item in page['TargetGroups']])
            if target_group_arns:
                for i in range(0, len(target_group_arns), 20):
                    tags = client.describe_tags(ResourceArns=[item['arn'] for item in target_group_arns[i:i + 20]])
                    for tg_tags in tags['TagDescriptions']:
                        for tg in target_group_arns:
                            if tg_tags['ResourceArn'] == tg['arn']:
                                for lb_arn in tg['lb']:
                                    if lb_arn.split('/')[1] == 'net':
                                        self.identifiers.append({
                                            'id': {
                                                'TargetGroup': tg['arn'].split(':')[-1],
                                                'LoadBalancer': lb_arn.split('loadbalancer/')[1]
                                            },
                                            'tags': [{
                                                'key': t['Key'],
                                                'value': t['Value']
                                            } for t in tg_tags['Tags']]
                                        })
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass