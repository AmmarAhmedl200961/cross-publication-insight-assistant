# This file will contain the web scraping tool.
import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_url(url: str, selector: Optional[str] = None) -> str:
    """
    Scrapes the text content from a given URL.
    If a selector is provided, it scrapes text only from that element.

    Args:
        url: The URL to scrape.
        selector: The CSS selector to target a specific element.

    Returns:
        The text content of the URL or targeted element.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        if selector:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator=" ", strip=True)
            else:
                return f"Element with selector '{selector}' not found."
        else:
            return soup.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException as e:
        return f"Error scraping URL: {e}"
