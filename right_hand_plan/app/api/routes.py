from flask import request, jsonify
from . import api_blueprint
from ..services.aws_service import upload_application_to_s3, analyze_policy_documents
from ..utils.helpers import generate_pdf_report

@api_blueprint.route('/submit_application', methods=['POST'])
def submit_application():
    application_data = request.get_json()
    upload_application_to_s3(application_data)
    validation_results = analyze_policy_documents(application_data)
    report = generate_pdf_report(validation_results)
    return jsonify({'message': 'Application submitted successfully', 'report': report})