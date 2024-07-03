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
# Load environment variables from .env file
load_dotenv()
# Add the parent directory of 'agents' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_travily

def lookup(name:str)->str:
    llm = Ollama(model="llama3")
    
    template = """Given the full name {name_of_person}, I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only the URL, without any additional text or explanations.
    """
    prompt_template=PromptTemplate(
        template=template, input_variables=["names_of_person"]
    )
    tools_for_agent=[
        Tool(
            name="Crawl Google 4 Linkedin profile",
            func=get_profile_url_travily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]
    react_prompt=hub.pull("hwchase17/react")
    agent=create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor=AgentExecutor(agent=agent, tools=tools_for_agent,verbose=True,handle_parsing_errors=True)#orchestrates all the react agent
    #invokes the fn
    result = agent_executor.invoke(
    input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    print("Raw LLM output:", result)  # Add this line
    linkedin_profile_url = result["output"]
    return linkedin_profile_url
    
if __name__=="__main__":
    linkedin_url=lookup(name="Siddharth Prakash PES University ")
    print(linkedin_url)