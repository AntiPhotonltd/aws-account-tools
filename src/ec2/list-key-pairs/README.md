List Key Pairs
=========

This is a simple script to retrieve a list of EC2 key pairs

## Simple Usage

```
./list-key-pairs.py
```

## Command Line Options

```

./list-key-pairs.py -h
usage: list-key-pairs.py [-h] [-r REGION]

List Key Pairs

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        The aws region

```

## Information Displayed

The following information is displayed in table form for all the key pairs located.

```
KeyName
KeyFingerprint
```
