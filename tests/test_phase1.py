import asyncio
from modules.competitor_parser import parse_competitor_seo_gaps
from agents.agent11_keyword_engine import KeywordIntelligenceEngine

async def main():
    # Test Parser Mock/Live check
    gaps = await parse_competitor_seo_gaps(
        "https://example.com", 
        {"services", "next.js", "missing_term"}
    )
    print("Parser Output:", gaps)

if __name__ == "__main__":
    asyncio.run(main())