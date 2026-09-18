from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from modules.pseo_generator import ProgrammaticSEOEngine
from modules.entity_graph_schema import MultiEntitySchemaGraph
from modules.content_decay_faq import ContentDecayFAQInjector

router = APIRouter(prefix="/api/v1/semantic-seo", tags=["Phase 4: Semantic SEO & Content Engine"])

class PSEORenderRequest(BaseModel):
    services: List[str]
    locations: List[str]
    brand_name: str = "Mohsin Shahzad"

class EntityGraphRequest(BaseModel):
    person_name: str
    person_job: str
    org_name: str
    org_url: str
    service_name: str
    faqs: Optional[List[Dict[str, str]]] = None

class DecayFAQRequest(BaseModel):
    current_html: str
    target_questions: List[Dict[str, str]]

@router.post("/pseo/generate")
async def generate_pseo_pages(req: PSEORenderRequest):
    engine = ProgrammaticSEOEngine()
    pages = engine.generate_landing_pages(req.services, req.locations, req.brand_name)
    return {"status": "success", "count": len(pages), "pages": pages}

@router.post("/schema/entity-graph")
async def build_entity_graph(req: EntityGraphRequest):
    builder = MultiEntitySchemaGraph()
    json_ld = builder.build_graph(
        req.person_name, req.person_job, req.org_name, req.org_url, req.service_name, req.faqs
    )
    return {"status": "success", "schema_graph_json_ld": json_ld}

@router.post("/decay/inject-faq")
async def inject_decay_faq(req: DecayFAQRequest):
    injector = ContentDecayFAQInjector()
    res = injector.process_decayed_page(req.current_html, req.target_questions)
    return {"status": "success", "data": res}