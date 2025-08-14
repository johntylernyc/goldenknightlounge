# Deployment Guide

## Prerequisites

1. GitHub repository
2. Replit account
3. Cloudflare account (for domain management)
4. PostgreSQL database (Replit provides this)

## Step 1: GitHub Repository Setup

1. Create a new repository on GitHub
2. Push this code to the repository:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/goldenknightlounge.git
git push -u origin main
```

3. Create staging branch:
```bash
git checkout -b staging
git push -u origin staging
```

## Step 2: Replit Configuration

### Production Environment

1. Go to [Replit](https://replit.com)
2. Create new Repl → Import from GitHub
3. Select your repository and `main` branch
4. Name it `goldenknightlounge`
5. Go to Deployments → Configure
6. Set run command: `bash scripts/start.sh`
7. Add secrets (Deployments → Secrets):
   - All variables from `.env.example`
   - Set `NODE_ENV=production`
   - Set proper `DATABASE_URL` (auto-provisioned)
   - Configure `CORS_ORIGINS` and `ALLOWED_HOSTS`

### Staging Environment

1. Create another Repl
2. Import same repository but select `staging` branch
3. Name it `goldenknightlounge-staging`
4. Go to Deployments → Configure
5. Set run command: `bash scripts/start.sh`
6. Add secrets with staging values:
   - Set `NODE_ENV=staging`
   - Use separate staging database (auto-provisioned)

## Step 3: Domain Configuration (Cloudflare)

### Production Domain

1. Log into Cloudflare Dashboard
2. Select your domain (goldenknightlounge.com)
3. Go to DNS settings
4. Add records:
   ```
   Type: CNAME
   Name: @
   Target: goldenknightlounge-johntylernyc.replit.app
   Proxy: ON (orange cloud)
   
   Type: CNAME
   Name: www
   Target: goldenknightlounge-johntylernyc.replit.app
   Proxy: ON (orange cloud)
   ```

### Staging Domain (Optional)

1. Add subdomain record:
   ```
   Type: CNAME
   Name: staging
   Target: goldenknightlounge-staging-johntylernyc.replit.app
   Proxy: ON (orange cloud)
   ```

## Step 4: Replit Domain Connection

### For each Replit project:

1. Go to your Repl
2. Navigate to Deployments tab
3. Click on Settings
4. Add custom domain:
   - Production: `goldenknightlounge.com` and `www.goldenknightlounge.com`
   - Staging: `staging.goldenknightlounge.com`
5. Replit will verify DNS configuration

## Step 5: Enable Always On (Production)

1. In production Repl Deployments settings
2. Enable "Always On" (requires paid Replit plan)
3. This ensures your app doesn't sleep

## Step 6: Database Setup

### PostgreSQL on Replit

1. PostgreSQL is auto-provisioned for Deployments
2. Database URL is automatically set as `DATABASE_URL`
3. Separate databases for staging and production

## Step 7: Verify Deployment

### Check endpoints:

1. Production:
   - https://goldenknightlounge.com/health
   - https://goldenknightlounge.com/api/health

2. Staging:
   - https://staging.goldenknightlounge.com/health
   - https://staging.goldenknightlounge.com/api/health

## Troubleshooting

### Domain not working
- Wait 5-10 minutes for DNS propagation
- Verify CNAME records in Cloudflare
- Check Replit domain settings
- Ensure SSL/TLS is set to "Flexible" in Cloudflare

### App not starting
- Check Replit console for errors
- Verify all secrets are set
- Check `.replit` and `replit.nix` configuration
- Review `scripts/start.sh` for issues

### CORS errors
- Update `CORS_ORIGINS` in secrets
- Include all domain variations
- Check backend CORS configuration

## Ongoing Deployment Process

### Development to Staging Workflow

#### Step 1: Make Changes Locally
```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Make your changes
# Test locally
# Commit changes
git add .
git commit -m "Your commit message"
```

#### Step 2: Deploy to Staging
```bash
# Push feature branch to GitHub
git push origin feature/your-feature-name

