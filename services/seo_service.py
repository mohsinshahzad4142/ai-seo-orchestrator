import json
import httpx
from bs4 import BeautifulSoup
from google import genai
from core.config import settings
from schemas.seo import SEOAuditRequest, SEOAuditResponse

class SEOService:
    @staticmethod
    def _generate_ai_suggestions(title: str, description: str, keywords: list[str]):
        """Gemini AI se target keywords ke mutabiq meta title aur description rewrite karwata hai."""
        
        # Check if API Key is set
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "AIzaSyYourActualGeminiApiKeyHere":
            print("\n[GEMINI CONFIG ERROR]: .env file mein GEMINI_API_KEY add nahi hui hai!\n")
            return "API Key Missing in .env", "API Key Missing in .env"

        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            prompt = f"""
            Act as an expert SEO Copywriter.
            Target Keywords: {', '.join(keywords)}
            Current Meta Title: {title}
            Current Meta Description: {description}

            Task: Provide an optimized Meta Title (30-60 chars) and Meta Description (120-160 chars) incorporating the target keywords naturally.

            Output format (Strict JSON):
            {{
                "suggested_title": "...",
                "suggested_description": "..."
            }}
            """

            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )

            raw_text = response.text.strip()
            
            # Clean markdown JSON block formatting if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            data = json.loads(raw_text)
            return data.get("suggested_title"), data.get("suggested_description")

        except Exception as e:
            # Exact error terminal par print karein
            print(f"\n[GEMINI API ERROR DETAIL]: {type(e).__name__} - {str(e)}\n")
            return f"AI Error: {str(e)[:30]}...", f"AI Error: {str(e)[:30]}..."

    @staticmethod
    def analyze_site(data: SEOAuditRequest) -> SEOAuditResponse:
        url = str(data.url)
        keywords = data.target_keywords
        recommendations = []
        score = 100

        try:
            # 1. Live HTML fetch karein
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                
            if response.status_code != 200:
                return SEOAuditResponse(
                    url=url,
                    score=0,
                    meta_title="N/A",
                    meta_description="N/A",
                    recommendations=[f"Target URL tak rasai mein nakami. Status code: {response.status_code}"]
                )

            # 2. BeautifulSoup Parse
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract Title Tag
            title_tag = soup.find('title')
            meta_title = title_tag.string.strip() if title_tag and title_tag.string else ""
            if not meta_title:
                recommendations.append("Critical: Meta title tag gayab hai.")
                score -= 25
            elif len(meta_title) < 30 or len(meta_title) > 60:
                recommendations.append(f"Meta title length ({len(meta_title)} chars) optimal nahi hai (30-60 chars hona chahiye).")
                score -= 10

            # Extract Meta Description Tag
            desc_tag = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'description'})
            meta_description = desc_tag.get('content', '').strip() if desc_tag else ""
            if not meta_description:
                recommendations.append("Critical: Meta description tag missing hai.")
                score -= 25
            elif len(meta_description) < 120 or len(meta_description) > 160:
                recommendations.append(f"Meta description length ({len(meta_description)} chars) optimal nahi hai (120-160 chars hona chahiye).")
                score -= 10

            # Headings & Images Check
            h1_tags = soup.find_all('h1')
            if len(h1_tags) == 0:
                recommendations.append("Page par H1 tag nahi mila.")
                score -= 15

            images = soup.find_all('img')
            missing_alt = [img for img in images if not img.get('alt')]
            if missing_alt:
                recommendations.append(f"{len(missing_alt)} images mein alt attribute missing hai.")
                score -= min(15, len(missing_alt) * 3)

            # 3. Gemini AI SEO Suggestions Generate Karein
            ai_title, ai_desc = SEOService._generate_ai_suggestions(meta_title, meta_description, keywords)

            return SEOAuditResponse(
                url=url,
                score=max(0, score),
                meta_title=meta_title or "N/A",
                meta_description=meta_description or "N/A",
                ai_suggested_title=ai_title,
                ai_suggested_description=ai_desc,
                recommendations=recommendations or ["Page structure optimized hai."]
            )

        except Exception as e:
            return SEOAuditResponse(
                url=url,
                score=0,
                meta_title="N/A",
                meta_description="N/A",
                recommendations=[f"Processing Error: {str(e)}"]
            )