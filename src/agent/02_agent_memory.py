import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from langgraph.checkpoint.memory import InMemorySaver  

from pprint import pprint

load_dotenv()

api_key = os.getenv("USAI_API_KEY")
base_url = os.getenv("USAI_BASE_URL")

def initialize_agent():

    # Initialize the model
    model = ChatOpenAI(
        model="claude_4_5_sonnet",
        base_url=base_url + "/api/v1",
        api_key=api_key,
        temperature=0,
    )

    # Instantiate the agent 
    agent = create_agent(
        model=model,
        checkpointer=InMemorySaver()
    )

    config = {"configurable": {"thread_id": "1"}}

    return agent, config 

def chat_agent(agent, config, query):

    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config,  
    )

    pprint(response)

    return config


if __name__ == "__main__":
    agent,config = initialize_agent()

    print("Chat 1: Setting favorite division of GSA...")
    chat_agent(agent, config, "My favorite division of GSA is FAS.")

    print("\nChat 2: Asking agent to recall favorite division...")
    chat_agent(agent, config, "What is my favorite division of GSA?")


