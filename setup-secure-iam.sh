#!/bin/bash

# Secure IAM Setup for GitHub Actions
# This script creates a highly secure IAM user with least privilege access

set -e

POLICY_NAME="GitHubActionsPortfolioSecurePolicy"
USER_NAME="github-actions-portfolio-secure"
BUCKET_NAME="christopher-corbin-portfolio-20251005195625"

echo "Creating secure IAM setup for GitHub Actions..."
echo "=============================================="

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $ACCOUNT_ID"

# Create secure IAM policy
echo "Creating secure IAM policy..."
aws iam create-policy \
  --policy-name $POLICY_NAME \
  --policy-document file://secure-iam-policy.json \
  --description "Secure policy for GitHub Actions portfolio deployment with least privilege access" || {
    echo "Policy might already exist, updating..."
    aws iam create-policy-version \
      --policy-arn "arn:aws:iam::$ACCOUNT_ID:policy/$POLICY_NAME" \
      --policy-document file://secure-iam-policy.json \
      --set-as-default
  }

# Create IAM user
echo "Creating IAM user..."
aws iam create-user --user-name $USER_NAME \
  --tags Key=Purpose,Value=GitHubActions Key=Project,Value=Portfolio || {
    echo "User might already exist, continuing..."
  }

# Attach secure policy to user
echo "Attaching secure policy to user..."
aws iam attach-user-policy \
  --user-name $USER_NAME \
  --policy-arn "arn:aws:iam::$ACCOUNT_ID:policy/$POLICY_NAME"

# Create access keys
echo "Creating access keys..."
ACCESS_KEY_OUTPUT=$(aws iam create-access-key --user-name $USER_NAME || {
  echo "Access key might already exist. Delete existing keys first if needed:"
  echo "aws iam list-access-keys --user-name $USER_NAME"
  echo "aws iam delete-access-key --user-name $USER_NAME --access-key-id YOUR_KEY_ID"
  exit 1
})

echo ""
echo "SUCCESS! Secure IAM setup completed."
echo "===================================="
echo ""
echo "IMPORTANT: Add these to your GitHub repository secrets:"
echo ""
echo "AWS_ACCESS_KEY_ID:"
echo "$ACCESS_KEY_OUTPUT" | jq -r '.AccessKey.AccessKeyId'
echo ""
echo "AWS_SECRET_ACCESS_KEY:"
echo "$ACCESS_KEY_OUTPUT" | jq -r '.AccessKey.SecretAccessKey'
echo ""
echo "Security Features Enabled:"
echo "- Exact bucket resource specification"
echo "- Region restriction (us-east-1 only)"
echo "- Content type validation"
echo "- Dangerous operations explicitly denied"
echo "- Time-based access control"
echo "- Least privilege principle"
echo ""
echo "⚠️  SECURITY REMINDER:"
echo "- Store these credentials securely in GitHub Secrets"
echo "- Never commit these credentials to code"
echo "- Rotate access keys regularly"
echo "- Monitor CloudTrail logs for unusual activity"
echo ""
echo "To test the policy:"
echo "aws iam simulate-principal-policy \\"
echo "  --policy-source-arn arn:aws:iam::$ACCOUNT_ID:user/$USER_NAME \\"
echo "  --action-names s3:PutObject \\"
echo "  --resource-arns arn:aws:s3:::$BUCKET_NAME/*"