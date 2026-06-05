import boto3


class Iot_core:

    def __init__(self, region):
        self.name = 'iotcore'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'IoTCore',
            'cfn-guardian': 'IoTCore'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('iot', region_name=self.region)
            response = client.list_topic_rules()
            rules = response.get('rules', [])
            while 'nextToken' in response:
                response = client.list_topic_rules(nextToken=response['nextToken'])
                rules.extend(response.get('rules', []))
            has_active_rules = any(not rule.get('ruleDisabled', False) for rule in rules)
            if has_active_rules:
                self.identifiers.append({
                    'id': 'MQTT',
                    'tags': []
                })
                self.identifiers.append({
                    'id': 'HTTP',
                    'tags': []
                })
        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
