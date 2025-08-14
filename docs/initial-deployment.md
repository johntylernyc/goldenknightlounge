# Initial Deployment Setup Guide

This guide covers the one-time setup required to deploy the Golden Knight Lounge application to staging and production environments using GitHub and Replit.

## Prerequisites

- GitHub account with repository access
- Replit account (paid plan for production)
- Cloudflare account for domain management
- Yahoo Developer account for API access

## Step 1: GitHub Repository Setup

### 1.1 Initialize Repository
If starting fresh:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/goldenknightlounge.git
git push -u origin main
```

### 1.2 Create Branch Structure
```bash
# Create staging branch from main
git checkout -b staging
git push -u origin staging

# Create develop branch for integration
git checkout -b develop
git push -u origin develop
```

### 1.3 Configure Branch Protection (Recommended)
In GitHub repository settings:
1. Go to Settings → Branches
2. Add rule for `main`:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date
3. Add rule for `staging`:
   - Require status checks to pass

## Step 2: Replit Project Setup

### 2.1 Production Environment

1. **Create Production Repl**:
   - Go to [Replit](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Repository: `https://github.com/yourusername/goldenknightlounge`
   - Branch: `main`
   - Name: `goldenknightlounge`

2. **Configure Deployment**:
   - Navigate to Deployments tab
   - Click "Configure"
   - Run command: `bash scripts/start.sh`
   - Enable "Always On" (requires paid plan)

3. **Set Production Secrets**:
   Go to Deployments → Secrets and add:
   ```
   NODE_ENV=production
   DATABASE_URL=(auto-provisioned by Replit)
   
   # Yahoo OAuth
   YAHOO_CLIENT_ID=your_production_client_id
   YAHOO_CLIENT_SECRET=your_production_client_secret
   YAHOO_REDIRECT_URI=https://goldenknightlounge.com/api/auth/callback
   
   # Security
   FLASK_SECRET_KEY=(generate secure key)
   TOKEN_ENCRYPTION_KEY=(generate with Fernet)
   JWT_SECRET=(generate secure key)
   
   # Domains
   CUSTOM_DOMAIN=goldenknightlounge.com
   ALLOWED_HOSTS=goldenknightlounge.com,www.goldenknightlounge.com
   CORS_ORIGINS=https://goldenknightlounge.com,https://www.goldenknightlounge.com
   
   # Feature Flags
   ENABLE_LIVE_STATS=true
   ENABLE_DEBUG_LOGGING=false
   ```

### 2.2 Staging Environment

1. **Create Staging Repl**:
   - Create new Repl → "Import from GitHub"
   - Same repository
   - Branch: `staging`
   - Name: `goldenknightlounge-staging`

2. **Configure Deployment**:
   - Same as production but different secrets
   - Can use free tier initially

3. **Set Staging Secrets**:
   ```
   NODE_ENV=staging
   DATABASE_URL=(separate staging database)
   
   # Yahoo OAuth (staging app)
   YAHOO_CLIENT_ID=your_staging_client_id
   YAHOO_CLIENT_SECRET=your_staging_client_secret
   YAHOO_REDIRECT_URI=https://staging.goldenknightlounge.com/api/auth/callback
   
   # Same security keys as production
   # Different domain configuration
   CUSTOM_DOMAIN=staging.goldenknightlounge.com
   ALLOWED_HOSTS=staging.goldenknightlounge.com
   CORS_ORIGINS=https://staging.goldenknightlounge.com
   
   # Feature Flags
   ENABLE_LIVE_STATS=false
   ENABLE_DEBUG_LOGGING=true
   ```

## Step 3: Domain Configuration (Cloudflare)

### 3.1 Production Domain Setup

1. **Log into Cloudflare Dashboard**
2. **Select your domain** (goldenknightlounge.com)
3. **Add DNS Records**:
   
   Root domain:
   ```
   Type: CNAME
   Name: @
   Target: goldenknightlounge-johntylernyc.replit.app
   Proxy: ON (orange cloud)
   ```
   
   WWW subdomain:
   ```
   Type: CNAME
   Name: www
   Target: goldenknightlounge-johntylernyc.replit.app
   Proxy: ON (orange cloud)
   ```

