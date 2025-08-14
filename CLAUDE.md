# Fantasy Baseball Analytics Platform - Development Guide

## Project Overview
A comprehensive fantasy baseball application that ingests Yahoo! Fantasy Baseball league data, enriches it with external sources, and provides advanced analytics through an intuitive UI.

## Tech Stack
- **Backend/Data Pipeline**: Python 3.11+
- **Frontend/API**: Node.js 20+ (Express.js)
- **Database**: PostgreSQL (Replit-compatible)
- **Deployment**: Replit (Staging + Production environments)
- **Version Control**: GitHub
- **CI/CD & Scheduling**: GitHub Actions (automated testing, deployments, scheduled data jobs)
- **Testing**: pytest (Python), Jest (Node.js)
- **Documentation**: Markdown, auto-generated API docs

## Development Workflow

### 1. Issue-Driven Development

#### Slash Commands for GitHub Workflow
- `/create-issue "[description]"` - Translates requirements into GitHub issue draft
- `/review-issue #[issue-number]` - Reviews existing issue and plans implementation
- `/review-pr #[pr-number]` - Reviews pull request for completeness and quality

#### Issue Creation Workflow
1. **Option A**: User describes feature/bug → Use `/create-issue` → Claude drafts issue as an ephemeral .md file → User reviews/edits → Create in GitHub
2. **Option B**: User creates issue directly in GitHub → Use `/review-issue` to analyze

#### Development Flow
1. Create or review GitHub issue with clear requirements
2. Claude develops solution following TDD principles
3. Submit PR with comprehensive tests
4. Claude creates release notes for the PR
5. Review PR before merging to staging
6. Release notes automatically added to changelog

### 2. Test-Driven Development (TDD) Cycle
1. **Red**: Write failing tests first
2. **Green**: Write minimal code to pass tests
3. **Refactor**: Improve code while maintaining passing tests
4. **Document**: Update relevant documentation

### 3. Branch Strategy
- `main`: Production-ready code (auto-deploys to Production Replit)
- `staging`: Testing environment (auto-deploys to Staging Replit)
- `develop`: Integration branch
- `feature/[issue-number]-[description]`: Feature branches
- `hotfix/[issue-number]-[description]`: Critical fixes

## Project Structure
```
goldenknightlounge/
  CLAUDE.md                    # This file - primary development reference
  README.md                    # User-facing documentation
  .github/
    workflows/                 # GitHub Actions CI/CD
    ISSUE_TEMPLATE/            # Issue templates
  docs/
    architecture.md            # System architecture
    infrastructure.md          # Infrastructure details
    database-design.md         # Database schema and relationships
    deployment.md              # Deployment procedures
    data-pipelines.md          # ETL pipeline documentation
  backend/
    requirements.txt           # Python dependencies
    src/
      api/                     # API endpoints (if Python-based)
      pipelines/               # Data pipeline modules
      models/                  # Data models
      enrichment/              # Data enrichment logic
      utils/                   # Utility functions
    tests/                     # Python tests
  frontend/
    package.json               # Node.js dependencies
    src/
      api/                     # Express API routes
      services/                # Business logic
      middleware/              # Express middleware
      public/                  # Static assets
    tests/                     # Node.js tests
  features/                    # Feature-specific modules
    [feature-name]/
      README.md                # Feature documentation
      src/                     # Feature code
      tests/                   # Feature tests
  database/
    migrations/                # Database migrations
    seeds/                     # Seed data
  scripts/
    setup.ps1                  # Windows setup script
    setup.sh                   # Unix setup script (for CI)
  config/
    replit.nix                 # Replit configuration
    .env.example               # Environment variables template
```

## Development Guidelines

### Before Starting Any Task
1. Review relevant documentation in `/docs`
2. Check existing issues and PRs
3. Ensure local environment is up-to-date
4. Run existing tests to verify baseline

### Code Standards
- **Python**: PEP 8, type hints required
- **JavaScript**: ESLint with Airbnb config
- **Testing**: Minimum 80% code coverage
- **Comments**: Only for complex logic
- **Documentation**: Update immediately with changes

### Windows-Compatible CLI Commands
```powershell
# Python virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r backend\requirements.txt
cd frontend && npm install

# Run tests
python -m pytest backend\tests
cd frontend && npm test

# Database migrations
python backend\src\migrate.py up
```

## Data Sources & APIs

### Primary Data Sources
1. **Yahoo! Fantasy Baseball API**
   - OAuth 2.0 authentication
   - Rate limit: 20,000 requests/hour
   - Endpoints: leagues, teams, players, transactions

