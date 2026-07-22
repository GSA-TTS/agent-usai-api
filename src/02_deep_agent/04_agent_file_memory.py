from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from models import get_model 
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model=get_model(),
    memory=["/memories/AGENTS.md"],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (
                    rt.server_info.assistant_id,
                ),
            ),
            "/skills/": StoreBackend(
                namespace=lambda rt: (
                    rt.server_info.assistant_id,
                ),
            ),
        },
    ),
    store=InMemoryStore(),
)

agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Remember that I work for the General Services Administration",
            }
        ]
    },
)

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
print(result["messages"][-1].content)