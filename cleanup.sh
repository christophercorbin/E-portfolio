#!/bin/bash

# AWS S3 Portfolio Cleanup Script
# Christopher Corbin - AWS Cloud Developer Portfolio

set -e

# Configuration
BUCKET_NAME="christopher-corbin-portfolio-20251005195625"

echo "🗑️  AWS S3 Portfolio Cleanup"
echo "==============================="
echo ""
echo "⚠️  WARNING: This will permanently delete your portfolio and S3 bucket!"
echo "Bucket: $BUCKET_NAME"
echo ""

read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm

if [[ $confirm != "yes" ]]; then
    echo "❌ Cleanup cancelled."
    exit 0
fi

echo ""
echo "🧹 Cleaning up AWS resources..."

# Remove all objects from the bucket
echo "📦 Removing all files from S3 bucket..."
aws s3 rm s3://$BUCKET_NAME --recursive

# Delete the bucket
echo "🗑️  Deleting S3 bucket..."
aws s3 rb s3://$BUCKET_NAME

echo ""
echo "✅ Cleanup completed successfully!"
echo "💰 Your portfolio hosting costs have stopped."
echo ""
echo "📝 Note: This script only deletes the S3 bucket."
echo "If you set up CloudFront or other AWS resources, please delete them manually."