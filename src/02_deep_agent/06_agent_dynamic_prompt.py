from dataclasses import dataclass

from deepagents import create_deep_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

from models import get_model


# the runtime context carries a user profile into each invocation
@dataclass
class Context:
    expertise: str


# build the system prompt dynamically based on the user's expertise level
@dynamic_prompt
def profile_prompt(request: ModelRequest) -> str:
    expertise = request.runtime.context.expertise

    base = "You are a helpful assistant that answers questions about technical topics."

    if expertise == "novice":
        base += " The user is a novice. Explain using plain, everyday language and avoid jargon."
    elif expertise == "expert":
        base += " The user is a technical expert. Use precise terminology and assume deep background knowledge."

    return base


# attach the middleware and declare the context schema
agent = create_deep_agent(
    model=get_model(),
    middleware=[profile_prompt],
    context_schema=Context,
)


question = "What is a vector embedding?"


# same question, novice profile: expect a plain-language answer
novice = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    context=Context(expertise="novice"),
)

print("=== NOVICE ===")
print(novice["messages"][-1].content)


# same question, expert profile: expect a technical answer
expert = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    context=Context(expertise="expert"),
)

print("\n=== EXPERT ===")
print(expert["messages"][-1].content)
