# Agent USAI API

A demonstration repository showing how to build LangChain agents using the USAI (US AI) API. This repository provides progressive examples from basic agents to advanced implementations with observability.

## Overview

This repository demonstrates three levels of LangChain agent implementation:

1. **Basic Agent** - Simple agent with no tools
2. **Agent with Tools** - Agent with custom tool integration
3. **Agent with Observability** - Full-featured agent with Phoenix tracing

All examples use the USAI API through OpenAI-compatible endpoints, making it easy to leverage models like Claude 4.5 Sonnet with LangChain's agent framework.

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

The application automatically appends `/api/v1` to the base URL.

## Examples

### Example 1: Basic Agent (00_agent.py)

A simple agent that responds to queries without any custom tools.

```bash
python src/agent/00_agent.py
```

**What it demonstrates:**
- Basic LangChain agent setup
- USAI API integration with OpenAI-compatible client
- Async execution with asyncio
- Example query: "What are the divisions of GSA?"

**Key code snippet:**
```python
llm = ChatOpenAI(
    model="usai/claude_4_5_sonnet",
    api_key=os.getenv("USAI_API_KEY"),
    base_url=f"{os.getenv('USAI_BASE_URL')}/api/v1"
)
```

### Example 2: Agent with Tools (01_agent_tool.py)

Extends the basic agent with a custom tool for computing square roots.

```bash
python src/agent/01_agent_tool.py
```

**What it demonstrates:**
- Creating custom tools with `@tool` decorator
- Passing tools to agents
- Function calling capabilities
- Example query: "What is the square root of 16?"

**Key code snippet:**
```python
@tool
def compute_square_root(number: float) -> float:
    """Compute the square root of a number"""
    return number ** 0.5

agent = create_agent(llm, [compute_square_root])
```

### Example 3: Agent with Observability (02_agent_phoenix.py)

Full-featured agent with Phoenix tracing for debugging and monitoring.

```bash
# First, start Phoenix server (in a separate terminal)
python -m phoenix.server.main serve

# Then run the agent
python src/agent/02_agent_phoenix.py
```

**What it demonstrates:**
- Phoenix OpenTelemetry integration
- Real-time trace viewing
- LangChain instrumentation
- Project-based trace organization
- Example query: "What is the square root of 625?"

**Phoenix UI:** http://localhost:6006

**Key code snippet:**
```python
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register(
    project_name="usai-agent-example",
    endpoint="http://localhost:4317"
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
```

## Available USAI Models

The USAI API provides access to multiple state-of-the-art models:

### Claude Models
- `usai/claude_4_5_sonnet` (default)
- `usai/claude_4_5_opus`
- `usai/claude_3_5_haiku`

### Gemini Models
- `usai/gemini_2_5_flash`
- `usai/gemini_2_5_pro`

### OpenAI Models
- `usai/gpt_4o`
- `usai/gpt_4o_mini`

To use a different model, simply change the `model` parameter in the `ChatOpenAI` constructor.

## OpenCode Integration

This repository includes configuration for use with [OpenCode](https://opencode.ai/) in Docker Sandboxes. See `opencode.jsonc` for the full configuration.

### Quick Start with Docker Sandboxes

```bash
sbx exec -it -e USAI_API_KEY="$USAI_API_KEY" -w $(pwd) SANDBOX opencode
```

For detailed security patterns and credential injection methods, see [docs/SBX_PATTERNS.md](docs/SBX_PATTERNS.md).

## Project Structure

```
agent-usai-api/
├── src/agent/
│   ├── 00_agent.py           # Basic agent example
│   ├── 01_agent_tool.py      # Agent with custom tool
│   └── 02_agent_phoenix.py   # Agent with observability
├── docs/
│   └── SBX_PATTERNS.md       # Docker Sandboxes security guide
├── opencode.jsonc            # OpenCode configuration
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## Dependencies

Key dependencies managed in `pyproject.toml`:

- **langchain** (≥1.3.2) - Core agent framework
- **langchain-openai** (≥1.2.2) - OpenAI-compatible LLM integration
- **arize-phoenix** (≥16.2.0) - Observability and tracing
- **openinference-instrumentation-langchain** (≥0.1.66) - LangChain instrumentation
- **python-dotenv** (≥1.2.2) - Environment variable management
- **tavily** (≥1.1.0) - Search API integration

## Architecture

All examples follow a consistent pattern:

1. **Environment Loading** - Load USAI credentials from `.env`
2. **LLM Configuration** - Create OpenAI-compatible client pointing to USAI
3. **Tool Definition** - Define custom tools (if applicable)
4. **Agent Creation** - Use `create_agent()` factory function
5. **Async Execution** - Run queries with `asyncio.run()`
6. **Output** - Pretty-print agent response dictionaries

## Security Considerations

When working with USAI credentials:

- Never commit `.env` files or hardcode API keys
- Use environment-based credential injection for Docker Sandboxes
- Scope tokens appropriately for your use case
- Review agent outputs before committing code
- See [docs/SBX_PATTERNS.md](docs/SBX_PATTERNS.md) for detailed security patterns

## Troubleshooting

### Common Issues

**"No module named 'phoenix'"**
- Solution: Install dependencies with `uv sync` or `pip install -e .`

**"API key not found"**
- Solution: Ensure `.env` file exists and contains `USAI_API_KEY`

**Phoenix UI not accessible**
- Solution: Start Phoenix server with `python -m phoenix.server.main serve`
- Default endpoint: http://localhost:6006

**Network policy blocking USAI**
- Solution: Configure "Balanced" network policy and allowlist USAI endpoint
- See [docs/SBX_PATTERNS.md](docs/SBX_PATTERNS.md) for details

## Contributing

Contributions are welcome! To add new examples:

1. Create a new file in `src/agent/` following the naming pattern
2. Include clear comments and docstrings
3. Add an example query that demonstrates the functionality
4. Update this README with the new example

## License

MIT License - Copyright (c) 2026 Technology Transformation Services

See [LICENSE](LICENSE) for full details.

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Phoenix Documentation](https://docs.arize.com/phoenix)
- [USAI API Documentation](https://api.prod.gsai.mcaas.fcs.gsa.gov/docs)
- [OpenCode Documentation](https://opencode.ai/docs)

## Support

For issues related to:
- **This repository**: Open an issue on [GitHub](https://github.com/GSA-TTS/agent-usai-api)
- **USAI API**: Contact your GSA USAI administrator
- **OpenCode**: See [OpenCode support](https://opencode.ai/docs)
