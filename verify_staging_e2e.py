import httpx
import asyncio

BASE_URL = "http://127.0.0.1:8000"

async def run_e2e_verification():
    async with httpx.AsyncClient(timeout=20.0) as client:
        print("🔍 1. Testing /health...")
        r = await client.get(f"{BASE_URL}/health")
        print("   Result:", r.json())

        print("🔍 2. Testing /api/v1/cron/status...")
        r = await client.get(f"{BASE_URL}/api/v1/cron/status")
        print("   Result:", r.json())

        print("🔍 3. Testing /api/v1/keywords/analyze...")
        r = await client.post(f"{BASE_URL}/api/v1/keywords/analyze", json={
            "seed_keywords": ["nextjs seo agency", "fastapi developer usa"],
            "target_country": "US"
        })
        print("   Result:", r.json())

        print("🔍 4. Testing Vercel Deploy Hook (/api/v1/phase4/deploy)...")
        r = await client.post(f"{BASE_URL}/api/v1/phase4/deploy")
        print("   Result:", r.json())

        print("✨ E2E Staging Verification Smoke Tests Completed.")

if __name__ == "__main__":
    asyncio.run(run_e2e_verification())
