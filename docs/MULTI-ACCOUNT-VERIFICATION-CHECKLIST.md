# Multi-Account Setup Verification Checklist

**Use this checklist to verify your multi-account setup is working correctly**

---

## Pre-Implementation Checklist

### AWS Organization Setup
- [ ] AWS Organization created in management account (438465156498)
- [ ] Development account (934862608865) added to organization
- [ ] Production account (590716168923) added to organization
- [ ] Consolidated billing enabled
- [ ] All accounts accessible via AWS Console

### GitHub Repository Setup
- [ ] Repository exists: christophercorbin/E-portfolio
- [ ] Admin access to repository settings
- [ ] GitHub Actions enabled
- [ ] Workflow files present in `.github/workflows/`

---

## Phase 1: OIDC Provider Setup

### Development Account (934862608865)
```bash
# Switch to dev account
aws sts get-caller-identity
# Should show Account: 934862608865
```

- [ ] OIDC provider created for token.actions.githubusercontent.com
- [ ] Provider thumbprint: 6938fd4d98bab03faadb97b34396831e3780aea1
- [ ] Provider visible in IAM console

**Verification Command:**
```bash
aws iam list-open-id-connect-providers
```

### Production Account (590716168923)
```bash
# Switch to prod account
aws sts get-caller-identity
# Should show Account: 590716168923
```

- [ ] OIDC provider created for token.actions.githubusercontent.com
- [ ] Provider thumbprint: 6938fd4d98bab03faadb97b34396831e3780aea1
- [ ] Provider visible in IAM console

**Verification Command:**
```bash
aws iam list-open-id-connect-providers
```

---

## Phase 2: IAM Role Setup

### Development Account Role
- [x] Role name: GitHubActionsDeployRole
- [x] Trust policy allows GitHub OIDC provider
- [x] Trust policy includes repository: christophercorbin/E-portfolio
- [x] Policy attached: dev-account-iam-policy.json
- [x] Role ARN: arn:aws:iam::934862608865:role/GitHubActionsDeployRole
- [x] Account-specific resource ARNs configured

**Verification Commands:**
```bash
# Check role exists
aws iam get-role --role-name GitHubActionsDeployRole

# Check trust policy
aws iam get-role --role-name GitHubActionsDeployRole \
  --query 'Role.AssumeRolePolicyDocument' --output json

# List attached policies
aws iam list-role-policies --role-name GitHubActionsDeployRole
```

### Production Account Role
- [x] Role name: GitHubActionsDeployRole
- [x] Trust policy allows GitHub OIDC provider
- [x] Trust policy restricts to main branch
- [x] Policy attached: prod-account-iam-policy.json
- [x] Role ARN: arn:aws:iam::590716168923:role/GitHubActionsDeployRole
- [x] Account-specific resource ARNs configured
- [x] Cross-account CloudFront permissions included

**Verification Commands:**
```bash
# Check role exists
aws iam get-role --role-name GitHubActionsDeployRole

# Check trust policy
aws iam get-role --role-name GitHubActionsDeployRole \
  --query 'Role.AssumeRolePolicyDocument' --output json

# List attached policies
aws iam list-role-policies --role-name GitHubActionsDeployRole
```

---

## Phase 3: S3 Bucket Configuration

### Development S3 Bucket
- [ ] Bucket exists: christopher-corbin-portfolio-dev-20251006
- [ ] Bucket in account: 934862608865
- [ ] Website hosting enabled
- [ ] Public access configured (dev only)
- [ ] Bucket accessible via HTTP

**Verification Commands:**
```bash
# List buckets
aws s3 ls

# Check bucket location
aws s3api get-bucket-location \
  --bucket christopher-corbin-portfolio-dev-20251006

# Test website endpoint
curl -I http://christopher-corbin-portfolio-dev-20251006.s3-website-us-east-1.amazonaws.com
```

### Production S3 Bucket
- [ ] Bucket exists: christopher-corbin-portfolio-20251005195625
- [ ] Bucket in account: 590716168923
- [ ] Bucket policy allows CloudFront access
- [ ] Cross-account policy configured
- [ ] Public access blocked (CloudFront only)

**Verification Commands:**
```bash
# List buckets
aws s3 ls

# Check bucket policy
aws s3api get-bucket-policy \
  --bucket christopher-corbin-portfolio-20251005195625

# Verify public access block
aws s3api get-public-access-block \
  --bucket christopher-corbin-portfolio-20251005195625
```

---

## Phase 4: GitHub Configuration

