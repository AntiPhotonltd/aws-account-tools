Check all RDS Instances
=========

This is a simple script to retrieve a list of all RDS instances that have upgrades available.

## Simple Usage

```
./check-all-rds-instances.py
```

## Command Line Options

```

usage: check-for-rds-upgrade.py [-h] [-a] [-e] [-r REGION] [-s]

Check for RDS Upgrades

optional arguments:
  -h, --help            show this help message and exit
  -a, --all-databases   List all databases (even if not upgradable)
  -e, --exit-code       Set exit code to number of available upgrades
  -r REGION, --region REGION
                        The aws region
  -s, --silent          Surpress all output

```

## Information Displayed

The following information is displayed in table form for all the RDS instances located.

```
Instance Name
Engine
Engine Version
Latest in PLace Upgrade
Latest Upgrade
Upgrade Available
```
