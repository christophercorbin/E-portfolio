#!/bin/bash

# Deploy CloudFront Distribution for Custom Domain
# Run this AFTER your SSL certificate is validated

DOMAIN_NAME="christophercorbin.cloud"
S3_BUCKET="christopher-corbin-portfolio-20251005195625"
REGION="us-east-1"

echo "🚀 Deploying CloudFront distribution for $DOMAIN_NAME"
echo ""

# Check if certificate ARN file exists
if [ ! -f ".cert-arn.txt" ]; then
    echo "❌ Certificate ARN file not found. Run ./setup-custom-domain.sh first"
    exit 1
fi

CERT_ARN=$(cat .cert-arn.txt)
echo "📜 Using Certificate ARN: $CERT_ARN"

# Check if certificate is validated
echo "🔍 Checking certificate status..."
CERT_STATUS=$(aws acm describe-certificate \
    --certificate-arn "$CERT_ARN" \
    --region us-east-1 \
    --query 'Certificate.Status' \
    --output text)

if [ "$CERT_STATUS" != "ISSUED" ]; then
    echo "⏳ Certificate status: $CERT_STATUS"
    echo "❌ Certificate is not yet validated. Please wait and try again."
    echo "💡 Go to AWS Console → Certificate Manager to check validation status"
    exit 1
fi

echo "✅ Certificate is validated and ready!"

# Create CloudFront distribution
echo "🌐 Creating CloudFront distribution..."

# First, let's create the Origin Access Control
OAC_ID=$(aws cloudfront create-origin-access-control \
    --origin-access-control-config \
    Name="${DOMAIN_NAME}-OAC",OriginAccessControlOriginType=s3,SigningBehavior=always,SigningProtocol=sigv4 \
    --query 'OriginAccessControl.Id' \
    --output text)

echo "🔐 Origin Access Control created: $OAC_ID"

# Create CloudFront distribution configuration
cat > cloudfront-config.json << EOF
{
    "CallerReference": "$(date +%s)",
    "Aliases": {
        "Quantity": 1,
        "Items": ["$DOMAIN_NAME"]
    },
    "DefaultRootObject": "index.html",
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "S3Origin",
                "DomainName": "$S3_BUCKET.s3.$REGION.amazonaws.com",
                "OriginAccessControlId": "$OAC_ID",
                "S3OriginConfig": {
                    "OriginAccessIdentity": ""
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3Origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        },
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {
                "Forward": "none"
            }
        },
        "MinTTL": 0
    },
    "Comment": "CloudFront distribution for $DOMAIN_NAME",
    "Enabled": true,
    "PriceClass": "PriceClass_100",
    "ViewerCertificate": {
        "ACMCertificateArn": "$CERT_ARN",
        "SSLSupportMethod": "sni-only",
        "MinimumProtocolVersion": "TLSv1.2_2021"
    },
    "CustomErrorResponses": {
        "Quantity": 1,
        "Items": [
            {
                "ErrorCode": 404,
                "ResponsePagePath": "/index.html",
                "ResponseCode": "200",
                "ErrorCachingMinTTL": 300
            }
        ]
    }
}
EOF

# Create the distribution
DISTRIBUTION_OUTPUT=$(aws cloudfront create-distribution --distribution-config file://cloudfront-config.json)
DISTRIBUTION_ID=$(echo "$DISTRIBUTION_OUTPUT" | jq -r '.Distribution.Id')
CLOUDFRONT_DOMAIN=$(echo "$DISTRIBUTION_OUTPUT" | jq -r '.Distribution.DomainName')

echo "✅ CloudFront distribution created!"
echo "📋 Distribution ID: $DISTRIBUTION_ID"
echo "🌐 CloudFront Domain: $CLOUDFRONT_DOMAIN"

# Save distribution info
echo "$DISTRIBUTION_ID" > .distribution-id.txt
echo "$CLOUDFRONT_DOMAIN" > .cloudfront-domain.txt

# Update S3 bucket policy to allow CloudFront access
echo "🔐 Updating S3 bucket policy for CloudFront access..."

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cat > s3-cloudfront-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$S3_BUCKET/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::$ACCOUNT_ID:distribution/$DISTRIBUTION_ID"
                }
            }
        }
    ]
}
EOF

aws s3api put-bucket-policy --bucket "$S3_BUCKET" --policy file://s3-cloudfront-policy.json

echo "✅ S3 bucket policy updated!"

echo ""
echo "🎉 SUCCESS! CloudFront distribution is being deployed..."
echo "📋 Next Steps:"
echo "1. Wait 15-20 minutes for CloudFront deployment to complete"
echo "2. Go to Route 53 and create an A record:"
echo "   - Name: (leave blank for root domain)"
echo "   - Type: A"
echo "   - Alias: Yes"
echo "   - Route traffic to: CloudFront distribution"
echo "   - Choose your distribution: $CLOUDFRONT_DOMAIN"
echo ""
echo "3. Test your domain: https://$DOMAIN_NAME (wait for deployment)"
echo ""
echo "Distribution ID: $DISTRIBUTION_ID (saved to .distribution-id.txt)"

# Cleanup temp files
rm -f cloudfront-config.json s3-cloudfront-policy.json