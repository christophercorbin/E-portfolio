# Multi-Account AWS Implementation Guide

**Project**: Christopher Corbin Portfolio  
**Date**: February 12, 2026  
**Status**: Implementation Ready

---

## Overview

This guide provides step-by-step instructions for implementing and maintaining the multi-account AWS setup for the portfolio project.

---

## Prerequisites

Before implementing the multi-account setup, ensure you have:

- [ ] AWS Organization created with management account (438465156498)
- [ ] Development account (934862608865) created and added to organization
- [ ] Production account (590716168923) created and added to organization
- [ ] AWS CLI installed and configured
- [ ] GitHub repository access with admin permissions
- [ ] Understanding of OIDC authentication

---

## Phase 1: AWS Account Setup

### Step 1: Configure OIDC Provider in Each Account

Run these commands for BOTH dev (934862608865) and prod (590716168923) accounts:

```bash
# Switch to target account
aws sts get-caller-identity

# Create OIDC provider for GitHub Actions
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

# Verify creation
aws iam list-open-id-connect-providers
```

### Step 2: Create IAM Roles

#### Development Account (934862608865)

```bash
# Create trust policy file
cat > github-oidc-trust-policy-dev.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::934862608865:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:christophercorbin/E-portfolio:*"
        }
      }
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name GitHubActionsDeployRole \
  --assume-role-policy-document file://github-oidc-trust-policy-dev.json \
  --description "Role for GitHub Actions to deploy to dev environment"

# Attach the policy (use the dev-account-iam-policy.json file)
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://aws-config/dev-account-iam-policy.json
```

#### Production Account (590716168923)

```bash
# Create trust policy file
cat > github-oidc-trust-policy-prod.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::590716168923:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:christophercorbin/E-portfolio:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name GitHubActionsDeployRole \
  --assume-role-policy-document file://github-oidc-trust-policy-prod.json \
  --description "Role for GitHub Actions to deploy to production environment"

# Attach the policy (use the prod-account-iam-policy.json file)
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://aws-config/prod-account-iam-policy.json
```

### Step 3: Configure S3 Buckets

#### Production S3 Bucket (in account 590716168923)

```bash
# Apply the cross-account CloudFront policy
aws s3api put-bucket-policy \
  --bucket christopher-corbin-portfolio-20251005195625 \
  --policy file://aws-config/enhanced-s3-policy.json
```

#### Development S3 Bucket (in account 934862608865)

```bash
# Enable website hosting
aws s3 website s3://christopher-corbin-portfolio-dev-20251006/ \
  --index-document index.html \
  --error-document index.html

# Set public access (dev only)
aws s3api put-public-access-block \
  --bucket christopher-corbin-portfolio-dev-20251006 \
  --public-access-block-configuration \
    "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

---

## Phase 2: GitHub Configuration

### Step 1: Configure GitHub Environments

1. Go to: `https://github.com/christophercorbin/E-portfolio/settings/environments`

2. Create "dev" environment:
   - Name: `dev`
   - No protection rules (auto-deploy)
   - No required reviewers

3. Create "production" environment:
   - Name: `production`
   - Enable "Required reviewers" (add yourself)
   - Enable "Wait timer" (optional, e.g., 5 minutes)

### Step 2: Configure GitHub Secrets

Go to: `https://github.com/christophercorbin/E-portfolio/settings/secrets/actions`

**Required Secrets:**
- `CONTACT_EMAIL`: christophercorbin24@gmail.com
- `CLOUDFRONT_DOMAIN`: christophercorbin.cloud (optional)

**Remove Old Secrets (if they exist):**
- ❌ `AWS_ACCESS_KEY_ID`
- ❌ `AWS_SECRET_ACCESS_KEY`

### Step 3: Verify Workflow Files

All workflow files should already be configured correctly. Verify:

- ✅ `.github/workflows/deploy-frontend-dev.yml` → Dev account (934862608865)
- ✅ `.github/workflows/deploy-backend-dev.yml` → Dev account (934862608865)
- ✅ `.github/workflows/deploy-frontend-prod.yml` → Prod account (590716168923)
- ✅ `.github/workflows/deploy-backend-prod.yml` → Prod account (590716168923)

---

## Phase 3: CloudFront Cross-Account Access

### Option A: Add Cross-Account Permission to Production Role (Recommended)

The production IAM policy already includes:

```json
{
  "Sid": "AllowCrossAccountCloudFrontInvalidation",
  "Effect": "Allow",
  "Action": [
    "cloudfront:CreateInvalidation",
    "cloudfront:GetInvalidation",
    "cloudfront:ListInvalidations"
  ],
  "Resource": "arn:aws:cloudfront::438465156498:distribution/E34Q2E7TZIYZAB"
}
```

**Verify this works by testing a deployment to production.**

### Option B: Create Separate Management Account Role (Alternative)

If Option A doesn't work due to cross-account restrictions:

1. Create a role in Management account (438465156498)
2. Allow Production account to assume it
3. Add separate workflow step to assume management role for CloudFront

---

## Phase 4: Testing & Validation

### Test Development Deployment

```bash
# Switch to develop branch
git checkout develop

# Make a small change
echo "# Multi-account test" >> README.md
git add README.md
git commit -m "test: Verify dev multi-account deployment"
git push origin develop

# Watch the workflow
# https://github.com/christophercorbin/E-portfolio/actions
```

