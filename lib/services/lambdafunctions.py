import boto3

class Lambdafunctions:

    def __init__(self,region):
        self.name = 'lambdafunctions'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('lambda', region_name=self.region)
            paginator = client.get_paginator('list_functions')
            page_iterator = paginator.paginate()
            functions = []
            for page in page_iterator:
                functions.extend([{
                    'name': item['FunctionName'],
                    'arn': item['FunctionArn'],
                } for item in page['Functions']])
            for function in functions:
                tags = client.list_tags(Resource=function['arn'])['Tags']
                self.identifiers.extend([{
                    'id': function['name'],
                    'tags': [{
                        'key':t[0],
                        'value':t[1]
                    } for t in tags.items()]
                }])
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True) 
            pass