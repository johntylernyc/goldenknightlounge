# Implement Team Data Ingestion from Yahoo API

## Feature Description
Build the data ingestion pipeline for Yahoo Fantasy Baseball team data, storing raw API responses and processing into normalized tables. This will capture team rosters, standings, and team-level configurations.

## User Story
As a **developer**, I want **to ingest and store team data from Yahoo API** so that **we can track team performance, rosters, and provide team-level analytics throughout the season**.

## Acceptance Criteria

### Database Schema
- [ ] Create `raw_teams` table with JSONB column for complete API responses
- [ ] Create `teams` normalized table with core team attributes
- [ ] Create supporting tables: `team_standings`, `team_rosters`, `team_stats`
- [ ] Implement proper indexing for query performance
- [ ] Add data versioning and audit columns

### Pipeline Implementation
- [ ] Implement TeamDataPipeline class extending base pipeline infrastructure
- [ ] Support three execution modes:
  - [ ] **Backfill**: Process all teams for all 18 seasons in parallel
  - [ ] **Incremental**: Hourly updates during season for active teams
  - [ ] **Lookback**: Re-fetch last N days for stat corrections
- [ ] Store team metadata (name, logo, manager GUID)
- [ ] Track current and historical roster composition
- [ ] Store team standings with point-in-time snapshots
- [ ] Capture team statistical totals by category
- [ ] Link teams to leagues, seasons, and managers
- [ ] Handle team changes (name updates, manager changes)

### Data Processing
- [ ] Parse team roster with player associations
- [ ] Calculate team standings and rankings
- [ ] Process team matchups and results
- [ ] Handle pagination for API responses
- [ ] Validate roster compliance with league rules
- [ ] Track roster moves and transactions
- [ ] Implement change detection for incremental updates

### Testing (TDD Approach)
- [ ] Write tests for team data parsing
- [ ] Test roster validation logic
- [ ] Validate standings calculations
- [ ] Test all three execution modes
- [ ] Performance tests with 18 years of data
- [ ] Test pagination handling

### GitHub Actions Integration
- [ ] Create `team-data-backfill.yml` workflow for historical load
- [ ] Create `team-data-hourly.yml` workflow for in-season updates
- [ ] Support manual trigger with parameters
- [ ] Implement failure notifications
- [ ] Archive logs and metrics

### Monitoring & Documentation
- [ ] Track pipeline metrics (teams processed, API calls, duration)
- [ ] Monitor data quality (roster validity, stat anomalies)
- [ ] Document team data model
- [ ] Create operational runbook
- [ ] Add data dictionary for team fields

## Technical Considerations
- **API Endpoints**: `/fantasy/v2/league/{league_key}/teams`
- **Data Volume**: ~200-300 teams total (8-16 teams × 18 seasons)
- **Parallelization**: Process multiple seasons/teams concurrently
- **Update Patterns**:
  - Backfill: One-time, all seasons in parallel
  - Incremental: Hourly during season (March-October)
  - Lookback: Daily for last 7 days (stat corrections)
- **Key Fields**: team_key, name, manager_guid, standings, roster
- **Rate Limiting**: Implement throttling to respect API limits
- **Data Freshness**: Hourly updates during active season

## Dependencies
- Data Pipeline Infrastructure implementation
- League data ingestion (must know league_key)
- Yahoo OAuth Authentication

## Priority
**High** - Team data is essential for league analytics

## Labels
- `feature`
- `backend`
- `data-pipeline`
- `database`

---
*Issue created for: Team Data Ingestion*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*