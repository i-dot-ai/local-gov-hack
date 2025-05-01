from app.services.aws_service import list_s3_objects, get_s3_object_content
from app.services.search_service import search_relevant_policies
import json

def analyze_policies(application_texts):
    """
    Analyze application content and identify relevant policies
    """
    # Extract combined text from all application documents
    combined_text = "\n".join([doc['content'] for doc in application_texts])
    
    # Get list of all policy documents
    policy_files = list_s3_objects(
        bucket=current_app.config['S3_POLICY_BUCKET'],
        prefix=current_app.config['S3_POLICY_PREFIX']
    )
    
    # Search for relevant policies using LLM
    relevant_policy_keys = search_relevant_policies(
        query_text=combined_text,
        policy_files=policy_files
    )
    
    # Retrieve content of relevant policies
    relevant_policies = []
    for policy_key in relevant_policy_keys:
        policy_content = get_s3_object_content(
            bucket=current_app.config['S3_POLICY_BUCKET'],
            key=policy_key
        )
        
        relevant_policies.append({
            'policy_name': policy_key.split('/')[-1],
            'policy_key': policy_key,
            'content': policy_content
        })
    
    return relevant_policies