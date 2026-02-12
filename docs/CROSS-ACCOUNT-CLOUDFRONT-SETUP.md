# Cross-Account CloudFront Access Setup

## Overview

This guide sets up automated CloudFront cache invalidation from the production account to the management account using AWS cross-account IAM roles.

### Problem
- CloudFront distribution (E34Q2E7TZIYZAB) is in management account (438465156498)
- GitHub Actions workflow runs in production account (590716168923)
- Production account cannot directly invalidate CloudFront cache

### Solution
- Create a role in management account with CloudFront invalidation permissions
- Allow production account role to assume the management account role
- Update workflow to assume cross-account role before invalidation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions Workflow (Production Branch)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 1. OIDC Authentication
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Production Account (590716168923)                           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ GitHubActionsDeployRole                            │    │
│  │ - Deploy to S3                                     │    │
│  │ - Assume CloudFront role in management account     │    │
│  └────────────────────┬───────────────────────────────┘    │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          │ 2. AssumeRole (with ExternalId)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Management Account (438465156498)                           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ CloudFrontInvalidationRole                         │    │
│  │ - Create CloudFront invalidations                  │    │
│  │ - List/Get invalidation status                     │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│                       │ 3. Invalidate Cache                 │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ CloudFront Distribution (E34Q2E7TZIYZAB)           │    │
│  │ - Origin: S3 bucket in production account          │    │
│  │ - Domain: christophercorbin.cloud                  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- AWS CLI installed and configured
- Access to both management and production AWS accounts
- Admin permissions in both accounts (for initial setup)
- GitHub repository with secrets access

## Setup Steps

### Step 1: Management Account - Create CloudFront Role

Log into the **management account (438465156498)** and run:

```bash
# Create the role with trust policy
aws iam create-role \
  --role-name CloudFrontInvalidationRole \
  --assume-role-policy-document file://aws-config/management-account-cloudfront-trust-policy.json \
  --description 'Allows production account to invalidate CloudFront distribution'

# Attach the CloudFront invalidation policy
aws iam put-role-policy \
  --role-name CloudFrontInvalidationRole \
  --policy-name CloudFrontInvalidationPolicy \
  --policy-document file://aws-config/management-account-cloudfront-role.json

# Verify the role was created
aws iam get-role --role-name CloudFrontInvalidationRole
```

**What this does:**
- Creates a role that can invalidate CloudFront distribution E34Q2E7TZIYZAB
- Trusts the production account's GitHubActionsDeployRole
- Requires an external ID for additional security

### Step 2: Production Account - Add AssumeRole Permission

Log into the **production account (590716168923)** and run:

```bash
# Add permission to assume the CloudFront role
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name AssumeCloudFrontRole \
  --policy-document file://aws-config/prod-account-assume-cloudfront-role-policy.json

# Verify the policy was attached
aws iam get-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name AssumeCloudFrontRole
```

**What this does:**
- Allows GitHubActionsDeployRole to assume the CloudFrontInvalidationRole
- Enables cross-account access from production to management account

### Step 3: Configure GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Click `New repository secret`
3. Add the following secrets:

| Secret Name | Secret Value |
|-------------|--------------|
| `CLOUDFRONT_ROLE_ARN` | `arn:aws:iam::438465156498:role/CloudFrontInvalidationRole` |
| `CLOUDFRONT_EXTERNAL_ID` | `christopher-corbin-portfolio-cloudfront-access` |

**Security Note:** The external ID adds an extra layer of security to prevent the "confused deputy" problem in cross-account access.

### Step 4: Test Cross-Account Access

Test that the setup works correctly:

```bash
# Test assuming the CloudFront role from production account
aws sts assume-role \
  --role-arn arn:aws:iam::438465156498:role/CloudFrontInvalidationRole \
  --role-session-name TestInvalidation \
  --external-id christopher-corbin-portfolio-cloudfront-access \
  --profile production

# If successful, test CloudFront invalidation
# (Use the credentials from the assume-role output)
export AWS_ACCESS_KEY_ID=<from-assume-role-output>
export AWS_SECRET_ACCESS_KEY=<from-assume-role-output>
export AWS_SESSION_TOKEN=<from-assume-role-output>

aws cloudfront create-invalidation \
  --distribution-id E34Q2E7TZIYZAB \
  --paths '/*'
```

