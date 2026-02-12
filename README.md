# Christopher Corbin - AWS Solutions Architect & Security Engineer Portfolio

[![Deploy Status](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy.yml/badge.svg)](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy.yml) [![SAM Backend](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy-prod.yml/badge.svg)](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy-prod.yml)

Professional portfolio showcasing AWS expertise, security engineering, and DevOps automation. Built with enterprise-grade cloud architecture, custom domain, and fully automated CI/CD pipelines.

## 🌐 Live Portfolio
**Visit**: [https://christophercorbin.cloud](https://christophercorbin.cloud)

**CloudFront Distribution**: https://d30iyriy15xq9k.cloudfront.net

## ✨ Features

### Frontend
- **Responsive Design**: Mobile-first approach with modern CSS Grid/Flexbox
- **Professional Timeline**: Interactive experience showcase with achievements
- **Project Portfolio**: Detailed project cards with live GitHub repositories
- **Certification Display**: AWS and CompTIA badge integration
- **Performance Optimized**: Global CDN, lazy loading, image optimization
- **Accessibility**: WCAG compliant with semantic HTML and ARIA labels
- **Custom Domain**: HTTPS with automated SSL certificate management

### Backend & Infrastructure
- **Serverless Contact Form**: AWS Lambda + API Gateway + DynamoDB
- **Email Notifications**: AWS SES integration with professional templates
- **Data Storage**: DynamoDB with TTL for GDPR compliance
- **Security**: Input validation, CORS protection, rate limiting
- **Monitoring**: CloudWatch logs and comprehensive error tracking

### DevOps & Automation
- **Multi-Environment CI/CD**: GitHub Actions with dev/prod pipelines
- **Infrastructure as Code**: AWS SAM templates for reproducible deployments
- **Security**: IAM policies with least privilege principles
- **Global Distribution**: CloudFront CDN with automatic cache invalidation
- **Branch Protection**: Separate development and production workflows

## 🏗️ Architecture

### Multi-Account Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    AWS Organization (438465156498)               │
│                         Management Account                       │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │  CloudFront CDN    │  │  Route 53 DNS      │                │
│  │  E34Q2E7TZIYZAB    │  │  christophercorbin │                │
│  │                    │  │  .cloud            │                │
│  └────────────────────┘  └────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
           │                           │
           ▼                           ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Dev Account         │    │  Prod Account        │
│  (934862608865)      │    │  (590716168923)      │
│                      │    │                      │
│  • S3 Bucket (Dev)   │    │  • S3 Bucket (Prod)  │
│  • Lambda (Dev)      │    │  • Lambda (Prod)     │
│  • API Gateway (Dev) │    │  • API Gateway       │
│  • DynamoDB (Dev)    │    │  • DynamoDB          │
└──────────────────────┘    └──────────────────────┘
           ▲                           ▲
           │                           │
           └───────────┬───────────────┘
                       │
              ┌────────────────┐
              │ GitHub Actions │
              │  OIDC Auth     │
              └────────────────┘
```

### Frontend Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │  GitHub Actions  │    │   AWS S3 Bucket │
│                 │───▶│   (OIDC Auth)    │───▶│  (Per Account)  │
│   Static Files  │    │  Build & Deploy  │    │  Static Hosting │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │ AWS CloudFront  │
                                                │ (Management)    │
                                                │ Global CDN      │
                                                └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Route 53 +    │
                                                │ Custom Domain   │
                                                │christophercorbin│
                                                │    .cloud       │
                                                └─────────────────┘
```

### Backend Architecture
```
┌─────────────┐    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Browser   │    │  API Gateway    │    │  Lambda Function │    │   DynamoDB      │
│             │───▶│  (Per Account)  │───▶│  (Per Account)   │───▶│  (Per Account)  │
│ Contact Form│    │  REST Endpoint  │    │  Form Handler    │    │  Submissions    │
└─────────────┘    └─────────────────┘    └──────────────────┘    └─────────────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │     AWS SES     │
                                            │                 │
                                            │ Email Service   │
                                            └─────────────────┘
```

## 💻 Technology Stack

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Vanilla JS (no dependencies for optimal performance)
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)
- **Build Tools**: Native browser APIs

### Backend
- **Runtime**: Python 3.9
- **Framework**: AWS Lambda
- **API**: AWS API Gateway (REST)
- **Database**: AWS DynamoDB
- **Email**: AWS SES
- **IaC**: AWS SAM (Serverless Application Model)

### DevOps
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions (Multi-pipeline)
- **Cloud Platform**: AWS
- **Domain**: Route 53 + Certificate Manager
- **Monitoring**: AWS CloudWatch

## ☁️ AWS Services Used

