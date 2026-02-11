# Site Scan Report

**URL**: https://christophercorbin.cloud
**Date**: 2026-02-09
**Method**: curl header inspection + manual review

## Security Headers

| Header | Status | Finding |
|--------|--------|---------|
| Strict-Transport-Security (HSTS) | MISSING | CloudFront serves over HTTPS but does not send HSTS header. Browsers can be downgraded to HTTP. |
| Content-Security-Policy (CSP) | MISSING | No CSP header. The site loads scripts from cdnjs, googleapis, credly, and html2pdf - all should be whitelisted. |
| X-Content-Type-Options | MISSING | Without `nosniff`, browsers may MIME-sniff responses into executable types. |
| X-Frame-Options | MISSING | Site can be embedded in iframes on any domain (clickjacking risk). |
| Referrer-Policy | MISSING | Browser default leaks full URL to third parties. |
| Permissions-Policy | MISSING | Browser features (camera, microphone, geolocation) not restricted. |

### Remediation

All headers can be added via a **CloudFront Response Headers Policy** (no code changes required). Recommended policy:

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com https://cdn.credly.com https://fonts.googleapis.com https://www.credly.com 'unsafe-inline'; style-src 'self' https://cdnjs.cloudflare.com https://fonts.googleapis.com 'unsafe-inline'; font-src https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' https://images.credly.com data:; frame-src https://www.credly.com; connect-src 'self' https://*.execute-api.us-east-1.amazonaws.com
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

**How to apply**: AWS Console > CloudFront > Distribution E34Q2E7TZIYZAB > Behaviors > Edit > Response headers policy > Create/attach custom policy with the headers above.

## Response Headers (Current)

```
HTTP/2 200
content-type: text/html
server: AmazonS3
x-amz-server-side-encryption: AES256
cache-control: image/*:max-age=31536000
x-cache: Miss from cloudfront
```

### Issues

- **`server: AmazonS3`** - Leaks server technology. Can be suppressed via CloudFront response headers policy (`Server` override).
- **`cache-control: image/*:max-age=31536000`** - Incorrect syntax. The `s3 sync --cache-control` flag doesn't work as a content-type filter this way. HTML is getting image cache headers. HTML should use `max-age=300` (5 min) and CSS/JS should use content-hashed names or short cache times.

## Lighthouse Scores

Lighthouse was not run in CI (requires Chrome). To run locally:

```bash
# Install
npm install -g lighthouse

# Run against deployed site
lighthouse https://christophercorbin.cloud --output html --output-path ./docs/audits/lighthouse-report.html

# Quick CLI view
lighthouse https://christophercorbin.cloud --output json --quiet | jq '{performance: .categories.performance.score, accessibility: .categories.accessibility.score, bestPractices: .categories["best-practices"].score, seo: .categories.seo.score}'
```

## Priority Fixes

| Priority | Issue | Impact | Effort |
|----------|-------|--------|--------|
| High | Add CloudFront response headers policy (all 6 security headers) | Security | Low (Console config) |
| High | Fix S3 sync cache-control flags in deploy workflow | Performance | Low (workflow edit) |
| Medium | Suppress `server: AmazonS3` header | Security | Low (Console config) |
| Low | Run Lighthouse and address findings | Performance/SEO | Medium |
