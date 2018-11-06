[![Build Status](https://img.shields.io/travis/AntiPhotonltd/aws-tools/master.svg)](https://travis-ci.org/AntiPhotonltd/aws-tools)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Release](https://img.shields.io/github/release/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools/releases/latest)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/AntiPhotonltd/aws-tools/latest.svg)](https://github.com/AntiPhotonltd/aws-tools/commits)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)
[![GitHub contributors](https://img.shields.io/github/contributors/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)

AWS Tools
=========

A collection of simply tools for managing and auditing AWS.

## Elastic Beanstalks

| Name | Description | Example Usage | 
| --- | --- | --- |
| [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) | Check to see if there is an upgrade available for your Elastic Beanstalk. | ./check-for-solution-stack-upgrade.py -p "Python 3.4 running on 64bit Amazon Linux" -o "2018.03" |


## RDS

| Name | Description |
| --- | --- |
| [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) | Check to see if there is an upgrade available for your RDS. | ./check-for-rds-upgrade.py |


