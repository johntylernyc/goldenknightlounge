# Implement Player Data Ingestion from Yahoo API

## Feature Description
Develop the data ingestion pipeline for Yahoo Fantasy Baseball player data, including player metadata, statistics, and eligibility. This high-volume pipeline will handle thousands of players with frequent updates during the season.

## User Story
As a **developer**, I want **to ingest and store comprehensive player data from Yahoo API** so that **we can provide player analytics, track performance, and support roster management decisions**.

## Acceptance Criteria

### Database Schema
- [ ] Create `raw_players` table with JSONB column for complete API responses
- [ ] Create `players` normalized table with core player attributes
- [ ] Create supporting tables: `player_stats`, `player_eligibility`, `player_status_history`
- [ ] Implement partitioning by season for stats tables
- [ ] Add indexes for search and filtering operations
- [ ] Include audit columns for tracking updates

### Pipeline Implementation
- [ ] Implement PlayerDataPipeline class extending base pipeline infrastructure
- [ ] Support three execution modes:
  - [ ] **Backfill**: Ingest all players for all 18 seasons with parallel workers
  - [ ] **Incremental**: Every 4 hours for rostered players during season
  - [ ] **Lookback**: Daily re-fetch last 7 days for stat corrections
- [ ] Store player metadata (name, team, positions, player_key)
- [ ] Track player eligibility changes over time
- [ ] Capture player status transitions (active, injured, NA, suspended)
- [ ] Store daily and season statistics with timestamps
- [ ] Implement bulk processing with configurable batch sizes

### Data Processing
- [ ] Parse player biographical data
- [ ] Process statistical categories (batting, pitching)
- [ ] Track position eligibility (games played by position)
- [ ] Handle player transactions (trades, call-ups, demotions)
- [ ] Detect and flag statistical anomalies
- [ ] Implement efficient pagination for large datasets
- [ ] Use parallel workers for bulk operations
- [ ] Cache frequently accessed players in Redis/memory

### Testing (TDD Approach)
- [ ] Write tests for player data parsing
- [ ] Test statistical calculations and aggregations
- [ ] Validate position eligibility logic
- [ ] Test pagination and batch processing
- [ ] Performance tests with thousands of players
- [ ] Test all three execution modes
- [ ] Validate data quality checks

### GitHub Actions Integration
- [ ] Create `player-data-backfill.yml` workflow for historical load
- [ ] Create `player-data-4hourly.yml` workflow for in-season updates
- [ ] Create `player-data-corrections.yml` for daily lookback
- [ ] Support manual triggers with filters (team, position, status)
- [ ] Implement progressive backfill to avoid API limits
- [ ] Add failure recovery mechanisms

### Monitoring & Documentation
- [ ] Track metrics (players processed, API calls, cache hits)
- [ ] Monitor data quality (null rates, outliers, duplicates)
- [ ] Alert on missing players or data gaps
- [ ] Document player data model and relationships
- [ ] Create runbook for operations
- [ ] Build data dictionary for all player fields

## Technical Considerations
- **API Endpoints**: `/fantasy/v2/league/{league_key}/players`
- **Data Volume**: ~15,000-20,000 player records (800-1000 per season × 18 seasons)
- **Parallelization**: 
  - Backfill: Process seasons in parallel, players in batches
  - Use 4-8 workers for optimal throughput
- **Update Patterns**:
  - Backfill: One-time, progressive over multiple runs
  - Incremental: Every 4 hours during season (rostered players only)
  - Lookback: Daily at 2 AM EST for last 7 days
- **Key Fields**: player_key, name, team, positions, status, stats
- **Performance Optimizations**:
  - Batch size: 25-50 players per API call
  - Connection pooling for database writes
  - Async I/O for API calls
- **Rate Limiting**: Implement adaptive throttling based on API response headers
- **Data Freshness**: 4-hour lag acceptable for most use cases

## Dependencies
- Data Pipeline Infrastructure implementation
- League data ingestion (for league context)
- Yahoo OAuth Authentication

## Priority
**High** - Player data is core to all fantasy baseball operations

## Labels
- `feature`
- `backend`
- `data-pipeline`
- `database`
- `performance`

---
*Issue created for: Player Data Ingestion*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*