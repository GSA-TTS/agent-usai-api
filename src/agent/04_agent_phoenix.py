import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

from langchain.tools import tool

# Phoenix imports for standalone server
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

load_dotenv()

api_key = os.getenv("USAI_API_KEY")
base_url = os.getenv("USAI_BASE_URL")

@tool
def compute_square_root(query: int) -> int:
    """Compute the square root of a number"""

    return {"result": float(query) ** 0.5}

def main():
    # Connect to standalone Phoenix server
    print("🔥 Connecting to Phoenix server...")
    tracer_provider = register(
        project_name="usai-agent-example",  # Name your project
        endpoint="http://localhost:4317",   # Phoenix OpenTelemetry endpoint
    )
    
    # Instrument LangChain to send traces to Phoenix
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    print("✅ LangChain instrumentation enabled")
    print("📊 Phoenix UI: http://localhost:6006\n")

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
        tools=[compute_square_root],
    )

    print("Invoking agent...")
    response = agent.invoke(
        {"messages": [HumanMessage(content="What is the square root of 625?")]},
    )

    pprint(response)
    
    print(f"\n🔍 View your traces at: http://localhost:6006")


if __name__ == "__main__":
    main()