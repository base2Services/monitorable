import boto3

class Alarms:

    def __init__(self):
        self.dimensions = {}
        self.dimensions.setdefault('us-east-1',[])

    def get(self,region):
        try:
            self.dimensions.setdefault(region,[])
            client = boto3.client('cloudwatch', region_name=region)
            paginator = client.get_paginator('describe_alarms')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                for alarm in page['MetricAlarms']:
                    self.dimensions[region].append(
                        {
                            'alarm_name': alarm['AlarmName'],
                            'dimensions': alarm['Dimensions']
                        }
                    )
        except Exception: 
            pass
        self.progress(region)

    def progress(self,region):
        if len(self.dimensions[region]) > 0:
            print('\033[92m✓\033[0m      ' + region.ljust(16) + 'alarms'.ljust(16) + str(len(self.dimensions[region])).rjust(4) + '  ' + '|' * len(self.dimensions[region]))
        else:
            print('\033[91mx\033[0m      ' + region.ljust(16) + 'alarms'.ljust(16) + str(len(self.dimensions[region])).rjust(4) + '  ' + '|' * len(self.dimensions[region]))