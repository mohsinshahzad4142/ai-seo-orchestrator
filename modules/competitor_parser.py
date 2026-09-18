import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Set
import re
from collections import Counter

async def parse_competitor_seo_gaps(target_url: str, reference_target_keywords: Set[str]) -> Dict[str, Any]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-SEO-Orchestrator/1.0"}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
        resp = await client.get(target_url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])]

    text_corpus = f"{title} {meta_desc} " + " ".join(headings)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text_corpus.lower())
    stop_words = {"the", "and", "for", "with", "that", "this", "from", "your", "are", "build", "using", "can", "our"}
    filtered_words = [w for w in words if w not in stop_words]
    word_freq = Counter(filtered_words)

    extracted_terms = set(word_freq.keys())
    missing_gaps = reference_target_keywords - extracted_terms

    return {
        "url": target_url,
        "title": title,
        "meta_description": meta_desc,
        "headings_count": len(headings),
        "top_competitor_terms": word_freq.most_common(12),
        "keyword_gaps": sorted(list(missing_gaps))
    }