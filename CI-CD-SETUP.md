# CI/CD Pipeline Setup for AWS Portfolio

This repository includes a professional GitHub Actions CI/CD pipeline that automatically deploys your portfolio to AWS S3.

## Pipeline Features

### Automated Deployment
- **Triggers**: Automatic deployment on push to `main`/`master` branch
- **Target**: AWS S3 static website hosting
- **Speed**: Sub-2 minute deployments
- **Rollback**: Git-based version control

### Quality Assurance
- **File validation**: Checks for required HTML, CSS, JS files
- **Security scanning**: Scans for potential sensitive data
- **Performance checks**: Measures response times and file sizes
- **Accessibility**: HTTP/HTTPS readiness validation

### Monitoring & Reporting
- **Deployment verification**: Confirms website accessibility
- **Performance metrics**: Response time measurements  
- **Deployment reports**: Comprehensive build summaries
- **Error handling**: Fails fast with detailed error messages

## Setup Instructions

### 1. Create GitHub Repository
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial portfolio commit"

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/christophercorbin/aws-portfolio.git
git branch -M main
git push -u origin main
```

### 2. Configure GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

**Security Note**: Use IAM user with minimal S3 permissions only!

### 3. Create IAM User for GitHub Actions
```bash
# Create IAM policy for S3 access
aws iam create-policy \
  --policy-name GitHubActionsS3Policy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::christopher-corbin-portfolio-*",
          "arn:aws:s3:::christopher-corbin-portfolio-*/*"
        ]
      }
    ]
  }'

# Create IAM user
aws iam create-user --user-name github-actions-portfolio

# Attach policy to user
aws iam attach-user-policy \
  --user-name github-actions-portfolio \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/GitHubActionsS3Policy

# Create access keys
aws iam create-access-key --user-name github-actions-portfolio
```

## Pipeline Workflow

```
Push to main → Checkout Code → Configure AWS → Validate Files → 
Deploy to S3 → Verify Deployment → Performance Check → 
Security Scan → Generate Report → Complete
```

## Pipeline Steps Explained

### Validation Phase
- Checks for required files (index.html, styles.css, script.js)
- Validates file integrity
- Ensures build readiness

### Deployment Phase 
- Syncs files to S3 with optimized cache headers
- Excludes unnecessary files (.git, .github, etc.)
- Sets appropriate content types and cache policies

### Verification Phase
- Tests website accessibility (HTTP 200 check)
- Measures response performance
- Generates deployment summary

### Security Phase
- Scans for potential secrets in code
- Validates HTTPS readiness
- Checks for security best practices

### Reporting Phase
- Comprehensive deployment report
- File size and performance metrics
- Next steps and recommendations

## Customization Options

### Environment Variables (in deploy.yml)
- `S3_BUCKET`: Your S3 bucket name
- `WEBSITE_URL`: Your website URL
- `AWS_REGION`: AWS region (default: us-east-1)

### Cache Headers
- HTML files: 5 minutes (frequent updates)
- CSS/JS files: 1 year (with versioning)
- Images: 1 year (static assets)

### Exclusions
Current exclusions: `*.json`, `*.sh`, `*.md`, `.git/*`, `.github/*`

## Benefits for Your Portfolio

### Professional DevOps Skills
- Demonstrates modern CI/CD practices
- Shows automation expertise
- Enterprise-grade deployment pipeline

### Reliability & Speed
- Automated deployments reduce errors
- Fast feedback loop for changes
- Version-controlled releases

### Monitoring & Quality
- Built-in performance monitoring
- Security scanning integration
- Deployment verification

## Integration with Future Enhancements

This pipeline is designed to work seamlessly with:
- **CloudFront CDN**: Easy cache invalidation
- **Custom Domain**: Automatic HTTPS deployment  
- **Multiple Environments**: Dev/staging/production
- **Advanced Monitoring**: Integration with AWS CloudWatch

## What This Shows Employers

- Modern DevOps Practices
- Automation Expertise
- AWS Integration Skills
- Security Awareness
- Performance Optimization
- Professional Workflow Management

This CI/CD pipeline showcases your ability to implement enterprise-grade automation and demonstrates your commitment to modern development practices.