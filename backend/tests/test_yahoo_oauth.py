"""Unit tests for Yahoo OAuth authentication."""

import os
import time
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.src.auth.yahoo_oauth import YahooOAuthClient
from backend.src.auth.token_manager import TokenManager


class TestYahooOAuthClient:
    """Test Yahoo OAuth client functionality."""
    
    @pytest.fixture
    def oauth_client(self):
        """Create OAuth client for testing."""
        return YahooOAuthClient(
            client_id='test_client_id',
            client_secret='test_client_secret',
            redirect_uri='http://localhost:5000/auth/callback'
        )
    
    @pytest.fixture
    def mock_token_manager(self):
        """Create mock token manager."""
        mock = Mock(spec=TokenManager)
        mock.get_valid_tokens.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_at': time.time() + 3600
        }
        return mock
    
    def test_initialization(self):
        """Test OAuth client initialization."""
        client = YahooOAuthClient(
            client_id='test_id',
            client_secret='test_secret'
        )
        assert client.client_id == 'test_id'
        assert client.client_secret == 'test_secret'
    
    def test_initialization_from_env(self):
        """Test OAuth client initialization from environment variables."""
        with patch.dict(os.environ, {
            'YAHOO_CLIENT_ID': 'env_client_id',
            'YAHOO_CLIENT_SECRET': 'env_client_secret'
        }):
            client = YahooOAuthClient()
            assert client.client_id == 'env_client_id'
            assert client.client_secret == 'env_client_secret'
    
    def test_initialization_missing_credentials(self):
        """Test OAuth client initialization with missing credentials."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="client_id and client_secret are required"):
                YahooOAuthClient()
    
    def test_get_redirect_uri_production(self):
        """Test redirect URI for production environment."""
        with patch.dict(os.environ, {'NODE_ENV': 'production'}):
            client = YahooOAuthClient(
                client_id='test',
                client_secret='test'
            )
            assert 'goldenknightlounge.com' in client.redirect_uri
    
    def test_get_redirect_uri_staging(self):
        """Test redirect URI for staging environment."""
        with patch.dict(os.environ, {'NODE_ENV': 'staging'}):
            client = YahooOAuthClient(
                client_id='test',
                client_secret='test'
            )
            assert 'staging.goldenknightlounge.com' in client.redirect_uri
    
    def test_get_redirect_uri_development(self):
        """Test redirect URI for development environment."""
        with patch.dict(os.environ, {'NODE_ENV': 'development'}):
            client = YahooOAuthClient(
                client_id='test',
                client_secret='test'
            )
            assert 'localhost' in client.redirect_uri
    
    def test_get_authorization_url(self, oauth_client):
        """Test authorization URL generation."""
        url = oauth_client.get_authorization_url(state='test_state')
        
        assert 'https://api.login.yahoo.com/oauth2/request_auth' in url
        assert 'client_id=test_client_id' in url
        assert 'state=test_state' in url
        assert 'response_type=code' in url
    
    @patch('requests.Session.post')
    def test_exchange_code_for_token_success(self, mock_post, oauth_client):
        """Test successful code exchange for token."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        result = oauth_client.exchange_code_for_token('test_code')
        
        assert result['access_token'] == 'new_access_token'
        assert result['refresh_token'] == 'new_refresh_token'
        assert oauth_client._access_token == 'new_access_token'
        mock_post.assert_called_once()
    
    @patch('requests.Session.post')
    def test_exchange_code_for_token_failure(self, mock_post, oauth_client):
        """Test failed code exchange for token."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Invalid code'
        mock_response.raise_for_status.side_effect = Exception('Bad request')
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception):
            oauth_client.exchange_code_for_token('invalid_code')
    
    @patch('requests.Session.post')
    def test_refresh_access_token_success(self, mock_post, oauth_client):
        """Test successful token refresh."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'refreshed_access_token',
            'refresh_token': 'refreshed_refresh_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        result = oauth_client.refresh_access_token('test_refresh_token')
        
        assert result['access_token'] == 'refreshed_access_token'
        assert oauth_client._access_token == 'refreshed_access_token'
        mock_post.assert_called_once()
    
    def test_refresh_access_token_no_token(self, oauth_client):
        """Test token refresh with no refresh token."""
        with pytest.raises(ValueError, match="No refresh token available"):
            oauth_client.refresh_access_token()
    
    def test_get_access_token_cached(self, oauth_client):
        """Test getting cached access token."""
        oauth_client._access_token = 'cached_token'
        oauth_client._token_expires_at = time.time() + 3600
        
        token = oauth_client.get_access_token()
        assert token == 'cached_token'
    
    def test_get_access_token_from_storage(self, oauth_client, mock_token_manager):
        """Test getting access token from storage."""
        oauth_client.token_manager = mock_token_manager
        
        token = oauth_client.get_access_token()
        assert token == 'test_access_token'
        mock_token_manager.get_valid_tokens.assert_called_once()
    
    @patch('requests.Session.post')
    def test_get_access_token_expired_refresh(self, mock_post, oauth_client, mock_token_manager):
        """Test refreshing expired access token."""
        # Set expired token
        mock_token_manager.get_valid_tokens.return_value = {
            'access_token': 'expired_token',
            'refresh_token': 'test_refresh_token',
            'expires_at': time.time() - 100  # Expired
        }
        oauth_client.token_manager = mock_token_manager
        
        # Mock refresh response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        token = oauth_client.get_access_token()
        assert token == 'new_token'
        mock_post.assert_called_once()
    
    @patch('requests.Session.request')
    def test_make_api_request_success(self, mock_request, oauth_client):
        """Test successful API request."""
        oauth_client._access_token = 'test_token'
        oauth_client._token_expires_at = time.time() + 3600
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test_data'}
        mock_request.return_value = mock_response
        
        result = oauth_client.make_api_request('test/endpoint')
        
        assert result == {'data': 'test_data'}
        mock_request.assert_called_once()
        assert mock_request.call_args[1]['headers']['Authorization'] == 'Bearer test_token'
    
    @patch('requests.Session.request')
    def test_make_api_request_rate_limited(self, mock_request, oauth_client):
        """Test API request with rate limiting."""
        oauth_client._access_token = 'test_token'
        oauth_client._token_expires_at = time.time() + 3600
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_request.return_value = mock_response
        
        with pytest.raises(Exception, match="Rate limited"):
            oauth_client.make_api_request('test/endpoint')
    
    @patch('backend.src.auth.yahoo_oauth.YahooOAuthClient.make_api_request')
    def test_test_connection_success(self, mock_api_request, oauth_client):
        """Test successful connection test."""
        mock_api_request.return_value = {'games': []}
        
        result = oauth_client.test_connection()
        assert result is True
        mock_api_request.assert_called_once_with('users;use_login=1/games')
    
    @patch('backend.src.auth.yahoo_oauth.YahooOAuthClient.make_api_request')
    def test_test_connection_failure(self, mock_api_request, oauth_client):
        """Test failed connection test."""
        mock_api_request.side_effect = Exception('Connection failed')
        
        result = oauth_client.test_connection()
        assert result is False