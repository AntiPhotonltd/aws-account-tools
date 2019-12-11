# AWS Tools Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For further info see our [changelogs](https://github.com/AntiPhotonltd/changelogs) guide.

## [Unreleased]

Documentation:

* Fix the date for the 1.0.9 release. ([@TGWolf][])
* Updated the badges ion the README to be a little more on brand and relevant. ([@TGWolf][])

## [v1.0.9] - December 11 2019

Documentation:

* A complete review and rework of the ChangeLog. ([@TGWolf][])

Chores:

* Added a whitelist entry to ensure the link checker doesnt file on the changelog. ([@TGWolf][])

## [v1.0.8] - December 10 2019

New Features:

* Added a new script elasticbeanstalk/change-asg-health-check-type.py. ([@TGWolf][])
* Added support for python 3.7 and 3.8 to the .travis.cfg file. ([@TGWolf][])

Improvements:

* Updated backup-ssm-to-s3.py as the 'day' was missing from the filename. ([@TGWolf][])

Removed:

* Removed support for python 2.7 and 3.4 from .travis.cfg file. ([@TGWolf][])

## [v1.0.7] - September 21 2019

New Features:

* Added a new script iam/show-password-policy.py. ([@TGWolf][])
* Added a new section for ssm scripts. ([@TGWolf][])
* Added a new script ssm/list-ssm-parameters.py. ([@TGWolf][])
* Added a new script ssm/get-ssm-parameter.py. ([@TGWolf][])
* Added a new script ssm/backup-ssm-to-s3.py. ([@TGWolf][])
* Added a new script ec2/backup-all-ebs-volumes.sh. ([@TGWolf][])
* Added a new script ec2/list-availability-zones.py. ([@TGWolf][])
* Added a new script ec2/list-all-ec2-instance-types.py. ([@TGWolf][])
* Added a new script list-aws-service-availability-by-region.  ([@TGWolf][])

## [v1.0.6] - November 22 2018

New Features:

* Added a new script ec2/list-account-attributes.py. ([@TGWolf][])
* Added a new script ec2/list-regions.py. ([@TGWolf][])

Improvements:

* Added tags column to the list-vpcs script. ([@TGWolf][])

## [v1.0.5] - November 15 2018

Chores:

* Only clone Travis Toolkit modules when required in travis build. ([@TGWolf][])

## [v1.0.4] - November 15 2018

New Features:

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

Style:

* General tidy up of all scripts and internal docs / readme files. ([@TGWolf][])

Chores:

* Updated the awesomebot_travis submodule. ([@TGWolf][])
* Updated the python_travis submodule. ([@TGWolf][])

## [v1.0.3] - November 7 2018

New Features:

* Added a new section for IAM scripts. ([@TGWolf][])
* Added a new section for EC2 scripts. ([@TGWolf][])
* Added a new script elasticbeanstalk/list-beanstalks.py. ([@TGWolf][])
* Added a new script iam/list-users.py script. ([@TGWolf][])
* Added a new script iam/list-roles.py script. ([@TGWolf][])
* Added a new script iam/list-access-keys.py script. ([@TGWolf][])
* Added a new script ec2/list-key-pairs.py script. ([@TGWolf][])

Improvements:

* Added better error detection to all scripts. ([@TGWolf][])

## [v1.0.2] - November 6 2018

New Features:

* Addition of new script to list all RDS instances and details about them. ([@TGWolf][])

Documentation:

* README.md added to each script to give more detailed overview. ([@TGWolf][])

Improvements:

* Tidy up of variable and function names to give them more meaning. ([@TGWolf][])
* Added 'exit code' mode - sets the exit code to be the number of real upgrades available. ([@TGWolf][])
* Added 'silent' mode so no output it given (designed to work with exit code above). ([@TGWolf][])
* Remove type=str from command line parameters as this is the default for python. ([@TGWolf][])
* Upgrade Available is now displayed as True/False instead of 1/0. ([@TGWolf][])

Bug Fixes:

* Bug found in check-for-solution-stack-upgrade.py due to unsafe assumption, change in the lookup logic. ([@TGWolf][])

## [v1.0.1] - November 6 2018

Improvements:

* Improve the version checking so that a version is checked to ensure it is an actual upgrade and not just a different version. ([@TGWolf][])

## [v1.0.0] - November 6 2018

* Initial Release ([@TGWolf][])

[@TGWolf]: https://github.com/TGWolf

[unreleased]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.9...HEAD
[v1.0.9]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.8...v1.0.9
[v1.0.8]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.7...v1.0.8
[v1.0.7]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.6...v1.0.7
[v1.0.6]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.5...v1.0.6
[v1.0.5]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.4...v1.0.5
[v1.0.4]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.3...v1.0.4
[v1.0.3]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.2...v1.0.3
[v1.0.2]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.1...v1.0.2
[v1.0.1]: https://github.com/AntiPhotonltd/aws-tools/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/AntiPhotonltd/aws-tools/releases/tag/v1.0.0

