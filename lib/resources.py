import os
import json

class Resources:

    def __init__(self):
        self.identifiers = {}
        self.identifiers_by_tag = {}
        
    def add(self,resource):
        self.identifiers.setdefault(resource.region,{})
        self.identifiers[resource.region].setdefault(resource.name,[])
        self.identifiers[resource.region][resource.name] = resource.identifiers
        self.progress(resource)

    def progress(self,resource):
        _, columns = os.popen('stty size', 'r').read().split()
        max_bar_width = int(columns) - 45
        if len(resource.identifiers) > 0:
            print('\033[92m✓\033[0m       ' + resource.region.ljust(16) + resource.name[:19].ljust(20) + str(len(resource.identifiers)).rjust(4) + '  ' + '|' * min(len(resource.identifiers),max_bar_width))
        else:
            print('\033[91mx\033[0m       ' + resource.region.ljust(16) + resource.name[:19].ljust(20) + str(len(resource.identifiers)).rjust(4) + '  ' + '|' * min(len(resource.identifiers),max_bar_width))

    def group_by_tag(self,tag):
        self.identifiers_by_tag.setdefault(tag,{})
        self.identifiers_by_tag[tag].setdefault(tag,{})
        self.identifiers_by_tag[tag] = self.resources_with_tag_key(tag)

    def filter_by_tag(self,tag_filter):
        filtered_identifiers = {} 
        for tagKey, values in self.identifiers_by_tag.items():
            for tagValue, _ in values.items():
                if tagValue == tag_filter:
                    filtered_identifiers.setdefault(tagKey,{})
                    filtered_identifiers[tagKey][tagValue] = self.identifiers_by_tag[tagKey][tagValue]
        self.identifiers_by_tag = filtered_identifiers
   
    def resources_with_tag_key(self,tag_key):
        identifiers = {}
        for region, services in self.identifiers.items():
            for service, resources in services.items():
                for resource in resources:
                    match = False
                    value = ''
                    for tag in resource['tags']:
                        if tag['key'] == tag_key:
                            match = True
                            value = tag['value']
                    if match:
                        identifiers.setdefault(value,{})
                        identifiers[value].setdefault(region,{})
                        identifiers[value][region].setdefault(service,[])
                        identifiers[value][region][service].extend([resource])
                    else:
                        identifiers.setdefault('Untagged',{})
                        identifiers['Untagged'].setdefault(region,{})
                        identifiers['Untagged'][region].setdefault(service,[])
                        identifiers['Untagged'][region][service].extend([resource])
        return identifiers



