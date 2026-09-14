import sys
import os

# Project root directory ko Python path mein dynamic append karein
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from core.schemas import SEOAuditOutput, SEOAuditItem
from integrations.openai_client import OpenAIClientWrapper
from integrations.gsc_client import GSCClient
from integrations.gsc_inspection import GSCInspectionClient
from integrations.ga4_client import GA4Client
from integrations.wordpress_client import WordPressClient
from core.multitenant import CredentialManager

def test_imports_and_schemas():
    print("[1/3] Testing Schemas...")
    item = SEOAuditItem(
        issue="Missing H1 tag",
        severity="High",
        recommendation="Add a primary H1 heading to the homepage"
    )
    audit = SEOAuditOutput(
        site_url="https://example.com",
        overall_score=85,
        summary="Good structure with minor fixes needed.",
        critical_issues=[item],
        recommended_actions=["Fix H1 tag"]
    )
    assert audit.overall_score == 85
    print("  ✓ Schemas & Validation PASSED")

def test_client_instantiations():
    print("[2/3] Testing Integrations Instantiation...")
    ai_client = OpenAIClientWrapper()
    assert ai_client is not None
    
    wp_client = WordPressClient("https://example.com", "user", "pass")
    assert wp_client.base_url == "https://example.com"
    print("  ✓ Clients Initialized Successfully")

async def test_multitenant_stub():
    print("[3/3] Testing Multitenant Manager Interface...")
    assert hasattr(CredentialManager, 'get_website_credentials')
    print("  ✓ Multitenant Structure PASSED")

if __name__ == "__main__":
    print("--- Phase 2 Verification Test Suite ---")
    test_imports_and_schemas()
    test_client_instantiations()
    asyncio.run(test_multitenant_stub())
    print("\n✅ Phase 2 Integration Verification Completed Successfully!")