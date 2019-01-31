Change ASG  Health Check Type
=========

## Simple Usage

```
./change-asg-health-check-type.py -b <beanstalk name>
```

## Command Line Options

```

usage: change-asg-health-check-type.py [-h] -b BEANSTALK [-g GRACE_PERIOD]
                                       [-r REGION]

Change ASG Health Check Type

optional arguments:
  -h, --help            show this help message and exit
  -b BEANSTALK, --beanstalk BEANSTALK
                        The beanstalk application name
  -g GRACE_PERIOD, --grace-period GRACE_PERIOD
                        Delay
  -r REGION, --region REGION
                        The aws region

```
