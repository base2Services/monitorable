import os

class Resources:

    def __init__(self):
        self.identifiers = {}
        
    def add(self,resource):
        self.identifiers.setdefault(resource.region,{})
        self.identifiers[resource.region].setdefault(resource.name,[])
        self.identifiers[resource.region][resource.name] = resource.identifiers
        self.progress(resource)

    def progress(self,resource):
        _, columns = os.popen('stty size', 'r').read().split()
        max_bar_width = int(columns) - 45
        if len(resource.identifiers) > 0:
            print('\033[92m✓\033[0m      ' + resource.region.ljust(16) + resource.name.ljust(16) + str(len(resource.identifiers)).rjust(4) + '  ' + '|' * min(len(resource.identifiers),max_bar_width))
        else:
            print('\033[91mx\033[0m      ' + resource.region.ljust(16) + resource.name.ljust(16) + str(len(resource.identifiers)).rjust(4) + '  ' + '|' * min(len(resource.identifiers),max_bar_width))
