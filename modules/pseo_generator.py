from typing import List, Dict, Any

class ProgrammaticSEOEngine:
    def generate_landing_pages(
        self, 
        services: List[str], 
        locations: List[str], 
        brand_name: str = "Mohsin Shahzad"
    ) -> List[Dict[str, Any]]:
        pages = []
        for service in services:
            slug_base = service.lower().replace(" ", "-")
            for loc in locations:
                loc_slug = loc.lower().replace(" ", "-")
                slug = f"/services/{slug_base}-{loc_slug}"
                title = f"Top {service} in {loc} | {brand_name}"
                h1 = f"Enterprise {service} Solutions for {loc} Businesses"
                content = (
                    f"Looking for a reliable {service} in {loc}? "
                    f"{brand_name} delivers scalable, high-performance web architecture, "
                    f"custom integrations, and enterprise-grade SEO optimization tailored for {loc} markets."
                )
                pages.append({
                    "slug": slug,
                    "title": title,
                    "h1": h1,
                    "content": content,
                    "meta_description": f"Hire expert {service} in {loc}. Boost conversions and rankings with {brand_name}."
                })
        return pages