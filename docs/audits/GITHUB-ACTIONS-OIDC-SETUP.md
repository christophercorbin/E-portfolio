# GitHub Actions OIDC Setup - Quick Reference

## ✅ Setup Complete!

Your GitHub Actions workflows now use secure OIDC authentication instead of long-lived access keys.

---

## Quick Start

### 1. Remove Old Secrets

Go to: https://github.com/christophercorbin/E-portfolio/settings/secrets/actions

**Delete these:**
- ❌ `AWS_ACCESS_KEY_ID`
- ❌ `AWS_SECRET_ACCESS_KEY`

**Keep these:**
- ✅ `CONTACT_EMAIL`
- ✅ `CLOUDFRONT_DOMAIN` (if exists)

### 2. Test Deployment

```bash
# Test dev deployment
git checkout develop
echo "# OIDC Test" >> README.md
git add README.md
git commit -m "Test OIDC authentication"
git push origin develop

# Watch: https://github.com/christophercorbin/E-portfolio/actions
```

---

## AWS Accounts & Roles

### Development (934862608865)
- **Role:** `arn:aws:iam::934862608865:role/GitHubActionsDeployRole`
- **Workflows:** deploy-frontend-dev.yml, deploy-backend-dev.yml
- **Branches:** develop, dev-backend-integration

### Production (590716168923)
- **Role:** `arn:aws:iam::590716168923:role/GitHubActionsDeployRole`
- **Workflows:** deploy-frontend-prod.yml, deploy-backend-prod.yml
- **Branches:** main

---

## Workflow Files Updated

✅ `.github/workflows/deploy-frontend-dev.yml`  
✅ `.github/workflows/deploy-backend-dev.yml`  
✅ `.github/workflows/deploy-frontend-prod.yml`  
✅ `.github/workflows/deploy-backend-prod.yml`  
✅ `.github/workflows/test-backend.yml` (if using AWS)  
✅ `.github/workflows/test-frontend.yml` (if using AWS)  

---

## How It Works

```yaml
permissions:
  id-token: write  # Required for OIDC
  contents: read

- name: Configure AWS credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::934862608865:role/GitHubActionsDeployRole
    aws-region: us-east-1
    role-session-name: GitHubActions-DevFrontend
```

**What happens:**
1. GitHub Actions requests a token from GitHub's OIDC provider
2. Token includes repository and branch information
3. AWS STS validates the token against the OIDC provider
4. If valid, AWS assumes the role and returns temporary credentials
5. Credentials expire after the workflow completes

---

## Troubleshooting

### "Not authorized to perform sts:AssumeRoleWithWebIdentity"

Check:
- OIDC provider exists in AWS account
- Role ARN is correct in workflow
- Trust policy allows your repository

### "Access Denied" during deployment

Check:
- Role has required permissions
- No SCPs blocking the action
- Resource policies allow access

### Workflow doesn't trigger

Check:
- Branch name matches trigger
- File paths match trigger patterns
- Workflow file syntax is valid

---

## Security Benefits

✅ No long-lived credentials in GitHub  
✅ Automatic credential rotation  
✅ Least privilege access  
✅ Full audit trail in CloudTrail  
✅ Repository-scoped access  

---

## Need Help?

- Full documentation: `OIDC-MIGRATION-COMPLETE.md`
- Deployment summary: `github-oidc-deployment-summary.md`
- CI/CD guide: `MD/CICD-Setup-Guide.md`

---

**Setup Date:** February 12, 2026  
**Status:** ✅ READY TO USE
