# Infrastructure Documentation

## Deployment Platform
**Replit** - Cloud-based development and deployment platform

## Environment Configuration

### Development Environment
- **Local machine** with Python 3.11+ and Node.js 20+
- **ngrok** for OAuth callback tunneling
- **Local PostgreSQL** or SQLite for database

### Staging Environment
- **Replit Project**: goldenknightlounge-staging
- **Branch**: staging
- **URL**: goldenknightlounge-staging-johntylernyc.replit.app
- **Custom Domain**: staging.goldenknightlounge.com
- **Database**: Replit-managed PostgreSQL (auto-provisioned)

### Production Environment
- **Replit Project**: goldenknightlounge
- **Branch**: main
- **URL**: goldenknightlounge-johntylernyc.replit.app
- **Custom Domains**: goldenknightlounge.com, www.goldenknightlounge.com
- **Database**: Replit-managed PostgreSQL (auto-provisioned)

## CI/CD Pipeline

### GitHub Actions Workflows
1. **PR to Staging**: Automated tests, linting, coverage
2. **Merge to Staging**: Auto-deploy to Staging Replit
3. **PR to Main**: Integration tests on staging
4. **Merge to Main**: Auto-deploy to Production Replit

### Scheduled Jobs
- Every 4 hours: Yahoo API data sync
- Daily 3 AM EST: Stats enrichment pipeline
- Daily 5 AM EST: Analytics pipeline
- Weekly: Database backup and optimization

## Domain & DNS Configuration

### Production Domain Setup
- DNS Provider: Cloudflare
- CNAME Records:
  - `@` → goldenknightlounge-johntylernyc.replit.app
  - `www` → goldenknightlounge-johntylernyc.replit.app
- SSL: Cloudflare Flexible SSL

### Staging Domain Setup
- CNAME Record: `staging` → goldenknightlounge-staging-johntylernyc.replit.app

## Environment Variables

### Required Variables
- `YAHOO_CLIENT_ID` - Yahoo OAuth client
- `YAHOO_CLIENT_SECRET` - Yahoo OAuth secret
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - API authentication
- `NODE_ENV` - Environment setting

### Environment-Specific Settings
- `ALLOWED_HOSTS` - Domain whitelist
- `CORS_ORIGINS` - CORS configuration
- `ENABLE_LIVE_STATS` - Feature flag
- `ENABLE_DEBUG_LOGGING` - Debug mode

## Monitoring & Logging
- Application logs: JSON structured format
- Error tracking: Sentry (planned)
- Performance monitoring: Custom metrics
- Health checks: `/api/health` endpoint

## Security Infrastructure
- SSL/TLS encryption via Cloudflare
- Environment variable management via Replit Secrets
- Rate limiting on API endpoints
- Input sanitization at application layer

## Resource Allocation
- **Replit Plan**: Paid plan required for custom domains and always-on
- **Database Storage**: Auto-scaled by Replit
- **Compute Resources**: Managed by Replit platform

---
*To be expanded as infrastructure evolves*