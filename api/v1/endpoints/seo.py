from fastapi import APIRouter, HTTPException, status
from schemas.seo import SEOAuditRequest, SEOAuditResponse
from services.seo_service import SEOService

router = APIRouter()

@router.post("/audit", response_model=SEOAuditResponse, status_code=status.HTTP_200_OK)
def run_seo_audit(request_data: SEOAuditRequest):
    try:
        result = SEOService.analyze_site(request_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SEO Audit processing error: {str(e)}"
        )