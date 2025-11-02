"""Authentication routes."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.auth_service import AuthService
from app.models.schemas import AuthCallbackResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/install")
async def install(shop: str):
    """Start OAuth flow for shop installation."""
    if not shop:
        raise HTTPException(status_code=400, detail="Missing 'shop' parameter")
    
    install_url = AuthService.get_install_url(shop)
    return RedirectResponse(url=install_url)


@router.get("/callback")
async def auth_callback(shop: str, code: str):
    """OAuth callback - exchange code for access token."""
    try:
        await AuthService.exchange_code_for_token(shop, code)
        return JSONResponse({
            "message": "App installed!",
            "shop": shop
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

