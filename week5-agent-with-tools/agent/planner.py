# Decides WHAT action to take
from schemas.action_schema import Action


class Planner:
    def decide(self, user_input: str) -> Action:
        text = user_input.lower()

        if any(op in text for op in ["+", "-", "*", "/"]):
            return {
                "action": "calculate",
                "arguments": {"expression": user_input}
            }

        if text.startswith("what is"):
            topic = text.replace("what is", "").strip()
            return {
                "action": "lookup",
                "arguments": {"topic": topic}
            }

        return {
            "action": "final",
            "arguments": {
                "answer": "I can answer this directly without tools."
            }
        }
