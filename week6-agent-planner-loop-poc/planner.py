# Planner logic (decision authority)
from llm import generate_plan

class Planner:
    def plan_if_needed(self, state):
        if not state.plan:
            state.plan = generate_plan(state.goal)

    def decide_next_step(self, state, observation, critic_feedback):
        if critic_feedback == "bad":
            # Change strategy instead of blind retry
            state.plan.insert(
                state.current_step_index + 1,
                "Do additional research to fix gaps"
            )

        if state.current_step_index >= len(state.plan):
            state.completed = True
            return None

        return state.current_step()
