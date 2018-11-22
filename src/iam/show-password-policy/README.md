List IAM Users
=========

## Simple Usage

```
./list-iam-users.py
```

## Command Line Options

```

usage: list-iam-users.py [-h]

List IAM Users

optional arguments:
  -h, --help  show this help message and exit

```

### Additional Information

AllowUsersToChangePassword -> Specifies whether IAM users are allowed to change their own password.
ExpirePasswords -> Indicates whether passwords in the account expire. Returns true if MaxPasswordAge contains a value greater than 0. Returns false if MaxPasswordAge is 0 or not present.
HardExpiry -> Specifies whether IAM users are prevented from setting a new password after their password has expired.
MaxPasswordAge -> The number of days that an IAM user password is valid.
MinimumPasswordLength -> Minimum length to require for IAM user passwords.
PasswordReusePrevention -> Specifies the number of previous passwords that IAM users are prevented from reusing.
RequireLowercaseCharacters -> Specifies whether to require lowercase characters for IAM user passwords.
RequireNumbers -> Specifies whether to require numbers for IAM user passwords.
RequireSymbols -> Specifies whether to require symbols for IAM user passwords.
RequireUppercaseCharacters -> Specifies whether to require uppercase characters for IAM user passwords.


