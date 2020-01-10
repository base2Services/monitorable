#!/usr/local/bin/python3.7

import os
import sys
import yaml
import boto3
import asyncio
import argparse
import importlib
import concurrent.futures

from lib.resources import Resources
from lib.output import Output
from lib.alarms import Alarms

# Get config from config file if it exists
try:
    config = yaml.load(open('config.yaml')) or {}
except:
    config = {}

# Get list of all regions from EC2 API
regions = [region['RegionName'] for region in boto3.client('ec2', 'ap-southeast-2').describe_regions()['Regions']]

# Set default and supported output formats
supported_formats = ['audit','json','yaml','cfn-monitor']
output_format = 'audit'

# Set default skipped services
skip = []

# Import services
services_dir = os.listdir('lib/services')
supported_services = [x.split('.py')[0] for x in services_dir if x not in ['__init__.py','__pycache__']]
service_classes = {}
for service in supported_services:
    service_module = importlib.import_module('lib.services.' + service)
    service_classes[service] = getattr(service_module, service.capitalize())

# Get CLI args
parser = argparse.ArgumentParser()
parser.add_argument("--format", help="output format", action="store")
parser.add_argument("--regions", help="comma seperated list of regions to query", action="store")
parser.add_argument("--skip", help="comma seperated list of services to skip", action="store")
parser.add_argument("--tag", help="tag to group resources by", action="store")
args = parser.parse_args()

# Error message for input validation
def input_error (arg,provided,supported):
    print(f'{provided} is not a valid {arg}\nvalid {arg}s: {supported}')
    exit(1)

# Group by tags if tag provided
if args.tag:
    tag = args.tag
    group = True
else:
    group = False

# Set format/region/skip if set in config and not provided as an argument
if 'format' in config and not args.format:
    if config['format'] in supported_formats:
        output_format = config['format']
    else:
        input_error('format',config['format'],str(supported_formats))
if 'regions' in config and not args.regions:
    if all(elem in regions for elem in config['regions']):
        regions = config['regions']
    else:
        input_error('region',str(list(set(config['regions']) - set(regions))[0]),str(regions))
if 'skip' in config and not args.skip:
    if all(elem in supported_services for elem in config['skip']):
        skip = config['skip']
    else:
        input_error('service',str(list(set(config['skip']) - set(supported_services))[0]),str(supported_services))

# Set format/region/skip if set by CLI args
if args.format:
    if args.format in supported_formats:
        output_format = args.format
    else:
        input_error('format',args.format,str(supported_formats))
if args.regions:
    arg_regions = args.regions.split(',')
    if all(elem in regions for elem in arg_regions):
        regions = arg_regions
    else:
        input_error('region',str(list(set(arg_regions) - set(regions))[0]),str(regions))
if args.skip:
    arg_skip = args.skip.split(',')
    if all(elem in supported_services for elem in arg_skip):
        skip = arg_skip
    else:
        input_error('service',str(list(set(arg_skip) - set(supported_services))[0]),str(supported_services))

# Create resources and alarm objects
resources = Resources()
alarms = Alarms()

# Get terminal size
rows, columns = os.popen('stty size', 'r').read().split()
print('=' * int(columns))

# Async function to get resources
async def get_resources(executor,regions):
    loop = asyncio.get_event_loop()
    blocking_tasks = []
    for region in regions:
        for service in supported_services:
            if service not in skip:
                blocking_tasks.append(loop.run_in_executor(executor, service_classes[service], region))
    for completed in asyncio.as_completed(blocking_tasks):
        resources.add(await completed)

# Async function to get alarms
async def get_alarms(executor,regions):
    loop = asyncio.get_event_loop()
    blocking_tasks = []
    for region in regions:
        blocking_tasks.append(loop.run_in_executor(executor, alarms.get, region))
    await asyncio.wait(blocking_tasks)

# Create thread pool for concurrent tasks
executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
event_loop = asyncio.get_event_loop()

# Loop over regions to scan resouces
event_loop.run_until_complete(get_resources(executor,regions))

# Loop over regions to scan alarms
if output_format == 'audit':
    event_loop.run_until_complete(get_alarms(executor,regions))

print('=' * int(columns))

# Group by tags if tag provided
if group:
    resources.group_by_tag(tag)

# Output in selected format
output = Output(resources,alarms,group)
if output_format == 'audit':
    print(output.audit())
if output_format == 'json':
    print(output.json())
if output_format == 'yaml':
    print(output.yaml())
if output_format == 'cfn-monitor':
    print(output.cfn_monitor())
