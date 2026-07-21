import os 
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
  model="claude_4_6_sonnet",
  base_url=os.environ["USAI_BASE_URL"] + "/api/v1",
  api_key=os.environ["USAI_API_KEY"],
)
