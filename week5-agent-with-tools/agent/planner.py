from schemas.action_schema import Action
from llm.llm_client import LLMClient


class Planner:
    def __init__(self):
        self.llm = LLMClient()

    def decide(self, user_input: str) -> Action:
        plan = self.llm.generate_plan(user_input)

        # Basic validation (expand later)
        if "action" not in plan or "arguments" not in plan:
            raise ValueError("Invalid plan returned by LLM")

        return plan
