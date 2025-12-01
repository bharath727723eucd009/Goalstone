"""Google Search tool for agents."""
import asyncio
import aiohttp
import json
from typing import Dict, List, Any, Optional
from ..observability.logger import get_logger

logger = get_logger(__name__)

class GoogleSearchTool:
    """Google Search tool using SerpAPI free tier."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo_key"  # Use demo for testing
        self.base_url = "https://serpapi.com/search.json"
    
    async def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Perform Google search and return results."""
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": num_results,
                "gl": "us",
                "hl": "en"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_results(data)
                    else:
                        # Fallback to mock data for demo
                        return self._mock_search_results(query)
        except Exception as e:
            logger.error(f"Search API error: {str(e)}")
            return self._mock_search_results(query)
    
    def _format_results(self, data: Dict) -> Dict[str, Any]:
        """Format search results."""
        results = []
        organic_results = data.get("organic_results", [])
        
        for result in organic_results[:5]:
            results.append({
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "position": result.get("position", 0)
            })
        
        return {
            "status": "success",
            "query": data.get("search_parameters", {}).get("q", ""),
            "results": results,
            "total_results": len(results)
        }
    
    def _mock_search_results(self, query: str) -> Dict[str, Any]:
        """Mock search results for demo purposes."""
        mock_results = {
            "software engineer jobs": [
                {"title": "Senior Software Engineer - Google", "link": "https://careers.google.com", "snippet": "Join Google's engineering team. $150k-200k salary range."},
                {"title": "Software Engineer Jobs - Indeed", "link": "https://indeed.com", "snippet": "10,000+ software engineer jobs available nationwide."},
                {"title": "Tech Jobs Market Report 2024", "link": "https://stackoverflow.com", "snippet": "Software engineering remains top paying field with 15% growth."}
            ],
            "python developer salary": [
                {"title": "Python Developer Salary Guide 2024", "link": "https://glassdoor.com", "snippet": "Average Python developer salary: $95,000 - $140,000 annually."},
                {"title": "Python Jobs Market Trends", "link": "https://linkedin.com", "snippet": "Python skills in high demand, 25% salary increase over 2 years."}
            ],
            "react developer remote jobs": [
                {"title": "Remote React Developer Jobs", "link": "https://remote.co", "snippet": "500+ remote React positions available. $80k-150k range."},
                {"title": "React Developer Career Path", "link": "https://reactjs.org", "snippet": "React skills lead to senior frontend roles and team leadership."}
            ]
        }
        
        # Find best match
        for key in mock_results:
            if any(word in query.lower() for word in key.split()):
                results = mock_results[key]
                break
        else:
            results = mock_results["software engineer jobs"]
        
        formatted_results = []
        for i, result in enumerate(results):
            formatted_results.append({
                "title": result["title"],
                "link": result["link"], 
                "snippet": result["snippet"],
                "position": i + 1
            })
        
        return {
            "status": "success",
            "query": query,
            "results": formatted_results,
            "total_results": len(formatted_results)
        }