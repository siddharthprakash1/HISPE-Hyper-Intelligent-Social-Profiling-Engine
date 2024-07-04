import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from dotenv import load_dotenv

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    Given the LinkedIn information {information} about a person, I want you to create:
    1) a short summary
    2) two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # Initialize Ollama with the Llama 2 model
    llm = Ollama(model="llama3")

    # Create a RunnableSequence instead of LLMChain
    chain = (
        {"information": RunnablePassthrough()} 
        | summary_prompt_template 
        | llm 
        | StrOutputParser()
    )

    res = chain.invoke(linkedin_data)
    return res

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    result = ice_break_with(name="Siddharth Prakash PES University")
    print(result)