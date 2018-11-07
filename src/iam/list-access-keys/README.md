List all Access Keys
=========

This is a simple script to retrieve a list of all access keys and display some information about them.

NOTE: This script does not take region as a parameter as IAM is NOT linked to a region.

## Simple Usage

```
./list-access-keys.py
```

## Command Line Options

```

usage: list-access-keys.py [-h]

List all Access Keys

optional arguments:
  -h, --help  show this help message and exit

```

## Information Displayed

The following information is displayed in table form for all the access keys located.

```
UserName
Status
Date Created
Access Key ID
```
