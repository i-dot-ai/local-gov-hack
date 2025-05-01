from flask import current_app
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_application_request(request):
    errors = []
    
    if 'files' not in request.files:
        errors.append('No files provided')
        return errors
        
    files = request.files.getlist('files')
    
    if not files or all(file.filename == '' for file in files):
        errors.append('No selected files')
        
    for file in files:
        if not allowed_file(file.filename):
            errors.append(f'File type not allowed: {file.filename}')
            
    return errors