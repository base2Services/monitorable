import json
import yaml

class Output:

    def __init__(self,resources,alarms):
        self.resources = resources
        self.alarms = alarms

    def audit(self):
        output = ''
        for region, regional_resources in self.resources.identifiers.items():
            alarm_resources = [dimension['Value'] for alarm in self.alarms.dimensions[region] for dimension in alarm['dimensions']]
            for resource, identifiers in regional_resources.items():
                for identifier in identifiers:
                    if identifier in alarm_resources:
                        output += '\033[92m✓\033[0m      ' + region.ljust(16) + resource.ljust(16) + identifier + '\n'
                    else:
                        output += '\033[91mx\033[0m      ' + region.ljust(16) + resource.ljust(16) + identifier + '\n'
        return output

    def json(self):
        return json.dumps(self.resources.identifiers)

    def yaml(self):
        return yaml.dump(self.resources.identifiers, default_flow_style=False)

    def cfn_monitor(self):
        output = '\n### cfn-moitor config ###\n\n'
        templates = {
            'lambda': 'LambdaMetrics',
            'apigateway': 'ApiGateway',
            'ecs': 'ECSCluster',
            'sqs': 'SQSQueue',
            'dynamodb': 'DynamoDBTable',
            'rds': 'RDSInstance',
            'aurora': 'DBCluster',
            'tg': 'ApplicationELBTargetGroup',
            'efs': 'ElasticFileSystem',
            'cloudfront': 'CloudFrontDistribution',
            'ec2': 'Ec2Instance',
            'asg': 'AutoScalingGroup',
            'elb': 'ElasticLoadBalancer',
            'elasticache': 'ElastiCacheReplicationGroup',
            'mq': 'AmazonMQBroker',
            'redshift': 'RedshiftCluster'
        }
        for region, regional_resources in self.resources.identifiers.items():
            region_output = {}
            for resource, identifiers in regional_resources.items():
                for identifier in identifiers:
                    region_output[identifier] = templates[resource]
            if region_output:
                output += '# ' + region + '\n\n'
                output += yaml.dump(region_output, default_flow_style=False)
                output += '\n\n'
        return output