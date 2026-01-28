# Entry point – runs the planner loop
from state import AgentState
from planner import Planner
from executor import Executor
from critic import Critic

def run_agent(goal: str):
    state = AgentState(goal)

    print(f"state ===>\n {state.plan}")
    planner = Planner()
    executor = Executor()
    critic = Critic()

    print(f"\nGoal: {goal}\n")

    while not state.completed:
        # 1. Planner
        planner.plan_if_needed(state)
        step = planner.decide_next_step(
            state,
            observation=None,
            critic_feedback=None
        )

        if step is None:
            break

        # 2. Executor
        result = executor.execute(step)

        # 3. Critic
        feedback = critic.evaluate(result)
        print(f"Critic feedback: {feedback}")

        # 4. Planner decides again
        planner.decide_next_step(
            state,
            observation=result,
            critic_feedback=feedback
        )

        state.history.append(
            {"step": step, "result": result, "critic": feedback}
        )
        print(f"current state ===>\n {state.plan}")
        state.current_step_index += 1

    print("\nAgent finished.\nHistory:")
    for h in state.history:
        print(h)


if __name__ == "__main__":
    run_agent("Research MCP and produce a summary")
