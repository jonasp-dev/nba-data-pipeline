import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name, default_value = None):
    return os.getenv(var_name, default_value)

AWS_REGION = get_env_variable("AWS_REGION", "us-east-1")
S3_BUCKET = get_env_variable("S3_BUCKET_NAME", "your-s3-bucket-name")
RABBITMQ_HOST = get_env_variable("RABBITMQ_URL", "your-rabbitmq-url")
RABBITMQ_PORT = get_env_variable("RABBITMQ_PORT", 5672)
RABBITMQ_USER = get_env_variable("RABBITMQ_USER", "your-rabbitmq-user")
RABBITMQ_PASSWORD = get_env_variable("RABBITMQ_PASSWORD", "your-rabbitmq-password")
ACCESS_ID = get_env_variable("AWS_ACCESS_KEY_ID", "your-access-key-id")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY", "your-access-key")
POSTGRES_HOST = get_env_variable("POSTGRES_HOST", "postgres")
POSTGRES_DB = get_env_variable("POSTGRES_DB", "nba_data")
POSTGRES_USER = get_env_variable("POSTGRES_USER", "user")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD", "password")