import boto3


class Iot_rule:

    def __init__(self, region):
        self.name = 'iotrule'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'IoTRule',
            'cfn-guardian': 'IoTRule'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('iot', region_name=self.region)
            rules = []
            response = client.list_topic_rules()
            rules.extend(response.get('rules', []))
            while 'nextToken' in response:
                response = client.list_topic_rules(nextToken=response['nextToken'])
                rules.extend(response.get('rules', []))
            for rule in rules:
                if not rule.get('ruleDisabled', False):
                    tags = []
                    try:
                        tag_response = client.list_tags_for_resource(resourceArn=rule['ruleArn'])
                        tags = [{'key': t['Key'], 'value': t['Value']} for t in tag_response.get('tags', [])]
                    except Exception:
                        pass
                    self.identifiers.append({
                        'id': rule['ruleName'],
                        'tags': tags
                    })
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
