"""Authentication routes for Yahoo OAuth."""

import os
import secrets
import logging
from flask import Blueprint, request, redirect, jsonify, session, url_for
from backend.src.auth import YahooOAuthClient, TokenManager

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize OAuth client and token manager as globals
oauth_client = None
token_manager = None


def init_auth(app):
    """Initialize authentication with app context."""
    global oauth_client, token_manager
    
    # Initialize token manager
    token_manager = TokenManager(
        db_url=app.config.get('DATABASE_URL'),
        encryption_key=app.config.get('TOKEN_ENCRYPTION_KEY')
    )
    
    # Initialize OAuth client
    oauth_client = YahooOAuthClient(
        client_id=app.config.get('YAHOO_CLIENT_ID'),
        client_secret=app.config.get('YAHOO_CLIENT_SECRET'),
        redirect_uri=app.config.get('YAHOO_REDIRECT_URI'),
        token_manager=token_manager
    )


@auth_bp.route('/login')
def login():
    """Initiate Yahoo OAuth login flow."""
    try:
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        # Get authorization URL
        auth_url = oauth_client.get_authorization_url(state=state)
        
        logger.info(f"Redirecting to Yahoo OAuth: {auth_url}")
        return redirect(auth_url)
        
    except Exception as e:
        logger.error(f"Login initiation failed: {e}")
        return jsonify({'error': 'Failed to initiate login'}), 500


@auth_bp.route('/callback')
def callback():
    """Handle Yahoo OAuth callback."""
    try:
        # Verify state for CSRF protection
        state = request.args.get('state')
        if state != session.pop('oauth_state', None):
            logger.warning("State mismatch in OAuth callback")
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Check for errors
        error = request.args.get('error')
        if error:
            logger.error(f"OAuth error: {error}")
            return jsonify({'error': f'OAuth error: {error}'}), 400
        
        # Get authorization code
        code = request.args.get('code')
        if not code:
            logger.error("No authorization code in callback")
            return jsonify({'error': 'No authorization code received'}), 400
        
        # Exchange code for tokens
        token_data = oauth_client.exchange_code_for_token(code)
        
        # Store success in session
        session['authenticated'] = True
        session['token_expires'] = token_data.get('expires_in', 3600)
        
        # Redirect to success page or dashboard
        redirect_url = os.getenv('AUTH_SUCCESS_REDIRECT', '/')
        logger.info(f"Authentication successful, redirecting to {redirect_url}")
        
        return redirect(redirect_url)
        
    except Exception as e:
        logger.error(f"OAuth callback failed: {e}")
        return jsonify({'error': 'Authentication failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout and clear tokens."""
    try:
        # Clear tokens from storage
        if token_manager:
            token_manager.delete_tokens()
        
        # Clear session
        session.clear()
        
        logger.info("User logged out successfully")
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        return jsonify({'error': 'Logout failed'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Manually refresh access token."""
    try:
        if not oauth_client or not token_manager:
            return jsonify({'error': 'Auth not initialized'}), 500
        
        # Check if we have tokens
        tokens = token_manager.get_valid_tokens()
        if not tokens or not tokens.get('refresh_token'):
            return jsonify({'error': 'No refresh token available'}), 401
        
        # Refresh the token
        new_tokens = oauth_client.refresh_access_token(tokens['refresh_token'])
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'expires_in': new_tokens.get('expires_in', 3600)
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        return jsonify({'error': 'Token refresh failed'}), 500


@auth_bp.route('/status')
def status():
    """Check authentication status."""
    try:
        if not token_manager:
            return jsonify({'authenticated': False, 'error': 'Auth not initialized'}), 500
        
        # Check if we have valid tokens
        tokens = token_manager.get_valid_tokens()
        is_expired = token_manager.is_token_expired()
        
        if tokens and not is_expired:
            # Test the connection
            connection_valid = oauth_client.test_connection() if oauth_client else False
            
            return jsonify({
                'authenticated': True,
                'connection_valid': connection_valid,
                'has_refresh_token': bool(tokens.get('refresh_token'))
            }), 200
        else:
            return jsonify({
                'authenticated': False,
                'expired': is_expired,
                'has_refresh_token': bool(tokens.get('refresh_token')) if tokens else False
            }), 200
            
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({'authenticated': False, 'error': str(e)}), 500