4. **Configure SSL/TLS**:
   - Go to SSL/TLS settings
   - Set encryption mode to "Flexible"

### 3.2 Staging Domain Setup

Add staging subdomain:
```
Type: CNAME
Name: staging
Target: goldenknightlounge-staging-johntylernyc.replit.app
Proxy: ON (orange cloud)
```

### 3.3 Connect Domains in Replit

For each Replit project:
1. Go to Deployments → Settings
2. Add custom domain(s):
   - Production: `goldenknightlounge.com` and `www.goldenknightlounge.com`
   - Staging: `staging.goldenknightlounge.com`
3. Wait for verification (5-10 minutes)

## Step 4: Yahoo App Configuration

### 4.1 Create Yahoo Apps

You need TWO separate Yahoo apps for proper environment isolation:

1. **Production App**:
   - Go to [Yahoo Developer](https://developer.yahoo.com/apps/)
   - Create new app: "Golden Knight Lounge - Production"
   - Redirect URI: `https://goldenknightlounge.com/api/auth/callback`
   - Permissions: Fantasy Sports Read/Write

2. **Staging App**:
   - Create another app: "Golden Knight Lounge - Staging"
   - Redirect URI: `https://staging.goldenknightlounge.com/api/auth/callback`
   - Same permissions

### 4.2 Local Development App (Optional)
For local testing:
- Create third app: "Golden Knight Lounge - Development"
- Redirect URI: Your ngrok URL (update as needed)

## Step 5: Database Setup

### 5.1 PostgreSQL on Replit

Replit auto-provisions PostgreSQL for deployments:
1. Database URL is automatically set as `DATABASE_URL`
2. Separate databases for staging and production
3. Accessible via Replit's database viewer

### 5.2 Initial Schema

The application automatically creates required tables on first run:
- `oauth_tokens` - OAuth token storage
- Additional tables created by migrations

### 5.3 Database Migrations (Future)

When using Alembic for migrations:
```bash
# Initialize migrations (one time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Step 6: GitHub Actions Setup

### 6.1 Create Workflow Files

Create `.github/workflows/staging.yml`:
```yaml
name: Deploy to Staging
on:
  push:
    branches: [staging]
  pull_request:
    branches: [staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      - name: Run tests
        run: |
          pytest backend/tests/
```

Create `.github/workflows/production.yml`:
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      - name: Run tests
        run: |
          pytest backend/tests/
```

## Step 7: Verification

### 7.1 Test Staging Deployment
1. Visit https://staging.goldenknightlounge.com/api/health
2. Check Replit logs for errors
3. Test OAuth flow if configured

### 7.2 Test Production Deployment
1. Visit https://goldenknightlounge.com/api/health
2. Verify SSL certificate (green padlock)
3. Check all subdomains work

### 7.3 Monitor Deployments
- GitHub Actions: Check workflows tab
- Replit: Monitor Deployments → Logs
- Cloudflare: Check Analytics for traffic

## Troubleshooting

### DNS Issues
- Wait 5-10 minutes for propagation
- Clear browser cache
- Check with: `nslookup goldenknightlounge.com`

### SSL/Certificate Errors
- Ensure Cloudflare SSL is set to "Flexible"
- Check Replit domain verification status
- Wait for Cloudflare's Universal SSL to activate

### Deployment Not Updating
- Check GitHub → Replit connection
- Verify correct branch is linked
- Manual redeploy: Deployments → Redeploy

### Database Connection Issues
- Check DATABASE_URL is set correctly
- Verify PostgreSQL is provisioned in Replit
- Check connection string format

## Security Checklist

- [ ] Different OAuth apps for each environment
- [ ] Unique encryption keys per environment
- [ ] Branch protection enabled on GitHub
- [ ] Secrets never committed to repository
- [ ] CORS properly configured
- [ ] Debug logging disabled in production

## Next Steps

Once initial deployment is complete:
1. Review [Development Workflow](./development-workflow.md) for day-to-day development
2. Set up [Local Testing](./local-testing.md) environment
3. Configure monitoring and alerts
4. Set up backups for production database

---
*Last Updated: [Current Date]*
*For ongoing development and deployment procedures, see [Development Workflow](./development-workflow.md)*