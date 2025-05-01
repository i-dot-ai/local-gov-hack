from app.services.aws_service import S3Service, TextractService, BedrockService

# Upload document
s3 = S3Service()
file_path = s3.upload_file(uploaded_file, "applications/123/plans.pdf")

# Extract text
textract = TextractService()
text = textract.extract_text(file_path)

# Process with Bedrock
bedrock = BedrockService()
result = bedrock.invoke_model(
    prompt=f"Analyze this document: {text}",
    model_id="anthropic.claude-v2"
)