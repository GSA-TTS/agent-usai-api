# Agent USAI API

A demonstration repository showing how to build agents on the USAI (US AI) API using the LangChain framework. Examples are organized into two progressive modules and are written to be shown live, copying and pasting individual lines of code.

## Overview

The repository is organized into two modules:

1. **`01_langchain_agent`** - Core LangChain agent patterns: basic agents, streaming, conversation memory, tools, and observability with Phoenix.
2. **`02_deep_agent`** - The [`deepagents`](https://github.com/langchain-ai/deepagents) framework: filesystem-backed agents with thread memory, long-term file memory, and skills.

All examples use the USAI API through OpenAI-compatible endpoints, making it easy to leverage models like Claude Sonnet with LangChain's agent framework.

## Prerequisites

- Python 3.14+
- USAI API access and credentials
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Environment Setup

Create a `.env` file in the root directory with your USAI credentials:

```bash
USAI_API_KEY=your-usai-api-key-here
USAI_BASE_URL=https://api.prod.gsai.mcaas.fcs.gsa.gov
```

The examples automatically append `/api/v1` to the base URL.

## Module 1: LangChain Agents (`src/01_langchain_agent`)

Core agent patterns built directly on `langchain.agents.create_agent`.

| File | Demonstrates |
| --- | --- |
| `00_agent.py` | A basic agent with no tools. Query: "What are the divisions of GSA?" |
| `01_agent_stream.py` | Streaming the response token by token with `agent.stream(..., stream_mode="messages")`. |
| `02_agent_memory.py` | Conversation memory across turns using an `InMemorySaver` checkpointer and a `thread_id`. |
| `03_agent_tool.py` | Custom tools via the `@tool` decorator (a `compute_square_root` tool). |
| `04_agent_phoenix.py` | Observability with Phoenix/OpenTelemetry tracing. Start the server first, then run the agent. |

Run any example, for example:

```bash
uv run python src/01_langchain_agent/00_agent.py
```

For the Phoenix example, start the server in a separate terminal first:

```bash
python -m phoenix.server.main serve   # UI at http://localhost:6006
uv run python src/01_langchain_agent/04_agent_phoenix.py
```

## Module 2: Deep Agents (`src/02_deep_agent`)

The `deepagents` framework adds a virtual filesystem, planning, subagents, and pluggable storage backends on top of a LangChain agent. Each example uses the shared `get_model()` helper in `models.py`.

| File | Demonstrates |
| --- | --- |
| `01_basic_deep_agent.py` | Creating a deep agent with `create_deep_agent` and invoking it. |
| `02_agent_no_memory.py` | The default (stateless) case: without memory the agent forgets facts between invocations. |
| `03_agent_thread_memory.py` | Short-term memory scoped to a conversation with a `MemorySaver` checkpointer and `thread_id`. Same thread remembers; a different thread does not. |
| `04_agent_file_memory.py` | Long-term memory persisted as files. A `CompositeBackend` routes `/memories/` to a `StoreBackend`; the agent writes a learned fact to `AGENTS.md` in one conversation and reads it back in another. |
| `05_skill_agent.py` | Skills (procedural memory). Compares an agent with and without a `report-format` skill; both are asked for a report, but only the skilled agent follows the five-bullet executive summary format. |
| `06_agent_dynamic_prompt.py` | Dynamic system prompts. A `@dynamic_prompt` middleware builds the system prompt from a user profile in the runtime context; the same question yields a plain-language answer for a novice and a technical answer for an expert. |

### File memory (`04_agent_file_memory.py`)

Memory is stored as files in a `StoreBackend` under a fixed namespace. The agent
reads `AGENTS.md` at startup and can update it with its `edit_file` tool. The
example seeds an empty memory file, tells the agent a fact ("I work for the
General Services Administration"), and verifies the fact is persisted to the
memory file and recalled in a later conversation.

### Skills (`05_skill_agent.py`)

Skills are reusable instructions that tell the agent *how* to perform a task.
They live in a directory containing a `SKILL.md` file with YAML frontmatter:

```
src/02_deep_agent/skills/report-format/SKILL.md
```

A `FilesystemBackend` reads the skill from disk and writes the generated reports
to `src/02_deep_agent/reports/`. Running the example produces two files so you
can compare the output side by side:

- `reports/report_no_skill.md` - a long, unstructured document
- `reports/report_with_skill.md` - a five-bullet executive summary matching the skill

```bash
uv run python src/02_deep_agent/05_skill_agent.py
```

### Dynamic system prompts (`06_agent_dynamic_prompt.py`)

A `Context` dataclass carries a user profile (`expertise`) into each invocation
via `context_schema`. A `@dynamic_prompt` middleware reads that profile and
builds the system prompt on the fly. The example asks the same question ("What
is a vector embedding?") twice — once as a `novice` and once as an `expert` — so
the only variable is the injected profile:

- Novice profile → a plain-language explanation with no jargon
- Expert profile → a technically precise answer assuming deep background

```bash
uv run python src/02_deep_agent/06_agent_dynamic_prompt.py
```

## Available USAI Models

The USAi API provides access to multiple state-of-the-art models. Change the `model` parameter in `ChatOpenAI` (or the `model_name` argument to `get_model()` in the deep agent module) to switch models.

### Anthropic (Claude) Models
- `claude_4_8_opus`
- `claude_4_7_opus`
- `claude_4_5_opus`
- `claude_4_6_sonnet`
- `claude_4_5_sonnet`
- `claude_4_5_haiku`

### Google (Gemini) Models
- `gemini-2.5-pro`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `text-embedding-005` (embeddings)

### OpenAI (GPT) Models
- `gpt-5.5-latest-guardrails-defaultv2`
- `gpt-5.4-latest-guardrails-defaultv2`
- `gpt-5.2-latest-guardrails-defaultv2`

### Other Models
- `llama_4_maverick` (Meta)
- `cohere_english_v3` (Cohere, embeddings)

## Project Structure

```
agent-usai-api/
├── src/
│   ├── 01_langchain_agent/
│   │   ├── 00_agent.py            # Basic agent
│   │   ├── 01_agent_stream.py     # Token streaming
│   │   ├── 02_agent_memory.py     # Conversation memory (checkpointer)
│   │   ├── 03_agent_tool.py       # Custom tool
│   │   └── 04_agent_phoenix.py    # Observability with Phoenix
│   └── 02_deep_agent/
│       ├── models.py              # Shared get_model() helper
│       ├── 01_basic_deep_agent.py # Basic deep agent
│       ├── 02_agent_no_memory.py  # Stateless (no memory)
│       ├── 03_agent_thread_memory.py  # Short-term thread memory
│       ├── 04_agent_file_memory.py    # Long-term file memory
│       ├── 05_skill_agent.py          # Skills demo
│       ├── 06_agent_dynamic_prompt.py # Dynamic system prompt from user profile
│       ├── memories/              # Seed memory files
│       ├── skills/                # Skill definitions (SKILL.md)
│       └── reports/               # Output from the skills demo
├── pyproject.toml                 # Python dependencies
└── README.md                      # This file
```

## Dependencies

Key dependencies managed in `pyproject.toml`:

- **langchain** - Core agent framework
- **langchain-openai** - OpenAI-compatible LLM integration
- **deepagents** (≥0.6.12) - Deep agent framework (filesystem, memory, skills)
- **arize-phoenix** - Observability and tracing
- **openinference-instrumentation-langchain** - LangChain instrumentation
- **python-dotenv** - Environment variable management

## Security Considerations

When working with USAI credentials:

- Never commit `.env` files or hardcode API keys

## Troubleshooting

### Common Issues

**"No module named 'phoenix'"**
- Solution: Install dependencies with `uv sync` or `pip install -e .`

**"API key not found"**
- Solution: Ensure `.env` file exists and contains `USAI_API_KEY`

**Phoenix UI not accessible**
- Solution: Start Phoenix server with `python -m phoenix.server.main serve`
- Default endpoint: http://localhost:6006

**Skills demo reports not written**
- Solution: The `FilesystemBackend` does not create directories. Ensure `src/02_deep_agent/reports/` exists before running `05_skill_agent.py`.

**Network policy blocking USAI**
- Solution: Configure "Balanced" network policy and allowlist USAI endpoint
- See [docs/SBX_PATTERNS.md](docs/SBX_PATTERNS.md) for details

## License

MIT License - Copyright (c) 2026 Technology Transformation Services

See [LICENSE](LICENSE) for full details.

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Deep Agents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [Phoenix Documentation](https://docs.arize.com/phoenix)
- [USAI API Documentation](https://api.prod.gsai.mcaas.fcs.gsa.gov/docs)
- [OpenCode Documentation](https://opencode.ai/docs)

## Support

For issues related to:
- **This repository**: Open an issue on [GitHub](https://github.com/GSA-TTS/agent-usai-api)
- **USAI API**: Contact your GSA USAI administrator
- **OpenCode**: See [OpenCode support](https://opencode.ai/docs)
