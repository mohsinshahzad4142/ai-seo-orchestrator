from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter(prefix="/api/v1/semantic-seo", tags=["Semantic & pSEO"])

class PSeoRequest(BaseModel):
    template_type: str = "location-service"
    seed_keywords: List[str] = []
    services: Optional[List[str]] = ["API Development", "Next.js Architecture"]
    locations: Optional[List[str]] = ["New York, NY", "Austin, TX"]

class EntityGraphRequest(BaseModel):
    brand_name: Optional[str] = "Mohsin SEO Agency"
    entities: List[str] = ["nextjs seo agency", "fastapi developer usa"]
    target_url: Optional[str] = "https://mohsinshahzad.vercel.app"

class DecayFAQRequest(BaseModel):
    target_url: str = "https://mohsinshahzad.vercel.app/blog/old-post"
    content: str = "Existing low-performing blog content needing topical depth refresh."
    decayed_keywords: List[str] = ["nextjs seo agency", "fastapi developer usa"]
    custom_faqs: Optional[List[Dict[str, str]]] = None

@router.post("/pseo/generate")
async def pseo_generate(req: PSeoRequest):
    eff_services = req.services if req.services else ["API Development", "Next.js Architecture"]
    eff_locations = req.locations if req.locations else ["New York, NY", "Austin, TX"]
    
    pages = []
    for loc in eff_locations:
        for srv in eff_services:
            slug_part = f"{loc.lower().replace(',', '').replace(' ', '-')}-{srv.lower().replace(' ', '-')}"
            pages.append({
                "slug": f"/solutions/{slug_part}",
                "title": f"Best {srv} in {loc} | Production Ready",
                "meta_description": f"High-conversion {srv} solutions specialized for businesses across {loc}.",
                "status": "bulk_generated"
            })
            
    return {
        "status": "success",
        "action": "pseo_bulk_generation",
        "template_type": req.template_type,
        "total_generated": len(pages),
        "pages": pages,
        "simulation": True
    }

@router.post("/schema/entity-graph")
async def build_entity_graph(req: EntityGraphRequest):
    nodes = [
        {
            "@id": f"{req.target_url or 'https://mohsinshahzad.vercel.app'}#website",
            "@type": "WebSite",
            "name": req.brand_name
        }
    ]
    edges = []
    target = req.target_url or "https://mohsinshahzad.vercel.app"
    for i, ent in enumerate(req.entities):
        node_id = f"{target}#entity-{i+1}"
        nodes.append({
            "@id": node_id,
            "@type": "DefinedTerm",
            "name": ent,
            "inDefinedTermSet": "SEO-Knowledge-Graph"
        })
        edges.append({
            "from": target,
            "relation": "about",
            "to": node_id,
            "label": ent
        })
        
    return {
        "status": "success",
        "action": "multi_entity_schema_graph_builder",
        "json_ld_graph": {
            "@context": "https://schema.org",
            "@graph": nodes
        },
        "nodes_count": len(nodes),
        "edges": edges,
        "simulation": True
    }

@router.post("/decay/inject-faq")
async def inject_decay_faq(req: DecayFAQRequest):
    faqs = req.custom_faqs if req.custom_faqs else []
    if not faqs:
        for kw in req.decayed_keywords:
            faqs.append({
                "question": f"Why is technical authority critical for a {kw}?",
                "answer": f"Optimizing semantic depth and direct CMS metadata sync prevents traffic decay for competitive queries like {kw}."
            })
    
    faq_markdown = "\n\n## Frequently Asked Questions\n" + "\n\n".join(
        f"### {item['question']}\n{item['answer']}" for item in faqs
    )
    patched_content = req.content.rstrip() + faq_markdown

    schema_main_entity = [
        {
            "@type": "Question",
            "name": item["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["answer"]
            }
        }
        for item in faqs
    ]
    
    return {
        "status": "success",
        "action": "content_decay_faq_injector",
        "target_url": req.target_url,
        "injected_faq_count": len(faqs),
        "patched_content": patched_content,
        "faq_json_ld": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": schema_main_entity
        },
        "simulation": True
    }