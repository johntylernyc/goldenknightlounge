"""Token storage and management for Yahoo OAuth."""

import os
import json
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages OAuth token storage and retrieval with encryption."""
    
    def __init__(self, db_url: Optional[str] = None, encryption_key: Optional[str] = None):
        """
        Initialize token manager.
        
        Args:
            db_url: PostgreSQL connection URL
            encryption_key: Fernet encryption key for token encryption
        """
        self.db_url = db_url or os.getenv('DATABASE_URL')
        
        # Use provided key or generate/load from environment
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        else:
            key = os.getenv('TOKEN_ENCRYPTION_KEY')
            if not key:
                # Generate a new key for development
                key = Fernet.generate_key().decode()
                logger.warning(f"Generated new encryption key: {key}")
                logger.warning("Set TOKEN_ENCRYPTION_KEY environment variable in production!")
            self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database table for token storage."""
        if not self.db_url:
            logger.warning("No database URL provided, using in-memory storage")
            self._memory_storage = {}
            return
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS oauth_tokens (
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
                        )
                    """)
                    
                    # Create index for faster lookups
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_oauth_tokens_service 
                        ON oauth_tokens(service)
                    """)
                    
                    conn.commit()
                    logger.info("OAuth tokens table initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            # Fall back to in-memory storage
            self._memory_storage = {}
    
    def save_tokens(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: int = 3600,
        scope: Optional[str] = None
    ) -> bool:
        """
        Save OAuth tokens with encryption.
        
        Args:
            access_token: Access token to store
            refresh_token: Refresh token to store
            expires_in: Token expiration in seconds
            scope: OAuth scope
            
        Returns:
            True if saved successfully
        """
        try:
            # Encrypt tokens
            encrypted_access = self.cipher.encrypt(access_token.encode()).decode()
            encrypted_refresh = self.cipher.encrypt(refresh_token.encode()).decode() if refresh_token else None
            
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            if hasattr(self, '_memory_storage'):
                # Use in-memory storage
                self._memory_storage['yahoo'] = {
                    'access_token': encrypted_access,
                    'refresh_token': encrypted_refresh,
                    'expires_at': expires_at.timestamp(),
                    'scope': scope
                }
                logger.info("Tokens saved to memory storage")
                return True
            
            # Save to database
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO oauth_tokens (service, access_token, refresh_token, expires_at, scope)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (service) 
                        DO UPDATE SET 
                            access_token = EXCLUDED.access_token,
                            refresh_token = COALESCE(EXCLUDED.refresh_token, oauth_tokens.refresh_token),
                            expires_at = EXCLUDED.expires_at,
                            scope = EXCLUDED.scope,
                            updated_at = CURRENT_TIMESTAMP
                    """, ('yahoo', encrypted_access, encrypted_refresh, expires_at, scope))
                    
                    conn.commit()
                    logger.info("Tokens saved to database")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to save tokens: {e}")
            return False
    
    def get_valid_tokens(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve valid tokens from storage.
        
        Returns:
            Dictionary with access_token, refresh_token, and expires_at
        """
        try:
            if hasattr(self, '_memory_storage'):
                # Get from memory storage
                data = self._memory_storage.get('yahoo')
                if not data:
                    return None
                
                return {
                    'access_token': self.cipher.decrypt(data['access_token'].encode()).decode(),
                    'refresh_token': self.cipher.decrypt(data['refresh_token'].encode()).decode() if data.get('refresh_token') else None,
                    'expires_at': data['expires_at'],
                    'scope': data.get('scope')
                }
            
            # Get from database
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT access_token, refresh_token, expires_at, scope
                        FROM oauth_tokens
                        WHERE service = %s
                        ORDER BY updated_at DESC
                        LIMIT 1
                    """, ('yahoo',))
                    
                    row = cursor.fetchone()
                    if not row:
                        return None
                    
                    # Decrypt tokens
                    return {
                        'access_token': self.cipher.decrypt(row['access_token'].encode()).decode(),
                        'refresh_token': self.cipher.decrypt(row['refresh_token'].encode()).decode() if row['refresh_token'] else None,
                        'expires_at': row['expires_at'].timestamp(),
                        'scope': row['scope']
                    }
                    
        except Exception as e:
            logger.error(f"Failed to retrieve tokens: {e}")
            return None
    
    def delete_tokens(self) -> bool:
        """
        Delete stored tokens.
        
        Returns:
            True if deleted successfully
        """
        try:
            if hasattr(self, '_memory_storage'):
                self._memory_storage.pop('yahoo', None)
                logger.info("Tokens deleted from memory storage")
                return True
            
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM oauth_tokens WHERE service = %s", ('yahoo',))
                    conn.commit()
                    logger.info("Tokens deleted from database")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to delete tokens: {e}")
            return False
    
    def is_token_expired(self) -> bool:
        """
        Check if the stored access token is expired.
        
        Returns:
            True if expired or no token found
        """
        tokens = self.get_valid_tokens()
        if not tokens:
            return True
        
        # Check with 60 second buffer
        return time.time() >= tokens.get('expires_at', 0) - 60