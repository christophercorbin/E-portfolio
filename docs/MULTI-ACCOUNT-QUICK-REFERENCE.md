# Multi-Account Quick Reference Card

**Quick access guide for daily operations**

---

## Account Information

| Account | ID | Purpose | Access |
|---------|-----|---------|--------|
| **Development** | 934862608865 | Dev/Test | Broad permissions |
| **Production** | 590716168923 | Live site | Restricted |
| **Management** | 438465156498 | Org/CloudFront | Admin only |

---

## Branch → Account Mapping

```
develop, dev-backend-integration  →  Dev Account (934862608865)
main, master                      →  Prod Account (590716168923)
```

---

## OIDC Roles

```bash
# Development
arn:aws:iam::934862608865:role/GitHubActionsDeployRole

# Production
arn:aws:iam::590716168923:role/GitHubActionsDeployRole
```

---

## Resource Names

### Development
- Stack: `christopher-corbin-portfolio-backend-dev`
- S3: `christopher-corbin-portfolio-dev-20251006`
- API: `https://cdmwb9tdlj.execute-api.us-east-1.amazonaws.com/prod/contact`

### Production
- Stack: `christopher-corbin-portfolio-backend`
- S3: `christopher-corbin-portfolio-20251005195625`
- API: `https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact`
- CloudFront: `E34Q2E7TZIYZAB` (in account 438465156498)
- Domain: `https://christophercorbin.cloud`

---

## Common Commands

### Check Current Account
```bash
aws sts get-caller-identity
```

### List Stacks
```bash
# Development
aws cloudformation list-stacks --region us-east-1

# Production (switch account first)
aws cloudformation list-stacks --region us-east-1
```

### View Stack Outputs
```bash
# Dev
aws cloudformation describe-stacks \
  --stack-name christopher-corbin-portfolio-backend-dev \
  --region us-east-1 \
  --query 'Stacks[0].Outputs'

# Prod
aws cloudformation describe-stacks \
  --stack-name christopher-corbin-portfolio-backend \
  --region us-east-1 \
  --query 'Stacks[0].Outputs'
```

### Test API Endpoint
```bash
# Dev
curl -X POST https://cdmwb9tdlj.execute-api.us-east-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","message":"Test message"}'

# Prod
curl -X POST https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","message":"Test message"}'
```

### Invalidate CloudFront Cache
```bash
aws cloudfront create-invalidation \
  --distribution-id E34Q2E7TZIYZAB \
  --paths "/*"
```

### Clean Up Dev Resources
```bash
aws cloudformation delete-stack \
  --stack-name christopher-corbin-portfolio-backend-dev \
  --region us-east-1
```

---

## Deployment Workflow

### Deploy to Development
```bash
git checkout develop
# Make changes
git add .
git commit -m "feat: your changes"
git push origin develop
# Auto-deploys to dev account
```

### Deploy to Production
```bash
git checkout main
git merge develop
git push origin main
# Requires approval, deploys to prod account
```

---

## Troubleshooting Quick Checks

### Authentication Issues
```bash
# 1. Check OIDC provider exists
aws iam list-open-id-connect-providers

# 2. Verify role exists
aws iam get-role --role-name GitHubActionsDeployRole

# 3. Check role trust policy
aws iam get-role --role-name GitHubActionsDeployRole \
  --query 'Role.AssumeRolePolicyDocument'
```

### Deployment Failures
```bash
# 1. Check stack status
aws cloudformation describe-stacks \
  --stack-name christopher-corbin-portfolio-backend-dev

# 2. View recent events
aws cloudformation describe-stack-events \
  --stack-name christopher-corbin-portfolio-backend-dev \
  --max-items 10

# 3. Check CloudWatch logs
aws logs tail /aws/lambda/christopher-corbin-portfolio-backend-dev-contact-form
```

### S3 Issues
```bash
# 1. List buckets
aws s3 ls

# 2. Check bucket policy
aws s3api get-bucket-policy \
  --bucket christopher-corbin-portfolio-dev-20251006

# 3. Test bucket access
aws s3 ls s3://christopher-corbin-portfolio-dev-20251006/
```

---

## Important URLs

- **GitHub Actions**: https://github.com/christophercorbin/E-portfolio/actions
- **GitHub Settings**: https://github.com/christophercorbin/E-portfolio/settings
- **Dev Website**: http://christopher-corbin-portfolio-dev-20251006.s3-website-us-east-1.amazonaws.com
- **Prod Website**: https://christophercorbin.cloud
- **CloudFront**: https://d30iyriy15xq9k.cloudfront.net

---

## Emergency Contacts

- **AWS Support**: https://console.aws.amazon.com/support/
- **GitHub Support**: https://support.github.com/
- **Documentation**: See `docs/MULTI-ACCOUNT-IMPLEMENTATION-GUIDE.md`

---

## Policy Files Location

```
aws-config/
├── dev-account-iam-policy.json      # Dev account permissions
├── prod-account-iam-policy.json     # Prod account permissions
├── enhanced-s3-policy.json          # S3 cross-account policy
└── github-actions-*-policy.json     # Legacy policies (reference)
```

---

## Monitoring

### CloudWatch Dashboards
- Dev: https://console.aws.amazon.com/cloudwatch/ (account 934862608865)
- Prod: https://console.aws.amazon.com/cloudwatch/ (account 590716168923)

### Cost Explorer
- Management: https://console.aws.amazon.com/cost-management/ (account 438465156498)

---

**Last Updated**: February 12, 2026  
**Print this page for quick reference!**
