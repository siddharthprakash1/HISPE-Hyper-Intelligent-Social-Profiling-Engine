import sys
import os
from dotenv import load_dotenv

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file
env_path = os.path.join(os.path.dirname(current_dir), '.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Debug print
print(f"TAVILY_API_KEY loaded: {'Yes' if os.getenv('TAVILY_API_KEY') else 'No'}")

# Add the parent directory of 'agents' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools1 import get_profile_url_tavily

def lookup(name: str) -> str:
    llm = Ollama(model="llama3")

    template = """
    Given the name {name_of_person}, I want you to find a link to their Twitter profile page, and extract from it their username.
    In your final answer, provide only the person's username.
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the Twitter Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_person=name)}
    )

    print(f"Raw result: {result}")  # Debug print
    twitter_username = result["output"].strip()
    print(f"Extracted username: {twitter_username}")  # Debug print
    return twitter_username

if __name__ == "__main__":
    print(lookup(name="Elon Musk"))