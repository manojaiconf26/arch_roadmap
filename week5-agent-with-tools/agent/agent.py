from agent.planner import Planner
from executor.tool_executor import ToolExecutor


class Agent:
    def __init__(self):
        self.planner = Planner()
        self.executor = ToolExecutor()

    def run(self, user_input: str) -> str:
        decision = self.planner.decide(user_input)

        if decision["action"] == "final":
            return decision["arguments"]["answer"]

        observation = self.executor.execute(
            decision["action"],
            decision["arguments"]
        )

        return f"Based on the tool result: {observation}"
