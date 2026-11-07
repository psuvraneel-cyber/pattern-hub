from operator import add
from typing import Annotated, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add]
    next_worker: str
    step_count: int
    max_steps: int
