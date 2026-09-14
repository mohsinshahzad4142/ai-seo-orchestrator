from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase4_models import TechnicalIssue, SeverityLevel


class TechnicalSEOAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_technical_health(
        self,
        website_id: int,
        audit_data: Dict[str, Any]
    ) -> List[TechnicalIssue]:
        """
        Analyzes technical SEO audit metrics for a page/site and records classified issues.
        """
        url = audit_data.get("url", "")
        issues: List[TechnicalIssue] = []

        # 1. HTTP Status Code Checks (404/500 Errors)
        status_code = audit_data.get("status_code", 200)
        if status_code >= 400:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="HTTP_ERROR",
                severity=SeverityLevel.CRITICAL,
                details={"status_code": status_code},
                recommendation=f"URL returned HTTP {status_code} status code. Fix broken link or configure appropriate redirect."
            ))

        # 2. HTTPS Security
        if not audit_data.get("is_https", True):
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="NON_HTTPS",
                severity=SeverityLevel.CRITICAL,
                details={"protocol": "http"},
                recommendation="Page is served over HTTP. Migrate to HTTPS and setup 301 redirects."
            ))

        # 3. Meta Robots Indexability
        meta_robots = audit_data.get("meta_robots", "").lower()
        if "noindex" in meta_robots:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="NOINDEX_TAG",
                severity=SeverityLevel.HIGH,
                details={"meta_robots": meta_robots},
                recommendation="Page contains 'noindex' tag. Verify whether blocking search engine indexing is intentional."
            ))

        # 4. Canonical Tag Missing
        canonical = audit_data.get("canonical_url")
        if not canonical:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="MISSING_CANONICAL",
                severity=SeverityLevel.HIGH,
                details={},
                recommendation="Add a self-referential canonical tag to prevent duplicate content risks."
            ))

        # 5. Redirect Chains
        redirect_length = audit_data.get("redirect_chain_length", 0)
        if redirect_length > 1:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="REDIRECT_CHAIN",
                severity=SeverityLevel.HIGH,
                details={"chain_length": redirect_length},
                recommendation=f"Redirect chain detected ({redirect_length} hops). Point origin URL directly to final destination."
            ))

        # 6. Title and H1 Tag Validations
        title = audit_data.get("title")
        h1_list = audit_data.get("h1", [])
        if not title:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="MISSING_TITLE",
                severity=SeverityLevel.HIGH,
                details={},
                recommendation="Add a unique title tag between 50-60 characters."
            ))

        if not h1_list:
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="MISSING_H1",
                severity=SeverityLevel.MEDIUM,
                details={},
                recommendation="Add a clear single <h1> tag containing target focus keywords."
            ))

        # 7. Schema Markup Missing
        if not audit_data.get("schema_present", True):
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="MISSING_SCHEMA",
                severity=SeverityLevel.MEDIUM,
                details={},
                recommendation="Implement JSON-LD structured data (e.g. Article, Organization, or Product)."
            ))

        # 8. Core Web Vitals (CWV Signals - LCP)
        cwv_lcp = audit_data.get("cwv_lcp", 0.0)
        if cwv_lcp > 2.5:
            severity = SeverityLevel.HIGH if cwv_lcp > 4.0 else SeverityLevel.LOW
            issues.append(TechnicalIssue(
                website_id=website_id,
                url=url,
                issue_type="SLOW_LCP",
                severity=severity,
                details={"lcp_seconds": cwv_lcp},
                recommendation=f"LCP duration ({cwv_lcp}s) exceeds fast performance threshold (2.5s). Compress assets and optimize caching."
            ))

        if issues:
            self.db.add_all(issues)
            await self.db.commit()
            for issue in issues:
                await self.db.refresh(issue)

        return issues