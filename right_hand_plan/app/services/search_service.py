import json
from flask import current_app
import logging

def search_relevant_policies(query_text, policy_files):
    """
    Use Bedrock to find relevant policies for the application
    """
    try:
        # Prepare prompt for policy search
        prompt = f"""You are a policy analysis assistant. Your task is to review the following application content and identify which of the available policy documents are relevant.

Application Content:
{query_text[:10000]}  # Limiting to first 10k chars for prompt

Available Policy Documents:
{", ".join([f.split('/')[-1] for f in policy_files])}

Instructions:
1. Analyze the application content to understand its purpose and requirements
2. Identify which policy documents are most relevant
3. Return ONLY a JSON array of the relevant policy document keys (full S3 paths)

Output should be ONLY the JSON array, nothing else.
"""
        
        # Call Bedrock
        response = bedrock_client.invoke_model(
            modelId=current_app.config['BEDROCK_MODEL_ID'],
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": current_app.config['BEDROCK_MAX_TOKENS'],
                "temperature": current_app.config['BEDROCK_TEMPERATURE']
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        relevant_policies = json.loads(response_body['completion'].strip())
        
        return relevant_policies
    except Exception as e:
        logging.error(f"Error searching relevant policies: {str(e)}")
        return []

def validate_against_policies(application_content, policy_documents):
    """
    Use Bedrock to validate application against policies
    """
    try:
        # Prepare prompt for validation
        prompt = f"""You are an application validation assistant. Your task is to review the application against the relevant policies and identify any issues or missing requirements.

Application Details:
Application ID: {application_content['application_id']}
Documents: {[doc['file_name'] for doc in application_content['documents']}

Application Content:
{"\n".join([f"{doc['file_name']}:\n{doc['content'][:5000]}" for doc in application_content['documents']])}

Relevant Policies:
{"\n".join([f"{policy['policy_name']}:\n{policy['content'][:5000]}" for policy in policy_documents])}

Instructions:
1. Analyze each application document against the relevant policies
2. Identify any discrepancies, missing information, or non-compliance issues
3. Provide specific feedback for each issue found
4. Return a JSON object with the following structure:
{{
    "summary": "Overall validation status",
    "issues": [
        {{
            "document": "Document name",
            "issue": "Description of issue",
            "policy_reference": "Relevant policy section",
            "severity": "high/medium/low",
            "suggestion": "How to fix the issue"
        }}
    ],
    "compliance_score": "Percentage of compliance"
}}

Output should be ONLY the JSON object, nothing else.
"""
        
        # Call Bedrock
        response = bedrock_client.invoke_model(
            modelId=current_app.config['BEDROCK_MODEL_ID'],
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": current_app.config['BEDROCK_MAX_TOKENS'],
                "temperature": current_app.config['BEDROCK_TEMPERATURE']
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        validation_results = json.loads(response_body['completion'].strip())
        
        return validation_results
    except Exception as e:
        logging.error(f"Error validating application: {str(e)}")
        return {
            "summary": "Validation failed",
            "issues": [],
            "compliance_score": "0%"
        }

def index_policy_documents(policy_documents):
    """
    Index policy documents for search (simplified version)
    In a real implementation, this would use a proper search service
    """
    # This is a placeholder - in a real system you might use OpenSearch, Pinecone, etc.
    # For this example, we'll just store the policy metadata in memory
    pass