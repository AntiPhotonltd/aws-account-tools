## 1.0.7 (Unreleased)

CHANGES:

* Added a new script iam/show-password-policy.py. ([@TGWolf][])
* Added a new section for ssm scripts. ([@TGWolf][])
* Added a new script ssm/list-ssm-parameters.py. ([@TGWolf][])
* Added a new script ssm/get-ssm-parameter.py. ([@TGWolf][])
* Added a new script ssm/backup-ssm-to-s3.py. ([@TGWolf][])
* Added a new script ec2/backup-all-ebs-volumes.sh. ([@TGWolf][])
* Added a new script ec2/list-availability-zones.py. ([@TGWolf][])
## 1.0.6 (November 22, 2018)

CHANGES:

* Added a new script ec2/list-account-attributes.py. ([@TGWolf][])
* Added a new script ec2/list-regions.py. ([@TGWolf][])
* Added tags column to the list-vpcs script. ([@TGWolf][])

## 1.0.5 (November 15, 2018)

CHANGES:

* Only clone Travis Toolkit modules when required in travis build. ([@TGWolf][])

## 1.0.4 (November 15, 2018)

CHANGES:

* Added a new section for acm scripts. ([@TGWolf][])
* Added a new section for dynamodb scripts. ([@TGWolf][])
* Added a new section for kinesis scripts. ([@TGWolf][])
* Added a new section for kms scripts. ([@TGWolf][])
* Added a new section for lambda scripts. ([@TGWolf][])
* Added a new section for route53 scripts. ([@TGWolf][])
* Added a new section for s3 scripts. ([@TGWolf][])
* Added a new script acm/list-certificates.py. ([@TGWolf][])
* Added a new script dynamodb/list-dynamodb-tables.py. ([@TGWolf][])
* Added a new script ec2/list-ebs-volumes.py. ([@TGWolf][])
* Added a new script ec2/list-vpcs.py. ([@TGWolf][])
* Added a new script ec2/list-vpc-peers.py. ([@TGWolf][])
* Added a new script kinesis/list-kinesis-streams.py. ([@TGWolf][])
* Added a new script kms/list-kms-keys.py. ([@TGWolf][])
* Added a new script lambda/list-lambda-functions.py ([@TGWolf][])
* Added a new script route53/list-route53-hosted-zones.py ([@TGWolf][])
* Added a new script s3/list-s3-buckets.py. ([@TGWolf][])
* General tidy up of all scripts and internal docs / readme files. ([@TGWolf][])
* Updated the awesomebot_travis submodule. ([@TGWolf][])
* Updated the python_travis submodule. ([@TGWolf][])

## 1.0.3 (November 7, 2018)

CHANGES:

* Added a new section for IAM scripts. ([@TGWolf][])
* Added a new section for EC2 scripts. ([@TGWolf][])
* Added a new script elasticbeanstalk/list-beanstalks.py. ([@TGWolf][])
* Added a new script iam/list-users.py script. ([@TGWolf][])
* Added a new script iam/list-roles.py script. ([@TGWolf][])
* Added a new script iam/list-access-keys.py script. ([@TGWolf][])
* Added a new script ec2/list-key-pairs.py script. ([@TGWolf][])
* Added better error detection to all scripts. ([@TGWolf][])

## 1.0.2 (November 6, 2018)

CHANGES:

* Addition of new script to list all RDS instances and details about them. ([@TGWolf][])
* Tidy up of variable and function names to give them more meaning. ([@TGWolf][])
* Added 'exit code' mode - sets the exit code to be the number of real upgrades available. ([@TGWolf][])
* Added 'silent' mode so no output it given (designed to work with exit code above). ([@TGWolf][])
* Remove type=str from command line parameters as this is the default for python. ([@TGWolf][])
* Upgrade Available is now displayed as True/False instead of 1/0. ([@TGWolf][])
* README.md added to each script to give more detailed overview. ([@TGWolf][])
* Bug found in check-for-solution-stack-upgrade.py due to unsafe assumption, change in the lookup logic. ([@TGWolf][])

## 1.0.1 (November 6, 2018)

CHANGES:

* Improve the version checking so that a version is checked to ensure it is an actual upgrade and not just a different version. ([@TGWolf][])

## 1.0.0 (November 6, 2018)

* Initial Release ([@TGWolf][])

[@TGWolf]: https://github.com/TGWolf
