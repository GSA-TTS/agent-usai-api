from deepagents import create_deep_agent
from models import get_model 

# initialize the deep agent with the default model 
agent = create_deep_agent(
    model=get_model(),
)

# invoke the agent with a user message
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What are the divisions of the General Services Administration?",
            }
        ]
    },
)

# print the agent's response
print(result["messages"][-1].content)