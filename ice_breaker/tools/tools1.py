import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from langchain.tools import Tool

# Load environment variables
load_dotenv()

def get_profile_url_tavily(name: str):
    """
    Searches for Twitter profile page.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    
    search = TavilySearchResults(api_key=api_key)
    res = search.run(f"{name} twitter profile")
    
    if res and len(res) > 0:
        for result in res:
            if 'twitter.com' in result['url']:
                return result['url'] + "\n"  # Add a newline character
    return "No Twitter profile found\n"  # Add a newline character here too

def extract_twitter_username(url: str):
    """
    Extracts the username from a Twitter profile URL.
    """
    return url.split('/')[-1]

# Define the tools
tools_for_agent = [
    Tool(
        name="Crawl Google for Twitter profile page",
        func=get_profile_url_tavily,
        description="Useful for when you need to get the Twitter Page URL",
    ),
    Tool(
        name="Extract Twitter username",
        func=extract_twitter_username,
        description="Extract the username from a Twitter profile URL",
    )
]

# Debug print to check if the API key is loaded
print(f"TAVILY_API_KEY loaded in tools.py: {'Yes' if os.getenv('TAVILY_API_KEY') else 'No'}")

# Function to get all tools
def get_tools():
    return tools_for_agent