# Yahoo OAuth Authentication Documentation

## Overview
This document describes the Yahoo OAuth 2.0 authentication implementation for the Golden Knight Lounge Fantasy Baseball platform. The authentication service handles secure access to Yahoo Fantasy Baseball API for both read and write operations.

## Architecture

### Components

1. **YahooOAuthClient** (`backend/src/auth/yahoo_oauth.py`)
   - Manages OAuth 2.0 flow
   - Handles token exchange and refresh
   - Provides authenticated API requests
   - Supports multiple environments

2. **TokenManager** (`backend/src/auth/token_manager.py`)
   - Secure token storage with encryption
   - PostgreSQL database persistence
   - Automatic fallback to memory storage
   - Token expiration management

3. **Authentication Routes** (`backend/src/api/auth_routes.py`)
   - `/api/auth/login` - Initiate OAuth flow
   - `/api/auth/callback` - Handle OAuth callback
   - `/api/auth/logout` - Clear tokens
   - `/api/auth/refresh` - Manual token refresh
   - `/api/auth/status` - Check authentication status

## Setup Instructions

### 1. Yahoo App Registration

1. Go to [Yahoo Developer Network](https://developer.yahoo.com/apps/)
2. Create a new app
3. Select "Fantasy Sports" > "Read/Write" permissions
4. Note your Client ID and Client Secret
5. Configure redirect URIs for each environment

### 2. Environment Configuration

#### Local Development
```bash
# .env file
YAHOO_CLIENT_ID=your_client_id
YAHOO_CLIENT_SECRET=your_client_secret
YAHOO_REDIRECT_URI=http://localhost:5000/api/auth/callback

# For HTTPS callback (required by Yahoo)
# Use ngrok: ngrok http 5000
# Then update YAHOO_REDIRECT_URI with ngrok URL
```

#### Staging Environment
```bash
NODE_ENV=staging
YAHOO_REDIRECT_URI=https://staging.goldenknightlounge.com/api/auth/callback
```

#### Production Environment
```bash
NODE_ENV=production
YAHOO_REDIRECT_URI=https://goldenknightlounge.com/api/auth/callback
```

### 3. Token Encryption Setup

Generate an encryption key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

Add to environment:
```bash
TOKEN_ENCRYPTION_KEY=your_generated_key_here
```

### 4. Database Setup

The token storage table is automatically created on first run:

```sql
CREATE TABLE oauth_tokens (
    id SERIAL PRIMARY KEY,
    service VARCHAR(50) NOT NULL DEFAULT 'yahoo',
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMP NOT NULL,
    scope TEXT,
    token_type VARCHAR(50) DEFAULT 'Bearer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service)
);
```

## Authentication Flow

### Initial Authentication

1. User clicks "Login with Yahoo"
2. Backend generates state token for CSRF protection
3. User is redirected to Yahoo consent page
4. User approves access
5. Yahoo redirects back with authorization code
6. Backend exchanges code for access/refresh tokens
7. Tokens are encrypted and stored
8. User is redirected to application dashboard

### Token Refresh

Tokens are automatically refreshed when:
- Access token expires (1 hour lifetime)
- API request returns 401 Unauthorized
- Manual refresh is triggered

The refresh flow:
1. Check token expiration (with 60-second buffer)
2. Use refresh token to get new access token
3. Update stored tokens
4. Retry original request

## Usage Examples

### Python Backend Usage

```python
from backend.src.auth import YahooOAuthClient, TokenManager

# Initialize
token_manager = TokenManager()
oauth_client = YahooOAuthClient(token_manager=token_manager)

# Make authenticated API request
leagues_data = oauth_client.make_api_request('users;use_login=1/games/mlb/leagues')

# Manual token refresh
oauth_client.refresh_access_token()

# Test connection
is_connected = oauth_client.test_connection()
```

### Frontend Integration

```javascript
// Initiate login
window.location.href = '/api/auth/login';

// Check authentication status
fetch('/api/auth/status', { credentials: 'include' })
  .then(res => res.json())
  .then(data => {
    if (data.authenticated) {
      console.log('User is authenticated');
    }
  });

// Logout
fetch('/api/auth/logout', { 
  method: 'POST',
  credentials: 'include' 
});
```

## Security Considerations

### Token Storage
- All tokens are encrypted using Fernet symmetric encryption
- Encryption keys must be kept secure and never committed
- Database storage preferred over memory for persistence
- Tokens isolated by service (extensible for other providers)

### CSRF Protection
- State parameter validates OAuth callbacks
- Session-based state verification
- Automatic cleanup after validation

### Environment Isolation
- Separate OAuth apps for dev/staging/production
- Environment-specific redirect URIs
- Isolated token storage per environment

### Rate Limiting
- Respects Yahoo's 20,000 requests/hour limit
- Automatic retry with exponential backoff
- Rate limit headers parsed and logged

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "No valid access token" | Token expired or missing | Re-authenticate via /api/auth/login |
| "Invalid state parameter" | CSRF token mismatch | Clear cookies and retry login |
| "Rate limited" | Too many API requests | Wait for Retry-After period |
| "Token refresh failed" | Invalid refresh token | Full re-authentication required |

### Logging

All authentication events are logged:
- Successful authentications
- Token refreshes
- Authentication failures
- API rate limiting

Check logs at:
- Development: Console output
- Staging/Production: Replit deployment logs

## Testing

### Running Tests

```bash
# Run all auth tests
pytest backend/tests/test_yahoo_oauth.py backend/tests/test_token_manager.py -v

# Run with coverage
pytest backend/tests/test_*.py --cov=backend/src/auth --cov-report=html
```

### Test Coverage

- OAuth flow initialization
- Token exchange and refresh
- Token storage and encryption
- Environment-specific configuration
- Error handling scenarios
- Rate limiting behavior

## Troubleshooting

### Local Development with ngrok

1. Install ngrok: `npm install -g ngrok`
2. Start backend: `python backend/src/app.py`
3. Start ngrok: `ngrok http 5000`
4. Copy HTTPS URL from ngrok
5. Update Yahoo app redirect URI
6. Update YAHOO_REDIRECT_URI in .env
7. Restart backend

### Token Expiration Issues

If tokens frequently expire:
1. Check system time synchronization
2. Verify TOKEN_ENCRYPTION_KEY is consistent
3. Ensure database connection is stable
4. Check refresh token validity (6 months lifetime)

### Database Connection Fallback

If PostgreSQL is unavailable:
- System automatically uses in-memory storage
- Tokens persist only during app lifetime
- Warning logged for operational awareness

## API Endpoints Reference

### POST /api/auth/login
Initiates OAuth flow
- Generates CSRF state token
- Redirects to Yahoo consent page

### GET /api/auth/callback
Handles OAuth callback
- Validates state parameter
- Exchanges code for tokens
- Stores encrypted tokens
- Redirects to application

### POST /api/auth/logout
Clears authentication
- Deletes stored tokens
- Clears session
- Returns success status

### POST /api/auth/refresh
Manually refreshes token
- Uses stored refresh token
- Updates access token
- Returns new expiration

### GET /api/auth/status
Check authentication status
- Returns authentication state
- Tests API connection
- Shows token availability

## Future Enhancements

- [ ] Multi-account support
- [ ] Token management UI
- [ ] Webhook-based token refresh
- [ ] OAuth scope management
- [ ] Audit trail for token usage
- [ ] Token rotation strategy
- [ ] Rate limit dashboard

---
*Last Updated: Implementation of Issue #3*
*Version: 1.0.0*