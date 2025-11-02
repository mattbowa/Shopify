"""Legacy main.py - redirects to new app structure."""
# This file is kept for backward compatibility
# New structure uses app/main.py
# To run the app, use: python run.py or uvicorn app.main:app

from app.main import app

__all__ = ["app"]
