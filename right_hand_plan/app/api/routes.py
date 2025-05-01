from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.core.application_validator import validate_application
from app.core.document_processor import process_application_documents
from app.core.policy_analyzer import analyze_policies
from app.services.aws_service import upload_to_s3
from app.utils.helpers import generate_report_pdf
import uuid
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/submit-application', methods=['POST'])
@cross_origin()
def submit_application():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
            
        files = request.files.getlist('files')
        application_id = str(uuid.uuid4())
        
        # Upload files to S3
        uploaded_files = []
        for file in files:
            file_key = f"{application_id}/{file.filename}"
            upload_to_s3(
                bucket=current_app.config['S3_APPLICATION_BUCKET'],
                key=f"{current_app.config['S3_APPLICATION_PREFIX']}{file_key}",
                file_obj=file
            )
            uploaded_files.append(file_key)
        
        # Process application documents
        processed_data = process_application_documents(application_id, uploaded_files)
        
        # Analyze relevant policies
        relevant_policies = analyze_policies(processed_data['text_content'])
        
        # Validate application against policies
        validation_results = validate_application(
            application_data=processed_data,
            policy_documents=relevant_policies
        )
        
        # Generate report
        report_url = generate_report_pdf(
            application_id=application_id,
            validation_results=validation_results,
            policy_recommendations=relevant_policies
        )
        
        return jsonify({
            'application_id': application_id,
            'status': 'submitted',
            'report_url': report_url,
            'relevant_policies': [p['policy_name'] for p in relevant_policies],
            'issues_found': validation_results.get('issues', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500