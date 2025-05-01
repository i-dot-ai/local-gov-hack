from app.services.aws_service import download_from_s3, extract_text_from_s3_object
from app.utils.helpers import extract_text_from_file
import os

def process_application_documents(application_id, file_keys):
    """
    Process uploaded application documents and extract text content
    """
    text_content = []
    metadata = []
    
    for file_key in file_keys:
        # Download file from S3
        file_path = download_from_s3(
            bucket=current_app.config['S3_APPLICATION_BUCKET'],
            key=f"{current_app.config['S3_APPLICATION_PREFIX']}{file_key}"
        )
        
        # Extract text from file
        text = extract_text_from_file(file_path)
        
        # Store metadata and content
        metadata.append({
            'file_name': os.path.basename(file_key),
            'file_type': os.path.splitext(file_key)[1][1:].lower(),
            'file_size': os.path.getsize(file_path)
        })
        
        text_content.append({
            'file_name': os.path.basename(file_key),
            'content': text
        })
        
        # Clean up downloaded file
        os.remove(file_path)
    
    return {
        'application_id': application_id,
        'metadata': metadata,
        'text_content': text_content
    }