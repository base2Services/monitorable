import json
import yaml

class Output:

    def __init__(self,resources,alarms,grouped):
        self.resources = resources
        self.alarms = alarms
        self.grouped = grouped

    def strip_tags(self,identifiers):
        output = {}
        if self.grouped:
            for tagKey, values in identifiers.items():
                for tagValue, regions in values.items():
                    for region, services in regions.items():
                        for service, resources in services.items():
                            for resource in resources:
                                output.setdefault(tagKey,{})
                                output[tagKey].setdefault(tagValue,{})
                                output[tagKey][tagValue].setdefault(region,{})
                                output[tagKey][tagValue][region].setdefault(service,[])
                                output[tagKey][tagValue][region][service].extend([resource['id']])
        else:
            for region, services in identifiers.items():
                for service, resources in services.items():
                    for resource in resources:
                        output.setdefault(region,{})
                        output[region].setdefault(service,[])
                        output[region][service].extend([resource['id']])
        return output

    def flatten(self,identifier):
        return list(identifier.values())[0] if type(identifier) is dict else identifier

    def audit(self):
        output = ''
        if self.grouped:
            for tagKey, values in self.strip_tags(self.resources.identifiers_by_tag).items():
                output += '\n' + 'Alarm'.ljust(8) + tagKey.ljust(20) + 'Region'.ljust(20) + 'Service'.ljust(20) + 'Identifier' + '\n\n'
                for tagValue, regions in values.items():
                    for region, regional_resources in regions.items():
                        alarm_resources = [dimension['Value'] for alarm in self.alarms.dimensions[region] for dimension in alarm['dimensions']]
                        for service, identifiers in regional_resources.items():
                            for identifier in identifiers:
                                if self.flatten(identifier) in alarm_resources:
                                    output += '\033[92m✓\033[0m       ' + tagValue[:19].ljust(20) + region.ljust(20) + service[:19].ljust(20) + self.flatten(identifier) + '\n'
                                else:
                                    output += '\033[91mx\033[0m       ' + tagValue[:19].ljust(20) + region.ljust(20) + service[:19].ljust(20) + self.flatten(identifier) + '\n'
        else:
            output += '\n' + 'Alarm'.ljust(8) + 'Region'.ljust(20) + 'Service'.ljust(20) + 'Identifier' + '\n\n'
            for region, regional_resources in self.strip_tags(self.resources.identifiers).items():
                alarm_resources = [dimension['Value'] for alarm in self.alarms.dimensions[region] for dimension in alarm['dimensions']]
                for service, identifiers in regional_resources.items():
                    for identifier in identifiers:
                        if self.flatten(identifier) in alarm_resources:
                            output += '\033[92m✓\033[0m       ' + region.ljust(20) + service[:19].ljust(20) + self.flatten(identifier) + '\n'
                        else:
                            output += '\033[91mx\033[0m       ' + region.ljust(20) + service[:19].ljust(20) + self.flatten(identifier) + '\n'
        return output

    def json(self):
        if self.grouped:
            return json.dumps(self.strip_tags(self.resources.identifiers_by_tag))
        else:
            return json.dumps(self.strip_tags(self.resources.identifiers))

    def yaml(self):
        if self.grouped:
            return yaml.dump(self.strip_tags(self.resources.identifiers_by_tag), default_flow_style=False)
        else:
            return yaml.dump(self.strip_tags(self.resources.identifiers), default_flow_style=False)

    def tags(self):
        tagKeys = {'tags': {}}
        for region_resources in self.resources.identifiers.values():
            for resources in region_resources.values():
                for resource in resources:
                    for tag in resource['tags']:
                        tagKeys['tags'].setdefault(tag['key'],{})
                        tagKeys['tags'][tag['key']].setdefault('count',0)
                        tagKeys['tags'][tag['key']].setdefault('resources',[])
                        tagKeys['tags'][tag['key']]['count'] += 1
                        tagKeys['tags'][tag['key']]['resources'].append(self.flatten(resource['id']))
        return yaml.dump(tagKeys, default_flow_style=False)

    def cfn_monitor(self):
        output = '\n### cfn-monitor config ###\n\n'
        templates = self.resources.templates
        if self.grouped:
            for tagKey, values in self.strip_tags(self.resources.identifiers_by_tag).items():
                for tagValue, regions in values.items():
                    output += '## ' + tagKey + ': ' + tagValue + '\n\n'
                    for region, regional_resources in regions.items():
                        region_output = {}
                        for resource, identifiers in regional_resources.items():
                            for identifier in identifiers:
                                region_output[self.flatten(identifier)] = templates[resource]['cfn-monitor']
                        if region_output:
                            output += '# ' + region + '\n\n'
                            output += yaml.dump(region_output, default_flow_style=False)
                            output += '\n\n'
        else:
            for region, regional_resources in self.strip_tags(self.resources.identifiers).items():
                region_output = {}
                for resource, identifiers in regional_resources.items():
                    for identifier in identifiers:
                        region_output[self.flatten(identifier)] = templates[resource]['cfn-monitor']
                if region_output:
                    output += '# ' + region + '\n\n'
                    output += yaml.dump(region_output, default_flow_style=False)
                    output += '\n\n'
        return output

    def cfn_guardian(self):
        output = '\n### cfn-guardian config ###\n\n'
        templates = self.resources.templates
        if self.grouped:
            for tagKey, values in self.strip_tags(self.resources.identifiers_by_tag).items():
                for tagValue, regions in values.items():
                    output += '## ' + tagKey + ': ' + tagValue + '\n\n'
                    for region, regional_resources in regions.items():
                        region_output = {'Resources': {}}
                        for resource, identifiers in regional_resources.items():
                            for identifier in identifiers:
                                region_output['Resources'].setdefault(templates[resource]['cfn-guardian'],[])
                                if type(identifier) is dict:
                                    identifier['Id'] = identifier.pop(templates[resource]['identifier'])
                                    region_output['Resources'][templates[resource]['cfn-guardian']].append(identifier)
                                else:
                                    region_output['Resources'][templates[resource]['cfn-guardian']].append({'Id': identifier})
                        if region_output:
                            output += '# ' + region + '\n\n'
                            output += yaml.dump(region_output, default_flow_style=False)
                            output += '\n\n'
        else:
            for region, regional_resources in self.strip_tags(self.resources.identifiers).items():
                region_output = {'Resources': {}}
                for resource, identifiers in regional_resources.items():
                    for identifier in identifiers:
                        region_output['Resources'].setdefault(templates[resource]['cfn-guardian'],[])
                        if type(identifier) is dict:
                            identifier['Id'] = identifier.pop(templates[resource]['identifier'])
                            region_output['Resources'][templates[resource]['cfn-guardian']].append(identifier)
                        else:
                            region_output['Resources'][templates[resource]['cfn-guardian']].append({'Id': identifier})
                if region_output:
                    output += '# ' + region + '\n\n'
                    output += yaml.dump(region_output, default_flow_style=False)
                    output += '\n\n'
        return output