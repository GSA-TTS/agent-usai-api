from deepagents import create_deep_agent
from models import get_model 


# initialize the deep agent with the default model 
agent = create_deep_agent(
    model=get_model(),
)

# tell the agent where I work 
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "I work at the General Services Administration",
            }
        ]
    },
)

# see if the agent remembers where I work 
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Where do I work?",
            }
        ]
    },
)

# print the agent's response
print(result["messages"][-1].content)