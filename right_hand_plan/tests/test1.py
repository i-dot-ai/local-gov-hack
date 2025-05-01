import requests
from io import BytesIO

# Prepare test files
file1 = ("application_form.pdf", BytesIO(b"PDF content here"))
file2 = ("supporting_docs.docx", BytesIO(b"Word doc content here"))

# Submit application
response = requests.post(
    "http://localhost:5000/api/submit-application",
    files=[
        ('files', file1),
        ('files', file2)
    ]
)

if response.status_code == 200:
    result = response.json()
    print("Application submitted successfully!")
    print(f"Application ID: {result['application_id']}")
    print(f"Report URL: {result['report_url']}")
    print(f"Relevant Policies: {', '.join(result['relevant_policies'])}")
    if result['issues_found']:
        print(f"Issues found: {len(result['issues_found'])}")
    else:
        print("No issues found!")
else:
    print(f"Error: {response.json()['error']}")