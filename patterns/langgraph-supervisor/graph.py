from langgraph.graph import START, StateGraph

from state import AgentState
from supervisor import supervisor
from workers import code_worker, research


def build_graph(code=code_worker):
    g = StateGraph(AgentState)
    g.add_node("supervisor", supervisor)
    g.add_node("research", research)
    g.add_node("code", code)
    g.add_edge(START, "supervisor")
    g.add_edge("research", "supervisor")
    g.add_edge("code", "supervisor")
    g.add_conditional_edges("supervisor", lambda s: s["next_worker"])
    return g.compile()


def init_state(query: str, max_steps: int) -> dict:
    return {"messages": [f"user: {query}"], "next_worker": "", "step_count": 0, "max_steps": max_steps}
