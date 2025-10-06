# Development Workflow Guide

This document outlines the development workflow for the Christopher Corbin Portfolio backend integration.

## Branch Strategy

### Main Branch (`main`)
- **Purpose**: Production-ready code
- **Deployment**: Automatically deploys to production AWS environment
- **Protection**: Protected branch, requires PR approval
- **Stack Name**: `christopher-corbin-portfolio-backend`

### Development Branch (`dev-backend-integration`)
- **Purpose**: Backend integration development and testing
- **Deployment**: Automatically deploys to dev AWS environment
- **Stack Name**: `christopher-corbin-portfolio-backend-dev`
- **Cleanup**: Can be automatically cleaned up after testing

## Workflow Process

### 1. Development Phase
```bash
# Work in development branch
git checkout dev-backend-integration

# Make changes to backend code
# - Update Lambda functions (src/)
# - Modify SAM templates (template.yaml)
# - Update configurations (samconfig*.toml)

# Commit and push changes
git add .
git commit -m "feat: your changes"
git push origin dev-backend-integration
```

**What happens:**
- GitHub Actions automatically deploys to dev environment
- Runs automated API tests
- Creates dev resources with `-dev` suffix
- Available for manual testing

### 2. Testing Phase
```bash
# Test the dev deployment
curl -X POST "https://api-dev-url/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com", 
    "message": "Testing dev environment"
  }'

# Use debug tools
open debug-form.html
```

**Manual verification:**
- Test contact form functionality
- Verify email notifications work
- Check CORS configuration
- Review CloudWatch logs

### 3. Production Deployment
```bash
# Create PR to main branch
gh pr create --base main --head dev-backend-integration \
  --title "Backend Integration: Contact Form API" \
  --body "Ready for production deployment"

# After PR approval and merge
git checkout main
git pull origin main
```

**What happens:**
- PR triggers dev environment deployment for final testing
- GitHub Actions comments on PR with test results
- After merge to main: production deployment begins
- Production resources are created/updated
- Automated testing verifies production deployment

### 4. Cleanup (Optional)
```bash
# Manual cleanup of dev resources
gh workflow run "Deploy SAM Backend - Development" \
  --field environment=dev \
  --field cleanup=true
```

## Environment Configurations

### Development Environment
- **Stack**: `christopher-corbin-portfolio-backend-dev`
- **API URL**: `https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/contact`
- **DynamoDB**: `christopher-corbin-portfolio-backend-dev-submissions`
- **Lambda**: `christopher-corbin-portfolio-backend-dev-contact-form`
- **CORS**: `*` (permissive for testing)

### Production Environment  
- **Stack**: `christopher-corbin-portfolio-backend`
- **API URL**: `https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/contact`
- **DynamoDB**: `christopher-corbin-portfolio-backend-submissions`
- **Lambda**: `christopher-corbin-portfolio-backend-contact-form`
- **CORS**: Specific domain or `*`

## GitHub Actions Workflows

### Development Workflow (`.github/workflows/deploy-sam.yml`)
**Triggers:**
- Push to `dev-backend-integration`
- Pull request to `main`
- Manual dispatch

**Features:**
- Environment-specific deployment
- Automated API testing
- PR comments with deployment info
- Optional resource cleanup
- Test results and API URLs

### Production Workflow (`.github/workflows/deploy-prod.yml`)
**Triggers:**
- Push to `main` (after merge)
- Manual dispatch

**Features:**
- Production deployment
- Comprehensive testing
- Deployment summaries
- Frontend config updates
- Success notifications

## Commands Reference

### Local Development
```bash
# Install SAM CLI
brew tap aws/tap && brew install aws-sam-cli

# Build and test locally
sam build
sam local start-api --port 3001

# Test local endpoint
curl -X POST "http://localhost:3001/contact" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","message":"Local test"}'
```

### Deploy to Dev Environment
```bash
# Deploy to dev with specific config
sam build
sam deploy --config-env dev --guided

# Or use GitHub Actions
gh workflow run "Deploy SAM Backend - Development" \
  --field environment=dev
```

### Deploy to Production
```bash
# Deploy to production (main branch only)
sam build  
sam deploy --no-confirm-changeset --stack-name christopher-corbin-portfolio-backend

# Or merge to main branch for automatic deployment
```

### Cleanup Development Resources
```bash
# Delete dev stack
aws cloudformation delete-stack \
  --stack-name christopher-corbin-portfolio-backend-dev \
  --region us-east-1

# Or use GitHub Actions cleanup
gh workflow run "Deploy SAM Backend - Development" \
  --field environment=dev \
  --field cleanup=true
```

## Best Practices

### Development
1. **Always test in dev first** before creating PR
2. **Use descriptive commit messages** with conventional commits
3. **Test API endpoints manually** after deployment
4. **Check CloudWatch logs** for any errors
5. **Verify email notifications** are working

### Pull Requests
1. **Include test results** in PR description
2. **Wait for automated tests** to pass
3. **Test the dev deployment** before requesting review
4. **Clean up dev resources** after merge (optional)

### Production
1. **Monitor deployment progress** in GitHub Actions
2. **Test production API** after deployment
3. **Verify contact form** on live portfolio
4. **Check email notifications** work correctly

## Troubleshooting

### Common Issues
1. **CORS errors**: Check CorsOrigin parameter
2. **Email failures**: Verify SES email verification
3. **API timeouts**: Check Lambda function logs
4. **Permission errors**: Verify IAM policies

### Debug Tools
- **debug-form.html**: Comprehensive form testing
- **CloudWatch Logs**: Lambda execution logs
- **API Gateway Logs**: Request/response logging
- **DynamoDB Console**: View stored submissions

### Support Commands
```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name christopher-corbin-portfolio-backend-dev

# View Lambda logs
aws logs describe-log-groups \
  --log-group-name-prefix "/aws/lambda/christopher-corbin"

# Test API health
curl -X OPTIONS "https://your-api-url/contact"
```

## Security Notes

- Dev and prod environments are completely isolated
- IAM policies follow least privilege principles
- All secrets are managed through GitHub Secrets
- CORS is configured appropriately for each environment
- Data in dev environment can be safely deleted

---

This workflow ensures safe development and deployment of backend features while maintaining production stability.