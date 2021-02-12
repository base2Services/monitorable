import boto3


class Rabbitmq:

    def __init__(self, region):
        self.name = 'rabbitmq'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-guardian': 'AmazonMQRabbitMQBroker'
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
                    'arn': item['BrokerArn']
                } for item in page['BrokerSummaries'] if item['EngineType'] == 'RabbitMQ' ])
            for broker in brokers:
                tags = client.list_tags(ResourceArn=broker['arn'])['Tags']
                self.identifiers.extend([{
                    'id': broker['name'],
                    'tags': [{
                        'key': t[0],
                        'value': t[1]
                    } for t in tags.items()]
                }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass