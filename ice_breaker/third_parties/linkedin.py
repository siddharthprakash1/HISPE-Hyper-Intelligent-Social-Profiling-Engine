import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """
    Scrape information from LinkedIn profiles using Proxycurl API.
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=100,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {"Authorization": f'Bearer {os.getenv("PROXYCURL_API_KEY")}'}#we are attaching a dictionary which is holds our api token
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers= headers,
            timeout=100
        )
    
    data=response.json()
    #our data will have many empty strings and value so we should remove that because we can hit the token limit
    data={
        k: v
        for k,v in data.items()
            if v not in([],"","",None)
            and k not in ["people_also_viewed","certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data

if __name__ == "__main__":
    profile_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/siddharth-prakash-771596241/"
    )
    print(profile_data)
