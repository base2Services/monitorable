import boto3


class Vpn_tunnels:

    def __init__(self, region):
        self.name = 'vpntunnel'
        self.region = region
        self.identifiers = []
        self.templates = {
            'cfn-monitor': 'VPNTunnel',
            'cfn-guardian': 'VPNTunnel'
        }
        self.get_resources()

    def get_resources(self):
        try:
            client = boto3.client('ec2', region_name=self.region)
            page = client.describe_vpn_connections()
            if 'VpnConnections' in page:
                connections = [item for item in page['VpnConnections']]
            for connection in connections:
                try:
                    for tunnel in connection['Options']['TunnelOptions']:

                        self.identifiers.extend([{
                        'id': tunnel['OutsideIpAddress'],
                        'tags': str(connection['Tags'])
                        }])
                except KeyError:
                    import xml.etree.ElementTree as ET
                    tree = ET.ElementTree(ET.fromstring(connection['CustomerGatewayConfiguration']))
                    root = tree.getroot()
                    ips = root.findall("tunnel_outside_address")
                    for i in ips:
                        self.identifiers.extend([{
                        'id': i
                    }])

        except Exception as e:
            print('ERROR'.ljust(7) + self.region.ljust(16) + self.name.ljust(19) + str(e), flush=True)
            pass
