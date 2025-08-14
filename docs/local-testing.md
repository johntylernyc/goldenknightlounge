# Local Testing Guide

This guide covers setting up and testing the Golden Knight Lounge application on your local development machine.

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (or use SQLite for development)
- Git
- ngrok (for OAuth testing)

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/goldenknightlounge.git
cd goldenknightlounge
```

### 2. Create Environment File

```bash
# Copy example environment file
cp config/.env.example .env

# Edit .env with your local settings
```

### 3. Configure Local Environment Variables

Edit `.env` file:

```bash
# Environment
NODE_ENV=development

# Backend
API_PORT=5000
PORT=3000

# Database - PostgreSQL (required)
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/goldenknightlounge_dev

# Yahoo OAuth (for testing OAuth)
YAHOO_CLIENT_ID=your_dev_client_id
YAHOO_CLIENT_SECRET=your_dev_client_secret
YAHOO_REDIRECT_URI=http://localhost:5000/api/auth/callback

# Security (generate these)
FLASK_SECRET_KEY=dev_secret_key_change_this
TOKEN_ENCRYPTION_KEY=generate_with_fernet_for_dev
JWT_SECRET=dev_jwt_secret_change_this

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Feature Flags
ENABLE_DEBUG_LOGGING=true
ENABLE_LIVE_STATS=false
```

## Backend Setup

### 1. Create Python Virtual Environment

Windows:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

Mac/Linux:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. PostgreSQL Setup (Required)

#### Windows Setup

1. **Install PostgreSQL**:
   - Download from https://www.postgresql.org/download/windows/
   - Run installer (version 15 or 16 recommended)
   - Remember your postgres password
   - Default port: 5432

2. **Add to PATH** (if not done by installer):
   ```powershell
   # Add to System PATH (run as Administrator)
   $postgresPath = "C:\Program Files\PostgreSQL\16\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$postgresPath", [EnvironmentVariableTarget]::Machine)
   ```

3. **Create Development Database**:
   ```bash
   # Open new terminal after PATH update
   psql -U postgres
   # Enter your postgres password
   
   # In psql prompt:
   CREATE DATABASE goldenknightlounge_dev;
   \q
   ```

#### Mac/Linux Setup

```bash
# Mac with Homebrew
brew install postgresql
brew services start postgresql
createdb goldenknightlounge_dev

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb goldenknightlounge_dev
```

### 3. Install Python Dependencies

#### For Python 3.13 on Windows

If you encounter issues with psycopg2-binary on Python 3.13:

**Option 1: Install Build Tools** (Recommended)
```bash
# 1. Install Microsoft C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Install "Desktop development with C++" workload

# 2. Install psycopg2 (not binary)
pip install psycopg2

# 3. Install rest of requirements
pip install -r requirements.txt
```

**Option 2: Use Python 3.12**
```bash
# Install Python 3.12 from python.org
# Create venv with Python 3.12
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### For Other Systems

```bash
# Should work without issues
pip install -r requirements.txt
```

### 4. Configure Database Connection

Update your `.env` file:
```bash
# Local PostgreSQL
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/goldenknightlounge_dev

# Or if using different user
DATABASE_URL=postgresql://username:password@localhost:5432/goldenknightlounge_dev
```

The database tables will be automatically created on first run when the application starts.

### 5. Run Backend Server

```bash
# From backend directory with venv activated
python src/app.py

# Server runs at http://localhost:5000
# Test with: curl http://localhost:5000/api/health
```

## Frontend Setup (If Applicable)

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
# Or
npm start

# Frontend runs at http://localhost:3000
```

## Testing OAuth Authentication

OAuth requires HTTPS callbacks, so we need ngrok for local testing.

### 1. Install ngrok

```bash
# Install globally
npm install -g ngrok

# Or download from https://ngrok.com/download
```

### 2. Start ngrok Tunnel

```bash
# In a new terminal, create tunnel to backend
ngrok http 5000

# You'll see output like:
# Forwarding https://abc123.ngrok.io -> http://localhost:5000
```

### 3. Update OAuth Configuration

1. Copy the HTTPS URL from ngrok (e.g., `https://abc123.ngrok.io`)

2. Update `.env`:
```bash
YAHOO_REDIRECT_URI=https://abc123.ngrok.io/api/auth/callback
```