| Service | Purpose | Implementation | Account |
|---------|---------|----------------|---------|
| **AWS Organizations** | Multi-account management | Centralized billing and governance | Management (438465156498) |
| **S3** | Static website hosting | Separate buckets per environment | Dev (934862608865) / Prod (590716168923) |
| **CloudFront** | Content Delivery Network | Global distribution with custom domain | Management (438465156498) |
| **Route 53** | DNS Management | Custom domain with SSL | Management (438465156498) |
| **Certificate Manager** | SSL/TLS Certificates | Automated certificate provisioning | Management (438465156498) |
| **Lambda** | Serverless compute | Contact form processing per environment | Dev / Prod |
| **API Gateway** | RESTful API endpoints | CORS-enabled REST API per environment | Dev / Prod |
| **DynamoDB** | NoSQL database | Contact form submissions per environment | Dev / Prod |
| **SES** | Simple Email Service | Professional email notifications | Dev / Prod |
| **IAM** | Identity and Access Management | OIDC + least-privilege policies per account | All accounts |
| **CloudFormation** | Infrastructure as Code | SAM template deployments per environment | Dev / Prod |
| **CloudWatch** | Logging and monitoring | Per-account monitoring | All accounts |

## 🚀 Deployment Process

### Automated CI/CD Pipeline

1. **Code Push**: Developer pushes code to GitHub
2. **GitHub Actions Trigger**: Workflow automatically starts
3. **Build Process**:
   - Validates HTML/CSS/JavaScript
   - Optimizes assets
   - Runs security checks
4. **AWS Deployment**:
   - Syncs files to S3 bucket
   - Invalidates CloudFront cache
   - Verifies deployment success
5. **Health Check**: Automated testing of live site

### Branch Strategy (Multi-Account)
- **main**: Production-ready code, deploys to Production account (590716168923)
- **develop**: Development branch, deploys to Development account (934862608865)
- **dev-backend-integration**: Backend development, deploys to Development account
- **Feature branches**: For individual features and experiments

### Account Mapping
- **Development Branches** (develop, dev-backend-integration) → Dev Account (934862608865)
- **Production Branches** (main, master) → Prod Account (590716168923)
- **Shared Services** (CloudFront, Route53) → Management Account (438465156498)

## 📁 Project Structure (Clean & Professional)

```
AWS-eportfolio/
├── 📄 index.html                    # Main portfolio page
├── 📄 resume.html                   # Professional resume page
├── 📄 styles.css                    # Main stylesheet
├── 📄 script.js                     # Interactive functionality
├── 📄 config.js                     # Production configuration
├── 📄 config-dev.js                 # Development configuration
├── 📂 images/                       # Portfolio assets
│   └── profile-photo.jpg            # Professional headshot
├── 📂 src/                          # Lambda function source code
│   └── contact_handler.py           # Contact form processor
├── 📂 infrastructure/               # AWS SAM templates and configs
│   ├── template.yaml               # SAM infrastructure definition
│   ├── samconfig.toml              # Production deployment config
│   ├── samconfig-dev.toml          # Development deployment config
│   ├── deploy-cloudfront.sh        # CloudFront deployment script
│   └── setup-custom-domain.sh     # Domain setup automation
├── 📂 aws-config/                   # AWS policies and configurations
│   ├── github-actions-sam-policy.json         # SAM deployment permissions
│   ├── github-actions-cloudfront-policy.json  # CloudFront permissions
│   ├── github-actions-iam-policy.json         # IAM management permissions
│   ├── enhanced-s3-policy.json               # S3 bucket policies
│   └── s3-cloudfront-policy.json             # S3-CloudFront integration
├── 📂 .github/workflows/            # CI/CD pipeline definitions
│   ├── deploy.yml                  # Main frontend deployment
│   ├── deploy-prod.yml             # Production backend deployment
│   ├── deploy-sam.yml              # Development backend deployment
│   └── deploy-dev-frontend.yml     # Development frontend pipeline
├── 📂 docs/                         # Project documentation
│   ├── CI-CD-SETUP.md              # CI/CD setup guide
│   └── DEVELOPMENT.md              # Development guidelines
├── 📄 .gitignore                    # Git ignore patterns
└── 📄 README.md                     # This comprehensive guide
```

## 🔒 Security Features

### Multi-Account Security
- **Account Isolation**: Dev and Prod resources in separate AWS accounts
- **OIDC Authentication**: No long-lived credentials, temporary tokens only
- **Cross-Account Protection**: Prevents accidental production changes
- **Audit Trail**: CloudTrail logging in all accounts
- **Consolidated Billing**: Cost tracking per account

### IAM Security
- **Least Privilege**: Custom IAM policies with minimal required permissions per account
- **Account-Specific Policies**: Dev has broader permissions, Prod is restricted
- **Resource-Specific**: Permissions scoped to specific resources only
- **Action Restrictions**: Limited to necessary operations per environment
- **Explicit Denies**: Protection against dangerous operations in production

### Application Security
- **Input Validation**: Server-side validation of all form inputs
- **CORS Protection**: Proper Cross-Origin Resource Sharing configuration
- **Rate Limiting**: Protection against spam and abuse
- **Data Privacy**: TTL on stored data for GDPR compliance
- **SSL/TLS**: End-to-end encryption with custom domain

## ⚡ Performance Optimizations

