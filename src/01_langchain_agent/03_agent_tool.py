import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

from langchain.tools import tool

load_dotenv()

api_key = os.getenv("USAI_API_KEY")
base_url = os.getenv("USAI_BASE_URL")

@tool
def compute_square_root(query: int) -> int:
    """Compute the square root of a number"""

    return {"result": float(query) ** 0.5}

def main():
    
    print("Initializing model...")
    model = ChatOpenAI(
        model="claude_4_5_sonnet",
        base_url=base_url + "/api/v1",
        api_key=api_key,
        temperature=0,
    )

    print("Creating agent...")
    agent = create_agent(
        model=model,
        tools=[compute_square_root]
    )

    print("Invoking agent...")
    response = agent.invoke(
        {"messages": [HumanMessage(content="What is the square root of 625?")]},
    )

    pprint(response)


if __name__ == "__main__":
    main()

