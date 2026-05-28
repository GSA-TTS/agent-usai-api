import asyncio
import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv()

api_key = os.getenv("USAI_API_KEY")
base_url = os.getenv("USAI_BASE_URL")

async def main():

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
    )

    # stream the reply token by token 
    for token, metadata in agent.stream(
        {"messages": [HumanMessage(content="What are the divisions of GSA?")]},
        stream_mode="messages"
    ):
        if token.content:  # Check if there's actual content
            print(token.content, end="", flush=True)  # Print token


if __name__ == "__main__":
    asyncio.run(main())
