import boto3
from flask import current_app
import os
import tempfile
from PyPDF2 import PdfReader
from docx import Document
import logging

s3_client = boto3.client(
    's3',
    aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
    region_name=current_app.config['AWS_REGION']
)

bedrock_client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
    region_name=current_app.config['AWS_REGION']
)

def upload_to_s3(bucket, key, file_obj):
    try:
        s3_client.upload_fileobj(file_obj, bucket, key)
        return True
    except Exception as e:
        logging.error(f"Error uploading to S3: {str(e)}")
        raise

def download_from_s3(bucket, key):
    try:
        _, file_extension = os.path.splitext(key)
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            s3_client.download_fileobj(bucket, key, temp_file)
            return temp_file.name
    except Exception as e:
        logging.error(f"Error downloading from S3: {str(e)}")
        raise

def list_s3_objects(bucket, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except Exception as e:
        logging.error(f"Error listing S3 objects: {str(e)}")
        return []

def get_s3_object_content(bucket, key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error getting S3 object content: {str(e)}")
        raise

def extract_text_from_s3_object(bucket, key):
    try:
        file_path = download_from_s3(bucket, key)
        text = extract_text_from_file(file_path)
        os.remove(file_path)
        return text
    except Exception as e:
        logging.error(f"Error extracting text from S3 object: {str(e)}")
        raise

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text
    elif file_extension.lower() in ('.doc', '.docx'):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_extension.lower() == '.txt':
        with open(file_path, 'r') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")