**Expected output:**
```json
{
    "Location": "https://cloudfront.amazonaws.com/2020-05-31/distribution/E34Q2E7TZIYZAB/invalidation/...",
    "Invalidation": {
        "Id": "I...",
        "Status": "InProgress",
        "CreateTime": "2026-02-12T...",
        "InvalidationBatch": {
            "Paths": {
                "Quantity": 1,
                "Items": ["/*"]
            },
            "CallerReference": "..."
        }
    }
}
```

## How It Works

### Workflow Behavior

The updated production frontend workflow now:

1. **Deploys to S3** (using production account credentials)
2. **Checks for secrets** (`CLOUDFRONT_ROLE_ARN` and `CLOUDFRONT_EXTERNAL_ID`)
3. **If secrets exist:**
   - Assumes CloudFrontInvalidationRole in management account
   - Creates CloudFront invalidation automatically
   - Reports invalidation ID and status
4. **If secrets missing:**
   - Skips automatic invalidation
   - Displays manual invalidation instructions
   - Deployment still succeeds

### Security Features

1. **OIDC Authentication**: No long-lived credentials in GitHub
2. **External ID**: Prevents confused deputy attacks
3. **Least Privilege**: CloudFront role can ONLY invalidate, nothing else
4. **Time-Limited**: Assumed role credentials expire after 15 minutes
5. **Audit Trail**: All actions logged in CloudTrail for both accounts

## Verification

After setup, push a change to the main branch and verify:

1. **Workflow runs successfully**
   ```
   ✅ S3 deployment completed
   🔐 Assuming CloudFront role in management account...
   ✅ Successfully assumed CloudFront role
   🔄 Invalidating CloudFront cache...
   ✅ CloudFront invalidation created: I...
   ```

2. **Check CloudFront invalidations**
   ```bash
   aws cloudfront list-invalidations \
     --distribution-id E34Q2E7TZIYZAB \
     --profile management
   ```

3. **Verify website updates**
   - Visit: https://christophercorbin.cloud
   - Check that changes are visible (may take 1-3 minutes)

## Troubleshooting

### Error: "User is not authorized to perform: sts:AssumeRole"

**Cause**: Production account role doesn't have permission to assume CloudFront role

**Fix**: Verify Step 2 was completed correctly
```bash
aws iam get-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name AssumeCloudFrontRole \
  --profile production
```

### Error: "Access denied" when creating invalidation

**Cause**: CloudFront role doesn't have invalidation permissions

**Fix**: Verify Step 1 was completed correctly
```bash
aws iam get-role-policy \
  --role-name CloudFrontInvalidationRole \
  --policy-name CloudFrontInvalidationPolicy \
  --profile management
```

### Error: "Invalid external ID"

**Cause**: External ID mismatch between trust policy and GitHub secret

**Fix**: Ensure both use: `christopher-corbin-portfolio-cloudfront-access`

### Workflow skips invalidation

**Cause**: GitHub secrets not configured

**Fix**: Verify secrets are set in GitHub repository settings
- `CLOUDFRONT_ROLE_ARN`
- `CLOUDFRONT_EXTERNAL_ID`

## Rollback

If you need to remove cross-account access:

```bash
# In production account
aws iam delete-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name AssumeCloudFrontRole \
  --profile production

# In management account
aws iam delete-role-policy \
  --role-name CloudFrontInvalidationRole \
  --policy-name CloudFrontInvalidationPolicy \
  --profile management

aws iam delete-role \
  --role-name CloudFrontInvalidationRole \
  --profile management
```

The workflow will automatically fall back to manual invalidation instructions.

## Cost Considerations

- **CloudFront Invalidations**: First 1,000 paths per month are free, then $0.005 per path
- **STS AssumeRole**: No additional cost
- **CloudTrail Logging**: Included in existing CloudTrail setup

For this portfolio project with infrequent deployments, costs are negligible.

## Alternative Solutions

If you prefer not to use cross-account roles:

### Option 1: Move CloudFront to Production Account
- Migrate CloudFront distribution to production account
- Update DNS records
- Simpler setup, but requires migration

### Option 2: Use AWS Lambda
- Create Lambda in management account
- Trigger from S3 events in production account
- More complex, but fully automated

### Option 3: Manual Invalidation
- Keep current manual process
- Use AWS Console or CLI after deployments
- Simplest, but requires manual step

## References

- [AWS Cross-Account Access](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)
- [CloudFront Invalidation API](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [Confused Deputy Problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)

---

**Last Updated**: February 12, 2026
**Maintained By**: Christopher Corbin
**Status**: Ready for implementation
