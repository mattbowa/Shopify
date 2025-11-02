"""Theme-related routes."""
from fastapi import APIRouter, HTTPException
from app.services.shopify_service import ShopifyService
from app.models.schemas import ThemeAssetResponse

router = APIRouter(prefix="/themes", tags=["Themes"])


@router.get("")
async def get_themes(shop: str):
    """Fetch all themes from the shop."""
    try:
        service = ShopifyService(shop)
        return await service.get_themes()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/asset")
async def get_theme_asset(shop: str, theme_id: str, asset_key: str):
    """Fetch a specific theme asset."""
    try:
        service = ShopifyService(shop)
        content = await service.get_theme_asset(theme_id, asset_key)
        
        if content is None:
            raise HTTPException(
                status_code=404,
                detail=f"Asset '{asset_key}' not found or could not be retrieved"
            )
        
        return ThemeAssetResponse(
            asset_key=asset_key,
            content=content
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

