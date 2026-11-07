"""These tests back every number on the carousel. If one fails, the post is wrong."""

import pytest
from langgraph.errors import GraphRecursionError
from langgraph.graph import END

from graph import build_graph, init_state
from workers import stubborn_code_worker


def count_supersteps(app, state, limit):
    return sum(1 for _ in app.stream(state, {"recursion_limit": limit}, stream_mode="updates"))


def test_normal_task_finishes_on_its_own():
    out = build_graph().invoke(init_state("q", 6), {"recursion_limit": 25})
    assert out["messages"][-1] == "code: done"
    assert out["step_count"] < 6  # finished before the budget mattered


def test_guard_turns_endless_loop_into_clean_exit():
    out = build_graph(stubborn_code_worker).invoke(init_state("q", 6), {"recursion_limit": 25})
    assert out["next_worker"] == END
    assert out["step_count"] == 7  # 6 routed hops + the exiting call
    assert len(out["messages"]) == 1 + 6  # user msg + every worker's partial work kept


def test_max_steps_6_uses_exactly_13_supersteps():
    # 7 supervisor steps + 6 worker steps
    assert count_supersteps(build_graph(stubborn_code_worker), init_state("q", 6), 25) == 13


def test_recursion_limit_must_be_at_least_2x_max_steps_plus_2():
    # recursion_limit also counts the input step, so 13 supersteps need a limit of 14.
    max_steps = 6
    floor = 2 * max_steps + 2
    assert count_supersteps(build_graph(stubborn_code_worker), init_state("q", max_steps), floor) == 13
    with pytest.raises(GraphRecursionError):
        count_supersteps(build_graph(stubborn_code_worker), init_state("q", max_steps), floor - 1)


def test_without_budget_recursion_limit_raises():
    with pytest.raises(GraphRecursionError):
        build_graph(stubborn_code_worker).invoke(init_state("q", 10_000), {"recursion_limit": 25})
