Check for RDS Upgrade
=========

## Simple Usage

```
./check-for-rds-upgrade.py
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
