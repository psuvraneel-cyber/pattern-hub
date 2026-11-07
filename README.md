# pattern-hub

Small, runnable AI-agent architecture patterns. Each one runs without an API key and ships with tests that check its claims.

| Pattern | What it shows |
|---|---|
| [langgraph-supervisor](patterns/langgraph-supervisor) | A supervisor that stops on a step budget instead of crashing at `recursion_limit` |

## Quickstart

```bash
git clone https://github.com/psuvraneel-cyber/pattern-hub
cd pattern-hub/patterns/langgraph-supervisor
uv run main.py
```

MIT licensed.
