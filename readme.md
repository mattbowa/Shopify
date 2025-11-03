# Shopify SEO Checker API

A FastAPI application for analyzing Shopify theme SEO.

## Project Structure

```
shopify/
├── app/
│   ├── main.py              # FastAPI app instance & startup
│   ├── config.py            # Configuration settings
│   ├── api/v1/              # API routes
│   │   ├── auth.py          # Authentication routes
│   │   ├── themes.py        # Theme routes
│   │   ├── seo.py           # SEO analysis routes
│   │   └── routes.py        # Route registration
│   ├── core/                # Core functionality
│   │   └── database.py      # Database helpers
│   ├── models/              # Pydantic schemas
│   │   └── schemas.py       # Request/response models
│   └── services/            # Business logic
│       ├── auth_service.py  # Authentication logic
│       ├── shopify_service.py  # Shopify API interactions
│       └── seo_service.py   # SEO analysis logic
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create this)
```

## Setup

### Local Development

#### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file** (copy from `.env.example`):
```bash
cp .env.example .env
```

Then edit `.env` with your actual values:
```
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
APP_URL=http://localhost:8000
```

**For OAuth to work locally, you need ngrok or similar:**
```bash
# Install ngrok (if not installed)
# Then run:
ngrok http 8000
# Use the ngrok URL for APP_URL in .env
```

3. **Run the application:**

**Option 1: Using run.py (recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Docker locally**
```bash
docker build -t shopify-seo-checker .
docker run -p 8000:8000 --env-file .env shopify-seo-checker
```

4. **Access the API:**
- API docs: http://localhost:8000/docs
- Root: http://localhost:8000/
- All endpoints available at http://localhost:8000

### Deployment to Railway (Docker)

1. **Push your code to GitHub** (if not already)

2. **Create Railway account** at [railway.app](https://railway.app)

3. **Create new project** and select "Deploy from GitHub repo"

4. **Set environment variables** in Railway dashboard:
   - `SHOPIFY_API_KEY` - Your Shopify API key
   - `SHOPIFY_API_SECRET` - Your Shopify API secret
   - `APP_URL` - Your Railway app URL (Railway provides this)

5. **Railway will automatically:**
   - Detect the `Dockerfile`
   - Build the container
   - Deploy the application
   - Set the `PORT` environment variable automatically

6. **Your app will be live** at `https://your-app-name.railway.app`

**Note:** Railway automatically uses the Dockerfile for container-based deployment. The container includes all dependencies and runs FastAPI with Uvicorn.

## API Endpoints

### New API (v1)
- `GET /api/v1/auth/install?shop=shop-name` - Start OAuth flow
- `GET /api/v1/auth/callback?shop=shop-name&code=code` - OAuth callback
- `GET /api/v1/themes?shop=shop-name` - Get themes
- `GET /api/v1/themes/asset?shop=shop-name&theme_id=id&asset_key=key` - Get theme asset
- `GET /api/v1/seo/check?shop=shop-name` - Run SEO analysis

### Legacy Endpoints (backward compatible)
- `GET /install?shop=shop-name`
- `GET /auth/callback?shop=shop-name&code=code`
- `GET /themes?shop=shop-name`
- `GET /theme-asset?shop=shop-name&theme_id=id&asset_key=key`
- `GET /seo-check?shop=shop-name`

## Features

- **Modular Architecture**: Separated into routes, services, and models
- **Type Safety**: Uses Pydantic for request/response validation
- **Scalable**: Easy to add new features and routes
- **Clean Code**: Business logic separated from API routes
