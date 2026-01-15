"""
Transforms memory logs into decision-shaping signals.
"""

def retrieve_relevant_memory(memory_store):
    interpreted_memory = {}

    for entry in memory_store.get_all():
        text = entry.lower()

        if "prefer aws" in text:
            interpreted_memory["preferred_cloud"] = "AWS"

        if "short answers" in text or "concise" in text:
            interpreted_memory["response_style"] = "concise"

    return interpreted_memory
