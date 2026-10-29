from domain.state import FactorieState


def process_task(state: FactorieState) -> dict:
    task = state["task"]

    return {"response": f"Que tal estas esta es tu : {task}"}
