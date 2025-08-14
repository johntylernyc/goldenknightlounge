# Golden Knight Lounge
Version: 1.0.0  
Last Updated: August 2025

Fantasy Baseball Analytics Platform

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/goldenknightlounge.git
cd goldenknightlounge
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Install dependencies:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. Run the application:
```bash
# Backend
python backend/src/app.py

# Frontend (in another terminal)
cd frontend && npm start
```

## Deployment

### Replit Setup

1. Create two Replit projects:
   - `goldenknightlounge` (production)
   - `goldenknightlounge-staging` (staging)

2. Connect each to the appropriate GitHub branch:
   - Production: `main` branch
   - Staging: `staging` branch

3. Configure secrets in each Replit project

### Custom Domain (Cloudflare)

1. Production domain:
   - Add CNAME record: `goldenknightlounge.com` → `goldenknightlounge.repl.co`
   - Add CNAME record: `www` → `goldenknightlounge.repl.co`

2. Staging domain (optional):
   - Add CNAME record: `staging` → `goldenknightlounge-staging.repl.co`

## Environments

- **Production**: https://goldenknightlounge.com
- **Staging**: https://staging.goldenknightlounge.com
- **Local**: http://localhost:3000

## Tech Stack

- Backend: Python/Flask
- Frontend: Node.js/Express
- Database: PostgreSQL
- Deployment: Replit
- CI/CD: GitHub Actions

## License

Private repository - All rights reserved
