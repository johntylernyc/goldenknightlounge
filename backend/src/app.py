"""
Barebones Flask application for Golden Knight Lounge backend
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['YAHOO_CLIENT_ID'] = os.getenv('YAHOO_CLIENT_ID')
app.config['YAHOO_CLIENT_SECRET'] = os.getenv('YAHOO_CLIENT_SECRET')
app.config['YAHOO_REDIRECT_URI'] = os.getenv('YAHOO_REDIRECT_URI')
app.config['TOKEN_ENCRYPTION_KEY'] = os.getenv('TOKEN_ENCRYPTION_KEY')

# Configure CORS
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins, supports_credentials=True)

# Import and register authentication blueprint
from api.auth_routes import auth_bp, init_auth
app.register_blueprint(auth_bp, url_prefix='/api/auth')
init_auth(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'environment': os.getenv('NODE_ENV', 'development'),
        'message': 'Golden Knight Lounge Backend API'
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Golden Knight Lounge Backend API',
        'version': '0.1.0'
    })

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('NODE_ENV', 'development') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)