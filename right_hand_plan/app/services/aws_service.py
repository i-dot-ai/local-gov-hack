import boto3
import json
from ..config import Config
import logging

s3 = boto3.client('s3', aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                      region_name=Config.AWS_REGION)

bedrock = boto3.client('bedrock-runtime', aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                           region_name=Config.AWS_REGION)

S3_BUCKET_NAME = Config.S3_BUCKET_NAME
POLICY_DOCS_PREFIX = 'Policy Docs/'
APPLICATIONS_PREFIX = 'applications/'

def upload_application_to_s3(application_data):
    # Logic to upload application to S3
    filename = application_data['filename']
    file_content = application_data['file']
    s3.put_object(Body=file_content, Bucket=S3_BUCKET_NAME, Key=APPLICATIONS_PREFIX + filename)

def list_policy_documents():
    # Logic to list policy documents from S3
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=POLICY_DOCS_PREFIX)
    policy_docs = [{'Key': obj['Key'], 'LastModified': obj['LastModified']} for obj in response.get('Contents', [])]
    return policy_docs

def get_policy_document_content(policy_docs):
    # Logic to get policy document content from S3
    policy_documents = []
    for policy_doc in policy_docs:
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=policy_doc['Key'])
        policy_documents.append({
            'policy_name': policy_doc['Key'].split('/')[-1],
            'content': response['Body'].read().decode('utf-8')
        })
    return policy_documents

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
{", ".join([f.split('/')[-1] for f in [policy['Key'] for policy in policy_files]])}

Instructions:
1. Analyze the application content to understand its purpose and requirements
2. Identify which policy documents are most relevant
3. Return ONLY a JSON array of the relevant policy document keys (full S3 paths)

Output should be ONLY the JSON array, nothing else.
"""
        
        # Call Bedrock
        response = bedrock.invoke_model(
            modelId=Config.BEDROCK_LLM_MODEL_ID,
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 1024,
                "temperature": 0.5
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read().decode())
        relevant_policies = json.loads(response_body['completion'].strip())
        
        return relevant_policies
    except Exception as e:
        logging.error(f"Error searching relevant policies: {str(e)}")
        return []

def validate_against_policies(application_content, policy_documents):
    try:
        nl = '\n'
        prompt = (
            f"You are an application validation assistant. Your task is to review the application against the relevant policies and identify any issues or missing requirements.\n"
            f"Application Details:\nApplication ID: {application_content['application_id']}\nDocuments: {[doc['file_name'] for doc in application_content['documents']]}\n"
            f"Application Content:\n"
        )
        for doc in application_content['documents']:
            prompt += f"{doc['file_name']}:\n{doc['content'][:5000]}\n\n"
        prompt += f"Relevant Policies:\n"
        for policy in policy_documents:
            prompt += f"{policy['policy_name']}:\n{policy['content'][:5000]}\n\n"
        prompt += f"Instructions:\n"
        prompt += "1. Analyze each application document against the relevant policies\n"
        prompt += "2. Identify any discrepancies"
        prompt += "3. Provide specific feedback for each issue found\n"
        prompt += "4. Return a JSON object with the following structure:\n"
        prompt += f"{{\n"
        prompt += f'    "summary": "Overall validation status",\n'
        prompt += '    "issues": [\n'
        prompt += '        {\n'
        prompt += '            "document": "Document name",\n'
        prompt += '            "issue": "Description of issue",\n'
        prompt += '            "policy_reference": "Relevant policy section",\n'
        prompt += '            "severity": "high/medium/low",\n'
        prompt += '            "suggestion": "How to fix the issue"\n'
        prompt += '        }\n'
        prompt += '    ],\n'
        prompt += f'    "compliance_score": "Percentage of compliance"\n'
        prompt += "}\n"
        prompt += "Output should be ONLY the JSON object, nothing else.\n"

        response = bedrock.invoke_model(
            modelId=Config.BEDROCK_LLM_MODEL_ID,
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 2048,
                "temperature": 0.5
            })
        )

        response_body = json.loads(response['body'].read().decode())
        validation_results = json.loads(response_body['completion'].strip())
        return validation_results
    except Exception as e:
        logging.error(f"Error validating application: {str(e)}")
        return {
            "summary": "Validation failed",
            "issues": [],
            "compliance_score": "0%"
        }
    

def analyze_policy_documents(application_data):
    # Logic to analyze policy documents using Bedrock LLM
    policy_docs = list_policy_documents()
    query_text = application_data['file']
    relevant_policies = search_relevant_policies(query_text, policy_docs)
    relevant_policy_docs = [policy for policy in policy_docs if policy['Key'] in relevant_policies]
    policy_documents = get_policy_document_content(relevant_policy_docs)
    application_content = {
        'application_id': application_data.get('application_id', 'Unknown'),
        'documents': [{'file_name': application_data['filename'], 'content': application_data['file']}]
    }
    validation_results = validate_against_policies(application_content, policy_documents)
    return validation_results