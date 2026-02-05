# Security Policy

## Supported Versions

Currently supported versions of this project:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do NOT** create a public GitHub issue
2. Email the details to: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond within 48 hours and will keep you updated on the fix progress.

## Security Scanning

This project implements multiple layers of security scanning:

### Automated Scans

All scans run automatically on:
- Every push to main/dev branches
- All pull requests
- Weekly scheduled scans (Mondays at 9 AM UTC)
- Manual workflow dispatch

### Scanning Tools

#### 1. **Bandit** - Python Security Scanner
- **Purpose**: Static analysis for Python code security issues
- **What it checks**: 
  - SQL injection vulnerabilities
  - Hard-coded credentials
  - Insecure crypto usage
  - Code execution risks
- **Configuration**: `.bandit`
- **Reports**: JSON artifacts in workflow runs

#### 2. **Safety** - Python Dependency Scanner
- **Purpose**: Checks Python dependencies for known vulnerabilities
- **What it checks**: CVE database for vulnerable packages
- **Runs on**: All Python dependencies in requirements

#### 3. **npm audit** - JavaScript Dependency Scanner
- **Purpose**: Checks npm packages for known vulnerabilities
- **What it checks**: npm advisory database
- **Threshold**: Moderate and above severity levels

#### 4. **Checkov** - Infrastructure Security Scanner
- **Purpose**: Scans CloudFormation/SAM templates
- **What it checks**:
  - Missing encryption
  - Overly permissive IAM policies
  - Insecure resource configurations
  - AWS best practices violations

#### 5. **TruffleHog** - Secrets Scanner
- **Purpose**: Detects accidentally committed secrets
- **What it checks**:
  - API keys
  - Passwords
  - Private keys
  - Tokens and credentials
- **Scans**: Full git history

#### 6. **CodeQL** - Advanced Code Analysis
- **Purpose**: Deep semantic code analysis
- **Languages**: Python, JavaScript
- **What it checks**:
  - SQL injection
  - XSS vulnerabilities
  - Path traversal
  - Code quality issues
- **Results**: GitHub Security tab

#### 7. **Dependabot** - Automated Dependency Updates
- **Purpose**: Keeps dependencies up-to-date
- **Frequency**: Weekly checks (Mondays)
- **Configuration**: `.github/dependabot.yml`
- **Auto-creates**: PRs for dependency updates

## Security Best Practices

### Code Development
- ✅ Never commit secrets or credentials
- ✅ Use environment variables for sensitive data
- ✅ Validate and sanitize all user inputs
- ✅ Use parameterized queries (prevent SQL injection)
- ✅ Keep dependencies updated
- ✅ Follow principle of least privilege for IAM

### AWS Resources
- ✅ Enable encryption at rest (DynamoDB, S3)
- ✅ Use HTTPS/TLS for all communications
- ✅ Implement proper CORS policies
- ✅ Use AWS Secrets Manager for sensitive data
- ✅ Enable CloudWatch logging
- ✅ Regular security audits

### CI/CD Pipeline
- ✅ All security scans must pass before merge
- ✅ Review dependency update PRs carefully
- ✅ Use branch protection rules
- ✅ Require code reviews
- ✅ Sign commits (optional but recommended)

## Reviewing Security Scan Results

### Accessing Reports

1. **GitHub Actions**:
   - Go to Actions tab
   - Click on "Security Scanning" workflow
   - Download artifacts for detailed reports

2. **Security Tab**:
   - CodeQL findings appear in Security → Code scanning alerts
   - Dependabot alerts in Security → Dependabot alerts

### Severity Levels

- **CRITICAL**: Address immediately
- **HIGH**: Address within 24-48 hours
- **MEDIUM**: Address within 1 week
- **LOW**: Address in next sprint

### False Positives

If a security finding is a false positive:
1. Document why it's a false positive
2. Add to ignore list in tool configuration
3. Include justification in PR comments

## Security Checklist for New Features

Before merging new code:

- [ ] No hardcoded secrets or credentials
- [ ] All user inputs validated and sanitized
- [ ] Dependencies scanned and up-to-date
- [ ] Security scans passing
- [ ] Appropriate error handling (no sensitive data in errors)
- [ ] Logging doesn't expose sensitive information
- [ ] IAM permissions follow least privilege
- [ ] Infrastructure changes reviewed with Checkov

## Incident Response

If a security incident occurs:

1. **Contain**: Disable affected systems if necessary
2. **Assess**: Determine scope and impact
3. **Notify**: Inform stakeholders
4. **Remediate**: Apply fixes
5. **Review**: Post-mortem and lessons learned
6. **Update**: Improve security measures

## Security Updates

Stay informed:
- Monitor GitHub Security Advisories
- Subscribe to AWS Security Bulletins
- Review Dependabot PRs promptly
- Check security scan results weekly

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [Python Security Guidelines](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Contact

For security concerns, contact: [your-email@example.com]

---

**Last Updated**: February 2026  
**Next Review**: Quarterly