# Create PR to staging branch on GitHub
# OR merge directly to staging for quick testing:
git checkout staging
git merge feature/your-feature-name
git push origin staging
```

#### Step 3: Automatic Staging Deployment
- **GitHub Actions**: Automatically runs tests when you push to staging
- **Replit Staging**: Automatically deploys when staging branch is updated
- **No manual action needed in Replit** - it auto-deploys on git push

#### Step 4: Verify Staging Deployment
1. Check GitHub Actions tab for build status
2. Visit https://staging.goldenknightlounge.com (or staging Replit URL)
3. Test your changes in staging environment
4. Check Replit staging console for any errors

### Keeping Staging in Sync with Main

Before deploying new features to staging, ensure staging has all production changes:

#### Option 1: Merge Main into Staging (Recommended)
```bash
# Ensure you have latest main
git checkout main
git pull origin main

# Merge main into staging
git checkout staging
git pull origin staging
git merge main

# Resolve any conflicts if they exist
# Then push the updated staging branch
git push origin staging
```

#### Option 2: Reset Staging to Main (Clean Slate)
```bash
# WARNING: This will discard any staging-only changes
git checkout main
git pull origin main

# Force staging to match main exactly
git checkout staging
git reset --hard main
git push origin staging --force
```

#### Option 3: Via GitHub UI
1. Go to your repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Set base: `staging`, compare: `main`
4. Create and merge the PR to bring main changes into staging

### Staging to Production Workflow

#### Step 1: Create Pull Request
```bash
# On GitHub, create PR from staging to main
# OR via CLI:
gh pr create --base main --head staging --title "Deploy to production"
```

#### Step 2: Review and Merge
1. Review changes in PR
2. Ensure all CI checks pass
3. Merge PR on GitHub (this triggers production deployment)

#### Step 3: Automatic Production Deployment
- **GitHub Actions**: Runs final tests on main branch
- **Replit Production**: Automatically deploys when main branch is updated
- **No manual action needed in Replit** - it auto-deploys on merge

#### Step 4: Verify Production Deployment
1. Check GitHub Actions tab for deployment status
2. Visit https://goldenknightlounge.com
3. Monitor for any issues

### Quick Reference: What Happens Where

| Action | GitHub | Replit |
|--------|--------|--------|
| Push to `staging` | CI/CD tests run | Auto-deploys to staging |
| Merge to `main` | CI/CD tests run | Auto-deploys to production |
| Manual deployment | Not needed | Not needed (auto-deploy) |
| View logs | Actions tab | Deployments → Logs |
| Check status | Actions tab | Deployments → Status |

### Rollback Process

If something goes wrong in production:

#### Option 1: Quick Revert (Recommended)
```bash
# Revert the last commit on main
git checkout main
git pull origin main
git revert HEAD
git push origin main
# This auto-deploys the reverted version
```

#### Option 2: Deploy Previous Version
1. Go to Replit production project
2. Deployments → History
3. Find previous working deployment
4. Click "Redeploy" on that version

### Monitoring Your Deployments

#### GitHub Side
- **Actions Tab**: Shows CI/CD pipeline status
- **Pull Requests**: Shows test results before merge
- **Insights → Actions**: Shows deployment history

#### Replit Side
- **Deployments Tab**: Shows current deployment status
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, request metrics
- **Domains**: Verify custom domains are connected

### Common Deployment Scenarios

#### Hotfix to Production
```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-fix

# Make fix
git add .
git commit -m "Fix: critical issue"

# Skip staging for critical fixes
git checkout main
git merge hotfix/critical-fix
git push origin main
```

#### Feature Development
```bash
# Feature → Staging → Production
git checkout -b feature/new-feature
# develop...
git push origin feature/new-feature
# PR to staging → test → PR to main
```

#### Configuration Changes
- Update secrets in Replit Deployments → Secrets
- Changes take effect on next deployment
- Force redeploy: Deployments → Redeploy button

## Maintenance

### Regular Maintenance Tasks
- Weekly: Review deployment logs for errors
- Monthly: Check and update dependencies
- Quarterly: Review and optimize deployment performance

### Monitoring
- Check Replit deployment status dashboard
- Monitor GitHub Actions for build failures
- Set up external monitoring (UptimeRobot, Pingdom)