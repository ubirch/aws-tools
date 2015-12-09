# IAM tools

## Setup
the tools in here use the AWS Boto Python framework. It reads AWS credentials by default from ~/.boto

This tool however tries to read it from the local directory first to allow for special credentials.

So create a .boto file in the $PWD with the credentials you wanna use.

## Check whether AWS MFA devices have been set

```
python check_mfa_devices.py -u <username>  -a mfa
```

## check for AWS Access Keys

```
python check_mfa_devices.py -u <username>  -a list
```