import sys
import os
import re
from dotenv import load_dotenv

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file
env_path = os.path.join(os.path.dirname(current_dir), '.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Debug print
print(f"TAVILY_API_KEY loaded: {'Yes' if os.getenv('TAVILY_API_KEY') else 'No'}")
# Load environment variables from .env file
load_dotenv()
# Add the parent directory of 'agents' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.llms import Ollama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_travily
import re
from tools.tools import get_profile_url_travily

def clean_linkedin_url(url):
    # Extract just the base profile URL
    matches = re.findall(r'(https?://(?:www\.|in\.)?linkedin\.com/in/[^/\s]+)', url)
    if matches:
        return matches[0]  # Return the first match
    return None

def lookup(name: str) -> str:
    llm = Ollama(model="llama3")
    
    template = """Given the full name {name_of_person}, I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only the URL of the LinkedIn profile page, without any additional text or explanations.
    Do not include any post URLs or activity URLs, only the base profile URL.
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkedin profile",
            func=get_profile_url_travily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)
    
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    print("Raw LLM output:", result)
    
    # Extract all potential LinkedIn URLs from the entire result
    full_result_string = str(result)
    all_urls = re.findall(r'(https?://(?:www\.|in\.)?linkedin\.com/(?:in/[^/\s]+|(?:posts|company)/[^\s]+))', full_result_string)
    
    # Filter and clean the URLs
    cleaned_urls = [clean_linkedin_url(url) for url in all_urls if clean_linkedin_url(url)]
    
    # Remove duplicates while preserving order
    unique_urls = list(dict.fromkeys(cleaned_urls))
    
    if unique_urls:
        return unique_urls[0]  # Return the first unique, cleaned URL
    else:
        return "No valid LinkedIn profile URL found"

if __name__ == "__main__":
    linkedin_url = lookup(name="Siddharth Prakash PES University")
    print(linkedin_url)