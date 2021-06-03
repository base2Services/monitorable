import boto3


class Vpn_connections:

    def __init__(self, region):
        self.name = 'vpnconnections'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'VPNConnection',
            'cfn-guardian': 'VPNConnection'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('ec2', region_name=self.region)
            page = client.describe_vpn_connections()
            for item in page['VpnConnections']:
                self.identifiers.extend([{
                'id': item['VpnConnectionId'],
                'tags': item['Tags']
                }])

        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
