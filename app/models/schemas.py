"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from typing import List, Optional


class AuthCallbackResponse(BaseModel):
    """Response model for auth callback."""
    message: str
    shop: str


class ThemeAssetResponse(BaseModel):
    """Response model for theme asset."""
    asset_key: str
    content: str


class SEOIssue(BaseModel):
    """SEO analysis result for a single file."""
    asset_key: str
    issues: List[str] = []
    warnings: List[str] = []
    checks_passed: List[str] = []
    score: float = 0.0
    error: Optional[str] = None


class SEOCheckResponse(BaseModel):
    """Response model for SEO check."""
    shop: str
    theme_id: str
    files_analyzed: int
    overall_score: float
    summary: dict
    results: List[SEOIssue]

