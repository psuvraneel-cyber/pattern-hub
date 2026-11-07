"""Mock workers. Deterministic, no API key needed.

Swap these for LLM-backed nodes; the supervisor and budget do not change.
"""

from state import AgentState


def research(state: AgentState) -> dict:
    notes = sum(m.startswith("research:") for m in state["messages"])
    return {"messages": [f"research: note {notes + 1}"]}


def code_worker(state: AgentState) -> dict:
    """Finishes once it has two research notes to work from."""
    notes = sum(m.startswith("research:") for m in state["messages"])
    if notes >= 2:
        return {"messages": ["code: done"]}
    return {"messages": ["code: needs more research"]}


def stubborn_code_worker(state: AgentState) -> dict:
    """Never satisfied. Models the LLM that keeps asking for one more pass."""
    return {"messages": ["code: needs more research"]}
