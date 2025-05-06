# ☁️ Accessing LLMs with AWS Bedrock

> **⚠️ DEPRECATED INFORMATION ⚠️**  
> The following instructions were specific to a past hackathon event and are no longer valid. The AWS accounts and access codes mentioned were temporary and have been deactivated. This document is preserved for reference only.

As part of the Local Government Hack you have been provided with a free AWS account. This will last for the duration of the hack and will be automatically deleted afterwards. You can use this AWS account to access LLMs and, if you want, other standard AWS features such as SageMaker, S3, Lambda, API Gateway etc for the duration of the hack.

The **aim** of this tutorial is to run Claude 3.7 Sonnet locally with AWS Bedrock, in around 15 mins.

## 1 - Setting up an AWS Account

In this section we want to setup a temporary AWS account that you can use for the duration of the hackathon.

AWS has a specific account configuration for hackathons such as this one. We'll use that to setup for this event.
1. Follow the instructions in the *AWS Generative AI Hackathon Tutorial* [here](https://catalog.workshops.aws/genai-hackathon/en-US). The access code for this event is `<this will be provided>`. 
2. Once you have joined the event (Environment Setup > Login to Workshop Studio > Step 5) you can access the AWS Console via the *Open AWS console* link on the bottom left of the page. 
3. If you initially try to access the Services via the *AWS Services for the Hackathon* page this can redirect you to a separate login page. If this happens, make sure to use the *Open AWS console* link instead.

You now have access to an AWS Account for the duration of the hackathon. Check you are logging on to the correct AWS Account. The Account number is shown at the top right corner of the screen, make sure it matches those of your teammates.
## 2 - Setting up Claude 3.7 Sonnet on AWS Bedrock

In this section we want to get access to Claude 3.7 Sonnet on AWS Bedrock.

1. Stay in the AWS console from the previous steps.
2. Navigate to AWS Bedrock using the search options at the top.
3. Open the *Model access* page. This is under Bedrock configurations at the very bottom left.
4. Go to the Claude 3.7 Sonnet model, click on *Available to Request* and then select *Request model access*.
5. This'll take you through to an *Edit Model Access* page, navigate to the bottom and click Next. Submit your request. 
6. The access status for Claude 3.7 Sonnet will immediately change to *In Progress*. You'll need to wait a minute or two to be granted access.

Verify your access to Claude 3.7 Sonnet by navigating to the model playground and having a quick play there. You can get there via the *Model catalog* or *Overview* sections on the left, selecting Claude 3.7 Sonnet, and then *Open in Playground*. 

You now have access to Claude 3.7 Sonnet in AWS Bedrock.
## 3 - Configuring AWS to run locally

We now want to run our model locally using. We'll follow the example AWS tutorial [here](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-ex-python.html). This tutorial has a few prerequisites:
- [x] You have an AWS account.
- [x] You have access to a Bedrock model.
- [ ] You have a user and a role with authentication set up for Amazon Bedrock.
- [ ] You've installed and set up authentication for the AWS SDK for Python.

We've covered off the first two. Let's tackle setting up an IAM role with permissions for bedrock. 
### Setting up an IAM role with Bedrock access
#### Setting up an IAM role
In this section we'll create an IAM role within AWS.
1. **Navigate to the IAM Service**
    - Click on the search bar at the top and type "IAM"
    - Select "IAM" from the results
2. **Create a New User**
    - In the left sidebar, click "Users"
    - Click the "Create user" button
    - Enter a username (e.g., "bedrock-api-user")
    - Click "Next"
3. **Set Permissions**
    - Choose "Attach policies directly"
    - Search for "Bedrock" in the search box
    - Check the box next to "AmazonBedrockFullAccess"
    - Click "Next"
4. **Review and Create**
    - Review the user details and permissions
    - Click "Create user"

#### Obtaining Access Keys
1. **Return to IAM Users**
    - Click on the username you just created in the IAM user list
2. **Create Access Keys**
    - Select the "Security credentials" tab
    - Scroll down to "Access keys"
    - Click "Create access key"
3. **Select Use Case**
    - Choose "Command Line Interface (CLI)"
    - Check the acknowledgment box
    - Click "Next"
4. **Add Description (Optional)**
    - You can add a description tag if desired
    - Click "Create access key"
5. **Save Your Credentials**
    - You'll see your "Access key ID" and "Secret access key"
    - Click "Download .csv file" to save these credentials
    - **This is the only time you'll be able to view or download the secret access key, so save it securely**
    - Click "Done"
You now have an IAM role with permissions for AWS Bedrock. If down the line you want to provide permissions for other services, then you'll need to add further permissions to this IAM role. Let's now tackle authentication for the AWS SDK. 
### Authentication for the AWS SDK

For additional resources you can view the Boto3 tutorial [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html), and the AWS CLI tutorial [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). We'll take a streamlined approach.

We'll want to configure AWS credentials locally. Setup a virtual python environment and install `boto3` and `awscli`. It's best to do this in the repository you'll work in for the hackathon.

```bash
python -m venv .venv
source .venv/bin/activate
pip install boto3 awscli
```

**If you don't have other AWS credentials setup** on your laptop, configure your AWS credentials locally using:
```bash
aws configure
```
When prompted, enter your access key ID, secret key, and region (this is likely `us-west-2` but you can confirm in the AWS Console). 

**If you have other AWS credentials setup** on your laptop and don't want to change these then you can run `aws configure --profile bedrock-api` to associate your new credentials with a distinct profile. Likewise enter your access key ID, secret key, and region when prompted. When running python code, you'll need to use this profile rather than the default profile:
```python
session = boto3.Session(profile_name='bedrock-api')
bedrock = session.client(
	service_name='bedrock-runtime',
	region_name='us-west-2'
)
```

You now have AWS credential setup locally so that you can run Bedrock from your laptop. These are stored in an AWS credentials file (typically `~/.aws/credentials` on Mac/Linux or `C:\Users\USERNAME\.aws\credentials` on Windows). 

### Setup an Inference Profile

An inference profile in AWS Bedrock defines how a foundation model is deployed and served. It specifies which model to use along with deployment parameters. Claude 3.7 Sonnet requires an inference profile to run. We can't just call the model directly but have to use a inference profile containing this model. 

In the *Inference and Assessment* section on the left, select *Cross-region Inference* and save the *Inference Profile ID* that corresponds to Claude 3.7 Sonnet. We'll use this later.
## 4 - Running an example script

We're getting close now, stay with me. So far we've done a few things:
- Setup an AWS account ✅
- Setup access to Claude 3.7 Sonnet within AWS Bedrock ✅ 
- Created an IAM role with access to AWS Bedrock and configured access keys ✅
- Setup the `aws-cli` and `boto3` in a virtual environment ✅
- Worked out how to serve Claude 3.7 Sonnet via an inference profile ✅

We now need to run a quick script to make sure it's all working. Then it's time to hack.

Setup a `demo.py` script. Include the following code. **You will need to include your own Inference Profile ID** you found in the previous section. 

```python
import boto3
import json

# Initialise the Bedrock client using the default profile
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

def generate_text(prompt, max_tokens=200, temperature=1):
    """
    Generate text using Claude 3.7 Sonnet on AWS Bedrock
    using an existing inference profile
    """
    # Claude 3.7 Sonnet inference profile ARN
    inference_profile_arn = <inference-profile-ID>
    
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
```

**If you used a custom profile in the earlier steps**, then make sure to use that snippet to initialise the `bedrock_runtime` client instead.

Run this script from your virtual environment using `python demo.py` and if it's all working, you should see a concise explanation of local government planning. If not then review the previous steps and make sure you've gone through them all correctly. There'll be people from AWS around during the hack that can help with these steps as well.

---
Nice, you've successfully set up Claude 3.7 Sonnet on AWS Bedrock and can use this as part of the hackathon. Your next steps could include exploring the model's capabilities through prompt engineering, integrating it with other AWS services, or exploring some of the tool use capabilities.