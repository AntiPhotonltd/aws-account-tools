List all RDS Instances
=========

This is a simple script to retrieve a list of all RDS instances and display some information about them.

## Simple Usage

```
./list-all-rds-instances.py
```

## Command Line Options

```

usage: list-all-rds-instances.py [-h] [-r REGION]

List all RDS Instances

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        The aws region

```

## Information Displayed

The following information is displayed in table form for all the RDS instances located.

```
Instance Name
Instance Class
Status
Availability Zone(s)
Publicly Accessible
Allocated Storage
Storage Encrypted
Engine
Engine Version
Performance Insights
```
