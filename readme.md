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

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with:
```
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
APP_URL=https://your-app-url.ngrok-free.app
```

3. Run the application:
```bash
python run.py
# or
uvicorn app.main:app --reload
```

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