2. **Enrichment Sources**
   - Baseball Reference
   - Fangraphs
   - MLB Stats API
   - Statcast

### API Design Principles
- RESTful endpoints
- JWT authentication
- Versioned APIs (`/api/v1/`)
- Comprehensive error handling
- Rate limiting per client

## Database Schema Overview
- **Core Tables**: leagues, teams, players, transactions, managers, seasons, drafts
- **Analytics Tables**: player_stats, projections, standings
- **Audit Tables**: data_loads, api_calls, data_job
- **Indexes**: Optimized for common query patterns

## Testing Requirements

### Unit Tests
- All functions with business logic
- Mock external API calls
- Test edge cases and error conditions

### Integration Tests
- API endpoint testing
- Database transaction testing
- Data pipeline end-to-end tests

### Performance Tests
- API response times < 200ms
- Database queries < 100ms
- Pipeline processing benchmarks

## Continuous Integration

### GitHub Actions Workflows
1. **On PR to Staging**: Run full test suite, lint, coverage report
2. **On Merge to Staging**: Deploy to Staging Replit, run smoke tests
3. **On PR from Staging to Main**: Run integration tests on staging environment
4. **On Merge to Main**: Deploy to Production Replit
5. **Scheduled Jobs**:
   - Every 4 hours: Yahoo API data sync
   - Daily at 3 AM EST: Full stats enrichment pipeline
   - Daily at 5 AM EST: Full analytic pipeline
   - Weekly: Database backup and optimization

## Environment Variables
```
# Yahoo API
YAHOO_CLIENT_ID=
YAHOO_CLIENT_SECRET=
YAHOO_REDIRECT_URI=

# Database (different for staging/production)
DATABASE_URL=postgresql://user:pass@host:port/db

# Application
NODE_ENV=development|staging|production
API_PORT=5000
PORT=3000
JWT_SECRET=
REPLIT_DEPLOYMENT_URL=  # Auto-populated by Replit
CUSTOM_DOMAIN=goldenknightlounge.com  # Production domain
ALLOWED_HOSTS=goldenknightlounge.com,www.goldenknightlounge.com,goldenknightlounge-johntylernyc.replit.app
CORS_ORIGINS=https://goldenknightlounge.com,https://www.goldenknightlounge.com,https://goldenknightlounge-johntylernyc.replit.app

# External APIs
MLB_API_KEY=

# Feature Flags
ENABLE_LIVE_STATS=false  # Enable in production only
ENABLE_DEBUG_LOGGING=true  # Disable in production
```

## GitHub Issue Templates

### Feature Issue Template
```markdown
## Feature Description
[Clear, concise description of the feature]

## User Story
As a [type of user], I want [goal] so that [benefit].

## Technical Requirements 
- Criterion 1
- Criterion 2
- Criterion 3

## Acceptance Criteria
- Criterion 1
- Criterion 2
- Criterion 3

## Dependencies
- [List any issues that must be completed first]

## Priority
[High/Medium/Low]

## Labels
[feature, enhancement, data-pipeline, frontend, backend, etc.]
```

**Note**: Technical requirements (API endpoints, database changes, data sources) will be determined by Claude during the `/review-issue` phase, ensuring implementation details align with the existing codebase and architecture.

### Bug Issue Template
```markdown
## Bug Description
[What is broken?]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- **Environment**: [Staging/Production]
- **Browser**: [If applicable]
- **Error Messages**: [Include any error messages]

## Priority
[Critical/High/Medium/Low]

## Proposed Solution
[If known]
```

## Common Development Tasks

### Adding a New Feature
1. Create issue with acceptance criteria
2. Create feature branch
3. Write failing tests
4. Implement feature
5. Update documentation
6. Submit PR with tests passing

### Updating Data Pipeline
1. Document new data source in `docs/data-pipelines.md`
2. Add pipeline module in `backend/src/pipelines/`
3. Write transformation logic with error handling
4. Add monitoring and logging
5. Update scheduling configuration

### Database Changes
1. Create migration script
2. Update `docs/database-design.md`
3. Test migration on development database
4. Include rollback procedure
5. Update ORM models

## Deployment Environments

### Local Development Environment
- **URL**: `http://localhost:3000` (frontend), `http://localhost:5000` (backend)
- **Database**: Local PostgreSQL or SQLite for development
- **OAuth Redirect**: Use ngrok for HTTPS tunnel ```ngrok http --url=wildly-innocent-pelican.ngrok-free.app 80```
- **Setup**:
  1. Copy `.env.example` to `.env`
  2. Install PostgreSQL locally or use Docker
  3. Run ngrok for Yahoo OAuth: `ngrok http 3000`
  4. Update `.env` with ngrok URL for `YAHOO_REDIRECT_URI`
