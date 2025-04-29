import os
from openai import AzureOpenAI

# Ensure your environment variables are set - these will have been provided as part of the hackathon
openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1")
api_version = os.environ.get("OPENAI_API_VERSION", "2024-08-01-preview")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    azure_deployment=openai_model,
    api_key=api_key,
)

completion = client.chat.completions.create(
    model=openai_model,
    messages=[
        {
            "role": "user",
            "content": "Summarise UK planning policy in a sentence",
        },
    ],
)

print(completion.to_json())

print("--------------------------------")

print(completion.choices[0].message.content)
