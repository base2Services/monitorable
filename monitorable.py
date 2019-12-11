#!/usr/local/bin/python3.7

import os
import sys
import yaml
import boto3
import argparse

from lib.resources import Resources
from lib.output import Output
from lib.alarms import Alarms
from lib.services.rds import Rds
from lib.services.aurora import Aurora
from lib.services.ec2 import Ec2
from lib.services.asg import Asg
from lib.services.elb import Elb
from lib.services.tg import Tg
from lib.services.ecs import Ecs
from lib.services.elasticache import Elasticache
from lib.services.efs import Efs
from lib.services.redshift import Redshift
from lib.services.dynamodb import Dynamodb
from lib.services.apigateway import Apigateway
from lib.services.mq import Mq
from lib.services.lambdafunctions import Lambda
from lib.services.sqs import Sqs
from lib.services.cloudfront import Cloudfront

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

# Get CLI args
parser = argparse.ArgumentParser()
parser.add_argument("--format", help="output format", action="store")
parser.add_argument("--regions", help="comma seperated list of regions to query", action="store")
args = parser.parse_args()

# Error message for input validation
def input_error (arg,provided,supported):
    print(f'{provided} is not a valid {arg}\nvalid {arg}s: {supported}')
    exit(1)

# Override format/region if set in config and not provided as an argument
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

# Override format/region if set by CLI args
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

# Create resources and alarm objects
resources = Resources()
alarms = Alarms()

# Get terminal size
rows, columns = os.popen('stty size', 'r').read().split()
print('=' * int(columns))

# Loop over regions to scan resouces and alarms
for region in regions:
    if output_format == 'audit':
        alarms.get(region)
    resources.add(Apigateway(region))
    resources.add(Asg(region))
    resources.add(Aurora(region))
    resources.add(Cloudfront(region))
    resources.add(Dynamodb(region))
    resources.add(Ec2(region))
    resources.add(Ecs(region))
    resources.add(Efs(region))
    resources.add(Elasticache(region))
    resources.add(Elb(region))
    resources.add(Lambda(region))
    resources.add(Mq(region))
    resources.add(Rds(region))
    resources.add(Redshift(region))
    resources.add(Tg(region))
    resources.add(Sqs(region))

print('=' * int(columns))

# Output in selected format
output = Output(resources,alarms)
if output_format == 'audit':
    print(output.audit())
if output_format == 'json':
    print(output.json())
if output_format == 'yaml':
    print(output.yaml())
if output_format == 'cfn-monitor':
    print(output.cfn_monitor())
