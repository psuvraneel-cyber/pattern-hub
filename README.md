# pattern-hub

Small, runnable AI-agent architecture patterns. Each one runs without an API key and ships with tests that check its claims.

## Start here: your agent can loop 10,007 times

In LangGraph 1.2, a looping agent with default settings takes **10,007 steps** before `recursion_limit` stops it. Then it raises `GraphRecursionError` and everything it did is lost. The [langgraph-supervisor](patterns/langgraph-supervisor) pattern gives the supervisor a step budget, so it stops on purpose and keeps the work.

Running it prints three cases. The last line of each:

```
== normal task, max_steps=6
  -> clean exit after 9 supersteps, 5 messages kept
== stubborn worker, max_steps=6
  -> clean exit after 13 supersteps, 7 messages kept
== stubborn worker, no budget
  -> GraphRecursionError after 25 supersteps. The run is lost.
```

## Quickstart

You need [uv](https://docs.astral.sh/uv/), a fast Python installer. If you don't have it:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then:

```bash
git clone https://github.com/psuvraneel-cyber/pattern-hub
cd pattern-hub/patterns/langgraph-supervisor
uv run main.py
```

uv downloads Python and LangGraph on the first run. No API key needed.

## Patterns

| Pattern | What it shows |
|---|---|
| [langgraph-supervisor](patterns/langgraph-supervisor) | A supervisor that stops on a step budget instead of crashing at `recursion_limit` |

MIT licensed.
