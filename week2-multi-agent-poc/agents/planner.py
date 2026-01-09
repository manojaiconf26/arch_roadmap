# agents/planner.py
"""
Planner Agent
Breaks a goal into high-level steps.
"""

from llm import call_llm

def run_planner(goal: str, prompt: str) -> str:
    return call_llm(
        system_prompt=prompt,
        user_prompt=goal
    )
