from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import current_app
import os
import tempfile
import logging

def generate_report_pdf(application_id, validation_results, policy_recommendations):
    """
    Generate a PDF report with validation results and policy recommendations
    """
    try:
        # Create a temporary file for the PDF
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"report_{application_id}.pdf")
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title = Paragraph("Application Validation Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add application ID
        app_id = Paragraph(f"Application ID: {application_id}", styles['Heading2'])
        story.append(app_id)
        story.append(Spacer(1, 12))
        
        # Add summary
        summary = Paragraph(f"<b>Summary:</b> {validation_results.get('summary', 'No summary available')}", styles['BodyText'])
        story.append(summary)
        story.append(Spacer(1, 12))
        
        # Add compliance score
        compliance = Paragraph(f"<b>Compliance Score:</b> {validation_results.get('compliance_score', 'N/A')}", styles['BodyText'])
        story.append(compliance)
        story.append(Spacer(1, 12))
        
        # Add issues if any
        if validation_results.get('issues'):
            issues_title = Paragraph("<b>Issues Found:</b>", styles['Heading2'])
            story.append(issues_title)
            story.append(Spacer(1, 6))
            
            for issue in validation_results['issues']:
                issue_text = f"""
                <b>Document:</b> {issue.get('document', 'Unknown')}<br/>
                <b>Issue:</b> {issue.get('issue', 'No description')}<br/>
                <b>Severity:</b> {issue.get('severity', 'Unknown')}<br/>
                <b>Policy Reference:</b> {issue.get('policy_reference', 'None')}<br/>
                <b>Suggestion:</b> {issue.get('suggestion', 'No suggestion')}
                """
                issue_para = Paragraph(issue_text, styles['BodyText'])
                story.append(issue_para)
                story.append(Spacer(1, 12))
        
        # Add recommended policies
        if policy_recommendations:
            policies_title = Paragraph("<b>Relevant Policy Documents:</b>", styles['Heading2'])
            story.append(policies_title)
            story.append(Spacer(1, 6))
            
            for policy in policy_recommendations:
                policy_text = f"<b>{policy.get('policy_name', 'Unknown Policy')}</b>"
                policy_para = Paragraph(policy_text, styles['BodyText'])
                story.append(policy_para)
                story.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(story)
        
        # Upload PDF to S3
        report_key = f"reports/{application_id}/validation_report.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            upload_to_s3(
                bucket=current_app.config['S3_APPLICATION_BUCKET'],
                key=f"{current_app.config['S3_APPLICATION_PREFIX']}{report_key}",
                file_obj=pdf_file
            )
        
        # Clean up temporary file
        os.remove(pdf_path)
        
        # Return the S3 URL (in a real app, you might generate a pre-signed URL)
        return f"s3://{current_app.config['S3_APPLICATION_BUCKET']}/{current_app.config['S3_APPLICATION_PREFIX']}{report_key}"
        
    except Exception as e:
        logging.error(f"Error generating report PDF: {str(e)}")
        return None