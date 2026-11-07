"""Run three scenarios side by side:

1. A normal task that finishes on its own.
2. A worker that never finishes, bounded by the step budget -> clean exit.
3. The same worker with no effective budget -> GraphRecursionError.
"""

from langgraph.errors import GraphRecursionError

from graph import build_graph, init_state
from workers import stubborn_code_worker

LIMIT = {"recursion_limit": 25}


def run(title, app, state):
    print(f"\n== {title}")
    supersteps = 0
    final = dict(state)
    try:
        for update in app.stream(state, LIMIT, stream_mode="updates"):
            supersteps += 1
            for node, delta in update.items():
                final.update({k: v for k, v in delta.items() if k != "messages"})
                final["messages"] = final["messages"] + delta.get("messages", [])
                print(f"  step {supersteps:>2}  {node:<10} {delta.get('messages', [delta.get('next_worker')])}")
        print(f"  -> clean exit after {supersteps} supersteps, {len(final['messages'])} messages kept")
    except GraphRecursionError:
        print(f"  -> GraphRecursionError after {supersteps} supersteps. The run is lost.")


if __name__ == "__main__":
    run("normal task, max_steps=6", build_graph(), init_state("add retries", 6))
    run("stubborn worker, max_steps=6", build_graph(stubborn_code_worker), init_state("add retries", 6))
    run("stubborn worker, no budget", build_graph(stubborn_code_worker), init_state("add retries", 10_000))
