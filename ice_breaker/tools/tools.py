import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_profile_url_travily(name: str):
    """
    Searches for LinkedIn or Twitter profile page.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    
    search = TavilySearchResults(api_key=api_key)
    res = search.run(f"{name} linkedin")
    
    if res and len(res) > 0:
        return res[0]["url"]
    else:
        return "No results found"

# Debug print to check if the API key is loaded
print(f"TAVILY_API_KEY loaded in tools.py: {'Yes' if os.getenv('TAVILY_API_KEY') else 'No'}")