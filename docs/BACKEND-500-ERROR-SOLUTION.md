# Backend 500 Error - Solution Guide

## Problem

Dev backend API returns HTTP 500 error when tested:
```
❌ API test failed - HTTP 500
Response: {"error": "Internal server error. Please try again later.", "statusCode": 500}
```

## Root Cause (Most Likely)

**SES Email Not Verified in Dev Account**

The Lambda function tries to send emails via Amazon SES, but the email address `christophercorbin24@gmail.com` is likely not verified in the dev account (934862608865).

When SES tries to send an email from an unverified address, it throws an error, which the Lambda catches and returns as a 500 error.

## Solution

### Option 1: Verify Email in Dev Account (Recommended)

1. **Log into AWS Dev Account** (934862608865)

2. **Navigate to SES Console**
   - Go to Amazon SES service
   - Region: us-east-1

3. **Verify Email Address**
   ```bash
   aws ses verify-email-identity \
     --email-address christophercorbin24@gmail.com \
     --region us-east-1
   ```

4. **Check Your Email**
   - You'll receive a verification email from AWS
   - Click the verification link

5. **Confirm Verification**
   ```bash
   aws ses list-verified-email-addresses --region us-east-1
   ```

6. **Re-test the API**
   - Push a change to trigger the workflow, or
   - Manually test the API endpoint

### Option 2: Use SES Sandbox Mode for Testing

If you don't want to verify the email, you can:

1. Add test email addresses to SES sandbox
2. Only send emails to verified addresses during testing
3. Request production access when ready

### Option 3: Mock SES for Dev Environment

Update the Lambda to skip SES in dev:

```python
# In contact_handler.py
if os.environ.get("ENVIRONMENT") == "dev":
    print(f"DEV MODE: Would send email to {CONTACT_EMAIL}")
    print(f"From: {email}, Name: {name}")
    print(f"Message: {message}")
else:
    send_email_notification(name, email, message, submission_id)
```

## Verification Steps

After implementing the solution:

1. **Check SES Status**
   ```bash
   aws ses get-identity-verification-attributes \
     --identities christophercorbin24@gmail.com \
     --region us-east-1
   ```

2. **Test API Manually**
   ```bash
   curl -X POST https://350n35sme0.execute-api.us-east-1.amazonaws.com/prod/contact \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "email": "test@example.com",
       "message": "Testing after SES verification"
     }'
   ```

3. **Check CloudWatch Logs**
   - Go to CloudWatch Logs in dev account
   - Log group: `/aws/lambda/christopher-corbin-portfolio-backend-dev-contact-form`
   - Look for recent invocations

4. **Expected Success Response**
   ```json
   {
     "message": "Thank you for your message! I will get back to you soon.",
     "submissionId": "uuid-here"
   }
   ```

## Other Possible Causes

If SES verification doesn't fix it, check:

### 1. DynamoDB Permissions
```bash
# Check if table exists
aws dynamodb describe-table \
  --table-name christopher-corbin-portfolio-backend-dev-submissions \
  --region us-east-1
```

### 2. Lambda Execution Role
```bash
# Get Lambda configuration
aws lambda get-function-configuration \
  --function-name christopher-corbin-portfolio-backend-dev-contact-form \
  --region us-east-1
```

### 3. Environment Variables
Check that Lambda has:
- `CONTACT_EMAIL`: christophercorbin24@gmail.com
- `DYNAMODB_TABLE`: christopher-corbin-portfolio-backend-dev-submissions
- `CORS_ORIGIN`: *

### 4. CloudWatch Logs
Look for actual error messages:
```bash
aws logs tail /aws/lambda/christopher-corbin-portfolio-backend-dev-contact-form \
  --since 1h \
  --region us-east-1
```

## Prevention

To prevent this in the future:

1. **Add SES Verification Check to Workflow**
   ```yaml
   - name: Verify SES email
     run: |
       STATUS=$(aws ses get-identity-verification-attributes \
         --identities ${{ secrets.CONTACT_EMAIL }} \
         --region us-east-1 \
         --query 'VerificationAttributes.*.VerificationStatus' \
         --output text)
       
       if [ "$STATUS" != "Success" ]; then
         echo "⚠️  Warning: SES email not verified"
         echo "Run: aws ses verify-email-identity --email-address ${{ secrets.CONTACT_EMAIL }}"
       fi
   ```

2. **Add Better Error Logging**
   Update Lambda to log more details:
   ```python
   except Exception as e:
       print(f"Error type: {type(e).__name__}")
       print(f"Error details: {str(e)}")
       import traceback
       traceback.print_exc()
   ```

3. **Add Health Check Endpoint**
   Create a `/health` endpoint that checks:
   - DynamoDB table accessible
   - SES email verified
   - Environment variables set

## Current Status

- ✅ Backend deployed to dev account
- ✅ API Gateway endpoint created
- ✅ Lambda function deployed
- ✅ DynamoDB table created
- ❌ SES email verification needed
- ⏳ API returning 500 errors

## Next Action

**Verify the email address in SES for the dev account (934862608865)**

This is the most likely fix and takes less than 2 minutes.
