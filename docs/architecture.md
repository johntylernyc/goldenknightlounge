# System Architecture

## Overview
Fantasy Baseball Analytics Platform - A comprehensive application for Yahoo! Fantasy Baseball league data analysis and insights.

## Architecture Pattern
**Three-Tier Architecture**
- **Presentation Layer**: Web-based UI (Node.js/Express)
- **Business Logic Layer**: Python data pipelines & Node.js API services
- **Data Layer**: PostgreSQL database

## Core Components

### 1. Frontend Application
- **Technology**: Node.js with Express.js
- **Purpose**: Serve web interface and handle user interactions
- **Key Features**:
  - Server-side rendered pages
  - RESTful API endpoints
  - Static asset serving
  - Session management

### 2. Backend Data Pipeline
- **Technology**: Python 3.11+
- **Purpose**: Data ingestion, enrichment, and analytics
- **Components**:
  - Yahoo API integration
  - Data enrichment modules
  - Analytics engine
  - Scheduled job runners

### 3. Database
- **Technology**: PostgreSQL
- **Purpose**: Persistent data storage
- **Schema Categories**:
  - Core tables (leagues, teams, players)
  - Analytics tables (stats, projections)
  - Audit tables (data_loads, api_calls)

## Data Flow

### 1. Data Ingestion Flow
```
Yahoo API → Python Pipeline → Data Validation → PostgreSQL
                    ↓
            Enrichment Sources
            (MLB API, Statcast)
```

### 2. User Request Flow
```
User Browser → Express Server → API Routes → Database
                    ↓              ↓
              Static Assets   Business Logic
```

### 3. Analytics Pipeline
```
Raw Data → Transformation → Analytics Engine → Processed Results
    ↓            ↓                ↓                  ↓
Database    Validation      Calculations       Database
```

## Integration Points

### External APIs
1. **Yahoo! Fantasy Sports API**
   - OAuth 2.0 authentication
   - Real-time league data
   - Rate limit: 20,000 requests/hour

2. **MLB Stats API**
   - Public API for player statistics
   - Real-time game data

3. **Enrichment Sources**
   - Baseball Reference
   - Fangraphs
   - Statcast

### Internal APIs
- RESTful endpoints (versioned: `/api/v1/`)
- JWT authentication
- JSON response format

## Security Architecture

### Authentication & Authorization
- OAuth 2.0 for Yahoo integration
- JWT tokens for internal API
- Session-based auth for web interface

### Data Security
- Environment variable configuration
- Encrypted database connections
- Input sanitization
- Rate limiting

## Deployment Architecture

### Environments
1. **Local Development**
   - Localhost deployment
   - SQLite/PostgreSQL local DB
   - ngrok for OAuth callbacks

2. **Staging**
   - Replit staging deployment
   - Separate PostgreSQL instance
   - Automated testing

3. **Production**
   - Replit production deployment
   - Production PostgreSQL
   - Custom domain (goldenknightlounge.com)

### CI/CD Pipeline
```
GitHub → GitHub Actions → Automated Tests → Replit Deployment
   ↓           ↓              ↓                    ↓
Feature    PR Checks    Test Results         Environment
Branch                                    (Staging/Production)
```

## Scalability Considerations

### Current Design
- Vertical scaling on Replit
- Database connection pooling
- Efficient query optimization
- Caching strategy for API responses

### Future Considerations
- Horizontal scaling capabilities
- Redis caching layer
- CDN for static assets
- Microservices architecture

## Monitoring & Logging

### Application Monitoring
- Structured JSON logging
- Error tracking (Sentry integration planned)
- Performance metrics
- Health check endpoints

### Data Quality
- Automated validation checks
- Data pipeline monitoring
- API call tracking
- Job execution logs

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Node.js/Express | Web server & UI |
| API | Express.js | RESTful endpoints |
| Data Pipeline | Python 3.11+ | ETL & analytics |
| Database | PostgreSQL | Data persistence |
| Deployment | Replit | Cloud hosting |
| CI/CD | GitHub Actions | Automation |
| Version Control | GitHub | Code repository |

## Architectural Decisions

### Why Three-Tier Architecture?
- Clear separation of concerns
- Independent scaling of layers
- Technology flexibility per layer
- Maintainable and testable

### Why Python for Data Pipeline?
- Rich ecosystem for data analysis (pandas, numpy)
- Excellent API client libraries
- Strong statistical computing capabilities
- PyBaseball integration

### Why Node.js/Express for Frontend?
- JavaScript ecosystem maturity
- Excellent for real-time features
- Strong community support
- Replit compatibility

### Why PostgreSQL?
- ACID compliance
- Complex query support
- JSON data type support
- Replit native integration

---
*Last Updated: [Auto-update on commit]*