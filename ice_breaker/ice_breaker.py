import os
from typing import Tuple
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets
from dotenv import load_dotenv
from output_parsers import summary_parser, Summary

def ice_break_with(name: str) ->Tuple[Summary,str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)
    
    summary_template = """
    Given the information about a person from LinkedIn {information} and Twitter posts {twitter_posts}, I want you to create:
    1) A short professional summary (about 2-3 sentences)
    2) Two interesting facts about them

    Instructions:
    - Use information from both LinkedIn and Twitter if available.
    - If Twitter information is not available (i.e., {twitter_posts} is empty or states "No Twitter profile found"), base your response solely on the LinkedIn data.
    - Focus on key professional achievements, skills, and unique aspects of their career or background.
    - If using Twitter data, incorporate any relevant insights from their tweets that add depth to their professional profile.
    - Ensure the interesting facts are notable and relevant to their professional life or industry.

    Please provide your response in the following format:
    {format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = Ollama(model="llama3")

    chain = (
        {"information": lambda x: x["information"], "twitter_posts": lambda x: x["twitter_posts"]}
        | summary_prompt_template 
        | llm 
        | StrOutputParser()
    )

    res:Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
    
    try:
        parsed_res = summary_parser.parse(res)
        return res,linkedin_data.get("profile_pic_url")
    
    except Exception as e:
        print(f"Error parsing result: {e}")
        return res  # Return the raw result if parsing fails

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    result = ice_break_with(name="eden marco udemy ")
    print(result)