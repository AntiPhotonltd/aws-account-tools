List EC@ Instance
=========

This is a simple script to retrieve a list of EC2 key pairs

## Simple Usage

```
./list-ec2-instances.py
```

## Command Line Options

```

usage: list-ec2-instances.py [-h] [-a] [-r REGION]

List EC2 Instances

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Show all instances
  -r REGION, --region REGION
                        The aws region

```

## Information Displayed

The following information is displayed in table form for all the EC2 instances located.

```
Name
State
Availability Zone
Instance ID
Instance Type
Private IP
VPC ID
SSH Key Name
```
