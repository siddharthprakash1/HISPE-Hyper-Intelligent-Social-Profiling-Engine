import os
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello Langchain!")
    summary_template = """
        given the linkedin information {information} about a person from I want you to create:
        1) a short summary
        2) two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    
    # Initialize Ollama with the Llama 2 model
    llm = Ollama(model="llama3")
    
    # Now we want to tie everything together
    chain = LLMChain(prompt=summary_prompt_template, llm=llm)
    
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/siddharth-prakash-771596241/")
    res = chain.invoke(input={"information": linkedin_data})
    print(res)