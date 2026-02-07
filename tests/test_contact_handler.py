"""Unit tests for contact_handler Lambda function."""
import json
import os
import sys
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from moto import mock_aws
import boto3

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set required environment variables before importing
os.environ['CONTACT_EMAIL'] = 'test@example.com'
os.environ['DYNAMODB_TABLE'] = 'test-contact-table'
os.environ['CORS_ORIGIN'] = '*'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

from contact_handler import (
    lambda_handler,
    validate_form_data,
    create_error_response
)


@pytest.fixture
def valid_contact_form():
    """Fixture for valid contact form data."""
    return {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'message': 'This is a test message that is long enough to pass validation.'
    }


@pytest.fixture
def lambda_event(valid_contact_form):
    """Fixture for Lambda event."""
    return {
        'httpMethod': 'POST',
        'body': json.dumps(valid_contact_form),
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        'requestContext': {
            'identity': {
                'sourceIp': '192.168.1.1'
            }
        }
    }


@pytest.fixture
def lambda_context():
    """Fixture for Lambda context."""
    context = Mock()
    context.function_name = 'test-function'
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test-function'
    context.aws_request_id = 'test-request-id'
    return context


class TestValidation:
    """Test form data validation."""
    
    def test_valid_form_data(self, valid_contact_form):
        """Test validation with valid data."""
        result = validate_form_data(valid_contact_form)
        assert result['valid'] is True
    
    def test_missing_name(self, valid_contact_form):
        """Test validation fails when name is missing."""
        data = valid_contact_form.copy()
        del data['name']
        result = validate_form_data(data)
        assert result['valid'] is False
        assert 'name' in result['error'].lower()
    
    def test_missing_email(self, valid_contact_form):
        """Test validation fails when email is missing."""
        data = valid_contact_form.copy()
        del data['email']
        result = validate_form_data(data)
        assert result['valid'] is False
        assert 'email' in result['error'].lower()
    
    def test_missing_message(self, valid_contact_form):
        """Test validation fails when message is missing."""
        data = valid_contact_form.copy()
        del data['message']
        result = validate_form_data(data)
        assert result['valid'] is False
        assert 'message' in result['error'].lower()
    
    def test_empty_name(self, valid_contact_form):
        """Test validation fails with empty name."""
        data = valid_contact_form.copy()
        data['name'] = '   '
        result = validate_form_data(data)
        assert result['valid'] is False
    
    def test_invalid_email_format(self, valid_contact_form):
        """Test validation fails with invalid email."""
        data = valid_contact_form.copy()
        data['email'] = 'invalid-email'
        result = validate_form_data(data)
        assert result['valid'] is False
        assert 'email' in result['error'].lower()
    
    def test_name_too_long(self, valid_contact_form):
        """Test validation fails when name exceeds 100 characters."""
        data = valid_contact_form.copy()
        data['name'] = 'a' * 101
        result = validate_form_data(data)
        assert result['valid'] is False
        assert '100' in result['error']
    
    def test_message_too_short(self, valid_contact_form):
        """Test validation fails when message is too short."""
        data = valid_contact_form.copy()
        data['message'] = 'short'
        result = validate_form_data(data)
        assert result['valid'] is False
        assert '10' in result['error']
    
    def test_message_too_long(self, valid_contact_form):
        """Test validation fails when message exceeds 1000 characters."""
        data = valid_contact_form.copy()
        data['message'] = 'a' * 1001
        result = validate_form_data(data)
        assert result['valid'] is False
        assert '1000' in result['error']
    
    def test_spam_detection(self, valid_contact_form):
        """Test spam detection blocks spam messages."""
        data = valid_contact_form.copy()
        data['message'] = 'Buy viagra now! Great deals on casino games and bitcoin.'
        result = validate_form_data(data)
        assert result['valid'] is False
        assert 'spam' in result['error'].lower()


class TestLambdaHandler:
    """Test Lambda handler function."""
    
    @mock_aws
    def test_successful_submission(self, lambda_event, lambda_context):
        """Test successful form submission."""
        # Setup mocked AWS resources
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        dynamodb.create_table(
            TableName='test-contact-table',
            KeySchema=[{'AttributeName': 'submissionId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'submissionId', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        ses = boto3.client('ses', region_name='us-east-1')
        ses.verify_email_identity(EmailAddress='test@example.com')
        
        # Call handler
        response = lambda_handler(lambda_event, lambda_context)
        
        # Assertions
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        body = json.loads(response['body'])
        assert 'submissionId' in body
        assert 'Thank you' in body['message']
    
    def test_options_request(self, lambda_context):
        """Test CORS preflight OPTIONS request."""
        event = {'httpMethod': 'OPTIONS'}
        response = lambda_handler(event, lambda_context)
        
        assert response['statusCode'] == 200
        assert response['headers']['Access-Control-Allow-Origin'] == '*'
        assert 'POST' in response['headers']['Access-Control-Allow-Methods']
    
    def test_missing_body(self, lambda_context):
        """Test handler fails gracefully with missing body."""
        event = {'httpMethod': 'POST'}
        response = lambda_handler(event, lambda_context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
    
    def test_invalid_json(self, lambda_context):
        """Test handler fails gracefully with invalid JSON."""
        event = {
            'httpMethod': 'POST',
            'body': 'invalid json{'
        }
        response = lambda_handler(event, lambda_context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'json' in body['error'].lower()
    
    @mock_aws
    def test_invalid_form_data(self, lambda_context):
        """Test handler rejects invalid form data."""
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({
                'name': 'John',
                'email': 'invalid-email',
                'message': 'Test message that is long enough'
            })
        }
        
        response = lambda_handler(event, lambda_context)
        assert response['statusCode'] == 400


class TestErrorResponse:
    """Test error response creation."""
    
    def test_create_error_response(self):
        """Test error response format."""
        headers = {'Access-Control-Allow-Origin': '*'}
        response = create_error_response(400, 'Test error', headers)
        
        assert response['statusCode'] == 400
        assert response['headers'] == headers
        
        body = json.loads(response['body'])
        assert body['error'] == 'Test error'
        assert body['statusCode'] == 400


class TestIntegration:
    """Integration tests for complete workflow."""
    
    @mock_aws
    def test_end_to_end_submission(self, lambda_event, lambda_context):
        """Test complete submission workflow."""
        # Setup AWS resources
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='test-contact-table',
            KeySchema=[{'AttributeName': 'submissionId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'submissionId', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        ses = boto3.client('ses', region_name='us-east-1')
        ses.verify_email_identity(EmailAddress='test@example.com')
        
        # Submit form
        response = lambda_handler(lambda_event, lambda_context)
        assert response['statusCode'] == 200
        
        # Verify DynamoDB storage
        body = json.loads(response['body'])
        submission_id = body['submissionId']
        
        item = table.get_item(Key={'submissionId': submission_id})
        assert 'Item' in item
        assert item['Item']['name'] == 'John Doe'
        assert item['Item']['email'] == 'john.doe@example.com'
        assert item['Item']['status'] == 'received'