3. Update Yahoo App:
   - Go to [Yahoo Developer](https://developer.yahoo.com/apps/)
   - Edit your development app
   - Add the ngrok redirect URI

4. Restart backend server

### 4. Test OAuth Flow

1. Navigate to: `http://localhost:5000/api/auth/login`
2. You'll be redirected to Yahoo
3. Approve access
4. Should redirect back to your callback URL
5. Check logs for token storage confirmation

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_yahoo_oauth.py -v

# Run specific test
pytest tests/test_yahoo_oauth.py::TestYahooOAuthClient::test_initialization -v
```

### Linting and Code Quality

```bash
cd backend

# Python linting
flake8 src/

# Auto-format code
black src/

# Type checking (if using)
mypy src/
```

## Common Development Tasks

### 1. Testing New API Endpoint

```python
# Quick test script (test_api.py)
import requests

# Test health endpoint
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Test auth status
response = requests.get('http://localhost:5000/api/auth/status')
print(response.json())
```

### 2. Testing Database Connections

```python
# Test database connection (test_db.py)
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print("Database connected successfully!")
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")
```

### 3. Debugging OAuth Issues

Enable detailed logging:

```python
# In your .env
ENABLE_DEBUG_LOGGING=true

# In your test code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. Testing with Mock Data

```python
# Create test_data.py for development
def get_mock_league_data():
    return {
        'league_key': '431.l.41728',
        'name': 'Test League',
        'season': 2024,
        # ... mock data
    }

# Use in development
if os.getenv('NODE_ENV') == 'development':
    from test_data import get_mock_league_data
    data = get_mock_league_data()
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000

# Kill the process or use different port
API_PORT=5001 python src/app.py
```

### Database Connection Errors

1. **PostgreSQL not running**:
```bash
# Start PostgreSQL
# Windows: Check Services
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

2. **Wrong connection string**:
   - Check DATABASE_URL format
   - Verify username/password
   - Check database exists

3. **Fallback to SQLite**:
```bash
DATABASE_URL=sqlite:///dev.db python src/app.py
```

### OAuth Redirect Errors

1. **Invalid redirect URI**:
   - Ensure ngrok URL matches Yahoo app
   - Include `/api/auth/callback` path
   - Use HTTPS URL from ngrok

2. **Session issues**:
   - Check FLASK_SECRET_KEY is set
   - Clear browser cookies
   - Try incognito mode

3. **Token storage fails**:
   - Verify TOKEN_ENCRYPTION_KEY is set
   - Check database connection
   - Review logs for encryption errors

### Import Errors

```bash
# Ensure virtual environment is activated
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Environment Variables Not Loading

```bash
# Check .env file location (project root)
# Install python-dotenv
pip install python-dotenv

# Verify in Python
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('YAHOO_CLIENT_ID'))
```

## Development Tips

### 1. Use Environment-Specific Config

```python
# In app.py
if os.getenv('NODE_ENV') == 'development':
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
```

### 2. Hot Reload

Backend auto-reloads with Flask debug mode:
```python
app.run(debug=True)
```

### 3. Database Migrations During Development

```bash
# If using Alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Testing Email/Notifications

Use tools like:
- [MailHog](https://github.com/mailhog/MailHog) for email testing
- Console logging for development

### 5. API Testing Tools

- [Postman](https://www.postman.com/) - GUI for API testing
- [HTTPie](https://httpie.io/) - CLI tool
- curl - Built-in CLI tool

Example:
```bash
# Test with HTTPie
http GET localhost:5000/api/health

# Test with curl
curl -X GET http://localhost:5000/api/health
```

## VSCode Setup (Recommended)

### Extensions
- Python
- Pylance
- Black Formatter
- GitLens

### Launch Configuration

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "backend/src/app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--port", "5000"],
      "jinja": true
    }
  ]
}
```

### Settings

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["backend/tests"],
  "[python]": {
    "editor.formatOnSave": true
  }
}
```

## Next Steps

1. Complete local setup
2. Run tests to verify everything works
3. Test OAuth flow with ngrok
4. Start developing features
5. Follow [Development Workflow](./development-workflow.md) for contributing

---
*Last Updated: [Current Date]*
*For deployment procedures, see [Development Workflow](./development-workflow.md)*