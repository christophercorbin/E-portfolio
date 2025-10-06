#!/bin/bash

# AWS S3 Portfolio Deployment Script
# Christopher Corbin - AWS Cloud Developer Portfolio

set -e

# Configuration
BUCKET_NAME="christopher-corbin-portfolio-20251005195625"
REGION="us-east-1"
WEBSITE_URL="http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com"

echo "🚀 Deploying Christopher Corbin's Portfolio to AWS S3..."
echo "Bucket: $BUCKET_NAME"
echo "Region: $REGION"
echo ""

# Check if AWS CLI is configured
if ! aws configure list >/dev/null 2>&1; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

echo "📦 Syncing files to S3..."
aws s3 sync . s3://$BUCKET_NAME \
    --delete \
    --exclude "*.json" \
    --exclude "*.sh" \
    --exclude ".DS_Store" \
    --exclude "README.md" \
    --exclude ".git/*" \
    --cache-control "text/html:max-age=0,no-cache" \
    --cache-control "text/css:max-age=31536000" \
    --cache-control "application/javascript:max-age=31536000"

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your portfolio is live at: $WEBSITE_URL"
echo ""
echo "📊 S3 Bucket Info:"
aws s3 ls s3://$BUCKET_NAME --human-readable --summarize

echo ""
echo "💰 Estimated monthly cost: $1-3 USD (for typical portfolio traffic)"
echo ""
echo "🔧 To update your portfolio:"
echo "1. Edit the HTML, CSS, or JS files"
echo "2. Run: ./deploy.sh"
echo ""
echo "🗑️  To delete the S3 bucket and stop costs:"
echo "aws s3 rb s3://$BUCKET_NAME --force"