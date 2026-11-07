from langgraph.graph import END

from state import AgentState


def route(state: AgentState) -> str:
    """Pick the next worker. Replace with an LLM router in real use."""
    last = state["messages"][-1] if state["messages"] else ""
    if last.startswith("code: done"):
        return END
    if last.startswith("research:"):
        return "code"
    return "research"


def supervisor(state: AgentState) -> dict:
    step = state["step_count"] + 1
    nxt = route(state)
    if step > state["max_steps"]:
        nxt = END
    return {"next_worker": nxt, "step_count": step}
