# Workflow Audit & Rationale

**Date**: 2026-02-09

## Workflow Inventory

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `deploy-frontend-prod.yml` | push to `main` | Sync static files to prod S3, invalidate CloudFront |
| `deploy-frontend-dev.yml` | push to `dev-backend-integration` | Sync static files to dev S3 bucket |
| `deploy-backend-prod.yml` | push to `main` (infra/src paths) | SAM build + deploy Lambda backend to prod |
| `deploy-backend-dev.yml` | push to `dev-backend-integration` (infra/src paths) | SAM build + deploy Lambda backend to dev |
| `security-scan.yml` | push, PR, weekly schedule | Bandit, npm audit, Checkov, TruffleHog, CodeQL |
| `test-backend.yml` | push (Python paths) | pytest, Black, flake8, pylint, mypy |
| `test-frontend.yml` | push (JS/HTML/CSS paths) | ESLint, Prettier, HTML validation |

## Changes Made

### 1. Added `permissions: read-all` (or narrower) to all workflows

**Why**: Without an explicit `permissions` block, GitHub Actions defaults to read-write for all scopes. This violates the principle of least privilege. If a workflow is compromised (e.g., via a malicious dependency), it could push code, create releases, or modify issues.

**Affected workflows**: All except `deploy-backend-dev.yml` (already had permissions).

### 2. Fixed S3 sync `--cache-control` syntax

**Why**: The `aws s3 sync --cache-control` flag accepts a single value, not content-type filters like `"text/html:max-age=300"`. The broken syntax caused all files to receive the last `--cache-control` value specified. HTML files were getting year-long cache headers, preventing visitors from seeing updates.

**Fix**: Split into multiple `aws s3 sync` commands — first sync all files with the default cache (short for HTML), then override CSS, JS, and images with longer cache durations using `--include`/`--exclude` filters.

### 3. Pinned action versions

| Action | Before | After | Why |
|--------|--------|-------|-----|
| `github/codeql-action/*` | `@v2` | `@v3` | v2 is deprecated and will stop receiving updates |
| `trufflesecurity/trufflehog` | `@main` | `@v3.82.13` | Pinning to `main` means every run uses unreviewed code |
| `codecov/codecov-action` | `@v3` | `@v4` | v3 is deprecated |

### 4. Removed `|| npm install` fallback from `npm ci`

**Why**: `npm ci` is designed to fail if `package-lock.json` is out of sync with `package.json`. The `|| npm install` fallback defeats this check and can introduce non-deterministic builds. If the lockfile is stale, CI should fail so the developer fixes it.

### 5. Removed `continue-on-error: true` from critical security steps

**Why**: When `continue-on-error: true` is set on Bandit and npm audit steps, real security vulnerabilities never fail the build. The scan results are only visible if someone manually checks workflow logs.

**Kept**: `continue-on-error: true` on informational steps (Checkov, safety) where false positives are common and the tools are advisory.

### 6. Fixed stale path trigger in `deploy-backend-dev.yml`

**Why**: The workflow referenced `.github/workflows/deploy-sam.yml` (an old filename) in its path trigger. Changed to `.github/workflows/deploy-backend-dev.yml` to match the actual filename.

## Known Issues (Not Fixed)

| Issue | Reason |
|-------|--------|
| `pylint --exit-zero` in test-backend.yml | Pylint generates many false positives on Lambda handlers; fixing requires substantial config work |
| `mypy || true` in test-backend.yml | mypy without type stubs for boto3 produces many errors; needs `boto3-stubs` package |
| Backend deploy tests create real DB entries | Requires a dedicated test table or mock; out of scope for this audit |
| Hard-coded S3 bucket/CloudFront IDs | These are not secrets (publicly discoverable), so acceptable in workflows |
