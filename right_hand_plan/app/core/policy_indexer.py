from app.services.aws_service import list_s3_objects, get_s3_object_content
from app.services.search_service import index_policy_documents
import logging

def index_all_policies():
    """
    Index all policy documents for search
    """
    try:
        # Get list of all policy documents
        policy_files = list_s3_objects(
            bucket=current_app.config['S3_POLICY_BUCKET'],
            prefix=current_app.config['S3_POLICY_PREFIX']
        )
        
        # Retrieve content of each policy
        policies = []
        for policy_key in policy_files:
            policy_content = get_s3_object_content(
                bucket=current_app.config['S3_POLICY_BUCKET'],
                key=policy_key
            )
            
            policies.append({
                'policy_name': policy_key.split('/')[-1],
                'policy_key': policy_key,
                'content': policy_content
            })
        
        # Index policies
        index_policy_documents(policies)
        
        return True
    except Exception as e:
        logging.error(f"Error indexing policies: {str(e)}")
        return False