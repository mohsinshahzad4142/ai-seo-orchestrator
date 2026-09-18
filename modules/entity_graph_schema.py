from typing import List, Dict, Any, Optional
import json

class MultiEntitySchemaGraph:
    def build_graph(
        self,
        person_name: str,
        person_job: str,
        org_name: str,
        org_url: str,
        service_name: str,
        faqs: Optional[List[Dict[str, str]]] = None
    ) -> str:
        faq_items = [
            {
                "@type": "Question",
                "name": f.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f.get("answer", "")
                }
            }
            for f in (faqs or [])
        ]

        graph_payload: Dict[str, Any] = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Person",
                    "@id": f"{org_url}/#person",
                    "name": person_name,
                    "jobTitle": person_job
                },
                {
                    "@type": "Organization",
                    "@id": f"{org_url}/#organization",
                    "name": org_name,
                    "url": org_url,
                    "founder": {"@id": f"{org_url}/#person"}
                },
                {
                    "@type": "ProfessionalService",
                    "@id": f"{org_url}/#service",
                    "name": service_name,
                    "provider": {"@id": f"{org_url}/#organization"}
                }
            ]
        }
        if faq_items:
            graph_payload["@graph"].append({
                "@type": "FAQPage",
                "mainEntity": faq_items
            })

        return json.dumps(graph_payload, indent=2)