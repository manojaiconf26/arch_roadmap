# LLM abstraction (mocked)
def generate_plan(goal: str):
    return [
        "Research the topic",
        "Summarize key findings",
        "Produce final output"
    ]

def decide_next_action(state_snapshot: dict):
    return "continue"