- **Running**: 
  - Backend: `python backend/src/app.py`
  - Frontend: `cd frontend && npm start`

### Staging Environment
- **Replit URL**: `goldenknightlounge-staging-johntylernyc.replit.app`
- **Custom Domain**: `staging.goldenknightlounge.com`
- **Purpose**: Testing and validation before production
- **Database**: Separate PostgreSQL instance with test data (auto-provisioned by Replit)
- **Auto-Deploy**: On merge to `staging` branch
- **Testing**: Full integration test suite runs post-deployment

### Production Environment
- **Replit URL**: `goldenknightlounge-johntylernyc.replit.app`
- **Custom Domain**: `goldenknightlounge.com` and `www.goldenknightlounge.com`
- **Purpose**: Live application for users
- **Database**: Production PostgreSQL with regular backups (auto-provisioned by Replit)
- **Auto-Deploy**: On merge to `main` branch (after staging validation)
- **Monitoring**: Real-time alerts for errors and performance issues

### Deployment Flow
1. Developer creates feature branch from `develop`
2. PR to `staging` branch triggers automated tests
3. Merge to `staging` auto-deploys to Staging Replit
4. Manual or automated testing on staging environment
5. PR from `staging` to `main` requires approval
6. Merge to `main` auto-deploys to Production Replit

### Replit Configuration
Each environment requires separate Replit projects:
- Production: `goldenknightlounge` linked to `main` branch
- Staging: `goldenknightlounge-staging` linked to `staging` branch
- Configure secrets separately for each environment (use Deployments → Secrets)
- Enable "Always On" for production environment (requires paid plan)
- Run command: `bash scripts/start.sh` (configured in Deployments)

### Custom Domain Setup
1. **Production Domain**:
   - Add custom domain in Replit Deployments settings (requires paid plan)
   - Configure DNS CNAME records in Cloudflare:
     - `@` → `goldenknightlounge-johntylernyc.replit.app`
     - `www` → `goldenknightlounge-johntylernyc.replit.app`
   - Enable HTTPS/SSL in Cloudflare (set to "Flexible")
   - Update `ALLOWED_HOSTS` and `CORS_ORIGINS` environment variables

2. **Staging Domain**:
   - Add custom domain in Replit Deployments settings
   - Configure DNS CNAME record in Cloudflare:
     - `staging` → `goldenknightlounge-staging-johntylernyc.replit.app`
   - Update staging environment variables accordingly

## Monitoring & Logging
- Application logs: Structured JSON format
- Error tracking: Sentry integration
- Performance monitoring: Custom metrics
- Data quality: Automated validation checks

## Security Considerations
- Never commit secrets or API keys
- Use environment variables for configuration
- Implement rate limiting on all endpoints
- Sanitize all user inputs
- Regular dependency updates

## Useful Commands Reference
```powershell
# Start development servers
python backend\src\app.py
cd frontend && npm run dev

# Run linters
python -m flake8 backend\src
cd frontend && npm run lint

# Generate coverage reports
python -m pytest --cov=backend\src backend\tests
cd frontend && npm run test:coverage

# Database operations
python backend\src\manage.py db upgrade
python backend\src\manage.py db seed
```

## Environment-Specific Configuration Summary

| Setting | Local Development | Staging | Production |
|---------|------------------|---------|------------|
| **NODE_ENV** | `development` | `staging` | `production` |
| **Frontend URL** | `http://localhost:3000` | `https://staging.goldenknightlounge.com` | `https://goldenknightlounge.com` |
| **Backend URL** | `http://localhost:5000` | (same domain) | (same domain) |
| **Database** | Local PostgreSQL | Replit PostgreSQL | Replit PostgreSQL |
| **Yahoo Redirect** | ngrok URL | staging domain | production domain |
| **Debug Logging** | `true` | `true` | `false` |
| **Live Stats** | `false` | `false` | `true` |

## Resources
- [Yahoo! Fantasy Sports API Documentation](https://developer.yahoo.com/fantasysports/guide/)
- [MLB Stats API Documentation](https://statsapi.mlb.com/docs/)
- [Replit Deployment Guide](https://docs.replit.com/)
- [PostgreSQL on Replit](https://docs.replit.com/hosting/databases/postgresql)
- [PyBaseball](https://github.com/jldbc/pybaseball)
- [ngrok Documentation](https://ngrok.com/docs) (for local OAuth development)

---
*Last Updated: [Auto-update on commit]*
*Version: 1.0.0*