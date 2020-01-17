import os
import boto3

class Alarms:

    def __init__(self):
        self.name = 'alarms'
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
                    if alarm['AlarmActions'] and 'scalingPolicy' not in alarm['AlarmActions'][0]:
                        self.dimensions[region].append(
                            {
                                'alarm_name': alarm['AlarmName'],
                                'dimensions': alarm['Dimensions']
                            }
                        )
        except Exception as e:
            print('ERROR'.ljust(7) + region.ljust(16) + self.name.ljust(19) + str(e)) 
            pass
        self.progress(region)

    def progress(self,region):
        _, columns = os.popen('stty size', 'r').read().split()
        max_bar_width = int(columns) - 50
        if len(self.dimensions[region]) > 0:
            print('\033[92m✓\033[0m       ' + region.ljust(16) + 'alarms'[:19].ljust(20) + str(len(self.dimensions[region])).rjust(4) + '  ' + '|' * min(len(self.dimensions[region]),max_bar_width))
        else:
            print('\033[91mx\033[0m       ' + region.ljust(16) + 'alarms'[:19].ljust(20) + str(len(self.dimensions[region])).rjust(4) + '  ' + '|' * min(len(self.dimensions[region]),max_bar_width))