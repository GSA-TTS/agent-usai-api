import os 

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

def get_model(model_name: str = "claude_4_6_sonnet") -> ChatOpenAI:
    """
    Returns a ChatOpenAI model instance with the specified model name.
    """
    return ChatOpenAI(
        model=model_name,
        base_url=os.environ["USAI_BASE_URL"] + "/api/v1",
        api_key=os.environ["USAI_API_KEY"],
    )
