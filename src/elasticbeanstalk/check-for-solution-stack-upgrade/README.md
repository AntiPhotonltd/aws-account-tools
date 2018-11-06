Check for Solution Stack Upgrades
=========

This script wil check all of your elastic beanstalks and inform you if there are any upgrades available.

## Simple Usage

```
./check-for-solution-stack-upgrade.py
```

## Command Line Options

```

usage: check-for-solution-stack-upgrade.py [-h] [-a] [-e] [-r REGION] [-s]

Check for Soution Stack Upgrades

optional arguments:
  -h, --help            show this help message and exit
  -a, --all-beanstalks  List all beanstalks (even if not upgradable)
  -e, --exit-code       Set exit code to number of available upgrades
  -r REGION, --region REGION
                        The aws region
  -s, --silent          Surpress all output

```

## Information Displayed

The following information is displayed in table form for all the beanstalks located.

```
Application Name - Elastic beanstalk appliation name
Environment Name - The name of the environment
Solution Stack - The name of the solution stack in use
Current Version - Current version of the platform
Latest Version - Latest version available
Upgrade Available - True/False
```
