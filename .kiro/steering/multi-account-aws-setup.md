---
inclusion: always
---

# Multi-Account AWS Setup - Portfolio Project

## Account Structure

This project uses a multi-account AWS Organization setup following AWS best practices:

### Account Inventory

1. **Development Account (934862608865)**
   - Purpose: Development, testing, and experimentation
   - Environment: dev
   - Resources: Dev S3 buckets, Lambda functions, API Gateway, DynamoDB tables
   - Cost: Low priority, can be torn down/rebuilt
   - Access: Developers have broader permissions for testing

2. **Production Account (590716168923)**
   - Purpose: Live production workloads
   - Environment: prod
   - Resources: Production S3 buckets, Lambda functions, API Gateway, DynamoDB tables, CloudFront
   - Cost: High priority, always available
   - Access: Restricted, requires approval for changes

3. **Management Account (438465156498)** 
   - Purpose: AWS Organization management, billing consolidation
   - Resources: CloudFront distributions, Route53 (shared services)
   - Access: Highly restricted, admin only
   - Note: Some legacy resources like CloudFront may reside here

## Deployment Strategy

### Branch-to-Account Mapping

- **develop, dev-backend-integration** → Development Account (934862608865)
- **main, master** → Production Account (590716168923)

### OIDC Authentication

All GitHub Actions workflows use OIDC (OpenID Connect) for secure, temporary credential access:

- **Dev Role**: `arn:aws:iam::934862608865:role/GitHubActionsDeployRole`
- **Prod Role**: `arn:aws:iam::590716168923:role/GitHubActionsDeployRole`

### Resource Naming Convention

All resources MUST follow this naming pattern:
```
christopher-corbin-portfolio-{component}-{environment}
```

Examples:
- `christopher-corbin-portfolio-backend-dev` (Dev stack)
- `christopher-corbin-portfolio-backend` (Prod stack)
- `christopher-corbin-portfolio-dev-20251006` (Dev S3 bucket)
- `christopher-corbin-portfolio-20251005195625` (Prod S3 bucket)

## Security Best Practices

### 1. Least Privilege Access

Each account role has ONLY the permissions needed for its environment:

- **Development**: Broader permissions for experimentation, can create/delete resources
- **Production**: Restricted to deployment operations only, no deletion of critical resources

### 2. Resource Isolation

- Dev and Prod resources are completely isolated in separate AWS accounts
- No cross-account access unless explicitly configured
- Prevents accidental production changes during development

### 3. Cost Management

- Development resources can be torn down when not in use
- Production resources are protected from deletion
- Separate billing allows cost tracking per environment

### 4. Compliance & Auditing

- All actions are logged in CloudTrail per account
- OIDC provides full audit trail of GitHub Actions
- No long-lived credentials stored in GitHub secrets

## IAM Policy Requirements

### Development Account Policies

The GitHubActionsDeployRole in the dev account (934862608865) needs:

1. **S3 Access**: Full CRUD on dev buckets
2. **CloudFormation**: Create/update/delete stacks with `*-dev` suffix
3. **Lambda**: Full management of dev Lambda functions
4. **API Gateway**: Full management of dev APIs
5. **DynamoDB**: Full management of dev tables
6. **IAM**: Create/manage Lambda execution roles for dev

### Production Account Policies

The GitHubActionsDeployRole in the prod account (590716168923) needs:

1. **S3 Access**: CRUD on prod buckets (NO DeleteBucket)
2. **CloudFormation**: Create/update stacks (limited delete)
3. **Lambda**: Deploy and update prod Lambda functions
4. **API Gateway**: Update prod APIs
5. **DynamoDB**: Create/update prod tables (NO DeleteTable without approval)
6. **IAM**: Limited role management for Lambda execution

### Management Account Policies

For CloudFront operations (if needed):
- CloudFront invalidation permissions
- Route53 DNS management (if applicable)

## Workflow Configuration Rules

### 1. Account-Specific Workflows

