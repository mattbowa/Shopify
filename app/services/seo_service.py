"""Service for SEO analysis."""
import re
from typing import Dict, List
from bs4 import BeautifulSoup
from app.services.shopify_service import ShopifyService


class SEOService:
    """Service for analyzing SEO in theme files."""
    
    def __init__(self, shopify_service: ShopifyService):
        """Initialize with Shopify service."""
        self.shopify_service = shopify_service
    
    @staticmethod
    def analyze_seo(content: str, asset_key: str) -> Dict:
        """Analyze HTML/Liquid content for SEO issues."""
        issues = []
        warnings = []
        checks_passed = []
        
        # Parse HTML (handles Liquid syntax gracefully)
        try:
            soup = BeautifulSoup(content, 'html.parser')
        except Exception:
            return {
                "asset_key": asset_key,
                "error": "Failed to parse HTML content",
                "issues": [],
                "warnings": [],
                "checks_passed": []
            }
        
        # Check for title tag
        title_tag = soup.find('title')
        if not title_tag:
            issues.append("Missing <title> tag")
        else:
            title_text = title_tag.get_text().strip()
            if not title_text:
                issues.append("Title tag is empty")
            elif len(title_text) > 60:
                warnings.append(
                    f"Title tag is too long ({len(title_text)} chars, recommended: 50-60)"
                )
            elif len(title_text) < 30:
                warnings.append(
                    f"Title tag is too short ({len(title_text)} chars, recommended: 30-60)"
                )
            else:
                checks_passed.append(
                    f"Title tag is well-optimized ({len(title_text)} chars)"
                )
        
        # Check for meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content'):
            issues.append("Missing meta description")
        else:
            desc_content = meta_desc.get('content', '').strip()
            if len(desc_content) > 160:
                warnings.append(
                    f"Meta description is too long ({len(desc_content)} chars, "
                    f"recommended: 150-160)"
                )
            elif len(desc_content) < 120:
                warnings.append(
                    f"Meta description is too short ({len(desc_content)} chars, "
                    f"recommended: 120-160)"
                )
            else:
                checks_passed.append(
                    f"Meta description is well-optimized ({len(desc_content)} chars)"
                )
        
        # Check for H1 tags
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            issues.append("No H1 tag found")
        elif len(h1_tags) > 1:
            warnings.append(f"Multiple H1 tags found ({len(h1_tags)}, should be 1)")
        else:
            checks_passed.append("Single H1 tag found (good)")
        
        # Check for Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        if len(og_tags) == 0:
            warnings.append("No Open Graph tags found")
        else:
            checks_passed.append(f"Found {len(og_tags)} Open Graph tag(s)")
        
        # Check for canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            warnings.append("Missing canonical URL")
        else:
            checks_passed.append("Canonical URL found")
        
        # Check for viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            issues.append("Missing viewport meta tag (required for mobile-friendly)")
        else:
            checks_passed.append("Viewport meta tag found")
        
        # Check images for alt text
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            warnings.append(f"{len(images_without_alt)} image(s) missing alt text")
        if images:
            images_with_alt = len(images) - len(images_without_alt)
            if images_with_alt > 0:
                checks_passed.append(
                    f"{images_with_alt}/{len(images)} images have alt text"
                )
        
        # Check for structured data (JSON-LD)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if len(json_ld_scripts) == 0:
            warnings.append("No structured data (JSON-LD) found")
        else:
            checks_passed.append(
                f"Found {len(json_ld_scripts)} structured data script(s)"
            )
        
        # Check for robots meta tag
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots:
            checks_passed.append("Robots meta tag found")
        
        total = len(issues) + len(warnings) + len(checks_passed)
        score = (len(checks_passed) / total * 100) if total > 0 else 0
        
        return {
            "asset_key": asset_key,
            "issues": issues,
            "warnings": warnings,
            "checks_passed": checks_passed,
            "score": round(score, 2)
        }
    
    async def check_seo(self, shop: str) -> Dict:
        """Perform SEO check on shop's active theme."""
        # Use the injected shopify_service or create a new one
        shopify_service = self.shopify_service
        
        # Get active theme ID
        theme_id = await shopify_service.get_active_theme_id()
        if not theme_id:
            raise ValueError("No active theme found")
        
        # List all assets
        assets = await shopify_service.list_theme_assets(theme_id)
        
        # Filter relevant SEO files (layouts, templates, sections)
        seo_relevant_files = [
            asset for asset in assets
            if asset.get("key", "").startswith(
                ("layout/", "templates/", "sections/", "snippets/")
            )
            and asset.get("key", "").endswith(".liquid")
        ]
        
        # If no assets from API, use common theme files as fallback
        if not seo_relevant_files:
            common_files = [
                "layout/theme.liquid",
                "templates/index.liquid",
                "templates/product.liquid",
                "templates/collection.liquid"
            ]
            seo_relevant_files = [{"key": key} for key in common_files]
        
        # Analyze each relevant file
        results = []
        for asset in seo_relevant_files:
            asset_key = asset.get("key")
            content = await shopify_service.get_theme_asset(theme_id, asset_key)
            
            if content:
                analysis = self.analyze_seo(content, asset_key)
                results.append(analysis)
        
        # Calculate overall score
        total_issues = sum(len(r.get("issues", [])) for r in results)
        total_warnings = sum(len(r.get("warnings", [])) for r in results)
        total_passed = sum(len(r.get("checks_passed", [])) for r in results)
        total_checks = total_issues + total_warnings + total_passed
        overall_score = (total_passed / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "shop": shop,
            "theme_id": theme_id,
            "files_analyzed": len(results),
            "overall_score": round(overall_score, 2),
            "summary": {
                "total_issues": total_issues,
                "total_warnings": total_warnings,
                "total_passed": total_passed
            },
            "results": results
        }

