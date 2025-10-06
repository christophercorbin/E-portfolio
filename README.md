# Christopher Corbin - AWS Cloud Developer Portfolio

A modern, responsive portfolio website showcasing cloud development skills and AWS expertise, deployed on AWS S3 with static website hosting.

## 🌐 Live Demo

**Portfolio URL:** [http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com](http://christopher-corbin-portfolio-20251005195625.s3-website-us-east-1.amazonaws.com)

## 🎯 Features

### Design & User Experience
- **Modern Design** - Clean, professional layout with AWS color scheme
- **Fully Responsive** - Optimized for desktop, tablet, and mobile devices
- **Interactive Elements** - Smooth animations and hover effects
- **Performance Optimized** - Fast loading with lazy loading and optimized assets

### Sections
- **Hero Section** - Eye-catching introduction with animated typing effect
- **About Me** - Professional summary with statistics counter animation
- **Skills & Technologies** - Organized display of AWS services, programming languages, and tools
- **Featured Projects** - Showcase of key projects with technology tags
- **Contact Form** - Interactive form with validation (ready for backend integration)

### Technical Features
- **Vanilla JavaScript** - No framework dependencies for fast loading
- **CSS Grid & Flexbox** - Modern layout techniques
- **Font Awesome Icons** - Professional iconography
- **Google Fonts** - Typography optimized for readability
- **SEO Optimized** - Proper meta tags and semantic HTML

## 🏗️ Architecture

### AWS Services Used
- **Amazon S3** - Static website hosting
- **S3 Website Endpoint** - Public web access
- **IAM Policies** - Secure bucket configuration

### File Structure
```
AWS-eportfolio/
├── index.html          # Main HTML structure
├── styles.css          # CSS styling and responsive design
├── script.js           # JavaScript functionality
├── deploy.sh           # Deployment automation script
├── README.md           # Project documentation
└── bucket-policy.json  # S3 bucket policy template
```

## 🚀 Deployment

### Prerequisites
- AWS CLI installed and configured
- AWS account with S3 access
- Basic familiarity with command line

### Quick Deploy
```bash
# Clone or download the project
cd AWS-eportfolio

# Make deployment script executable
chmod +x deploy.sh

# Deploy to AWS S3
./deploy.sh
```

### Manual Deployment Steps

1. **Create S3 Bucket**
   ```bash
   BUCKET_NAME="your-portfolio-bucket-name"
   aws s3 mb s3://$BUCKET_NAME
   ```

2. **Configure Static Website Hosting**
   ```bash
   aws s3api put-bucket-website --bucket $BUCKET_NAME --website-configuration '{
       "IndexDocument": {"Suffix": "index.html"},
       "ErrorDocument": {"Key": "index.html"}
   }'
   ```

3. **Set Public Access**
   ```bash
   aws s3api put-public-access-block --bucket $BUCKET_NAME \
     --public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false
   ```

4. **Apply Bucket Policy**
   ```bash
   # Update bucket-policy.json with your bucket name
   aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy.json
   ```

5. **Upload Files**
   ```bash
   aws s3 sync . s3://$BUCKET_NAME --exclude "*.json" --exclude "*.md" --exclude "*.sh"
   ```

## 💰 Cost Breakdown

### Monthly Costs (Estimated)
- **S3 Storage**: ~$0.01-0.05 (for small website files)
- **S3 Requests**: ~$0.01-0.10 (GET requests for visitors)
- **Data Transfer**: ~$0.50-2.00 (depends on traffic)

**Total Monthly Cost: $1-3 USD** for typical portfolio traffic

### Cost Optimization Tips
- Use CloudFront CDN for better performance and potentially lower costs
- Enable S3 Transfer Acceleration for global visitors
- Monitor usage with AWS Cost Explorer

## 🔧 Customization Guide

### Personal Information
Update the following in `index.html`:
- Name and title in hero section
- About me content
- Skills and technologies
- Project information
- Contact details

### Styling
Modify `styles.css`:
- Color scheme in CSS variables (`:root` section)
- Typography and spacing
- Layout and responsive breakpoints

### Functionality
Enhance `script.js`:
- Add contact form backend integration
- Implement analytics tracking
- Add more interactive features

## 🚀 Enhancement Ideas

### Phase 1 - Basic Enhancements
- [ ] Add a blog section using AWS Lambda + DynamoDB
- [ ] Integrate contact form with AWS SES
- [ ] Add visitor counter with AWS Lambda + DynamoDB
- [ ] Implement dark/light theme toggle

### Phase 2 - Advanced Features
- [ ] Set up CloudFront CDN distribution
- [ ] Add custom domain with Route 53
- [ ] Implement CI/CD with AWS CodePipeline
- [ ] Add SSL certificate with AWS Certificate Manager

### Phase 3 - Full Stack Integration
- [ ] Build admin panel for content management
- [ ] Add authentication with AWS Cognito
- [ ] Implement real-time chat with AWS WebSocket API
- [ ] Create portfolio analytics dashboard

## 🛠️ Technologies Used

### Frontend
- **HTML5** - Semantic structure
- **CSS3** - Modern styling with Grid and Flexbox
- **Vanilla JavaScript** - Interactive functionality
- **Font Awesome** - Icons
- **Google Fonts** - Typography

### AWS Services
- **Amazon S3** - Static website hosting
- **AWS CLI** - Deployment automation

### Development Tools
- **VS Code** - Code editor
- **Chrome DevTools** - Testing and debugging
- **Git** - Version control

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

- **Email:** your.email@example.com
- **LinkedIn:** [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- **GitHub:** [github.com/yourusername](https://github.com/yourusername)

---

**Built with ❤️ using AWS services**

*This portfolio demonstrates practical AWS knowledge and modern web development skills, perfect for showcasing cloud development capabilities to potential employers and clients.*