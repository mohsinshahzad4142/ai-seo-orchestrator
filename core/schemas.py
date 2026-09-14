from pydantic import BaseModel, Field
from typing import List, Optional

class SEOAuditItem(BaseModel):
    issue: str = Field(..., description="Identified SEO issue")
    severity: str = Field(..., description="Severity level: High, Medium, Low")
    recommendation: str = Field(..., description="Actionable fix recommendation")

class SEOAuditOutput(BaseModel):
    site_url: str
    overall_score: int = Field(..., ge=0, le=100)
    summary: str
    critical_issues: List[SEOAuditItem]
    recommended_actions: List[str]

class ContentGenerationOutput(BaseModel):
    title: str
    meta_description: str
    target_keywords: List[str]
    content_markdown: str