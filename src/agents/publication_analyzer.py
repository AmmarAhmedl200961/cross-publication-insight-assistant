# This file will contain the PublicationAnalyzer agent.

from ..tools.web_scraper import scrape_url
from ..tools.keyword_extractor import extract_keywords
from typing import Optional


class PublicationAnalyzer:
    def __init__(self, url: str, selector: Optional[str] = None):
        self.url = url
        self.selector = selector

    def analyze(self) -> list[str]:
        """
        Analyzes a publication by scraping its content and extracting keywords.

        Returns:
            A list of keywords extracted from the publication.
        """
        print(f"Analyzing publication: {self.url}")
        text = scrape_url(self.url, self.selector)
        if text.startswith("Error"):
            print(text)
            return []
        return extract_keywords(text)
