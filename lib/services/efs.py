import boto3

class Efs:

    def __init__(self,region):
        self.name = 'efs'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'ElasticFileSystem',
            'cfn-guardian': 'ElasticFileSystem'
        }
        self.get_resources()
        
    def get_resources(self):
        try: 
            client = boto3.client('efs', region_name=self.region)
            paginator = client.get_paginator('describe_file_systems')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([{
                    'id': item['FileSystemId'],
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in item.get('Tags', [])]
                } for item in page['FileSystems']])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass