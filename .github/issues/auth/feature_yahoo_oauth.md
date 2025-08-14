# Implement Yahoo OAuth Authentication Service for Fantasy Baseball Data Ingestion

## Feature Description
Implement a robust OAuth 2.0 authentication service to securely connect with Yahoo Fantasy Baseball API for both read and write operations. This service will handle token management, automatic refresh, proper scope management, and support multiple environments (local development, staging, and production on Replit).

## User Story
As a **developer**, I want **a reusable authentication service for Yahoo Fantasy Baseball API** so that **we can securely read league data and perform write operations (like roster changes, trades, etc.) across all environments without manual token management**.

## Acceptance Criteria
- [ ] OAuth 2.0 flow implementation for Yahoo Fantasy Baseball API
- [ ] Secure token storage mechanism (database or secure environment variables)
- [ ] Automatic token refresh before expiration
- [ ] Support for local development using ngrok
- [ ] Support for staging environment on Replit
- [ ] Support for production environment on Replit
- [ ] Error handling for authentication failures and rate limits
- [ ] Logging for authentication events and debugging
- [ ] Unit tests with mocked Yahoo API responses
- [ ] Integration tests for token refresh flow
- [ ] Documentation for setup and configuration across environments
- [ ] Environment-specific configuration templates (.env.example updates)

## Technical Considerations
- **Authentication Flow**: OAuth 2.0 three-legged authentication
- **Token Storage**: PostgreSQL table for tokens with encryption
- **Token Refresh**: Background job or on-demand refresh before API calls
- **Rate Limiting**: Respect Yahoo's 20,000 requests/hour limit
- **Environment Support**:
  - Local: ngrok for HTTPS redirect URI
  - Staging: staging.goldenknightlounge.com redirect
  - Production: goldenknightlounge.com redirect

## Dependencies
- None (foundational component)

## Priority
**High** - This is a blocking requirement for all Yahoo API data ingestion features

## Labels
- `feature`
- `backend`
- `authentication`

## Additional Notes
- This authentication service will be the foundation for all Yahoo Fantasy Baseball API interactions
- Consider implementing a token management UI for administrators to manually trigger re-authentication if needed
- Ensure compliance with Yahoo's API terms of service and rate limits
- Consider implementing a circuit breaker pattern for API failures

---
*Issue created for: Yahoo OAuth Authentication Implementation*
*Project: Golden Knight Lounge - Fantasy Baseball Analytics Platform*