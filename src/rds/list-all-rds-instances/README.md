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
                        ISO Country code

```

## Information Displayed

The following information is displayed in table form for all the RDS instances located.

```
Instance Name - instance identifier / name
Instance Class - instance size
Status - current instane status
Availability Zone(s) - region(s)
Publicly Accessible - True/False
Allocated Storage - Size in GB
Storage Encrypted - True/False
Engine - database engine (postgres/mysql etc)
Engine Version - current version
```
