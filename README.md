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

### Frontend Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │  GitHub Actions  │    │   AWS S3 Bucket │
│                 │───▶│                  │───▶│                 │
│   Static Files  │    │  Build & Deploy  │    │  Static Hosting │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │ AWS CloudFront  │
                                                │                 │
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
│             │───▶│                 │───▶│                  │───▶│                 │
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

| Service | Purpose | Implementation |
|---------|---------|----------------|
| **S3** | Static website hosting | Bucket with website configuration |
| **CloudFront** | Content Delivery Network | Global distribution with custom domain |
| **Route 53** | DNS Management | Custom domain with SSL |
| **Certificate Manager** | SSL/TLS Certificates | Automated certificate provisioning |
| **Lambda** | Serverless compute | Contact form processing |
| **API Gateway** | RESTful API endpoints | CORS-enabled REST API |
| **DynamoDB** | NoSQL database | Contact form submissions |
| **SES** | Simple Email Service | Professional email notifications |
| **IAM** | Identity and Access Management | Least-privilege security policies |
| **CloudFormation** | Infrastructure as Code | SAM template deployments |
| **CloudWatch** | Logging and monitoring | Application and infrastructure monitoring |

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

### Branch Strategy
- **main**: Production-ready code, auto-deploys to live site
- **dev-backend-integration**: Development branch for backend features
- **Feature branches**: For individual features and experiments

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

### IAM Security
- **Least Privilege**: Custom IAM policies with minimal required permissions
- **Resource-Specific**: Permissions scoped to specific resources only
- **Action Restrictions**: Limited to necessary operations
- **Explicit Denies**: Protection against dangerous operations

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

# Christopher Corbin - AWS Portfolio

Professional AWS portfolio with automated CI/CD deployment pipeline.

## Features
- Professional timeline with real experience
- SOC2 ML Image Analyzer project showcase  
- GitHub Actions CI/CD pipeline
- Secure IAM policy with least privilege
- Responsive design with Credly badge integration

## Live Portfolio
Visit: http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com

Built with AWS S3, GitHub Actions, and professional DevOps practices. OCT/7/2025
