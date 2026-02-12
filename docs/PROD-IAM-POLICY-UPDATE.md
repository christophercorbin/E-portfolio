# Production IAM Policy Update Required

## Issue

Production frontend deployment is failing with CloudFront invalidation permission error:

```
User: arn:aws:sts::590716168923:assumed-role/GitHubActionsDeployRole/GitHubActions-ProdFrontend 
is not authorized to perform: cloudfront:CreateInvalidation on resource: 
arn:aws:cloudfront::590716168923:distribution/E34Q2E7TZIYZAB
```

## Root Cause

The IAM policy for `GitHubActionsDeployRole` in the production account (590716168923) needs to be updated with:
1. CloudFront invalidation permissions
2. S3 bucket management permissions (for bucket creation)

## Solution

The updated IAM policy has been prepared in `aws-config/prod-account-iam-policy.json`.

### Changes Made

1. **Added S3 Bucket Management Permissions**
   - `s3:CreateBucket` - Create the production bucket if it doesn't exist
   - `s3:PutBucketWebsite` - Configure bucket for website hosting
   - `s3:PutBucketPolicy` - Set bucket policy for CloudFront OAI access
   - `s3:PutBucketTagging` - Add tags to the bucket

2. **Fixed CloudFront Invalidation Permissions**
   - Corrected the ARN format for CloudFront distribution
   - Added proper permissions for cache invalidation

3. **Removed Overly Restrictive Deny**
   - Removed `s3:PutBucketWebsite` from the deny list (needed for initial setup)
   - Kept critical denies: DeleteBucket, DeleteFunction, DeleteTable, DeleteStack

## How to Apply

### Step 1: Update the IAM Policy in AWS Console

1. Log into AWS Console for production account (590716168923)
2. Go to IAM → Roles → GitHubActionsDeployRole
3. Click on the inline policy or attached policy
4. Replace the entire policy with the content from `aws-config/prod-account-iam-policy.json`
5. Save the policy

### Step 2: Or Use AWS CLI

```bash
# Assuming you have AWS CLI configured for prod account
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://aws-config/prod-account-iam-policy.json \
  --profile prod-account
```

### Step 3: Verify the Update

```bash
# Check the policy is applied
aws iam get-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --profile prod-account
```

### Step 4: Re-run the Deployment

Once the policy is updated, merge the PR to main or manually trigger the workflow:

```bash
gh workflow run "Deploy Portfolio to AWS (S3 + CloudFront)" --ref main
```

## Updated Policy Highlights

### CloudFront Permissions
```json
{
  "Sid": "AllowCloudFrontInvalidation",
  "Effect": "Allow",
  "Action": [
    "cloudfront:CreateInvalidation",
    "cloudfront:GetInvalidation",
    "cloudfront:ListInvalidations"
  ],
  "Resource": "arn:aws:cloudfront::590716168923:distribution/E34Q2E7TZIYZAB"
}
```

### S3 Bucket Management
```json
{
  "Sid": "AllowProdS3BucketManagement",
  "Effect": "Allow",
  "Action": [
    "s3:CreateBucket",
    "s3:GetBucketWebsite",
    "s3:PutBucketWebsite",
    "s3:GetBucketPolicy",
    "s3:PutBucketPolicy",
    "s3:PutBucketTagging",
    ...
  ],
  "Resource": "arn:aws:s3:::christopher-corbin-portfolio-20251005195625"
}
```

## Security Notes

- The policy still denies dangerous operations (DeleteBucket, DeleteFunction, etc.)
- CloudFront invalidation is scoped to the specific distribution
- S3 permissions are scoped to the specific production bucket
- All operations are restricted to us-east-1 region where applicable

## Expected Outcome

After applying this policy update:
1. ✅ S3 bucket will be created automatically if it doesn't exist
2. ✅ Bucket will be configured for website hosting
3. ✅ Bucket policy will be set for CloudFront OAI access
4. ✅ CloudFront cache invalidation will succeed
5. ✅ Production deployment will complete successfully

## Troubleshooting

If the deployment still fails after applying the policy:

1. **Check Policy Propagation**
   - IAM policy changes can take a few seconds to propagate
   - Wait 30 seconds and try again

2. **Verify CloudFront Distribution**
   - Confirm distribution E34Q2E7TZIYZAB exists in prod account
   - Check if it's in the correct account (590716168923)

3. **Check S3 Block Public Access**
   - Production account has Block Public Access enabled (good!)
   - Bucket policy uses CloudFront OAI, not public access
   - This is the correct and secure approach

4. **Review CloudWatch Logs**
   - Check GitHub Actions logs for detailed error messages
   - Look for any other permission issues

## Related Files

- `aws-config/prod-account-iam-policy.json` - Updated policy
- `.github/workflows/deploy-frontend-prod.yml` - Production deployment workflow
- `docs/MULTI-ACCOUNT-IMPLEMENTATION-GUIDE.md` - Multi-account setup guide

---

**Created**: February 12, 2026  
**Status**: Pending Application  
**Priority**: High - Blocks production deployment