### GitHub Secrets
- [ ] Navigate to: Settings → Secrets and variables → Actions
- [ ] CONTACT_EMAIL secret exists
- [ ] CLOUDFRONT_DOMAIN secret exists (optional)
- [ ] No AWS_ACCESS_KEY_ID secret (removed)
- [ ] No AWS_SECRET_ACCESS_KEY secret (removed)

### GitHub Environments
- [ ] "dev" environment created
- [ ] "production" environment created
- [ ] Production environment has required reviewers
- [ ] Environment protection rules configured

**Verification:**
Visit: https://github.com/christophercorbin/E-portfolio/settings/environments

---

## Phase 5: Workflow Verification

### Development Workflows

#### Frontend Dev Workflow
- [ ] File: `.github/workflows/deploy-frontend-dev.yml`
- [ ] Uses role: arn:aws:iam::934862608865:role/GitHubActionsDeployRole
- [ ] Triggers on: develop, dev-backend-integration branches
- [ ] Deploys to: christopher-corbin-portfolio-dev-20251006
- [ ] No CloudFront invalidation

#### Backend Dev Workflow
- [ ] File: `.github/workflows/deploy-backend-dev.yml`
- [ ] Uses role: arn:aws:iam::934862608865:role/GitHubActionsDeployRole
- [ ] Triggers on: develop, dev-backend-integration branches
- [ ] Stack name: christopher-corbin-portfolio-backend-dev
- [ ] Uses: samconfig-dev.toml

### Production Workflows

#### Frontend Prod Workflow
- [ ] File: `.github/workflows/deploy-frontend-prod.yml`
- [ ] Uses role: arn:aws:iam::590716168923:role/GitHubActionsDeployRole
- [ ] Triggers on: main, master branches
- [ ] Deploys to: christopher-corbin-portfolio-20251005195625
- [ ] Includes CloudFront invalidation

#### Backend Prod Workflow
- [ ] File: `.github/workflows/deploy-backend-prod.yml`
- [ ] Uses role: arn:aws:iam::590716168923:role/GitHubActionsDeployRole
- [ ] Triggers on: main branch
- [ ] Stack name: christopher-corbin-portfolio-backend
- [ ] Uses: samconfig.toml

---

## Phase 6: Deployment Testing

### Test Development Deployment

```bash
# Create test branch
git checkout develop
echo "# Multi-account test $(date)" >> README.md
git add README.md
git commit -m "test: Verify dev deployment"
git push origin develop
```

**Expected Results:**
- [ ] Workflow triggers automatically
- [ ] Authenticates to dev account (934862608865)
- [ ] Deploys to dev S3 bucket
- [ ] No errors in workflow logs
- [ ] Dev website accessible

**Verification:**
- [ ] Check: https://github.com/christophercorbin/E-portfolio/actions
- [ ] Visit: http://christopher-corbin-portfolio-dev-20251006.s3-website-us-east-1.amazonaws.com

### Test Production Deployment

```bash
# Merge to main
git checkout main
git merge develop
git push origin main
```

**Expected Results:**
- [ ] Workflow triggers automatically
- [ ] Requires approval (if environment protection enabled)
- [ ] Authenticates to prod account (590716168923)
- [ ] Deploys to prod S3 bucket
- [ ] CloudFront invalidation succeeds
- [ ] No errors in workflow logs
- [ ] Production website updated

**Verification:**
- [ ] Check: https://github.com/christophercorbin/E-portfolio/actions
- [ ] Visit: https://christophercorbin.cloud
- [ ] Verify changes are live

---

## Phase 7: Backend Testing

### Test Development Backend

```bash
# Test dev API endpoint
curl -X POST https://cdmwb9tdlj.execute-api.us-east-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "Testing dev backend deployment"
  }'
```

**Expected Results:**
- [ ] HTTP 200 response
- [ ] Success message returned
- [ ] Email received (if SES configured)
- [ ] DynamoDB entry created

**Verification:**
```bash
# Check Lambda function exists
aws lambda get-function \
  --function-name christopher-corbin-portfolio-backend-dev-contact-form

# Check DynamoDB table
aws dynamodb describe-table \
  --table-name christopher-corbin-portfolio-backend-dev-submissions
```

### Test Production Backend

```bash
# Test prod API endpoint
curl -X POST https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "Testing prod backend deployment"
  }'
```

**Expected Results:**
- [ ] HTTP 200 response
- [ ] Success message returned
- [ ] Email received
- [ ] DynamoDB entry created

**Verification:**
```bash
# Check Lambda function exists
aws lambda get-function \
  --function-name christopher-corbin-portfolio-backend-contact-form

# Check DynamoDB table
aws dynamodb describe-table \
  --table-name christopher-corbin-portfolio-backend-submissions
```

