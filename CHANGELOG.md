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
