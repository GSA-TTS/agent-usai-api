from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from models import get_model


# use a filesystem backend so skills are read from disk and reports are
# written to real files in this directory
backend = FilesystemBackend(root_dir=Path(__file__).parent, virtual_mode=True)


# an agent WITHOUT the skill: it has no guidance on how to format a report
plain_agent = create_deep_agent(
    model=get_model(),
    backend=backend,
)

plain_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Write a short executive summary report on agent harness frameworks. Save it to /reports/report_no_skill.md",
            }
        ]
    },
)


# an agent WITH the skill: it loads the report-format skill on demand and
# follows the eight-section structure
skilled_agent = create_deep_agent(
    model=get_model(),
    backend=backend,
    skills=["/skills/"],
)

skilled_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Write a report on agent harness frameworks. Save it to /reports/report_with_skill.md",
            }
        ]
    },
)

print("Done. Compare /reports/report_no_skill.md and /reports/report_with_skill.md")
