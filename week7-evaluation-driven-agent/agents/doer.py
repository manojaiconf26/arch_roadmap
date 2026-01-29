class DoerAgent:
    def generate(self, task: str, feedback: str | None = None) -> str:
        """
        Generates an answer for the given task.
        Uses feedback (if provided) to improve output.
        """

        if feedback:
            return (
                "An AI agent is a software system that can understand a goal, "
                "make decisions, and take actions autonomously to achieve that goal. "
                "Unlike a simple chatbot, an agent can reason, use tools, and learn "
                "from feedback to improve its behavior over time."
            )

        # First attempt (intentionally weak)
        return "An agent is a system that gives responses based on input."
