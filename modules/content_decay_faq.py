from typing import List, Dict, Any

class ContentDecayFAQInjector:
    def process_decayed_page(
        self, 
        current_html: str, 
        target_questions: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        faq_section_html = "\n<section class='ai-faq-recovery'>\n<h2>Frequently Asked Questions</h2>\n"
        schema_faqs = []
        
        for item in target_questions:
            q = item.get("question", "")
            a = item.get("answer", "")
            faq_section_html += f"<h3>{q}</h3>\n<p>{a}</p>\n"
            schema_faqs.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })
            
        faq_section_html += "</section>"
        enhanced_html = current_html.replace("</body>", f"{faq_section_html}\n</body>") if "</body>" in current_html else current_html + faq_section_html

        return {
            "injected_html_snippet": faq_section_html,
            "updated_full_html": enhanced_html,
            "faq_schema_ld": {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": schema_faqs
            }
        }