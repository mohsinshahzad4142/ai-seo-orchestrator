from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class SEOAuditRequest(BaseModel):
    url: HttpUrl
    target_keywords: List[str]

class SEOAuditResponse(BaseModel):
    url: str
    score: int
    meta_title: str
    meta_description: str
    ai_suggested_title: Optional[str] = None
    ai_suggested_description: Optional[str] = None
    recommendations: List[str]