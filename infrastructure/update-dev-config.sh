#!/bin/bash
# Script to update config-dev.js with actual dev backend API URL
# Used during GitHub Actions deployment workflow

set -e

STACK_NAME="christopher-corbin-portfolio-backend-dev"
REGION="us-east-1"
CONFIG_FILE="config-dev.js"

echo "🔍 Looking for dev backend stack: $STACK_NAME"

# Try to get dev backend API URL from CloudFormation
DEV_API_URL=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs[?OutputKey==`ContactFormApi`].OutputValue' \
  --output text 2>/dev/null || echo "")

if [ -z "$DEV_API_URL" ] || [ "$DEV_API_URL" = "None" ]; then
  echo "⚠️  Dev backend stack not found or not deployed yet"
  echo "💡 The config file will use a placeholder URL"
  echo "   Deploy backend first by pushing changes to infrastructure/ or src/"
  echo "   Or manually trigger: Actions → Deploy SAM Backend - Development"
  exit 0
fi

echo "✅ Found dev backend API URL: $DEV_API_URL"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
  echo "❌ Error: $CONFIG_FILE not found"
  exit 1
fi

# Backup original config
cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"

# Update the API URL in config-dev.js
# This handles both single and double quotes
sed -i.tmp "s|CONTACT_API_URL: ['\"][^'\"]*['\"]|CONTACT_API_URL: '$DEV_API_URL'|g" "$CONFIG_FILE"
rm -f "${CONFIG_FILE}.tmp"

# Verify the change was made
if grep -q "$DEV_API_URL" "$CONFIG_FILE"; then
  echo "✅ Successfully updated $CONFIG_FILE with dev API URL"
  echo ""
  echo "📝 Updated configuration:"
  grep "CONTACT_API_URL:" "$CONFIG_FILE" || true
  
  # Clean up backup
  rm -f "${CONFIG_FILE}.backup"
else
  echo "❌ Failed to update $CONFIG_FILE"
  echo "Restoring backup..."
  mv "${CONFIG_FILE}.backup" "$CONFIG_FILE"
  exit 1
fi

echo ""
echo "🎉 Dev configuration ready for deployment!"
