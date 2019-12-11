import boto3

class Efs:

    def __init__(self,region):
        self.name = 'efs'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try: 
            client = boto3.client('efs', region_name=self.region)
            paginator = client.get_paginator('describe_file_systems')
            page_iterator = paginator.paginate()
            for page in page_iterator:
                self.identifiers.extend([item['FileSystemId'] for item in page['FileSystems']])
        except Exception: 
            pass