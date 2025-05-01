from app.services.search_service import validate_against_policies

def validate_application(application_data, policy_documents):
    """
    Validate application against relevant policies
    """
    # Prepare application content for validation
    application_content = {
        'application_id': application_data['application_id'],
        'documents': application_data['text_content']
    }
    
    # Perform validation using LLM
    validation_results = validate_against_policies(
        application_content=application_content,
        policy_documents=policy_documents
    )
    
    return validation_results