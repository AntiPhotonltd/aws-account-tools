[![Build Status](https://img.shields.io/travis/AntiPhotonltd/aws-tools/master.svg)](https://travis-ci.org/AntiPhotonltd/aws-tools)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Release](https://img.shields.io/github/release/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools/releases/latest)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/AntiPhotonltd/aws-tools/latest.svg)](https://github.com/AntiPhotonltd/aws-tools/commits)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)
[![GitHub contributors](https://img.shields.io/github/contributors/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)

AWS Tools
=========

A collection of simply tools for managing and auditing AWS.

## ACM

* [list-certificates.py](src/acm/list-acm-certificates/list-acm-certificates.py) - [README.md](src/acm/list-acm-certificates/README.md)

## EC2

* [list-key-pairs.py](src/ec2/list-key-pairs/list-key-pairs.py) - [README.md](src/ec2/list-key-pairs/README.md)

## Elastic Beanstalks

* [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) - [README.md](src/elasticbeanstalk/check-for-solution-stack-upgrade/README.md)
* [list-beanstalks.py](src/elasticbeanstalk/list-beanstalks/list-beanstalks.py) - [README.md](src/elasticbeanstalk/list-beanstalks/README.md)

## IAM

* [list-access-keys.py](src/iam/list-access-keys/list-access-keys.py) - [README.md](src/iam/list-access-keys/README.md)
* [list-roles.py](src/iam/list-roles/list-roles.py) - [README.md](src/iam/list-roles/README.md)
* [list-users.py](src/iam/list-users/list-users.py) - [README.md](src/iam/list-users/README.md)

## KMS

* [list-kms-keys.py](src/kms/list-kms-keys/list-kms-keys.py) - [README.md](src/kms/list-kms-keys/README.md)

## RDS

* [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) - [README.md](src/rds/check-for-rds-upgrade/README.md)
* [list-rds-instances.py](src/rds/list-rds-instances/list-rds-instances.py) [README.md](src/rds/list-rds-instances/README.md)

## S3

* [list-s3-buckets.py](src/s3/list-s3-buckets/list-s3-buckets.py) - [README.md](src/s3/list-s3-buckets/README.md)

**********

| Name | Documentation |
| [list-certificates.py](src/acm/list-certificates/list-certificates.py) | [README.md](src/acm/list-certificates/README.md)
| [list-key-pairs.py](src/ec2/list-key-pairs/list-key-pairs.py) | [README.md](src/ec2/list-key-pairs/README.md)
| [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) | [README.md](src/elasticbeanstalk/check-for-solution-stack-upgrade/README.md)
| [list-beanstalks.py](src/elasticbeanstalk/list-beanstalks/list-beanstalks.py) | [README.md](src/elasticbeanstalk/list-beanstalks/README.md)
| [list-access-keys.py](src/iam/list-access-keys/list-access-keys.py) | [README.md](src/iam/list-access-keys/README.md)
| [list-roles.py](src/iam/list-roles/list-roles.py) | [README.md](src/iam/list-roles/README.md)
| [list-users.py](src/iam/list-users/list-users.py) | [README.md](src/iam/list-users/README.md)
| [list-kms-keys.py](src/kms/list-kms-keys/list-kms-keys.py) | [README.md](src/kms/list-kms-keys/README.md)
| [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) | [README.md](src/rds/check-for-rds-upgrade/README.md) |
| [list-rds-instances.py](src/rds/list-rds-instances/list-rds-instances.py) | [README.md](src/rds/list-rds-instances/README.md) |
| [list-s3-buckets.py](src/s3/list-s3-buckets/list-s3-buckets.py) | [README.md](src/s3/list-s3-buckets/README.md) |

**********


## ACM

| Name | Description | README.md |
| --- | --- | --- |
| [list-certificates.py](src/acm/list-certificates/list-certificates.py) | List of the certificates. | [README.md](src/acm/list-certificates/README.md)

## EC2

| Name | Description | README.md |
| --- | --- | --- |
| [list-key-pairs.py](src/ec2/list-key-pairs/list-key-pairs.py) | List of the available key pairs. | [README.md](src/ec2/list-key-pairs/README.md)

## Elastic Beanstalks

| Name | Description | README.md |
| --- | --- | --- |
| [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) | Check to see if there is an upgrade available for your Elastic Beanstalk. | [README.md](src/elasticbeanstalk/check-for-solution-stack-upgrade/README.md)
| [list-beanstalks.py](src/elasticbeanstalk/list-beanstalks/list-beanstalks.py) | List of the available beanstalks and some details about them. | [README.md](src/elasticbeanstalk/list-beanstalks/README.md)

## IAM

| Name | Description | README.md |
| --- | --- | --- |
| [list-access-keys.py](src/iam/list-access-keys/list-access-keys.py) | List of the available access keys and some details about them . | [README.md](src/iam/list-access-keys/README.md)
| [list-roles.py](src/iam/list-roles/list-roles.py) | List all of the available roles and some details about them. | [README.md](src/iam/list-roles/README.md)
| [list-users.py](src/iam/list-users/list-users.py) | List all of the available users and some details about them. | [README.md](src/iam/list-users/README.md)

## KMS

| Name | Description | README.md |
| --- | --- | --- |
| [list-kms-keys.py](src/kms/list-kms-keys/list-kms-keys.py) | List all of the available users and some details about them. | [README.md](src/kms/list-kms-keys/README.md)

## RDS

| Name | Description | README.md |
| --- | --- | --- |
| [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) | Check to see if there is an upgrade available for your RDS. | [README.md](src/rds/check-for-rds-upgrade/README.md) |
| [list-rds-instances.py](src/rds/list-rds-instances/list-rds-instances.py) | List of the available RDS instances and some details about them. |  [README.md](src/rds/list-rds-instances/README.md) |

## S3

| Name | Description | README.md |
| --- | --- | --- |
| [list-s3-buckets.py](src/s3/list-s3-buckets/list-s3-buckets.py) | List of the available S3 buckets and some details about them. |  [README.md](src/s3/list-s3-buckets/README.md) |
