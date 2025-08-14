# Implement Draft Data Ingestion from Yahoo API

## Feature Description
Build the data ingestion pipeline for Yahoo Fantasy Baseball draft data, capturing complete draft results, pick order, and auction values. This historical data enables draft analysis, trend identification, and strategy optimization for future seasons.

## User Story
As a **developer**, I want **to ingest and store complete draft data from Yahoo API** so that **we can analyze draft strategies, identify value picks, and provide insights for future draft preparation**.

## Acceptance Criteria

### Database Schema
- [ ] Create `raw_drafts` table with JSONB column for complete API responses
- [ ] Create `drafts` table for draft metadata (date, type, league, status)
- [ ] Create `draft_picks` table for individual pick details
- [ ] Create `draft_analysis` table for calculated metrics
- [ ] Implement indexing for draft queries and analysis
- [ ] Add audit columns for tracking ingestion

### Pipeline Implementation
- [ ] Implement DraftDataPipeline class extending base pipeline infrastructure
- [ ] Support three execution modes:
  - [ ] **Backfill**: Ingest all 18 years of draft data
  - [ ] **Incremental**: Post-draft ingestion for current season
  - [ ] **Lookback**: Re-process for updated player values
- [ ] Store draft settings (snake/auction, keeper rules, roster size)
- [ ] Capture complete pick details (round, pick, team, player, cost)
- [ ] Handle different draft types (snake, auction, keeper, dynasty)
- [ ] Process keeper selections with associated costs
- [ ] Support incomplete drafts (auto-picks, disconnections)

### Data Processing
- [ ] Parse draft configuration and rules
- [ ] Process pick-by-pick results with timestamps
- [ ] Calculate positional runs and scarcity metrics
- [ ] Compute ADP (Average Draft Position) variance
- [ ] Identify reaches and values based on consensus rankings
- [ ] Track draft pace and time per pick
- [ ] Generate team draft grades and summaries
- [ ] Build historical draft trend analysis

### Analytics & Metrics
- [ ] Calculate value over replacement at draft position
- [ ] Track positional scarcity by round
- [ ] Identify draft strategy patterns (zero RB, etc.)
- [ ] Compare actual vs projected draft values
- [ ] Analyze keeper value trends across seasons
- [ ] Generate draft report cards by team

### Testing (TDD Approach)
- [ ] Write tests for draft data parsing
- [ ] Test different draft type handling
- [ ] Validate metric calculations
- [ ] Test keeper and auction logic
- [ ] Performance tests for historical processing
- [ ] Test edge cases (auto-drafts, disconnects)

### GitHub Actions Integration
- [ ] Create `draft-data-backfill.yml` workflow for historical load
- [ ] Create `draft-data-ingest.yml` for post-draft processing
- [ ] Support manual triggers for specific seasons
- [ ] Generate draft summary reports as artifacts
- [ ] Send notifications on draft ingestion completion

### Monitoring & Documentation
- [ ] Track metrics (drafts processed, picks ingested)
- [ ] Monitor data quality (missing picks, invalid players)
- [ ] Document draft data model and relationships
- [ ] Create draft analytics methodology guide
- [ ] Build data dictionary for draft fields

## Technical Considerations
- **API Endpoints**: `/fantasy/v2/league/{league_key}/draftresults`
- **Data Volume**: ~3,600-5,400 total picks (200-300 picks × 18 drafts)
- **Parallelization**: Process drafts by season concurrently
- **Update Patterns**:
  - Backfill: One-time for all historical drafts
  - Incremental: Once after draft completion (typically March)
  - Lookback: Optional, for updated player valuations
- **Key Fields**: pick_number, round, team_key, player_key, cost, keeper_status
- **Draft Types**: 
  - Snake drafts (standard)
  - Auction drafts (with budgets)
  - Keeper leagues (with kept players)
- **Performance**: Low volume, can process sequentially
- **Data Freshness**: One-time ingestion post-draft

## Dependencies
- Data Pipeline Infrastructure implementation
- League data ingestion (draft linked to league)
- Player data ingestion (picks reference players)
- Team data ingestion (picks linked to teams)
- Yahoo OAuth Authentication

## Priority
**Medium** - Draft data is valuable for analytics but not required for daily operations

## Labels
- `feature`
- `backend`
- `data-pipeline`
- `database`
- `analytics`

---
*Issue created for: Draft Data Ingestion*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*