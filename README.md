# Monitorable

Query an AWS account for resources monitorable by cloudwatch alarms and report on alarm coverage of those resources

## Getting started

Export IAM credentials with read only permissions to the AWS account you want to query 

### Access Keys

```bash
export AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXX"
export AWS_SESSION_TOKEN="XXXXXXXXXXXXXXXXXXXXX"
```

### Profile reference

Using the appropriate name from ```~/.aws/credentials```
```bash
export AWS_PROFILE="XXXXXXXXXXXXXXXXXXXXX"
```

## Usage

```bash
./monitorable.py -h
usage: monitorable.py [-h] [--format FORMAT] [--regions REGIONS]

optional arguments:
  -h, --help         show this help message and exit
  --format FORMAT    output format
  --regions REGIONS  comma seperated list of regions to query
```

## Available options

argument | example value | description
--- | --- | ---
format | audit | query monitorable resources and cloudwatch alarms in each region and report on alarm coverage of resources
format | cfn-monitor | query monitorable resources and output in cfn-monitor alarms config format with default templates
format | cfn-guardian | query monitorable resources and output in cfn-guardian alarms config format with default templates
format | tags | shows all tags on monitorable resources and lists which resources have each tag. useful to discover 'tag coverage' and to help to choose good candidates to use with the --tag argument
tag | Environment | groups output by different tag values. e.g. `--tag Environment` will group resources by those tagged with `Environment:prod` and `Environment:stage`
format | json | query monitorable resources and output in json format
format | yaml | query monitorable resources and output in yaml format
regions | ap-southeast-2,us-west-2 | query monitorable resources only within the regions provided

## Default options

argument | value
--- | ---
format | audit
regions | all

## Config file

In addtion to CLI args, you can also provide a config file. The file must be named `config.yaml` and reside in the same directory as monitorable.py

#### Example config file

```yaml
format: yaml
regions:
 - ap-southeast-2
 - us-west-2
```