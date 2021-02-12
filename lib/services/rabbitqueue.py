import boto3


class Rabbitqueue:

    def __init__(self, region):
        self.name = 'rabbitqueue'
        self.region = region
        self.identifiers = []
        self.templates = {
            'identifier': 'Broker',
            'cfn-guardian': 'AmazonMQRabbitMQQueue'
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


            client = boto3.client('cloudwatch', region_name=self.region)
            paginator = client.get_paginator('list_metrics')
            for broker in brokers:
                metrics = paginator.paginate(
                    Namespace='AWS/AmazonMQ',
                    Dimensions=[
                        {
                            'Name': 'Broker',
                            'Value': broker['name']
                        },
                        {
                            'Name': 'Queue'
                        },
                        {
                            'Name': 'VirtualHost'
                        }
                    ],
                    RecentlyActive='PT3H'
                )
                for item in metrics:
                    for metric in item['Metrics']:
                        for idx, dimension in enumerate(metric['Dimensions']):
                            if dimension['Name'] == 'VirtualHost':
                                # The API orders results back with brokername, virtualhost then queue name.
                                # Checking the next index for the queue name ensures we get the correct queue for the correct Vhost
                                next_iter = metric['Dimensions'][idx+1]
                                if next_iter['Name'] == 'Queue':
                                    queue = {
                                        'id': {
                                            'Broker': broker['name'],
                                            'Queue': next_iter['Value'],
                                            'Vhost': dimension['Value']
                                        }
                                    }
                                    # Ensure queue data is unique and we're not getting duplicates due to multiple metrics returning the same queue data
                                    if queue not in self.identifiers:
                                        self.identifiers.append(queue)
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass