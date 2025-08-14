"""Yahoo OAuth 2.0 Authentication Client for Fantasy Baseball API."""

import os
import time
import json
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class YahooOAuthClient:
    """Handles Yahoo OAuth 2.0 authentication flow and token management."""
    
    BASE_AUTH_URL = "https://api.login.yahoo.com/oauth2"
    BASE_API_URL = "https://fantasysports.yahooapis.com/fantasy/v2"
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        token_manager: Optional['TokenManager'] = None
    ):
        """
        Initialize Yahoo OAuth client.
        
        Args:
            client_id: Yahoo app client ID
            client_secret: Yahoo app client secret
            redirect_uri: OAuth redirect URI
            token_manager: Token storage manager instance
        """
        self.client_id = client_id or os.getenv('YAHOO_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('YAHOO_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or self._get_redirect_uri()
        self.token_manager = token_manager
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Yahoo client_id and client_secret are required")
        
        self._session = requests.Session()
        self._access_token = None
        self._token_expires_at = 0
    
    def _get_redirect_uri(self) -> str:
        """Get environment-specific redirect URI."""
        env = os.getenv('NODE_ENV', 'development')
        
        if env == 'production':
            return os.getenv('YAHOO_REDIRECT_URI', 'https://goldenknightlounge.com/auth/callback')
        elif env == 'staging':
            return os.getenv('YAHOO_REDIRECT_URI', 'https://staging.goldenknightlounge.com/auth/callback')
        else:
            # Local development - use ngrok URL
            return os.getenv('YAHOO_REDIRECT_URI', 'http://localhost:5000/auth/callback')
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate Yahoo OAuth authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL for user consent
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'language': 'en-us'
        }
        
        if state:
            params['state'] = state
        
        return f"{self.BASE_AUTH_URL}/request_auth?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Token response containing access_token and refresh_token
        """
        url = f"{self.BASE_AUTH_URL}/get_token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        response = self._session.post(
            url,
            data=data,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code != 200:
            logger.error(f"Token exchange failed: {response.text}")
            response.raise_for_status()
        
        token_data = response.json()
        
        # Store tokens if token manager is available
        if self.token_manager:
            self.token_manager.save_tokens(
                access_token=token_data['access_token'],
                refresh_token=token_data.get('refresh_token'),
                expires_in=token_data.get('expires_in', 3600)
            )
        
        # Cache access token
        self._access_token = token_data['access_token']
        self._token_expires_at = time.time() + token_data.get('expires_in', 3600)
        
        logger.info("Successfully exchanged code for tokens")
        return token_data
    
    def refresh_access_token(self, refresh_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Refresh the access token using refresh token.
        
        Args:
            refresh_token: Refresh token (if not provided, loads from storage)
            
        Returns:
            New token response
        """
        if not refresh_token and self.token_manager:
            tokens = self.token_manager.get_valid_tokens()
            refresh_token = tokens.get('refresh_token') if tokens else None
        
        if not refresh_token:
            raise ValueError("No refresh token available")
        
        url = f"{self.BASE_AUTH_URL}/get_token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = self._session.post(
            url,
            data=data,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code != 200:
            logger.error(f"Token refresh failed: {response.text}")
            response.raise_for_status()
        
        token_data = response.json()
        
        # Update stored tokens
        if self.token_manager:
            self.token_manager.save_tokens(
                access_token=token_data['access_token'],
                refresh_token=token_data.get('refresh_token', refresh_token),
                expires_in=token_data.get('expires_in', 3600)
            )
        
        # Update cached token
        self._access_token = token_data['access_token']
        self._token_expires_at = time.time() + token_data.get('expires_in', 3600)
        
        logger.info("Successfully refreshed access token")
        return token_data
    
    def get_access_token(self) -> str:
        """
        Get valid access token, refreshing if necessary.
        
        Returns:
            Valid access token
        """
        # Check cached token first
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token
        
        # Try to get from storage
        if self.token_manager:
            tokens = self.token_manager.get_valid_tokens()
            if tokens and tokens.get('access_token'):
                self._access_token = tokens['access_token']
                self._token_expires_at = tokens.get('expires_at', 0)
                
                # Check if token needs refresh (with 60 second buffer)
                if time.time() < self._token_expires_at - 60:
                    return self._access_token
                
                # Token expired, try to refresh
                if tokens.get('refresh_token'):
                    logger.info("Access token expired, refreshing...")
                    self.refresh_access_token(tokens['refresh_token'])
                    return self._access_token
        
        raise ValueError("No valid access token available. Please authenticate first.")
    
    def make_api_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retry_on_401: bool = True
    ) -> Dict[str, Any]:
        """
        Make authenticated API request to Yahoo Fantasy API.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method
            params: Query parameters
            data: Request body data
            retry_on_401: Whether to retry with refreshed token on 401
            
        Returns:
            API response data
        """
        url = f"{self.BASE_API_URL}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Accept': 'application/json'
        }
        
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data
        )
        
        # Handle token expiration
        if response.status_code == 401 and retry_on_401:
            logger.info("Received 401, attempting token refresh...")
            if self.token_manager:
                tokens = self.token_manager.get_valid_tokens()
                if tokens and tokens.get('refresh_token'):
                    self.refresh_access_token(tokens['refresh_token'])
                    # Retry request with new token
                    return self.make_api_request(
                        endpoint, method, params, data, retry_on_401=False
                    )
        
        # Check for rate limiting
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After', '60')
            logger.warning(f"Rate limited. Retry after {retry_after} seconds")
            raise Exception(f"Rate limited. Retry after {retry_after} seconds")
        
        response.raise_for_status()
        return response.json()
    
    def test_connection(self) -> bool:
        """
        Test the OAuth connection by making a simple API call.
        
        Returns:
            True if connection successful
        """
        try:
            # Try to get user's games
            self.make_api_request('users;use_login=1/games')
            logger.info("OAuth connection test successful")
            return True
        except Exception as e:
            logger.error(f"OAuth connection test failed: {e}")
            return False