---

## Phase 8: Cross-Account Verification

### CloudFront Access to Production S3
- [ ] CloudFront distribution: E34Q2E7TZIYZAB
- [ ] Distribution in management account: 438465156498
- [ ] Origin points to prod S3: christopher-corbin-portfolio-20251005195625
- [ ] S3 bucket policy allows CloudFront service principal
- [ ] Website accessible via CloudFront

**Verification:**
```bash
# Check CloudFront distribution (from management account)
aws cloudfront get-distribution --id E34Q2E7TZIYZAB

# Test CloudFront URL
curl -I https://d30iyriy15xq9k.cloudfront.net

# Test custom domain
curl -I https://christophercorbin.cloud
```

### CloudFront Invalidation from Production Account
- [x] Production workflow includes invalidation step
- [x] Cross-account CloudFront permissions configured
- [x] Production role can invalidate CloudFront in management account
- [ ] Invalidation succeeds without errors (test required)
- [ ] Cache clears within 1-3 minutes (test required)

**Verification:**
```bash
# Create test invalidation (from prod account)
aws cloudfront create-invalidation \
  --distribution-id E34Q2E7TZIYZAB \
  --paths "/*"

# Check invalidation status
aws cloudfront list-invalidations \
  --distribution-id E34Q2E7TZIYZAB
```

---

## Phase 9: Monitoring & Logging

### CloudTrail Setup
- [ ] CloudTrail enabled in dev account
- [ ] CloudTrail enabled in prod account
- [ ] CloudTrail enabled in management account
- [ ] Logs being written to S3
- [ ] Events visible in CloudTrail console

**Verification:**
```bash
# Check CloudTrail status
aws cloudtrail get-trail-status --name portfolio-audit-trail

# List recent events
aws cloudtrail lookup-events --max-results 10
```

### CloudWatch Logs
- [ ] Lambda logs visible in CloudWatch (dev)
- [ ] Lambda logs visible in CloudWatch (prod)
- [ ] API Gateway logs enabled
- [ ] No errors in recent logs

**Verification:**
```bash
# List log groups
aws logs describe-log-groups

# Tail Lambda logs
aws logs tail /aws/lambda/christopher-corbin-portfolio-backend-dev-contact-form
```

---

## Phase 10: Cost Management

### Billing Setup
- [ ] Consolidated billing active
- [ ] Cost allocation tags configured
- [ ] Cost Explorer enabled
- [ ] Budget alerts configured
- [ ] Costs tracked per account

**Verification:**
- Visit AWS Cost Management console in management account
- Check cost breakdown by linked account

---

## Final Verification

### Documentation
- [x] All documentation files created
- [x] Steering document active in .kiro/steering/
- [x] README updated with multi-account info
- [x] Implementation guide complete
- [x] Quick reference available
- [x] IAM policies documented and applied

### Security
- [x] No AWS credentials in GitHub secrets
- [x] OIDC authentication working
- [x] Least privilege policies applied
- [x] Account-specific IAM policies configured
- [x] Production resources protected from deletion
- [x] Cross-account CloudFront access configured
- [ ] Audit logging enabled (CloudTrail setup required)

### Functionality
- [ ] Dev deployments working
- [ ] Prod deployments working
- [ ] Backend APIs responding
- [ ] CloudFront serving content
- [ ] Custom domain working
- [ ] Email notifications working

---

## Troubleshooting Failed Checks

### If OIDC Authentication Fails
1. Verify OIDC provider exists: `aws iam list-open-id-connect-providers`
2. Check role trust policy includes correct repository
3. Verify workflow has `id-token: write` permission
4. Check role ARN matches account

### If Deployment Fails
1. Check workflow logs in GitHub Actions
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Check IAM policy permissions
4. Verify resource names match environment

### If CloudFront Invalidation Fails
1. Verify distribution ID is correct
2. Check cross-account permissions
3. Try manual invalidation from AWS Console
4. Review CloudFront access logs

---

## Success Criteria

✅ **All checks passed** = Multi-account setup is fully operational

⚠️ **Some checks failed** = Review troubleshooting section and implementation guide

❌ **Many checks failed** = Start from Phase 1 and work through systematically

---

## Next Steps After Verification

1. **Document any issues** encountered and solutions
2. **Update steering document** with lessons learned
3. **Set up monitoring alerts** for production
4. **Schedule quarterly review** of setup
5. **Share success** with team/portfolio viewers!

---

**Checklist Version**: 1.0  
**Last Updated**: February 12, 2026  
**Estimated Time**: 2-3 hours for complete verification
