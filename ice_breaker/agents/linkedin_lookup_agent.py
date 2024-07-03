import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)
from langchain import hub

def lookup(name:str)->str:
    llm=ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo"
    )
    template="""given the full name {name_of_person} I want you to get it me a link to their linkedin profile page.
        your answer should contain only links
    """
    prompt_template=PromptTemplate(
        template=template, input_variables=["names_of_person"]
    )
    tools_for_agent=[
        Tool(
            name="Crawl Google 4 Linkedin profile",
            func="?",
            description="useful for when you need get the Linkedin Page URL",
        )
    ]
    react_prompt=hub.pull("hwchase17/react")
    agent=create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor=AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)#orchestrates all the react agent
    #invokes the fn
    result=agent_executor.invoke(
        input={"input":prompt_template.format_prompt(name_of_person=name)}
    )
    
    linkedin_profile_url=result["output"]
    return linkedin_profile_url
    