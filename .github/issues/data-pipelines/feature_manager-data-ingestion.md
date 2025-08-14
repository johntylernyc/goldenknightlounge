# Implement Manager Data Ingestion from Yahoo API

## Feature Description
Create the data ingestion pipeline for Yahoo Fantasy Baseball manager (user) data, capturing manager profiles, historical performance, and cross-season participation. This data links human users to their teams across multiple leagues and seasons.

## User Story
As a **developer**, I want **to ingest and store manager data from Yahoo API** so that **we can track manager performance history, provide personalized analytics, and maintain user continuity across seasons**.

## Acceptance Criteria

### Database Schema
- [ ] Create `raw_managers` table with JSONB column for complete API responses
- [ ] Create `managers` normalized table with core manager attributes
- [ ] Create supporting tables: `manager_seasons`, `manager_achievements`, `manager_stats`
- [ ] Implement proper indexing for GUID lookups
- [ ] Add privacy flags and data retention columns

### Pipeline Implementation
- [ ] Implement ManagerDataPipeline class extending base pipeline infrastructure
- [ ] Support three execution modes:
  - [ ] **Backfill**: Process all managers for all 18 seasons
  - [ ] **Incremental**: Weekly updates for active managers
  - [ ] **Lookback**: Not typically needed (manager data rarely changes)
- [ ] Store manager profile data (GUID, nickname, avatar)
- [ ] Track manager's team associations across all seasons
- [ ] Calculate historical performance metrics (championships, finishes)
- [ ] Link managers to their teams in each season
- [ ] Handle manager privacy settings appropriately

### Data Processing
- [ ] Parse manager profile information
- [ ] Build manager-team association history
- [ ] Calculate career statistics (wins, championships, average finish)
- [ ] Track manager tenure and league participation
- [ ] Identify returning vs new managers
- [ ] Handle manager name changes across seasons
- [ ] Respect Yahoo privacy settings (hide real names if private)

### Testing (TDD Approach)
- [ ] Write tests for manager data parsing
- [ ] Test manager-team association logic
- [ ] Validate privacy setting handling
- [ ] Test historical stat calculations
- [ ] Test all execution modes
- [ ] Verify GUID consistency across seasons

### GitHub Actions Integration
- [ ] Create `manager-data-backfill.yml` workflow for historical load
- [ ] Create `manager-data-weekly.yml` workflow for updates
- [ ] Support manual triggers for specific managers
- [ ] Implement privacy compliance checks
- [ ] Log all data access for audit purposes

### Monitoring & Documentation
- [ ] Track metrics (managers processed, associations created)
- [ ] Monitor data completeness (missing managers)
- [ ] Document privacy handling procedures
- [ ] Create operational runbook
- [ ] Build data dictionary for manager fields

## Technical Considerations
- **API Endpoints**: `/fantasy/v2/users;use_login=1/games/mlb/leagues`
- **Data Volume**: ~150-200 unique managers across 18 seasons
- **Parallelization**: Process by season, relatively low volume
- **Update Patterns**:
  - Backfill: One-time for all historical data
  - Incremental: Weekly on Sundays at 3 AM EST
  - Lookback: Not typically required
- **Key Fields**: manager_guid, nickname, image_url, team_keys
- **Privacy Considerations**:
  - Store only public Yahoo profile data
  - Implement data retention policies
  - Allow manager opt-out if requested
- **Data Freshness**: Weekly updates sufficient

## Dependencies
- Data Pipeline Infrastructure implementation
- Team data ingestion (managers linked to teams)
- Yahoo OAuth Authentication

## Priority
**Medium** - Manager data enhances analytics but isn't blocking core functionality

## Labels
- `feature`
- `backend`
- `data-pipeline`
- `database`
- `privacy`

---
*Issue created for: Manager Data Ingestion*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*