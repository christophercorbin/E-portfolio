import json
import boto3
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
import re

# Initialize AWS clients
ses_client = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')

# Environment variables
CONTACT_EMAIL = os.environ['CONTACT_EMAIL']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
CORS_ORIGIN = os.environ.get('CORS_ORIGIN', '*')

# Get DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for contact form submissions.
    Processes form data, stores in DynamoDB, and sends email via SES.
    """
    
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': CORS_ORIGIN,
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }
    
    try:
        # Handle preflight OPTIONS request
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight successful'})
            }
        
        # Parse request body
        if not event.get('body'):
            return create_error_response(400, 'Request body is required', cors_headers)
        
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return create_error_response(400, 'Invalid JSON in request body', cors_headers)
        
        # Validate required fields
        validation_result = validate_form_data(body)
        if not validation_result['valid']:
            return create_error_response(400, validation_result['error'], cors_headers)
        
        # Extract validated data
        name = body['name'].strip()
        email = body['email'].strip().lower()
        message = body['message'].strip()
        
        # Generate unique submission ID
        submission_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Store submission in DynamoDB
        store_submission(submission_id, timestamp, name, email, message, event)
        
        # Send email notification
        send_email_notification(name, email, message, submission_id)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'message': 'Thank you for your message! I will get back to you soon.',
                'submissionId': submission_id
            })
        }
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(500, 'Internal server error. Please try again later.', cors_headers)

def validate_form_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate contact form data."""
    
    # Check required fields
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if field not in data or not data[field] or not str(data[field]).strip():
            return {'valid': False, 'error': f'Field "{field}" is required'}
    
    name = str(data['name']).strip()
    email = str(data['email']).strip()
    message = str(data['message']).strip()
    
    # Validate name length
    if len(name) < 1 or len(name) > 100:
        return {'valid': False, 'error': 'Name must be between 1 and 100 characters'}
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return {'valid': False, 'error': 'Please provide a valid email address'}
    
    # Validate message length
    if len(message) < 10 or len(message) > 1000:
        return {'valid': False, 'error': 'Message must be between 10 and 1000 characters'}
    
    # Basic spam detection
    spam_indicators = ['viagra', 'casino', 'loan', 'bitcoin', 'crypto']
    message_lower = message.lower()
    if any(indicator in message_lower for indicator in spam_indicators):
        return {'valid': False, 'error': 'Message content appears to be spam'}
    
    return {'valid': True}

def store_submission(submission_id: str, timestamp: str, name: str, email: str, message: str, event: Dict[str, Any]) -> None:
    """Store form submission in DynamoDB."""
    
    # Calculate TTL (30 days from now)
    ttl = int((datetime.utcnow() + timedelta(days=30)).timestamp())
    
    # Get client IP (if available)
    client_ip = 'unknown'
    if 'requestContext' in event and 'identity' in event['requestContext']:
        client_ip = event['requestContext']['identity'].get('sourceIp', 'unknown')
    
    # Store in DynamoDB
    table.put_item(
        Item={
            'submissionId': submission_id,
            'timestamp': timestamp,
            'name': name,
            'email': email,
            'message': message,
            'clientIp': client_ip,
            'userAgent': event.get('headers', {}).get('User-Agent', 'unknown'),
            'status': 'received',
            'ttl': ttl
        }
    )

def send_email_notification(name: str, email: str, message: str, submission_id: str) -> None:
    """Send email notification via SES."""
    
    subject = f"Portfolio Contact Form: Message from {name}"
    
    # Create HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #ff9900, #146eb4); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
            .field {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #232f3e; }}
            .value {{ background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #ff9900; }}
            .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>New Portfolio Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="field">
                    <div class="label">Name:</div>
                    <div class="value">{name}</div>
                </div>
                
                <div class="field">
                    <div class="label">Email:</div>
                    <div class="value">{email}</div>
                </div>
                
                <div class="field">
                    <div class="label">Message:</div>
                    <div class="value">{message}</div>
                </div>
                
                <div class="footer">
                    <p><strong>Submission Details:</strong></p>
                    <p>Submission ID: {submission_id}</p>
                    <p>Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    <p>Sent from: Christopher Corbin Portfolio Contact Form</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    text_body = f"""
New Portfolio Contact Form Submission

Name: {name}
Email: {email}

Message:
{message}

---
Submission ID: {submission_id}
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Sent from: Christopher Corbin Portfolio Contact Form
    """
    
    # Send email via SES
    ses_client.send_email(
        Source=CONTACT_EMAIL,
        Destination={
            'ToAddresses': [CONTACT_EMAIL]
        },
        ReplyToAddresses=[email],
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': html_body,
                    'Charset': 'UTF-8'
                },
                'Text': {
                    'Data': text_body,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

def create_error_response(status_code: int, message: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Create standardized error response."""
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps({
            'error': message,
            'statusCode': status_code
        })
    }