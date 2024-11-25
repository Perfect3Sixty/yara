# services/search_api.py
from typing import List, Dict, Optional
import aiohttp
import trafilatura
import asyncio
from urllib.parse import quote_plus
from core.config import BRAVE_SEARCH_API_KEY

class SourceExtractorService:
    def __init__(self):
        self.brave_api_key = BRAVE_SEARCH_API_KEY
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_SEARCH_API_KEY
        }
        self.brave_search_url = "https://api.search.brave.com/res/v1/web/search"
        
    async def search(self, query: str, country: str = "in", count: int = 5) -> Dict:
        """Perform Brave search and return results"""
        params = {
            "q": quote_plus(query),
            "country": country,
            "summary": "true",
            "count": count
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.brave_search_url,
                headers=self.headers,
                params=params
            ) as response:
                return await response.json()

    async def extract_content(self, url: str) -> Optional[str]:
        """Extract main content from a URL using Trafilatura"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    return await asyncio.to_thread(
                        trafilatura.extract,
                        html,
                        include_links=False,
                        include_images=False,
                        include_tables=False
                    )
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None

    async def get_source_context(self, query: str) -> List[Dict]:
        """Get context from multiple sources for a query"""
        try:
            # Get search results
            search_results = await self.search(query)
            sources = []
            
            # Extract content from each result
            for result in search_results.get("web", {}).get("results", []):
                url = result.get("url")
                if not url:
                    continue
                    
                content = await self.extract_content(url)
                if content:
                    sources.append({
                        "url": url,
                        "title": result.get("title", ""),
                        "description": result.get("description", ""),
                        "content": content
                    })
            
            return sources
        except Exception as e:
            print(f"Error getting source context: {str(e)}")
            return []

    def format_context_for_prompt(self, sources: List[Dict]) -> str:
        """Format extracted sources into context for the prompt"""
        context_parts = []
        
        for idx, source in enumerate(sources, 1):
            context_parts.append(
                f"Source {idx}:\n"
                f"Title: {source['title']}\n"
                f"URL: {source['url']}\n"
                f"Content:\n{source['content']}\n"
            )
        
        return "\n".join(context_parts)