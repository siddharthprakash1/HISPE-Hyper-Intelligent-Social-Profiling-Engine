import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets
from dotenv import load_dotenv

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)
    
    summary_template = """
    `Given the information about a person from LinkedIn {information} and Twitter posts {twitter_posts}, I want you to create:
    1) A short professional summary (about 2-3 sentences)
    2) Two interesting facts about them

    Instructions:
    - Use information from both LinkedIn and Twitter if available.
    - If Twitter information is not available (i.e., {twitter_posts} is empty or states "No Twitter profile found"), base your response solely on the LinkedIn data.
    - Focus on key professional achievements, skills, and unique aspects of their career or background.
    - If using Twitter data, incorporate any relevant insights from their tweets that add depth to their professional profile.
    - Ensure the interesting facts are notable and relevant to their professional life or industry.

    Please provide your response in a clear, concise manner.`
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template
    )

    llm = Ollama(model="llama3")

    chain = (
        {"information": lambda x: x["information"], "twitter_posts": lambda x: x["twitter_posts"]}
        | summary_prompt_template 
        | llm 
        | StrOutputParser()
    )

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
    return res

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    result = ice_break_with(name="eden marco udemy ")
    print(result)