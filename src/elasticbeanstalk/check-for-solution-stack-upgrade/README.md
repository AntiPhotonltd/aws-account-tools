Check for Solution Stack Upgrades
=========

This script wil check all of your elastic beanstalks and inform you if there are any upgrades available.

## Simple Usage

```
./check-for-solution-stack-upgrade.py -p "Python 3.4 running on 64bit Amazon Linux" -o "2018.03"
```

## Command Line Options

```

usage: check-for-solution-stack-upgrade.py [-h] [-a] [-e] [-o OS_VERSION] -p
                                           PLATFORM_NAME [-r REGION] [-s]

Check for Soution Stack Upgrades

optional arguments:
  -h, --help            show this help message and exit
  -a, --all-beanstalks  List all beanstalks (even if not upgradable)
  -e, --exit-code       Set exit code to number of available upgrades
  -o OS_VERSION, --os-version OS_VERSION
                        Operating system version
  -p PLATFORM_NAME, --platform-name PLATFORM_NAME
                        Current platform stack name
  -r REGION, --region REGION
                        The aws region
  -s, --silent          Surpress all output

```

## Information Displayed

The following information is displayed in table form for all the beanstalks located.

```
Application Name - Elastic beanstalk appliation name
Environment Name - The name of the environment
Current Platform Version - Current version of the platform
Latest Platform Version - Latest version available
Upgrade Available - True/False
```




