# This is a demo of how to use the AWS Bedrock API to access the Claude 3.7 Sonnet model.
# It uses an existing inference profile to access the model. You will need to update the inference profile ID below.

import boto3
import json

# Initialise the Bedrock client using the default profile
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

# If you used a custom profile, you can use the following code to set it up instead:
# session = boto3.Session(profile_name='bedrock-api')
# bedrock = session.client(
# 	service_name='bedrock-runtime',
# 	region_name='us-west-2'
# )

def generate_text(prompt, max_tokens=200, temperature=1):
    """
    Generate text using Claude 3.7 Sonnet on AWS Bedrock
    using an existing inference profile
    """
    # Claude 3.7 Sonnet inference profile ARN - REPLACE WITH YOUR OWN IF NEEDED
    inference_profile_arn = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "top_k": 250,
        "stop_sequences": [],
        "temperature": temperature,
        "top_p": 0.999,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    response = bedrock.invoke_model(
        modelId=inference_profile_arn,  # Use the inference profile ARN
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body)
    )
    
    # Parse the response
    response_body = json.loads(response.get('body').read())
    return response_body

# Example usage
if __name__ == "__main__":
    response = generate_text("Tell me about local planning in the UK in a sentence or two.")
    
    # Extract and print the assistant's message
    if 'content' in response:
        for item in response['content']:
            if item['type'] == 'text':
                print(item['text'])