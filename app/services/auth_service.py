"""Service for authentication and OAuth flow."""
from fastapi.responses import RedirectResponse
import httpx
from app.config import settings
from app.core.database import save_token


class AuthService:
    """Service for handling Shopify OAuth authentication."""
    
    @staticmethod
    def get_install_url(shop: str) -> str:
        """Generate the Shopify OAuth install URL."""
        redirect_uri = f"{settings.app_url}/auth/callback"
        scopes = "read_themes,read_content,read_files"
        
        return (
            f"https://{shop}/admin/oauth/authorize"
            f"?client_id={settings.shopify_api_key}"
            f"&scope={scopes}"
            f"&redirect_uri={redirect_uri}"
        )
    
    @staticmethod
    async def exchange_code_for_token(shop: str, code: str) -> str:
        """Exchange OAuth code for access token."""
        token_url = f"https://{shop}/admin/oauth/access_token"
        
        async with httpx.AsyncClient() as client:
            res = await client.post(token_url, json={
                "client_id": settings.shopify_api_key,
                "client_secret": settings.shopify_api_secret,
                "code": code
            })
            data = res.json()
        
        access_token = data.get("access_token")
        if not access_token:
            raise ValueError(f"Failed to get access token: {data}")
        
        # Save token to database
        save_token(shop, access_token)
        return access_token

