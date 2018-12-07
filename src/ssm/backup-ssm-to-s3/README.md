Backup Parameter Store to S3
=========

## Simple Usage

```
./backup-ssm-to-s3.py -b 'my-backup-bucket'
```

## Command Line Options

```

usage: backup-ssm-to-s3.py [-h] -b BUCKET [-c] [-d] [-f] [-p PREFIX]
                           [-r REGION] [-u] [-x]

Backup Parameter Store

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                        The bucket to write to
  -c, --csv             Write the backup as a csv file [default: json]
  -d, --default-region  Use the AWS_DEFAULT_REGION
  -f, --force           Force the creation of the bucket if it does not exist
  -p PREFIX, --prefix PREFIX
                        The prefix for the backup file [default: backup]
  -r REGION, --region REGION
                        The AWS region
  -u, --unencrypted     Unencrypted backup?
  -x, --xml             Write the backup as a xml file [default: json]

```
