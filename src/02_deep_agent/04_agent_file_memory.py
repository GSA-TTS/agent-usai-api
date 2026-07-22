from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from deepagents.backends.utils import create_file_data
from langgraph.store.memory import InMemoryStore

from models import get_model


# the store is where long term memory files are persisted across conversations
store = InMemoryStore()

# seed an empty memory file so the agent has something to read and update
# note: the store key has the "/memories/" route prefix stripped off
store.put(
    ("my-agent",),
    "/AGENTS.md",
    create_file_data("## About the user\n(nothing yet)\n"),
)


# create a deep agent that reads and writes memory to /memories/AGENTS.md
agent = create_deep_agent(
    model=get_model(),
    memory=["/memories/AGENTS.md"],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda rt: ("my-agent",)),
        },
    ),
    store=store,
)


# first conversation: tell the agent a fact and ask it to save it to memory
agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Remember that I work for the General Services Administration. Save this to your memory file.",
            }
        ]
    },
)

# see what the agent wrote to its memory file
print("Memory file contents:")
print(store.get(("my-agent",), "/AGENTS.md").value["content"])


# second conversation: the agent reads memory and recalls the fact
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

print("\nAgent response:")
print(result["messages"][-1].content)
