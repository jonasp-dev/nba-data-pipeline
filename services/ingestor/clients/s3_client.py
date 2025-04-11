import boto3
from config.config import AWS_REGION, ACCESS_ID, AWS_SECRET_ACCESS_KEY

def create_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )