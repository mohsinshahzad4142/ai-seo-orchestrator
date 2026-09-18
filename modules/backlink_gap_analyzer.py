from typing import List, Dict, Any, Set

class CompetitorBacklinkGapAnalyzer:
    def analyze_gaps(
        self, 
        target_backlinks: List[Dict[str, Any]], 
        competitor_backlinks_map: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        target_domains = {b.get("domain", "").lower() for b in target_backlinks if b.get("domain")}
        
        gap_opportunities = []
        seen_domains = set()

        for comp_domain, links in competitor_backlinks_map.items():
            for link in links:
                link_domain = link.get("domain", "").lower()
                if link_domain and link_domain not in target_domains and link_domain not in seen_domains:
                    seen_domains.add(link_domain)
                    score = link.get("authority_score", 50)
                    gap_opportunities.append({
                        "opportunity_domain": link_domain,
                        "linking_competitor": comp_domain,
                        "authority_score": score,
                        "sample_backlink_url": link.get("url", ""),
                        "outreach_priority": "High" if score >= 60 else "Medium"
                    })

        gap_opportunities.sort(key=lambda x: x.get("authority_score", 0), reverse=True)
        return {
            "total_gaps_found": len(gap_opportunities),
            "opportunities": gap_opportunities
        }