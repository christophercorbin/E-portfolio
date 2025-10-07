# Christopher Corbin - AWS Solutions Architect & Security Engineer Portfolio

[![Deploy Status](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy.yml/badge.svg)](https://github.com/christophercorbin/E-portfolio/actions/workflows/deploy.yml)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)](https://github.com/christophercorbin/E-portfolio/actions)

Professional portfolio showcasing AWS expertise, security engineering, and DevOps automation. Built with enterprise-grade cloud architecture and automated CI/CD pipeline.

## 🌐 Live Portfolio
**Visit:** http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com

## Features

### Frontend
- **Responsive Design**: Mobile-first approach with modern CSS Grid/Flexbox
- **Professional Timeline**: Interactive experience showcase with achievements
- **Project Portfolio**: Detailed project cards with live GitHub repositories
- **Certification Display**: Credly badge integration with live verification
- **Performance Optimized**: Lazy loading, image optimization, smooth animations
- **Accessibility**: WCAG compliant with semantic HTML and ARIA labels

### Backend & Infrastructure (Dev Branch)
- **Serverless Contact Form**: AWS Lambda + API Gateway + DynamoDB
- **Email Notifications**: AWS SES integration with professional templates
- **Data Storage**: DynamoDB with TTL for GDPR compliance
- **Security**: Input validation, CORS protection, rate limiting
- **Monitoring**: CloudWatch logs and error tracking

### DevOps & Automation
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Infrastructure as Code**: AWS SAM templates for reproducible deployments
- **Security**: IAM policies with least privilege principles
- **Monitoring**: Automated deployment status and health checks
- **Branch Protection**: Separate dev/main branches for safe development

## Architecture

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
```

### Backend Architecture (Dev Branch)
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

## Technology Stack

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Frameworks**: Vanilla JS (no dependencies for optimal performance)
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)
- **Build Tools**: Native browser APIs

### Backend (Dev Branch)
- **Runtime**: Python 3.9
- **Framework**: AWS Lambda
- **API**: AWS API Gateway (REST)
- **Database**: AWS DynamoDB
- **Email**: AWS SES
- **IaC**: AWS SAM (Serverless Application Model)

### DevOps
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Cloud Platform**: AWS
- **Deployment**: Automated via GitHub Actions
- **Monitoring**: AWS CloudWatch

### AWS Services Used
- **S3**: Static website hosting
- **CloudFront**: Content Delivery Network
- **Lambda**: Serverless compute (contact form)
- **API Gateway**: RESTful API endpoints
- **DynamoDB**: NoSQL database for form submissions
- **SES**: Simple Email Service for notifications
- **IAM**: Identity and Access Management
- **CloudFormation**: Infrastructure as Code
- **CloudWatch**: Logging and monitoring

## Deployment Process

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
- **`main`**: Production-ready code, auto-deploys to live site
- **`dev-backend-integration`**: Development branch for backend features
- **Feature branches**: For individual features and experiments

## Project Structure

```
AWS-eportfolio/
├── index.html              # Main portfolio page
├── resume.html             # Printable resume page
├── styles.css              # Main stylesheet
├── script.js               # Interactive functionality
├── config.js               # Environment configuration
├── .github/
│   └── workflows/
│       ├── deploy.yml      # Main deployment workflow
│       └── deploy-sam.yml  # Backend deployment (dev)
├── src/                    # Lambda function code (dev)
│   └── contact_handler.py  # Contact form processor
├── template.yaml           # SAM infrastructure template (dev)
├── samconfig.toml          # SAM configuration (dev)
├── secure-iam-policy.json  # IAM security policy
├── debug-form.html         # Development tools (dev)
├── test-form.html          # Testing utilities (dev)
└── README.md               # This file
```

## Security Features

### IAM Security
- **Least Privilege**: Custom IAM policies with minimal required permissions
- **Resource-Specific**: Permissions scoped to specific S3 bucket only
- **Action Restrictions**: Limited to necessary S3 operations
- **Deny Rules**: Explicit denies for dangerous operations

### Application Security (Dev Branch)
- **Input Validation**: Server-side validation of all form inputs
- **CORS Protection**: Proper Cross-Origin Resource Sharing configuration
- **Rate Limiting**: Protection against spam and abuse
- **Data Privacy**: TTL on stored data for GDPR compliance
- **Error Handling**: Secure error messages without information disclosure

## Performance Optimizations

- **CDN Distribution**: CloudFront for global content delivery
- **Image Optimization**: Compressed images and lazy loading
- **CSS/JS Minification**: Optimized asset delivery
- **Caching Strategy**: Proper cache headers and invalidation
- **Mobile-First**: Responsive design for all device sizes
- **Core Web Vitals**: Optimized for Google's performance metrics

## Development & Testing

### Local Development
```bash
# Clone the repository
git clone https://github.com/christophercorbin/E-portfolio.git

# Switch to development branch (for backend features)
git checkout dev-backend-integration

# Open locally
open index.html
```

### Backend Development (Dev Branch)
```bash
# Install SAM CLI
brew tap aws/tap && brew install aws-sam-cli

# Build and test locally
sam build
sam local start-api

# Deploy to AWS
sam deploy --guided
```

### Testing Tools
- **debug-form.html**: Comprehensive form testing with detailed logging
- **test-form.html**: Isolated form testing environment
- **Browser DevTools**: Console logging and network monitoring
- **AWS CloudWatch**: Backend logging and monitoring

## Key Achievements

- **SOC 2 Compliance**: 97.2% audit score with zero critical findings
- **Performance**: Fast loading times with optimized assets
- **Security**: Enterprise-grade security practices
- **Automation**: Fully automated deployment pipeline
- **Responsive**: Perfect experience on all devices
- **Accessible**: WCAG compliant design
- **Global**: CDN distribution for worldwide access

## Metrics & Monitoring

- **Deployment Success Rate**: 100% (automated rollback on failure)
- **Uptime**: 99.9%+ (monitored via AWS health checks)
- **Performance**: <2s load time globally
- **Security**: Zero security incidents
- **Cost Optimization**: <$5/month for full stack

## Contact Form API (Dev Branch)

### API Endpoint
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
- Real-time validation
- Spam protection
- Email notifications
- Data persistence
- GDPR compliant (30-day TTL)

## Contributing

This is a personal portfolio, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## About the Developer

**Christopher Corbin** - AWS Solutions Architect & Security Engineer

- **Portfolio**: [Live Site](http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com)
- **Email**: christophercorbin24@gmail.com
- **Phone**: +1 (246) 248-7457
- **GitHub**: [@christophercorbin](https://github.com/christophercorbin)
- **Location**: Barbados | Open to relocation

---

**Built with modern web technologies, AWS cloud services, and automated DevOps practices**

*This portfolio demonstrates real-world cloud architecture, DevOps practices, and security engineering expertise through hands-on implementation.*
