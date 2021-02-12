import boto3


class Rabbitnode:

    def __init__(self, region):
        self.name = 'rabbitnode'
        self.region = region
        self.identifiers = []
        self.templates = {
            'identifier': 'Broker',
            'cfn-guardian': 'AmazonMQRabbitMQNode'
        }
        self.get_resources()

    def get_resources(self):
        try:
            mq_client = boto3.client('mq', region_name=self.region)
            mq_paginator = mq_client.get_paginator('list_brokers')
            page_iterator = mq_paginator.paginate()
            brokers = []
            for page in page_iterator:
                brokers.extend([{
                    'name': item['BrokerName'],
                    'arn': item['BrokerArn']
                } for item in page['BrokerSummaries'] if item['EngineType'] == 'RabbitMQ'])

            for broker in brokers:
                client = boto3.client('cloudwatch', region_name=self.region)
                paginator = client.get_paginator('list_metrics')
                metrics = paginator.paginate(
                    Namespace='AWS/AmazonMQ',
                    Dimensions=[
                        {
                            'Name': 'Broker',
                            'Value': broker['name']
                        },
                        {
                            'Name': 'Node'
                        }
                    ],
                    RecentlyActive='PT3H'
                )
                for item in metrics:
                    for metric in item['Metrics']:
                        for dimension in metric['Dimensions']:
                            if dimension['Name'] == 'Node':
                                node = {
                                    'id': {
                                        'Broker': broker['name'],
                                        'Node': dimension['Value']
                                    }
                                }
                                # Ensure node data is unique and we're not getting duplicates due to multiple metrics returning the same node names
                                if node not in self.identifiers:
                                    self.identifiers.append(node)
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass