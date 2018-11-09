List Certificates
=========

This is a simple script to retrieve a list of all acm certificates and display some information about them.

NOTE: This script does not take region as a parameter as IAM is NOT linked to a region.

## Simple Usage

```
./list-certificates.py
```

## Command Line Options

```

usage: list-certificates.py [-h]

List Certificates

optional arguments:
  -h, --help  show this help message and exit

```

## Information Displayed

The following information is displayed in table form for all the certificates located.

```
Domain Name
Certificate Arn
```
