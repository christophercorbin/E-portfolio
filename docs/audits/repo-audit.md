# Repo Audit Report

**Date**: 2026-02-09
**Branch**: `dowldresume`

## Findings

| Severity | Finding | Fix | Status |
|----------|---------|-----|--------|
| High | `.gitignore` excludes `*.pdf` — blocks resume PDF commit | Added `!assets/Christopher_Corbin_Resume.pdf` exception | Fixed |
| High | `package.json` repo URL is placeholder `YOUR_USERNAME` | Updated to `christophercorbin/AWS-eportfolio` | Fixed |
| Medium | Footer says "2024" — outdated | Updated to "2025" | Fixed (Phase 4) |
| Medium | README has duplicate "Live Portfolio" section at bottom (lines 309-324) | Removed duplicate | Fixed |
| Medium | ESLint 8 is deprecated (warnings on install) | Pinned to `~8.57.1`; ESLint 9 migration is future work | Fixed |
| Low | No `test` script in package.json | Added `"test": "npm run lint && npm run format:check"` | Fixed |
| Low | 0 npm audit vulnerabilities | Documented as clean | N/A |

## npm audit

```
found 0 vulnerabilities
```

No action required.

## ESLint 9 Migration (Future Work)

ESLint 8.x is end-of-life but ESLint 9 requires a flat config (`eslint.config.js`) migration. Pinning to `~8.57.1` avoids breaking changes now. Migration steps when ready:

1. `npm install eslint@9 --save-dev`
2. Convert `.eslintrc.json` to `eslint.config.js` (flat config format)
3. Update `package.json` lint scripts if needed
4. Test all rules still apply correctly
