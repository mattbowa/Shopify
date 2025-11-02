"""Main FastAPI application."""
from fastapi import FastAPI
from app.core.database import init_db
from app.api.v1.routes import api_router

# Create FastAPI app instance
app = FastAPI(
    title="Shopify SEO Checker API",
    description="API for analyzing Shopify theme SEO",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Shopify SEO Checker API is running 🚀"}


# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Include legacy routes for backward compatibility
@app.get("/install")
async def install_legacy(shop: str):
    """Legacy install endpoint - redirects to new route."""
    from fastapi.responses import RedirectResponse
    from app.services.auth_service import AuthService
    install_url = AuthService.get_install_url(shop)
    return RedirectResponse(url=install_url)


@app.get("/auth/callback")
async def auth_callback_legacy(shop: str, code: str):
    """Legacy auth callback - redirects to new route."""
    from fastapi.responses import JSONResponse
    from app.services.auth_service import AuthService
    try:
        await AuthService.exchange_code_for_token(shop, code)
        return JSONResponse({"message": "App installed!", "shop": shop})
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/themes")
async def themes_legacy(shop: str):
    """Legacy themes endpoint - redirects to new route."""
    from app.services.shopify_service import ShopifyService
    try:
        service = ShopifyService(shop)
        return await service.get_themes()
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/theme-asset")
async def theme_asset_legacy(shop: str, theme_id: str, asset_key: str):
    """Legacy theme-asset endpoint - redirects to new route."""
    from fastapi import HTTPException
    from app.services.shopify_service import ShopifyService
    try:
        service = ShopifyService(shop)
        content = await service.get_theme_asset(theme_id, asset_key)
        if content is None:
            raise HTTPException(status_code=404, detail="Asset not found")
        return {"asset_key": asset_key, "content": content}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/seo-check")
async def seo_check_legacy(shop: str):
    """Legacy seo-check endpoint - redirects to new route."""
    from fastapi import HTTPException
    from app.services.seo_service import SEOService
    from app.services.shopify_service import ShopifyService
    try:
        ShopifyService(shop)  # Verify authentication
        seo_service = SEOService(ShopifyService(shop))
        result = await seo_service.check_seo(shop)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

