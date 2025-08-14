# Implement League-Specific WAR (Wins Above Replacement) Calculation

## Feature Description
Develop a custom WAR (Wins Above Replacement) calculation methodology tailored to our fantasy baseball league's specific scoring categories. Unlike traditional MLB WAR which considers defensive metrics and park factors, this league-specific WAR will focus exclusively on the offensive and pitching statistics tracked in our Yahoo Fantasy Baseball league, providing managers with a single-value metric to evaluate player contributions.

## User Story
As a **league manager**, I want **a league-specific WAR calculation for both batters and pitchers** so that **I can objectively evaluate and compare player value based on our league's unique scoring categories rather than generic MLB metrics**.

## Acceptance Criteria
- [ ] Research and document methodology for fantasy-specific WAR calculations
- [ ] Implement batter WAR calculation using league offensive stats (H, R, 3B, HR, RBI, SB, AVG, OBP, SLG)
- [ ] Implement pitcher WAR calculation using league pitching stats (APP, W, QS, HLD, SV, K, ERA, WHIP, K/BB)
- [ ] Define "replacement level" baseline for both batters and pitchers in fantasy context
- [ ] Support full-season WAR calculations
- [ ] Support custom date range WAR calculations (e.g., player's tenure on specific roster)
- [ ] Handle rate stats (AVG, OBP, SLG, ERA, WHIP) appropriately in partial-season calculations
- [ ] Weight statistics based on league scoring impact and scarcity
- [ ] Create database tables to store WAR calculations and methodology parameters
- [ ] Build API endpoints to retrieve WAR data (by player, team, date range)
- [ ] Implement caching strategy for expensive WAR calculations
- [ ] Add WAR trends and visualizations to player profiles
- [ ] Document the calculation methodology for transparency
- [ ] Unit tests for WAR calculation logic with various edge cases
- [ ] Integration tests for API endpoints
- [ ] Performance benchmarks for bulk WAR calculations

## Technical Considerations
- **Methodology Research**: Review existing fantasy WAR approaches (e.g., FanGraphs Auction Calculator, Standing Gain Points)
- **Replacement Level**: Determine baseline (e.g., waiver wire quality, bottom 25% of rostered players)
- **Statistical Weighting**: Consider category scarcity and relative importance
- **Date Range Handling**: Account for playing time and rate stat stabilization
- **Performance**: Pre-calculate and cache common queries

## Dependencies
- Yahoo OAuth Authentication implementation (for fetching player stats)
- Database schema for player statistics
- Historical league data ingestion

## Priority
**Medium** - This is a value-add analytics feature requested by league managers but not blocking core functionality

## Labels
- `feature`
- `analytics`
- `backend`
- `algorithm`
- `data-pipeline`

## Additional Notes
- Consider creating multiple WAR variants (e.g., offensive WAR, pitching WAR, total WAR)
- May want to compare our custom WAR with traditional MLB WAR for validation
- Consider seasonal adjustments for injuries and playing time
- Future enhancement: WAR projections and rest-of-season WAR
- Consider creating a WAR leaderboard and historical WAR tracking

---
*Issue created for: League-Specific WAR Calculation*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*