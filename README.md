[![Build Status](https://img.shields.io/travis/AntiPhotonltd/aws-tools/master.svg)](https://travis-ci.org/AntiPhotonltd/aws-tools)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Release](https://img.shields.io/github/release/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools/releases/latest)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/AntiPhotonltd/aws-tools/latest.svg)](https://github.com/AntiPhotonltd/aws-tools/commits)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)
[![GitHub contributors](https://img.shields.io/github/contributors/AntiPhotonltd/aws-tools.svg)](https://github.com/AntiPhotonltd/aws-tools)

AWS Tools
=========

A collection of simply tools for managing and auditing AWS.

| Name | Script Documentation | AWS CLI Reference |
| --- | --- | --- |
| [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) | [README](src/rds/check-for-rds-upgrade/README.md) | [rds][L_rds] |
| [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) | [README](src/elasticbeanstalk/check-for-solution-stack-upgrade/README.md)| [elasticbeanstalk][L_elasticbeanstalk] |
| [list-acm-certificates.py](src/acm/list-acm-certificates/list-acm-certificates.py) | [README](src/acm/list-certificates/README.md) | [acm][L_acm] |
| [list-ebs-volumes.py](src/ec2/list-ebs-volumes/list-ebs-volumes.py) | [README](src/ec2/list-ebs-volumes/README.md) | [ec2][L_ec2] |
| [list-ec2-instances.py](src/ec2/list-ec2-instances/list-ec2-instances.py) | [README](src/ec2/list-ec2-instances/README.md) | [ec2][L_ec2] |
| [list-ec2-key-pairs.py](src/ec2/list-ec2-key-pairs/list-ec2-key-pairs.py) | [README](src/ec2/list-ec2-key-pairs/README.md) | [ec2][L_ec2] |
| [list-elastic-beanstalks.py](src/elasticbeanstalk/list-elastic-beanstalks/list-elastic-beanstalks.py) | [README](src/elasticbeanstalk/list-elastic-beanstalks/README.md) | [elasticbeanstalk][L_elasticbeanstalk] |
| [list-iam-access-keys.py](src/iam/list-iam-access-keys/list-iam-access-keys.py) | [README](src/iam/list-iam-access-keys/README.md) | [iam][L_iam] |
| [list-iam-roles.py](src/iam/list-iam-roles/list-iam-roles.py) | [README](src/iam/list-iam-roles/README.md) | [iam][L_iam] |
| [list-iam-users.py](src/iam/list-iam-users/list-iam-users.py) | [README](src/iam/list-iam-users/README.md) | [iam][L_iam] |
| [list-kinesis-streams.py](src/kinesis/list-kinesis-streams/list-kinesis-streams.py) | [README](src/kinesis/list-kinesis-streams/README.md) | [kinesis][L_kinesis] |
| [list-kms-keys.py](src/kms/list-kms-keys/list-kms-keys.py) | [README](src/kms/list-kms-keys/README.md) | [kms][L_kms] |
| [list-lambda-functions.py](src/lambda/list-lambda-functions/list-lambda-functions.py) | [README](src/lambda/list-lambda-functions/README.md) | [lambda][L_lambda] |
| [list-rds-instances.py](src/rds/list-rds-instances/list-rds-instances.py) | [README](src/rds/list-rds-instances/README.md) | [rds][L_rds] |
| [list-s3-buckets.py](src/s3/list-s3-buckets/list-s3-buckets.py) | [README](src/s3/list-s3-buckets/README.md) | [s3][L_s3] |
| [list-vpc-peers.py](src/ec2/list-vpc-peers/list-vpc-peers.py) | [README](src/ec2/list-vpc-peers/README.md) | [ec2][L_ec2] |
| [list-vpcs.py](src/ec2/list-vpcs/list-vpcs.py) | [README](src/ec2/list-vpcs/README.md) | [ec2][L_ec2] |


[L_acm]: https://docs.aws.amazon.com/cli/latest/reference/acm/index.html
[L_ec2]: https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html
[L_elasticbeanstalk]: https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/index.html
[L_iam]: https://docs.aws.amazon.com/cli/latest/reference/iam/index.html
[L_kinesis]: https://docs.aws.amazon.com/cli/latest/reference/kinesis/index.html
[L_kms]: https://docs.aws.amazon.com/cli/latest/reference/kms/index.html
[L_lambda]: https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html
[L_rds]: https://docs.aws.amazon.com/cli/latest/reference/rds/index.html
[L_s3]: https://docs.aws.amazon.com/cli/latest/reference/s3/index.html
