import json


class LLMClient:
    def generate_plan(self, user_input: str) -> dict:
        """
        Simulates an LLM producing JSON output.
        Replace this with a real LLM call later.
        """

        text = user_input.lower()

        if any(op in text for op in ["+", "-", "*", "/"]):
            return {
                "action": "calculate",
                "arguments": {
                    "expression": user_input
                }
            }

        if text.startswith("what is"):
            topic = text.replace("what is", "").strip()
            return {
                "action": "lookup",
                "arguments": {
                    "topic": topic
                }
            }

        return {
            "action": "final",
            "arguments": {
                "answer": "I can answer this without using tools."
            }
        }