- **Global CDN**: CloudFront distribution for worldwide < 100ms response times
- **Image Optimization**: Compressed images and lazy loading
- **Asset Optimization**: Minified CSS/JS with proper caching
- **Cache Strategy**: Intelligent cache headers and automated invalidation
- **Mobile-First**: Responsive design optimized for all device sizes
- **Core Web Vitals**: Optimized for Google's performance metrics

## 🛠️ Development & Testing

### Local Development
```bash
# Clone the repository
git clone https://github.com/christophercorbin/E-portfolio.git
cd AWS-eportfolio

# Start local development server
python -m http.server 8000
# Visit http://localhost:8000
```

### Backend Development
```bash
# Switch to development branch
git checkout dev-backend-integration

# Install SAM CLI
brew tap aws/tap && brew install aws-sam-cli

# Build and test locally
cd infrastructure
sam build
sam local start-api

# Deploy to AWS development environment
sam deploy --config-file samconfig-dev.toml --config-env dev
```

### Testing Tools
- **Browser DevTools**: Console logging and network monitoring
- **AWS CloudWatch**: Backend logging and monitoring
- **SAM Local**: Local Lambda testing environment
- **GitHub Actions**: Automated CI/CD testing

## 📊 Key Achievements & Metrics

### Professional Accomplishments
- **AWS Solutions Architect Associate** certified (2025)
- **CompTIA Security+** certified (2024)
- **Multi-Account AWS Architecture**: Implemented enterprise-grade account separation
- **SOC 2 Compliance**: 97.2% audit score with zero critical findings
- **Cost Optimization**: 20% cloud spend reduction ($150K annually)
- **Security**: Remediated 500+ CVEs in under 30 days
- **Automation**: 60% reduction in manual patching effort

### Portfolio Performance
- **Deployment Success Rate**: 100% (automated rollback on failure)
- **Global Uptime**: 99.9%+ (monitored via AWS health checks)
- **Performance**: <2s load time globally via CloudFront
- **Security**: Zero security incidents since deployment
- **Cost Efficiency**: <$10/month for full production stack
- **Scalability**: Handles 10,000+ requests/minute via Lambda
- **Multi-Account Setup**: 3 AWS accounts with proper isolation

## 🏢 Multi-Account AWS Setup

This portfolio demonstrates enterprise-grade AWS architecture using multiple accounts:

### Account Structure
- **Development Account (934862608865)**: Isolated environment for testing and experimentation
- **Production Account (590716168923)**: Live production workloads with restricted access
- **Management Account (438465156498)**: Organization management and shared services

### Benefits
- **Security**: Complete isolation between dev and prod environments
- **Cost Management**: Separate billing and cost tracking per environment
- **Compliance**: Audit trail and governance across all accounts
- **Risk Mitigation**: Prevents accidental production changes during development

### Authentication
- **OIDC Integration**: GitHub Actions uses OpenID Connect for secure, temporary credentials
- **No Long-Lived Keys**: Zero AWS access keys stored in GitHub secrets
- **Least Privilege**: Account-specific IAM policies with minimal permissions

📖 **Documentation**: See `docs/MULTI-ACCOUNT-IMPLEMENTATION-GUIDE.md` for complete setup guide

## 🔗 Contact Form API

### Production Endpoint
```
POST https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact

Payload:
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "message": "Your message here"
}
```

### Features
- ✅ Real-time validation
- ✅ Spam protection
- ✅ Professional email notifications
- ✅ Data persistence with DynamoDB
- ✅ GDPR compliant (30-day TTL)
- ✅ CORS enabled for secure cross-origin requests

## 🤝 Contributing

This is a personal portfolio, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is open source and available under the MIT License.

## 📚 Documentation

- **Multi-Account Setup**: `.kiro/steering/multi-account-aws-setup.md`
- **Implementation Guide**: `docs/MULTI-ACCOUNT-IMPLEMENTATION-GUIDE.md`
- **Quick Reference**: `docs/MULTI-ACCOUNT-QUICK-REFERENCE.md`
- **Audit Report**: `docs/MULTI-ACCOUNT-AUDIT.md`
- **CI/CD Setup**: `docs/CI-CD-SETUP.md`
- **Development Guide**: `docs/DEVELOPMENT.md`
- **OIDC Setup**: `GITHUB-ACTIONS-OIDC-SETUP.md`

## 👨‍💻 About the Developer

**Christopher Corbin** - AWS Solutions Architect & Security Engineer

- 🌐 **Portfolio**: [christophercorbin.cloud](https://christophercorbin.cloud)
- 📧 **Email**: [christophercorbin@gmail.com](mailto:christophercorbin@gmail.com)
- 📱 **Phone**: +1 (246) 248-7457
- 🐙 **GitHub**: [@christophercorbin](https://github.com/christophercorbin)
- 🌍 **Location**: Barbados | Open to relocation

---

**Built with modern web technologies, AWS cloud services, and automated DevOps practices**

*This portfolio demonstrates real-world cloud architecture, DevSecOps practices, and security engineering expertise through hands-on implementation.*

⭐ **Star this repository** if you find it helpful for your own AWS portfolio projects!
