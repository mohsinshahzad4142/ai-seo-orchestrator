import xml.etree.ElementTree as ET
import httpx
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.seo import IndexingStatus

class IndexingAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_and_parse_sitemap(self, sitemap_url: str) -> List[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(sitemap_url, timeout=10.0)
            response.raise_for_status()

        urls = []
        root = ET.fromstring(response.text)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_tag in root.findall('ns:url', namespace):
            loc = url_tag.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        if not urls:
            for url_tag in root.findall('.//{*}loc'):
                if url_tag.text:
                    urls.append(url_tag.text.strip())

        return urls

    async def process_url_inspection(
        self, website_id: int, url: str, inspection_data: Dict[str, Any]
    ) -> IndexingStatus:
        index_result = inspection_data.get('indexStatusResult', {})

        verdict = index_result.get('verdict', 'NEUTRAL')
        coverage_state = index_result.get('coverageState', 'UNKNOWN')
        robots_txt_state = index_result.get('robotsTxtState', 'UNKNOWN')
        indexing_state = index_result.get('indexingState', 'UNKNOWN')

        stmt = select(IndexingStatus).where(
            IndexingStatus.website_id == website_id,
            IndexingStatus.url == url
        )
        result = await self.db.execute(stmt)
        existing = result.scalars().first()

        if existing:
            existing.verdict = verdict
            existing.coverage_state = coverage_state
            existing.robots_txt_state = robots_txt_state
            existing.indexing_state = indexing_state
            record = existing
        else:
            record = IndexingStatus(
                website_id=website_id,
                url=url,
                verdict=verdict,
                coverage_state=coverage_state,
                robots_txt_state=robots_txt_state,
                indexing_state=indexing_state
            )
            self.db.add(record)

        await self.db.commit()
        return record