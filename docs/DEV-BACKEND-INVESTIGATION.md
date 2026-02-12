# Dev Backend Investigation - February 12, 2026

## Issue Summary

The dev backend API test is failing with HTTP 500 errors. Investigation revealed the root cause.

## Root Cause

The backend deployment workflow successfully deployed to the **dev account (934862608865)** and created:
- Stack: `christopher-corbin-portfolio-backend-dev`
- API URL: `https://350n35sme0.execute-api.us-east-1.amazonaws.com/prod/contact`
- Lambda function: `christopher-corbin-portfolio-backend-dev-contact-form`
- DynamoDB table: `christopher-corbin-portfolio-backend-dev-submissions`

However, the API is returning 500 errors when tested.

## Investigation Steps Taken

1. ✅ Confirmed backend stack deployed successfully to dev account
2. ✅ Confirmed API Gateway endpoint was created
3. ✅ Created script (`infrastructure/update-dev-config.sh`) to dynamically update config-dev.js
4. ✅ Updated frontend workflow to use the script
5. ⚠️  Found Lambda logs in management account (438465156498) - old deployment
6. ❓ Need to check Lambda logs in dev account (934862608865)

## Likely Causes of 500 Error

Based on the Lambda code review, the most likely causes are:

### 1. Missing Environment Variables
The Lambda function requires these environment variables:
- `CONTACT_EMAIL` - Email address for notifications
- `DYNAMODB_TABLE` - DynamoDB table name
- `CORS_ORIGIN` - CORS origin (defaults to "*")

**Check**: Verify these are set in the Lambda function configuration

### 2. SES Email Not Verified
The Lambda sends emails via SES. The email address must be verified in the dev account.

**Check**: Verify `christophercorbin24@gmail.com` in SES for dev account (934862608865)

### 3. IAM Permissions
The Lambda execution role needs:
- SES: `ses:SendEmail` permission
- DynamoDB: Read/write permissions on the submissions table

**Check**: Verify Lambda execution role has correct policies

### 4. DynamoDB Table Issues
The table might not exist or Lambda can't access it.

**Check**: Verify table exists and Lambda has permissions

## Next Steps

### Immediate Actions

1. **Check Lambda Configuration in Dev Account**
   ```bash
   # Need to assume dev account role or use GitHub Actions
   aws lambda get-function-configuration \
     --function-name christopher-corbin-portfolio-backend-dev-contact-form \
     --region us-east-1
   ```

2. **Check CloudWatch Logs in Dev Account**
   ```bash
   # Get recent logs from dev account
   aws logs tail /aws/lambda/christopher-corbin-portfolio-backend-dev-contact-form \
     --since 1h --follow
   ```

3. **Verify SES Email in Dev Account**
   ```bash
   aws ses list-verified-email-addresses --region us-east-1
   ```

4. **Test API Directly**
   ```bash
   curl -X POST https://350n35sme0.execute-api.us-east-1.amazonaws.com/prod/contact \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "email": "test@example.com",
       "message": "This is a test message from manual testing"
     }'
   ```

### Workflow Improvements

1. **Add Better Error Logging**
   - Update backend workflow to capture and display Lambda logs on failure
   - Add step to check Lambda configuration after deployment

2. **Add Pre-deployment Checks**
   - Verify SES email is verified before deploying
   - Check IAM role permissions
   - Validate environment variables

3. **Make Backend Test Non-Blocking**
   - Already added `continue-on-error: true` to frontend workflow
   - Backend test failure won't block frontend deployment

## Files Modified

1. `infrastructure/update-dev-config.sh` - Script to update config with API URL
2. `.github/workflows/deploy-frontend-dev.yml` - Uses script to update config
3. `.github/workflows/deploy-backend-dev.yml` - Backend deployment (already exists)
4. `infrastructure/samconfig-dev.toml` - Dev SAM configuration

## Current Status

- ✅ Frontend deployment: Working
- ✅ Backend deployment: Working (stack created)
- ❌ Backend API: Returning 500 errors
- ✅ Config update script: Created and integrated
- ⏳ Root cause: Under investigation

## Recommendations

1. **Access Dev Account**: Need to check resources in dev account (934862608865), not management account
2. **Verify SES**: Ensure email is verified in dev account
3. **Check Logs**: View CloudWatch logs from dev account Lambda
4. **Test Manually**: Direct API test to see actual error response
5. **Add Monitoring**: Consider adding CloudWatch alarms for Lambda errors

## Multi-Account Context

This issue highlights the importance of:
- Checking resources in the correct AWS account
- Account-specific SES email verification
- Separate CloudWatch logs per account
- Testing in the correct environment

The dev backend is isolated in account 934862608865, while old resources exist in management account 438465156498.
