"""
Web Search Tool
Tool for searching the web to research similar projects and best practices
"""

from crewai.tools import BaseTool
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Type
import logging
import time
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WebSearchInput(BaseModel):
    """Input schema for Web Search Tool."""
    search_query: str = Field(..., description="Search terms or keywords related to the project")


class WebSearchTool(BaseTool):
    """
    Custom tool for web searching to research similar projects,
    best practices, and gather competitive intelligence.
    """
    
    name: str = "Web Search Tool"
    description: str = """
    Searches the web for information about similar projects, best practices,
    and trends related to the given repository topic or technology stack.
    
    Useful for:
    - Finding similar projects for comparison
    - Researching best practices for documentation
    - Discovering popular keywords and tags
    - Understanding market trends in specific technologies
    
    Input should be search terms or keywords related to the project.
    """
    args_schema: Type[BaseModel] = WebSearchInput
    
    def _get_session(self) -> requests.Session:
        """Create a configured requests session."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return session
    
    def _run(self, search_query: str) -> str:
        """
        Execute web search for the given query.
        
        Args:
            search_query: Search terms or keywords
            
        Returns:
            Formatted search results with insights
        """
        try:
            # Perform multiple search strategies
            results = []
            
            # Search for GitHub repositories
            github_results = self._search_github_repos(search_query)
            if github_results:
                results.append(f"=== SIMILAR GITHUB REPOSITORIES ===\n{github_results}\n")
            
            # Search for documentation best practices
            docs_results = self._search_documentation_practices(search_query)
            if docs_results:
                results.append(f"=== DOCUMENTATION BEST PRACTICES ===\n{docs_results}\n")
            
            # Search for trending topics
            trends_results = self._search_trending_topics(search_query)
            if trends_results:
                results.append(f"=== TRENDING TOPICS AND KEYWORDS ===\n{trends_results}\n")
            
            return "\n".join(results) if results else "No relevant search results found."
            
        except Exception as e:
            logger.error(f"Error in web search: {str(e)}")
            return f"Error performing web search: {str(e)}"
    
    def _search_github_repos(self, query: str) -> str:
        """Search for similar GitHub repositories."""
        try:
            # Use GitHub's search API
            search_url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": 5
            }
            
            session = self._get_session()
            response = session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                repos = data.get("items", [])
                
                results = []
                for repo in repos[:5]:  # Top 5 repositories
                    repo_info = {
                        "name": repo.get("full_name"),
                        "description": repo.get("description", "No description"),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language", "Unknown"),
                        "topics": repo.get("topics", []),
                        "url": repo.get("html_url")
                    }
                    
                    results.append(
                        f"• {repo_info['name']} ({repo_info['stars']} ⭐)\n"
                        f"  Language: {repo_info['language']}\n"
                        f"  Description: {repo_info['description']}\n"
                        f"  Topics: {', '.join(repo_info['topics'][:5])}\n"
                        f"  URL: {repo_info['url']}\n"
                    )
                
                return "\n".join(results)
            
            return "Could not fetch GitHub repository data"
            
        except Exception as e:
            logger.error(f"Error searching GitHub repos: {str(e)}")
            return f"Error searching GitHub: {str(e)}"
    
    def _search_documentation_practices(self, query: str) -> str:
        """Search for documentation best practices."""
        try:
            # Search for README and documentation best practices
            search_terms = f"{query} README best practices documentation"
            results = self._general_web_search(search_terms, max_results=3)
            
            if results:
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        f"• {result.get('title', 'Unknown Title')}\n"
                        f"  {result.get('snippet', 'No description available')}\n"
                        f"  Source: {result.get('url', 'Unknown URL')}\n"
                    )
                return "\n".join(formatted_results)
            
            return "No documentation best practices found"
            
        except Exception as e:
            logger.error(f"Error searching documentation practices: {str(e)}")
            return f"Error searching documentation: {str(e)}"
    
    def _search_trending_topics(self, query: str) -> str:
        """Search for trending topics and keywords."""
        try:
            # Search for trending topics in the technology domain
            search_terms = f"{query} trending topics popular keywords"
            results = self._general_web_search(search_terms, max_results=3)
            
            if results:
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        f"• {result.get('title', 'Unknown Title')}\n"
                        f"  {result.get('snippet', 'No description available')}\n"
                    )
                return "\n".join(formatted_results)
            
            return "No trending topics found"
            
        except Exception as e:
            logger.error(f"Error searching trending topics: {str(e)}")
            return f"Error searching trends: {str(e)}"
    
    def _general_web_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform a general web search using DuckDuckGo (no API key required).
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, snippet, and URL
        """
        try:
            # Use DuckDuckGo Instant Answer API
            search_url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_redirect": "1",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            session = self._get_session()
            response = session.get(search_url, params=params, timeout=10)
            
            results = []
            if response.status_code == 200:
                data = response.json()
                
                # Get related topics
                related_topics = data.get("RelatedTopics", [])
                for topic in related_topics[:max_results]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", "")
                        })
                
                # Get abstract if available
                abstract = data.get("Abstract")
                if abstract:
                    results.insert(0, {
                        "title": data.get("Heading", "Summary"),
                        "snippet": abstract,
                        "url": data.get("AbstractURL", "")
                    })
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error in general web search: {str(e)}")
            return []
    
    def _scrape_page_content(self, url: str) -> str:
        """
        Scrape content from a web page.
        
        Args:
            url: URL to scrape
            
        Returns:
            Extracted text content
        """
        try:
            session = self._get_session()
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            return text[:2000] if len(text) > 2000 else text
            
        except Exception as e:
            logger.error(f"Error scraping page {url}: {str(e)}")
            return f"Error scraping page: {str(e)}"
