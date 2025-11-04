"""Service for interacting with Shopify API."""
import httpx
from typing import Dict, List, Optional
from app.config import settings
from app.core.database import get_token


class ShopifyService:
    """Service class for Shopify API operations"""
    
    API_VERSION = "2025-01"
    
    def __init__(self, shop: str):
        """Initialize with shop domain."""
        self.shop = shop
        self.access_token = get_token(shop)
        if not self.access_token:
            raise ValueError(f"Shop {shop} not authenticated")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Shopify API requests."""
        return {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def get_themes(self) -> Dict:
        """Fetch all themes for the shop."""
        url = f"https://{self.shop}/admin/api/{self.API_VERSION}/themes.json"
        
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._get_headers())
        
        if res.status_code != 200:
            raise Exception(f"Failed to fetch themes: {res.status_code} - {res.text}")
        
        return res.json()
    
    async def get_active_theme_id(self) -> Optional[str]:
        """Get the active (main) theme ID for the shop."""
        themes_data = await self.get_themes()
        themes = themes_data.get("themes", [])
        
        for theme in themes:
            if theme.get("role") == "main":
                return str(theme.get("id"))
        return None
    
    async def get_theme_asset(self, theme_id: str, asset_key: str) -> Optional[str]:
        """Get the content of a specific theme asset."""
        url = f"https://{self.shop}/admin/api/{self.API_VERSION}/themes/{theme_id}/assets.json"
        params = {"asset[key]": asset_key}
        
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._get_headers(), params=params)
        
        if res.status_code != 200:
            return None
        
        data = res.json()
        return data.get("asset", {}).get("value")
    
    async def list_theme_assets(self, theme_id: str) -> List[Dict]:
        """List all assets for a theme (Note: REST API may not support this)."""
        url = f"https://{self.shop}/admin/api/{self.API_VERSION}/themes/{theme_id}/assets.json"
        
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._get_headers())
        
        if res.status_code != 200:
            return []
        
        data = res.json()
        return data.get("assets", [])

