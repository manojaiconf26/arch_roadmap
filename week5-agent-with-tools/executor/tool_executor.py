# Executes tools (side-effect boundary)
from tools.calculator import calculate
from tools.knowledge_base import lookup


class ToolExecutor:
    def execute(self, action: str, arguments: dict):
        if action == "calculate":
            return calculate(**arguments)

        if action == "lookup":
            return lookup(**arguments)

        raise ValueError(f"Unknown action: {action}")