Each workflow MUST specify the correct account role:

```yaml
# Development workflows
- name: Configure AWS credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::934862608865:role/GitHubActionsDeployRole
    aws-region: us-east-1
    role-session-name: GitHubActions-Dev{Component}

# Production workflows  
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::590716168923:role/GitHubActionsDeployRole
    aws-region: us-east-1
    role-session-name: GitHubActions-Prod{Component}
```

### 2. Environment Protection

- Production deployments require manual approval (GitHub Environments)
- Development deployments are automatic on push
- All deployments include verification steps

### 3. Stack Naming

SAM/CloudFormation stacks MUST use environment-specific names:

```toml
# samconfig-dev.toml
stack_name = "christopher-corbin-portfolio-backend-dev"

# samconfig.toml (production)
stack_name = "christopher-corbin-portfolio-backend"
```

## Cross-Account Considerations

### Shared Resources

Some resources may be shared across accounts:

1. **CloudFront Distribution**: Currently in management account (438465156498)
   - Distribution ID: E34Q2E7TZIYZAB
   - Requires cross-account S3 bucket policy for origin access

2. **Route53 Hosted Zone**: Likely in management or production account
   - Domain: christophercorbin.cloud
   - DNS records point to appropriate environment

### S3 Bucket Policies

Production S3 buckets need policies allowing CloudFront OAI access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontOAI",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {OAI-ID}"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::christopher-corbin-portfolio-20251005195625/*"
    }
  ]
}
```

## Troubleshooting Multi-Account Issues

### Issue: "Access Denied" during deployment

**Check:**
1. Verify you're using the correct account role ARN
2. Confirm the role exists in the target account
3. Check the role's trust policy allows GitHub OIDC
4. Verify the role has required permissions

### Issue: CloudFormation stack not found

**Check:**
1. Confirm you're deploying to the correct AWS account
2. Verify stack name matches the environment (dev vs prod)
3. Check the region (should be us-east-1)

### Issue: S3 bucket access denied

**Check:**
1. Bucket exists in the account you're deploying to
2. Role has s3:ListBucket and s3:PutObject permissions
3. Bucket name matches the environment

### Issue: CloudFront invalidation fails

**Check:**
1. CloudFront distribution is in management account (438465156498)
2. You may need a separate role or cross-account access
3. Current setup may need adjustment for multi-account

## Migration Checklist

When adding new resources or modifying existing ones:

- [ ] Determine which account the resource belongs in (dev/prod/management)
- [ ] Update IAM policies in the correct account
- [ ] Use environment-specific naming conventions
- [ ] Update workflow files with correct role ARN
- [ ] Test in development account first
- [ ] Document any cross-account dependencies
- [ ] Update this steering document with new patterns

## Cost Optimization

### Development Account
- Use smaller instance sizes
- Enable auto-shutdown for non-critical resources
- Clean up old stacks regularly
- Consider using AWS Lambda for compute (pay per use)

### Production Account
- Right-size resources based on actual usage
- Enable S3 Intelligent-Tiering
- Use CloudFront caching to reduce origin requests
- Monitor costs with AWS Cost Explorer

## Compliance Notes

- All accounts are part of the same AWS Organization
- Consolidated billing through management account
- Service Control Policies (SCPs) may apply organization-wide
- Ensure compliance with any organizational policies
- CloudTrail logging enabled in all accounts

## Future Enhancements

Consider implementing:

1. **Staging Account**: Add a third account for pre-production testing
2. **Shared Services Account**: Centralize common resources (monitoring, logging)
3. **Cross-Account CI/CD**: Use AWS CodePipeline for more complex deployments
4. **Infrastructure as Code**: Manage account setup with AWS CDK or Terraform
5. **Automated Testing**: Add integration tests that run in dev before prod deployment

---

**Last Updated**: February 12, 2026
**Maintained By**: Christopher Corbin
**Review Frequency**: Quarterly or when adding new AWS accounts
