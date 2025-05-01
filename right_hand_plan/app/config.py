import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_POLICY_BUCKET = os.getenv('S3_POLICY_BUCKET')
    S3_POLICY_PREFIX = os.getenv('S3_POLICY_PREFIX')
    S3_APPLICATION_BUCKET = os.getenv('S3_APPLICATION_BUCKET')
    S3_APPLICATION_PREFIX = os.getenv('S3_APPLICATION_PREFIX')
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID')
    BEDROCK_MAX_TOKENS = int(os.getenv('BEDROCK_MAX_TOKENS', 4096))
    BEDROCK_TEMPERATURE = float(os.getenv('BEDROCK_TEMPERATURE', 0.5))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = eval(os.getenv('MAX_CONTENT_LENGTH', '16 * 1024 * 1024'))