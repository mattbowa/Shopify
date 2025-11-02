"""SEO analysis routes."""
from fastapi import APIRouter, HTTPException
from app.services.seo_service import SEOService
from app.services.shopify_service import ShopifyService
from app.models.schemas import SEOCheckResponse

router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/check", response_model=SEOCheckResponse)
async def seo_check(shop: str):
    """Analyze theme files for SEO issues."""
    try:
        # Create services
        shopify_service = ShopifyService(shop)  # This will raise ValueError if not authenticated
        seo_service = SEOService(shopify_service)
        result = await seo_service.check_seo(shop)
        
        return SEOCheckResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

