List all Users
=========

This is a simple script to retrieve a list of all users and display some information about them.

NOTE: This script does not take region as a parameter as IAM is NOT linked to a region.

## Simple Usage

```
./list-users.py
```

## Command Line Options

```

usage: list-users.py [-h]

List all Users

optional arguments:
  -h, --help  show this help message and exit

```

## Information Displayed

The following information is displayed in table form for all the users located.

```
UserName
Path
Date Created
User Id
Arn
Password Last Used
```
