# Implement League Data Ingestion from Yahoo API

## Feature Description
Create the data ingestion pipeline for Yahoo Fantasy Baseball league data, following a two-stage pattern: storing raw API responses in JSONB format, then processing into normalized tables. Implementation will ingest 18 years of historical league data (2008-2025) for our POC league, providing rich historical context for analytics.

## User Story
As a **developer**, I want **to ingest and store our league's complete historical data from Yahoo API** so that **we have 18 years of league configuration and results data to power advanced analytics and trend analysis**.

## Acceptance Criteria

### Database Schema
- [ ] Create `raw_leagues` table with JSONB column for complete API responses
- [ ] Create `leagues` normalized table with core league attributes
- [ ] Create supporting tables: `league_settings`, `scoring_categories`, `roster_positions`
- [ ] Implement proper indexing for query performance
- [ ] Add data versioning columns (created_at, updated_at, version)

### Pipeline Implementation
- [ ] Implement LeagueDataPipeline class extending base pipeline infrastructure
- [ ] Support three execution modes:
  - [ ] **Backfill**: Ingest all 18 years (2008-2025) with parallel processing
  - [ ] **Incremental**: Daily updates for current season only
  - [ ] **Lookback**: Re-fetch last N days for corrections
- [ ] Import league_keys configuration from provided Python file (.github\issues\data-pipelines\supporting_files\league_keys.py)
- [ ] Implement data extraction from Yahoo API
- [ ] Store raw responses with metadata (fetch_time, api_version)
- [ ] Transform and normalize data into relational structure
- [ ] Handle league setting variations across seasons

### Data Processing
- [ ] Parse league settings (roster positions, scoring categories, playoff structure)
- [ ] Handle different league types (H2H, Roto, Points)
- [ ] Track league status (pre-draft, in-season, completed)
- [ ] Store season start/end dates from configuration
- [ ] Validate data completeness and integrity
- [ ] Implement idempotent operations for safe re-runs

### Testing (TDD Approach)
- [ ] Write tests for API response parsing
- [ ] Test data transformation logic
- [ ] Validate database schema with sample data
- [ ] Test all three execution modes
- [ ] Performance tests for bulk operations
- [ ] Error handling and recovery tests

### GitHub Actions Integration
- [ ] Create `league-data-backfill.yml` workflow for one-time historical load
- [ ] Create `league-data-daily.yml` workflow for scheduled updates
- [ ] Support manual trigger with parameters (mode, seasons, lookback_days)
- [ ] Add job status notifications
- [ ] Store logs as artifacts

### Monitoring & Documentation
- [ ] Structured logging with progress indicators
- [ ] Track metrics (API calls, records processed, duration)
- [ ] Document league data model and relationships
- [ ] Create runbook for operations
- [ ] Add data dictionary for league fields

## Technical Considerations
- **API Endpoints**: `/fantasy/v2/leagues;league_keys={league_key}`
- **Data Volume**: 18 seasons of league data (2008-2025)
- **Parallelization**: Process multiple seasons concurrently for backfill
- **Update Patterns**:
  - Backfill: One-time, all seasons in parallel
  - Incremental: Daily at 6 AM EST (current season only)
  - Lookback: On-demand or weekly (last 7 days)
- **Key Fields**: league_key, name, season, game_code, scoring_type
- **Rate Limiting**: Batch requests with throttling to stay within 20,000/hour
- **Data Freshness**: Near real-time not required, daily updates sufficient

## Dependencies
- Data Pipeline Infrastructure implementation
- Yahoo OAuth Authentication implementation
- Database schema initialization

## Priority
**High** - League data is required for all other data ingestion

## Labels
- `feature`
- `backend`
- `data-pipeline`
- `database`

---
*Issue created for: League Data Ingestion*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*