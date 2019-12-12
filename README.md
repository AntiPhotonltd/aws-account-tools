[![Build Status](https://img.shields.io/travis/AntiPhotonltd/aws-tools/master?style=for-the-badge&logo=travis)](https://travis-ci.org/AntiPhotonltd/aws-tools)
[![Release](https://img.shields.io/github/release/AntiPhotonltd/aws-tools?color=blueviolet&style=for-the-badge&logo=github)](https://github.com/AntiPhotonltd/aws-tools/releases/latest)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/AntiPhotonltd/aws-tools/latest?color=blueviolet&style=for-the-badge&logo=github)](https://github.com/AntiPhotonltd/aws-tools/commits)
[![Software License](https://img.shields.io/badge/license-MIT-blueviolet?style=for-the-badge)](LICENSE.md)
[![Wolf](https://img.shields.io/badge/Created%20By-Wolf-blueviolet?style=for-the-badge)](https://github.com/TGWolf)

AWS Tools
=========

A collection of simply tools for managing and auditing AWS.

| Name | Script Documentation | AWS CLI Reference |
| --- | --- | --- |
| [backup-ssm-to-s3.py](src/ssm/backup-ssm-to-s3/backup-ssm-to-s3.py) | [README](src/ssm/backup-ssm-to-s3/README.md) | [ssm][L_ssm] |
| [backup-all-ebs-volumes.sh](src/ec2/backup-all-ebs-volumes/backup-all-ebs-volumes.sh) | [README](src/ec2/backup-all-ebs-volumes/README.md) | [ec2][L_ec2] |
| [change-asg-health-check-type.py](src/elasticbeanstalk/change-asg-health-check-type/change-asg-health-check-type.py) | [README](src/elasticbeanstalk/change-asg-health-check-type/README.md)| [elasticbeanstalk][L_elasticbeanstalk] |
| [check-for-rds-upgrade.py](src/rds/check-for-rds-upgrade/check-for-rds-upgrade.py) | [README](src/rds/check-for-rds-upgrade/README.md) | [rds][L_rds] |
| [check-for-solution-stack-upgrade.py](src/elasticbeanstalk/check-for-solution-stack-upgrade/check-for-solution-stack-upgrade.py) | [README](src/elasticbeanstalk/check-for-solution-stack-upgrade/README.md)| [elasticbeanstalk][L_elasticbeanstalk] |
| [get-ssm-parameter.py](src/ssm/get-ssm-parameter/get-ssm-parameter.py) | [README](src/ssm/get-ssm-parameter/README.md) | [ssm][L_ssm] |
| [list-account-attributes.py](src/ec2/list-account-attributes/list-account-attributes.py) | [README](src/ec2/list-account-attributes/README.md) | [ec2][L_ec2] |
| [list-acm-certificates.py](src/acm/list-acm-certificates/list-acm-certificates.py) | [README](src/acm/list-acm-certificates/README.md) | [acm][L_acm] |
| [list-all-ec2-instance-types.py](https://github.com/AntiPhotonltd/list-all-ec2-instance-types/blob/master/src/list-all-ec2-instance-types.py) | [README](https://github.com/AntiPhotonltd/list-all-ec2-instance-types/blob/master/README.md) | [ec2][L_ec2] |
| [list-availability-zones.py](src/ec2/list-availability-zones/list-availability-zones.py) | [README](src/ec2/list-availability-zones/list-availability-zones/README.md) | [acm][L_acm] |
| [list-aws-service-availability-by-region.py](https://github.com/AntiPhotonltd/list-aws-service-availability-by-region/blob/master/src/list-aws-service-availability-by-region.py) | [README](https://github.com/AntiPhotonltd/list-aws-service-availability-by-region/blob/master/README.md) | [ec2][L_ec2] |
| [list-dynamodb-tables.py](src/dynamodb/list-dynamodb-tables/list-dynamodb-tables.py) | [README](src/dynamodb/list-dynamodb-tables/README.md) | [dynamodb][L_dynamodb] |
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
| [list-regions.py](src/ec2/list-regions/list-regions.py) | [README](src/ec2/list-regions/README.md) | [ec2][L_ec2] |
| [list-s3-buckets.py](src/s3/list-s3-buckets/list-s3-buckets.py) | [README](src/s3/list-s3-buckets/README.md) | [s3][L_s3] |
| [list-ssm-parameters.py](src/ssm/list-ssm-parameters/list-ssm-parameters.py) | [README](src/ssm/list-ssm-parameters/README.md) | [ssm][L_ssm] |
| [list-vpc-peers.py](src/ec2/list-vpc-peers/list-vpc-peers.py) | [README](src/ec2/list-vpc-peers/README.md) | [ec2][L_ec2] |
| [list-vpcs.py](src/ec2/list-vpcs/list-vpcs.py) | [README](src/ec2/list-vpcs/README.md) | [ec2][L_ec2] |
| [show-password-policy.py](src/iam/show-password-policy/show-password-policy.py) | [README](src/iam/show-password-policy/README.md) | [iam][L_iam] |


## ToDo List

- [ ] Add Tags column to all scripts that have tag outputs.
- [ ] Allow searching by name or tag or glab.
- [ ] Add a path to the backup ssm so it doesnt go into the bucket root.
- [ ] Ensure everything works with switch role!

[L_acm]: https://docs.aws.amazon.com/cli/latest/reference/acm/index.html
[L_dynamodb]: https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html
[L_ec2]: https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html
[L_elasticbeanstalk]: https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/index.html
[L_iam]: https://docs.aws.amazon.com/cli/latest/reference/iam/index.html
[L_kinesis]: https://docs.aws.amazon.com/cli/latest/reference/kinesis/index.html
[L_kms]: https://docs.aws.amazon.com/cli/latest/reference/kms/index.html
[L_lambda]: https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html
[L_rds]: https://docs.aws.amazon.com/cli/latest/reference/rds/index.html
[L_s3]: https://docs.aws.amazon.com/cli/latest/reference/s3/index.html
[L_ssm]: https://docs.aws.amazon.com/cli/latest/reference/ssm/index.html
