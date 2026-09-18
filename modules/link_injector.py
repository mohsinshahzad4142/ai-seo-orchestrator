from bs4 import BeautifulSoup
import re
from typing import Dict, List, Tuple

class AutoInternalLinkInjector:
    def __init__(self, keyword_link_map: Dict[str, str]):
        self.map = keyword_link_map

    def inject_links(self, html_content: str, max_injections_per_keyword: int = 1) -> Tuple[str, List[str]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        injected_keywords = []

        for kw, url in self.map.items():
            count = 0
            pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
            
            for text_node in list(soup.find_all(text=True)):
                if count >= max_injections_per_keyword:
                    break
                parent = text_node.parent
                if parent.name in ['a', 'script', 'style', 'title', 'meta', 'head']:
                    continue
                
                original_text = text_node.string
                if original_text and pattern.search(original_text):
                    new_text, subs = pattern.subn(f'<a href="{url}">\\1</a>', original_text, count=1)
                    if subs > 0:
                        new_soup = BeautifulSoup(new_text, 'html.parser')
                        text_node.replace_with(new_soup)
                        count += subs
                        if kw not in injected_keywords:
                            injected_keywords.append(kw)

        return str(soup), injected_keywords