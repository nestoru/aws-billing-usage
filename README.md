# AWS Billing
Extract AWS billing information.

The name of the scripts should be self explanatory.

## Preconditions
- Use a virtual environment
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
- (Optional) If you need to deactivate
```
deactivate
```
- If you add new dependencies
```
pip freeze > requirements.txt
```
-  Set an AWS profile with access to AWS billing

## Running it for July 2024
```
python aws_billing_usage.py --profile <your profile here> 2024-07-01 2024-07-30
```
