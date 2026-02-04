# Testing Guide

This directory contains unit and integration tests for the AWS ePortfolio project.

## Setup

### Python Backend Tests

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run all tests:**
   ```bash
   pytest tests/ -v
   ```

3. **Run tests with coverage:**
   ```bash
   pytest tests/ -v --cov=src --cov-report=html
   ```

4. **View coverage report:**
   ```bash
   open htmlcov/index.html
   ```

### Linting and Formatting

#### Python

```bash
# Check formatting
black --check src/ tests/

# Auto-format code
black src/ tests/

# Run pylint
pylint src/

# Run flake8
flake8 src/ tests/ --max-line-length=120

# Type checking
mypy src/ --ignore-missing-imports
```

#### JavaScript

```bash
# Install dependencies
npm install

# Check formatting
npm run format:check

# Auto-format code
npm run format

# Run ESLint
npm run lint

# Fix linting issues
npm run lint:fix
```

## Test Structure

### Backend Tests (`test_contact_handler.py`)

- **TestValidation**: Tests for form data validation
  - Valid data
  - Missing fields
  - Invalid email formats
  - Length constraints
  - Spam detection

- **TestLambdaHandler**: Tests for Lambda handler function
  - Successful submissions
  - CORS preflight requests
  - Error handling
  - Invalid JSON

- **TestIntegration**: End-to-end integration tests
  - Complete submission workflow
  - DynamoDB storage verification
  - SES email sending

## Continuous Integration

Tests run automatically on GitHub Actions:

- **test-backend.yml**: Runs Python tests and linting
  - Triggers: Push to main/dev branches, PRs
  - Tests on Python 3.9, 3.10, 3.11
  - Generates coverage reports

- **test-frontend.yml**: Runs JavaScript linting and validation
  - Triggers: Push to main/dev branches, PRs
  - ESLint and Prettier checks
  - HTML validation
  - Security scanning

## Writing New Tests

### Python Test Example

```python
def test_new_feature(valid_contact_form):
    """Test description."""
    # Arrange
    data = valid_contact_form.copy()
    data['new_field'] = 'value'
    
    # Act
    result = validate_form_data(data)
    
    # Assert
    assert result['valid'] is True
```

### Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_contact_handler.py -v

# Run a specific test class
pytest tests/test_contact_handler.py::TestValidation -v

# Run a specific test method
pytest tests/test_contact_handler.py::TestValidation::test_valid_form_data -v
```

## Mocking AWS Services

Tests use `moto` library to mock AWS services:

```python
from moto import mock_aws

@mock_aws
def test_with_aws_mocks():
    # AWS services are mocked automatically
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # ... test code
```

## Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- Focus on critical paths: validation, error handling, AWS integrations

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. You're running pytest from the project root
2. The `src/` directory is in your Python path
3. Environment variables are set in test fixtures

### Moto Issues

If AWS mocking fails:
1. Check moto version: `pip show moto`
2. Verify AWS credentials are NOT set (tests use mocks)
3. Ensure region is specified in boto3 calls

## Best Practices

1. ✅ Write tests before fixing bugs
2. ✅ Keep tests independent and isolated
3. ✅ Use descriptive test names
4. ✅ Test edge cases and error conditions
5. ✅ Mock external dependencies (AWS, APIs)
6. ✅ Run tests locally before pushing
7. ✅ Maintain high code coverage (80%+)
