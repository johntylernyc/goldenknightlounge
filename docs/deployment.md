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
5. Add secrets (Settings → Secrets):
   - All variables from `.env.example`
   - Set `NODE_ENV=production`
   - Set proper `DATABASE_URL`
   - Configure `CORS_ORIGINS` and `ALLOWED_HOSTS`

### Staging Environment

1. Create another Repl
2. Import same repository but select `staging` branch
3. Name it `goldenknightlounge-staging`
4. Add secrets with staging values:
   - Set `NODE_ENV=staging`
   - Use separate staging database

## Step 3: Domain Configuration (Cloudflare)

### Production Domain

1. Log into Cloudflare Dashboard
2. Select your domain (goldenknightlounge.com)
3. Go to DNS settings
4. Add records:
   ```
   Type: CNAME
   Name: @
   Target: goldenknightlounge.repl.co
   Proxy: ON (orange cloud)
   
   Type: CNAME
   Name: www
   Target: goldenknightlounge.repl.co
   Proxy: ON (orange cloud)
   ```

### Staging Domain (Optional)

1. Add subdomain record:
   ```
   Type: CNAME
   Name: staging
   Target: goldenknightlounge-staging.repl.co
   Proxy: ON (orange cloud)
   ```

## Step 4: Replit Domain Connection

### For each Replit project:

1. Go to your Repl
2. Click on "Webview" tab
3. Click domain settings (pencil icon)
4. Add custom domain:
   - Production: `goldenknightlounge.com` and `www.goldenknightlounge.com`
   - Staging: `staging.goldenknightlounge.com`
5. Replit will verify DNS configuration

## Step 5: Enable Always On (Production)

1. In production Repl settings
2. Enable "Always On" (requires Replit subscription)
3. This ensures your app doesn't sleep

## Step 6: Database Setup

### PostgreSQL on Replit

1. In your Repl, go to "Tools" → "Database"
2. Create PostgreSQL database
3. Copy connection string to secrets as `DATABASE_URL`

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

## Maintenance

### Updates
1. Push to `staging` branch first
2. Test on staging environment
3. Create PR to `main` branch
4. Merge after testing

### Monitoring
- Check Replit console for logs
- Monitor GitHub Actions for CI/CD status
- Set up uptime monitoring (e.g., UptimeRobot)