from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from models import get_model 


# initialize the deep agent with the default model 
agent = create_deep_agent(
    model=get_model(),
    checkpointer=MemorySaver(),
)

config = {"configurable": {"thread_id": "my-thread"}}


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
    config=config 
)

print("Response using same thread id:")
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
    config=config
)

# print the agent's response
print(result["messages"][-1].content)

print("\n\nResponse using different thread id:")
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
    config={"configurable": {"thread_id": "my-other-thread"}}
)
print(result["messages"][-1].content)