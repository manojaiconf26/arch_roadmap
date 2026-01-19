# Mock knowledge lookup
KNOWLEDGE_BASE = {
    "agentic ai": "Agentic AI refers to systems that can plan, act, and reflect autonomously.",
    "llm": "A Large Language Model is a probabilistic model trained on vast text data."
}


def lookup(topic: str) -> str:
    return KNOWLEDGE_BASE.get(topic.lower(), "No data found.")
