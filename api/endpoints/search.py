from typing import Optional, Dict, List
from fastapi import APIRouter, Query
from schemas.search import SearchResponse
from services.search_api import SourceExtractorService
from core.config import BRAVE_SEARCH_API_KEY

router = APIRouter()
source_extractor = SourceExtractorService()

@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    country: str = Query("in", description="Country code"),
    count: int = Query(5, description="Number of results to return")
) -> Dict[str, List]:
    """Search endpoint that returns web and video results from Brave search"""
    try:
        # Get search results from Brave
        search_results = await source_extractor.search(q, country, count)
        
        # Extract web results
        web_results = []
        if "web" in search_results:
            for result in search_results.get("web", {}).get("results", []):
                # Validate result has required fields
                if result.get("url") and result.get("title"):
                    web_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "profile": result.get("profile", {}),
                        "type": result.get("type", ""),
                        "subtype": result.get("subtype", ""),
                        "language": result.get("language", ""),
                        "thumbnail": result.get("thumbnail", {}),
                        "meta_url": result.get("meta_url", {})
                    })

        # Extract video results
        video_results = []
        if "videos" in search_results:
            for result in search_results.get("videos", {}).get("results", []):
                if result.get("url") and result.get("title"):
                    video_results.append({
                        "type": "video_result",
                        "url": result.get("url", ""),
                        "title": result.get("title", ""),
                        "description": result.get("description", ""),
                        "age": result.get("age", ""),
                        "page_age": result.get("page_age", ""),
                        "thumbnail": result.get("thumbnail", {}),
                        "meta_url": result.get("meta_url", {})
                    })

        # Return formatted results
        return {
            "web": web_results,
            "videos": video_results
        }

    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        return {
            "web": [],
            "videos": []
        }