**Expected Results:**
- ✅ Workflow authenticates to dev account (934862608865)
- ✅ Deploys to dev S3 bucket
- ✅ No CloudFront invalidation (dev doesn't use CloudFront)
- ✅ API Gateway URL returned

### Test Production Deployment

```bash
# Switch to main branch
git checkout main

# Merge from develop
git merge develop
git push origin main

# Watch the workflow (requires approval if environment protection enabled)
# https://github.com/christophercorbin/E-portfolio/actions
```

**Expected Results:**
- ✅ Workflow authenticates to prod account (590716168923)
- ✅ Deploys to prod S3 bucket
- ✅ CloudFront invalidation succeeds
- ✅ Website accessible at https://christophercorbin.cloud

---

## Phase 5: Monitoring & Maintenance

### Enable CloudTrail Logging

In EACH account (dev, prod, management):

```bash
# Create CloudTrail trail
aws cloudtrail create-trail \
  --name portfolio-audit-trail \
  --s3-bucket-name portfolio-cloudtrail-logs-$(aws sts get-caller-identity --query Account --output text)

# Start logging
aws cloudtrail start-logging \
  --name portfolio-audit-trail
```

### Set Up Cost Alerts

In the Management account (consolidated billing):

```bash
# Create SNS topic for alerts
aws sns create-topic --name portfolio-cost-alerts

# Subscribe your email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:438465156498:portfolio-cost-alerts \
  --protocol email \
  --notification-endpoint christophercorbin24@gmail.com

# Create budget alert
aws budgets create-budget \
  --account-id 438465156498 \
  --budget file://budget-config.json
```

### Regular Maintenance Tasks

**Weekly:**
- [ ] Review CloudWatch logs for errors
- [ ] Check deployment success rates
- [ ] Monitor API Gateway metrics

**Monthly:**
- [ ] Review AWS costs per account
- [ ] Clean up old dev resources
- [ ] Update dependencies

**Quarterly:**
- [ ] Review and update IAM policies
- [ ] Audit CloudTrail logs
- [ ] Update this documentation
- [ ] Review security best practices

---

## Troubleshooting

### Issue: OIDC Authentication Fails

**Error**: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

**Solution:**
1. Verify OIDC provider exists in target account
2. Check role trust policy allows your repository
3. Verify role ARN in workflow file matches account
4. Check GitHub Actions has `id-token: write` permission

```bash
# Verify OIDC provider
aws iam list-open-id-connect-providers

# Check role trust policy
aws iam get-role --role-name GitHubActionsDeployRole
```

### Issue: CloudFormation Stack Not Found

**Error**: "Stack does not exist"

**Solution:**
1. Verify you're in the correct AWS account
2. Check stack name matches environment (dev vs prod)
3. Confirm region is us-east-1

```bash
# List all stacks
aws cloudformation list-stacks --region us-east-1

# Check current account
aws sts get-caller-identity
```

### Issue: S3 Access Denied

**Error**: "Access Denied" when syncing to S3

**Solution:**
1. Verify bucket exists in target account
2. Check IAM policy includes s3:PutObject permission
3. Verify bucket name matches environment

```bash
# List buckets in current account
aws s3 ls

# Check bucket policy
aws s3api get-bucket-policy --bucket christopher-corbin-portfolio-dev-20251006
```

### Issue: CloudFront Invalidation Fails

**Error**: "Access Denied" when creating invalidation

**Solution:**
1. Verify CloudFront distribution is in management account
2. Check production role has cross-account CloudFront permissions
3. Consider implementing Option B (separate management role)

```bash
# Check CloudFront distribution
aws cloudfront get-distribution --id E34Q2E7TZIYZAB

# Verify current account
aws sts get-caller-identity
```

---

## Rollback Procedures

### Rollback Development Deployment

```bash
# Delete the dev stack
aws cloudformation delete-stack \
  --stack-name christopher-corbin-portfolio-backend-dev \
  --region us-east-1

# Or use the workflow cleanup option
# Go to Actions → Deploy SAM Backend - Development → Run workflow
# Enable "Cleanup dev resources after testing"
```

### Rollback Production Deployment

```bash
# List stack events to find last successful version
aws cloudformation describe-stack-events \
  --stack-name christopher-corbin-portfolio-backend \
  --region us-east-1

# Update to previous template version
aws cloudformation update-stack \
  --stack-name christopher-corbin-portfolio-backend \
  --template-url <previous-template-url> \
  --region us-east-1
```

---

## Security Checklist

- [x] OIDC authentication configured (no long-lived credentials)
- [x] Least privilege IAM policies per account
- [x] Production resources protected from deletion
- [x] CloudTrail logging enabled
- [x] S3 bucket policies restrict access
- [x] GitHub environment protection for production
- [x] Secrets properly configured in GitHub
- [x] Cross-account access properly scoped
- [ ] Cost alerts configured
- [ ] Regular security audits scheduled

---

## Next Steps

1. **Complete Phase 1-2**: Set up AWS accounts and GitHub configuration
2. **Test Deployments**: Verify both dev and prod deployments work
3. **Enable Monitoring**: Set up CloudTrail and cost alerts
4. **Document Issues**: Update troubleshooting section with any new issues
5. **Schedule Review**: Set calendar reminder for quarterly review

---

## Additional Resources

- [AWS Multi-Account Best Practices](https://aws.amazon.com/organizations/getting-started/best-practices/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

---

**Document Version**: 1.0  
**Last Updated**: February 12, 2026  
**Maintained By**: Christopher Corbin  
**Next Review**: May 12, 2026
