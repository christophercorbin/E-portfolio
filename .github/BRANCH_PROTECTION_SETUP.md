# Branch Protection Rules Setup

## Steps to Configure Branch Protection on GitHub

1. **Navigate to Repository Settings**
   - Go to your GitHub repository: `https://github.com/YOUR_USERNAME/AWS-eportfolio`
   - Click **Settings** tab
   - Click **Branches** in the left sidebar

2. **Add Branch Protection Rule for `main`**
   - Click **Add rule** button
   - Branch name pattern: `main`

3. **Configure Protection Settings**

   ### Required Settings:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: `1`
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Add status checks (workflows that must pass):
       - `deploy-backend-dev`
       - `deploy-frontend-dev`
       - `test-backend` (we'll create this)
       - `lint-and-format` (we'll create this)
   
   - ✅ **Require conversation resolution before merging**
   
   - ✅ **Do not allow bypassing the above settings**
   
   ### Optional but Recommended:
   - ✅ **Require linear history** (prevents merge commits)
   - ✅ **Require deployments to succeed before merging**
   - ✅ **Lock branch** (if you want to prevent all pushes)

4. **Save Changes**
   - Click **Create** or **Save changes**

## Verification

After setup, attempting to push directly to `main` will fail:
```bash
git push origin main
# Error: protected branch hook declined
```

All changes must now go through pull requests with:
- At least 1 approval
- All status checks passing
- All conversations resolved

## Notes

- Repository admins can still override these rules (but shouldn't!)
- Consider adding CODEOWNERS file for automatic reviewer assignment
- These rules apply to everyone, including repo owners (unless bypass is enabled)
