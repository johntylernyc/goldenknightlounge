"""Unit tests for token manager."""

import os
import sys
import time
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from cryptography.fernet import Fernet

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth.token_manager import TokenManager


class TestTokenManager:
    """Test token manager functionality."""
    
    @pytest.fixture
    def encryption_key(self):
        """Generate test encryption key."""
        return Fernet.generate_key().decode()
    
    @pytest.fixture
    def token_manager_memory(self, encryption_key):
        """Create token manager with memory storage."""
        # Force memory storage by not providing DB URL
        return TokenManager(db_url=None, encryption_key=encryption_key)
    
    @pytest.fixture
    def mock_db_connection(self):
        """Create mock database connection."""
        with patch('psycopg2.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.__enter__.return_value = mock_conn
            mock_conn.__exit__.return_value = None
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_conn.cursor.return_value.__exit__.return_value = None
            mock_connect.return_value = mock_conn
            yield mock_connect, mock_cursor
    
    def test_initialization_with_key(self, encryption_key):
        """Test token manager initialization with provided key."""
        manager = TokenManager(encryption_key=encryption_key)
        assert manager.cipher is not None
    
    def test_initialization_generate_key(self):
        """Test token manager initialization with generated key."""
        with patch.dict(os.environ, {}, clear=True):
            manager = TokenManager()
            assert manager.cipher is not None
    
    def test_initialization_with_env_key(self):
        """Test token manager initialization with environment key."""
        test_key = Fernet.generate_key().decode()
        with patch.dict(os.environ, {'TOKEN_ENCRYPTION_KEY': test_key}):
            manager = TokenManager()
            assert manager.cipher is not None
    
    def test_save_tokens_memory(self, token_manager_memory):
        """Test saving tokens to memory storage."""
        result = token_manager_memory.save_tokens(
            access_token='test_access',
            refresh_token='test_refresh',
            expires_in=3600,
            scope='read write'
        )
        
        assert result is True
        assert 'yahoo' in token_manager_memory._memory_storage
        stored = token_manager_memory._memory_storage['yahoo']
        assert stored['scope'] == 'read write'
    
    def test_save_tokens_database(self, encryption_key, mock_db_connection):
        """Test saving tokens to database."""
        mock_connect, mock_cursor = mock_db_connection
        
        manager = TokenManager(
            db_url='postgresql://test',
            encryption_key=encryption_key
        )
        
        result = manager.save_tokens(
            access_token='test_access',
            refresh_token='test_refresh',
            expires_in=3600
        )
        
        assert result is True
        # Check that INSERT was called
        assert mock_cursor.execute.called
        insert_call = mock_cursor.execute.call_args_list[-1]
        assert 'INSERT INTO oauth_tokens' in insert_call[0][0]
    
    def test_get_valid_tokens_memory(self, token_manager_memory):
        """Test retrieving tokens from memory storage."""
        # Save tokens first
        token_manager_memory.save_tokens(
            access_token='test_access',
            refresh_token='test_refresh',
            expires_in=3600
        )
        
        # Retrieve tokens
        tokens = token_manager_memory.get_valid_tokens()
        
        assert tokens is not None
        assert tokens['access_token'] == 'test_access'
        assert tokens['refresh_token'] == 'test_refresh'
        assert tokens['expires_at'] > time.time()
    
    def test_get_valid_tokens_not_found(self, token_manager_memory):
        """Test retrieving tokens when none exist."""
        tokens = token_manager_memory.get_valid_tokens()
        assert tokens is None
    
    def test_get_valid_tokens_database(self, encryption_key, mock_db_connection):
        """Test retrieving tokens from database."""
        mock_connect, mock_cursor = mock_db_connection
        
        # Create cipher for encryption
        cipher = Fernet(encryption_key.encode())
        encrypted_access = cipher.encrypt(b'db_access_token').decode()
        encrypted_refresh = cipher.encrypt(b'db_refresh_token').decode()
        
        # Mock database response
        mock_cursor.fetchone.return_value = {
            'access_token': encrypted_access,
            'refresh_token': encrypted_refresh,
            'expires_at': datetime.now() + timedelta(hours=1),
            'scope': 'read'
        }
        
        manager = TokenManager(
            db_url='postgresql://test',
            encryption_key=encryption_key
        )
        
        tokens = manager.get_valid_tokens()
        
        assert tokens is not None
        assert tokens['access_token'] == 'db_access_token'
        assert tokens['refresh_token'] == 'db_refresh_token'
    
    def test_delete_tokens_memory(self, token_manager_memory):
        """Test deleting tokens from memory storage."""
        # Save tokens first
        token_manager_memory.save_tokens(
            access_token='test_access',
            refresh_token='test_refresh'
        )
        
        # Delete tokens
        result = token_manager_memory.delete_tokens()
        
        assert result is True
        assert 'yahoo' not in token_manager_memory._memory_storage
    
    def test_delete_tokens_database(self, encryption_key, mock_db_connection):
        """Test deleting tokens from database."""
        mock_connect, mock_cursor = mock_db_connection
        
        manager = TokenManager(
            db_url='postgresql://test',
            encryption_key=encryption_key
        )
        
        result = manager.delete_tokens()
        
        assert result is True
        # Check that DELETE was called
        assert mock_cursor.execute.called
        delete_call = mock_cursor.execute.call_args_list[-1]
        assert 'DELETE FROM oauth_tokens' in delete_call[0][0]
    
    def test_is_token_expired_no_token(self, token_manager_memory):
        """Test token expiration check with no token."""
        assert token_manager_memory.is_token_expired() is True
    
    def test_is_token_expired_valid(self, token_manager_memory):
        """Test token expiration check with valid token."""
        # Save valid token
        token_manager_memory.save_tokens(
            access_token='test_access',
            expires_in=3600
        )
        
        assert token_manager_memory.is_token_expired() is False
    
    def test_is_token_expired_expired(self, token_manager_memory):
        """Test token expiration check with expired token."""
        # Save expired token
        token_manager_memory.save_tokens(
            access_token='test_access',
            expires_in=-100  # Already expired
        )
        
        assert token_manager_memory.is_token_expired() is True
    
    def test_encryption_decryption(self, token_manager_memory):
        """Test that tokens are properly encrypted and decrypted."""
        original_access = 'my_secret_access_token'
        original_refresh = 'my_secret_refresh_token'
        
        # Save tokens
        token_manager_memory.save_tokens(
            access_token=original_access,
            refresh_token=original_refresh
        )
        
        # Check that stored tokens are encrypted (not plain text)
        stored = token_manager_memory._memory_storage['yahoo']
        assert stored['access_token'] != original_access
        assert stored['refresh_token'] != original_refresh
        
        # Retrieve and check decryption
        tokens = token_manager_memory.get_valid_tokens()
        assert tokens['access_token'] == original_access
        assert tokens['refresh_token'] == original_refresh
    
    @patch('psycopg2.connect')
    def test_database_init_error_fallback(self, mock_connect, encryption_key):
        """Test fallback to memory storage on database error."""
        mock_connect.side_effect = Exception('Database connection failed')
        
        manager = TokenManager(
            db_url='postgresql://test',
            encryption_key=encryption_key
        )
        
        # Should have memory storage as fallback
        assert hasattr(manager, '_memory_storage')
        assert isinstance(manager._memory_storage, dict)