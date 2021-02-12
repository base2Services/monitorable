import boto3


class Mq:

    def __init__(self, region):
        self.name = 'mq'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'AmazonMQBroker',
            'cfn-guardian': 'AmazonMQBroker'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('mq', region_name=self.region)
            paginator = client.get_paginator('list_brokers')
            page_iterator = paginator.paginate()
            brokers = []
            for page in page_iterator:
                brokers.extend([{
                    'name': item['BrokerName'],
                    'arn': item['BrokerArn'],
                    'mode': item['DeploymentMode']
                } for item in page['BrokerSummaries'] if item['EngineType'] != "RabbitMQ"]) # Skip any rabbit brokers as they have their own type
            for broker in brokers:
                tags = client.list_tags(ResourceArn=broker['arn'])['Tags']
                if broker['mode'] == 'ACTIVE_STANDBY_MULTI_AZ':
                    self.identifiers.extend([{
                        'id': broker['name'] + '-1',
                        'tags': [{
                            'key': t[0],
                            'value': t[1]
                        } for t in tags.items()]
                    }])
                    self.identifiers.extend([{
                        'id': broker['name'] + '-2',
                        'tags': [{
                            'key': t[0],
                            'value': t[1]
                        } for t in tags.items()]
                    }])
                if broker['mode'] == 'SINGLE_INSTANCE':
                    self.identifiers.extend([{
                        'id': broker['name'] + '-1',
                        'tags': [{
                            'key': t[0],
                            'value': t[1]
                        } for t in tags.items()]
                    }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass

