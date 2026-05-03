# CLAUDE.md — Christopher Corbin E-Portfolio

## Project Overview

Personal portfolio website for Christopher Corbin, AWS Solutions Architect & Security Engineer.  
**Live URL**: https://christophercorbin.cloud  
**GitHub**: https://github.com/christophercorbin/AWS-eportfolio  

The site is a **pure static frontend** (no build step, no framework) backed by a **serverless AWS contact form** (Lambda + API Gateway + SES + DynamoDB), deployed via GitHub Actions CI/CD to a multi-account AWS setup.

---

## Repository Structure

```
E-portfolio/
├── index.html                  # Main portfolio page (single page, all sections)
├── resume.html                 # Standalone resume page
├── styles.css                  # All site styles
├── script.js                   # All site JS (nav, animations, contact form)
├── config.js                   # Prod config: API URL, form settings, feature flags
├── config-dev.js               # Dev config: points to dev API, adds dev banner
├── assets/
│   └── Christopher_Corbin_Resume.pdf
├── images/
│   └── profile-photo.jpg
├── src/
│   └── contact_handler.py      # Lambda handler (Python 3.9)
├── infrastructure/
│   ├── template.yaml           # AWS SAM template (API GW + Lambda + DynamoDB)
│   ├── samconfig.toml          # SAM deploy config (prod)
│   ├── samconfig-dev.toml      # SAM deploy config (dev)
│   └── *.sh / *.yaml           # Infrastructure scripts & CloudFormation templates
├── aws-config/                 # IAM policy JSON files
├── .github/
│   └── workflows/
│       ├── deploy-frontend-prod.yml   # S3 sync + CloudFront invalidation (prod)
│       ├── deploy-frontend-dev.yml    # S3 sync (dev)
│       ├── deploy-backend-prod.yml    # SAM deploy (prod)
│       ├── deploy-backend-dev.yml     # SAM deploy (dev)
│       ├── security-scan.yml          # Bandit, Checkov, TruffleHog, CodeQL, Safety
│       ├── test-frontend.yml          # ESLint + Prettier
│       └── test-backend.yml           # Python unit tests
├── tests/
│   └── integration/
│       └── test_deployed_api.py       # Integration tests run post-deploy
├── docs/                       # Architecture and runbook docs
└── package.json                # ESLint + Prettier devDeps; npm test = lint + format check
```

---

## Architecture

### Multi-Account AWS Setup

```
Management Account (438465156498)
  ├── CloudFront Distribution: E34Q2E7TZIYZAB
  │     URL: d30iyriy15xq9k.cloudfront.net
  └── Route 53: christophercorbin.cloud

Prod Account (590716168923)
  ├── S3 Bucket: christopher-corbin-portfolio-20251005195625
  ├── Lambda: christopher-corbin-portfolio-backend-contact-form
  ├── API Gateway: 9rau1nnkg3 (prod contact endpoint)
  └── DynamoDB: christopher-corbin-portfolio-backend-submissions

Dev Account (934862608865)
  ├── S3 Bucket: (dev bucket)
  ├── Lambda: (dev contact form)
  └── API Gateway: cdmwb9tdlj (dev contact endpoint)
```

CloudFront (management account) → S3 via OAC (prod account). Cross-account role assumption is required for cache invalidation — see `docs/CROSS-ACCOUNT-CLOUDFRONT-SETUP.md`.

### Backend (Contact Form)

```
Browser → API Gateway → Lambda (contact_handler.py)
                              ├── DynamoDB (store submission, 30-day TTL)
                              └── SES (email notification to christophercorbin24@gmail.com)
```

SAM stack name: `christopher-corbin-portfolio-backend`  
Prod API: `https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact`  
Dev API:  `https://cdmwb9tdlj.execute-api.us-east-1.amazonaws.com/prod/contact`

---

## CI/CD Pipelines

All pipelines use **OIDC authentication** — no long-lived AWS keys stored in GitHub.

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy-frontend-prod.yml` | Push to `main` | Syncs static files to prod S3, invalidates CloudFront |
| `deploy-backend-prod.yml` | Push to `main` (infra/src changes) | SAM build + deploy to prod, runs integration tests |
| `deploy-frontend-dev.yml` | Push to `dev-*` branches | Syncs to dev S3 |
| `deploy-backend-dev.yml` | Push to `dev-*` branches | SAM deploy to dev |
| `security-scan.yml` | Push to main + weekly Monday 9AM UTC | Bandit, Safety, Checkov, TruffleHog, CodeQL |
| `test-frontend.yml` | PRs | ESLint + Prettier check |
| `test-backend.yml` | PRs | Python unit tests |

**Required GitHub secrets**: `CONTACT_EMAIL`, `CLOUDFRONT_ROLE_ARN`, `CLOUDFRONT_EXTERNAL_ID`, `CLOUDFRONT_DOMAIN`

---

## Local Development

### Frontend

No build step. Edit `index.html`, `styles.css`, `script.js` directly and open in browser.

To test against the **dev backend**, swap `config.js` for `config-dev.js` (or point `script.js` at the dev API URL). The dev config adds an orange banner to the page so you know you're in dev mode.

### Backend

```bash
# Install Python deps
pip install -r requirements-dev.txt

# Build and run Lambda locally
cd infrastructure
sam build
sam local start-api --env-vars env.json

# Run integration tests against a deployed endpoint
export API_URL=https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact
pytest tests/integration/test_deployed_api.py -v
```

### JS Linting & Formatting

```bash
npm install
npm run lint          # ESLint
npm run lint:fix      # ESLint with auto-fix
npm run format        # Prettier (writes)
npm run format:check  # Prettier (check only)
npm test              # lint + format:check
```

### Python Linting & Security

```bash
bandit -r src/        # Security scan
pylint src/           # Linting
```

---

## Key Files to Know

- **`index.html`** — Single-page portfolio with nav, hero, about, experience, skills, projects, certifications, and contact sections. All content lives here.
- **`config.js`** — Controls which API endpoint the contact form uses and feature flags. Edit here when the API URL changes.
- **`script.js`** — Contact form submission logic (fetch to API GW), mobile nav toggle, scroll animations, stats counter, notification system.
- **`src/contact_handler.py`** — Lambda entry point. Validates input, stores to DynamoDB, sends SES email. CORS headers are set here.
- **`infrastructure/template.yaml`** — SAM template defining Lambda, API GW, DynamoDB. Modify here to change backend infrastructure.

---

## Deployment Notes

### Deploying Frontend (manual)

```bash
aws s3 sync . s3://christopher-corbin-portfolio-20251005195625 \
  --exclude "*.json" --exclude "*.sh" --exclude "*.md" \
  --exclude ".git/*" --exclude "node_modules/*" --exclude "docs/*" \
  --exclude "aws-config/*" --exclude "infrastructure/*" --exclude "src/*" \
  --exclude "tests/*" --cache-control "max-age=300"

# Long-cache for static assets
aws s3 sync . s3://christopher-corbin-portfolio-20251005195625 \
  --exclude "*" --include "*.css" --include "*.js" --include "*.jpg" \
  --include "*.png" --include "*.pdf" --cache-control "max-age=31536000"
```

### Invalidating CloudFront (requires management account credentials)

```bash
aws cloudfront create-invalidation \
  --distribution-id E34Q2E7TZIYZAB \
  --paths '/*'
```

### Deploying Backend (manual)

```bash
cd infrastructure
sam build
sam deploy --config-file samconfig.toml   # prod
sam deploy --config-file samconfig-dev.toml  # dev
```

---

## Content Sections (index.html)

| Section ID | Content |
|---|---|
| `#home` | Hero with name, title, CTA buttons, profile photo |
| `#about` | Bio paragraph + key stats (2000+ resources, 500+ CVEs, 97.2% SOC 2) |
| `#experience` | Timeline: GovTech Barbados, Protexxa, TORE, iShop |
| `#skills` | 8 skill categories + achievements grid |
| `#projects` | 3 project cards: SOC2 ML Analyzer, Task Management, Secure Moodle |
| `#certifications` | AWS SAA, CompTIA Sec+, Cybersecurity Analyst, BSc CS, AWS DevOps Pro (in progress) + Cisco badges |
| `#contact` | Contact info + live contact form (posts to API GW) |

Credly badges are embedded via `//cdn.credly.com/assets/utilities/embed.js`.  
Fonts: Inter (Google Fonts). Icons: Font Awesome 6.

---

## Gotchas & Known Patterns

- **No framework or bundler** — changes to HTML/CSS/JS are immediate. Do not introduce npm build tools or transpilation without updating the CI/CD workflows.
- **CloudFront is in a different AWS account** than S3 — cross-account role assumption is needed for cache invalidation. If `CLOUDFRONT_ROLE_ARN` secret is missing, the pipeline skips invalidation and prints manual instructions.
- **CORS** — The Lambda currently allows `*` for all origins. If locking down to the prod domain, update `CORS_ORIGIN` env var in SAM template and the `cors_headers` dict in `contact_handler.py`.
- **SES** — The `christophercorbin24@gmail.com` address must be verified in SES in `us-east-1` on the prod account for emails to send.
- **DynamoDB TTL** — Submissions auto-expire after 30 days. This is intentional for GDPR alignment.
- **S3 cache headers** — HTML is served with `max-age=300` (5 min); CSS/JS/images with `max-age=31536000` (1 year). After a deploy, CloudFront invalidation is needed for users to see HTML changes immediately.
- **`config.js` is checked into git** — It contains the public API URL (not a secret). Do not put credentials or secrets in this file.
