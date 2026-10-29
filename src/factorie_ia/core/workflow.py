from langgraph.graph import StateGraph, START, END
from nodes.task import process_task
from domain.state import FactorieState


def build_workflow():
    builder = StateGraph(FactorieState)

    builder.add_node("process_task", process_task)

    builder.add_edge(START, "process_task")
    builder.add_edge("process_task", END)

    return builder.compile()


workflow = build_workflow()
