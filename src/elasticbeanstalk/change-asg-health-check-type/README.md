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

## Bash

```shell
#!/usr/bin/env bash

ASG_NAME=$(aws elasticbeanstalk describe-environment-resources --region "${REGION}" --environment-name "${BEANSTALK_ENVIRONMENT_NAME}" --query 'EnvironmentResources.AutoScalingGroups[*].Name' --output text)

if [[ ! -z $asg_name ]]; then
    aws --region "${REGION}" autoscaling update-auto-scaling-group --auto-scaling-group-name "${ASG_NAME}" --health-check-type ELB --health-check-grace-period "${GRACE_PERIOD}"
fi
```
