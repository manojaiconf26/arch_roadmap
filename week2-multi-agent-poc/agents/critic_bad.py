# agents/critic.py
"""
Critic Agent
Approves or rejects executor output.
"""

from llm import call_llm
from typing import Tuple, Optional

def run_critic(output: str, prompt: str, attempt: int) -> Tuple[str, Optional[str]]:
    user_input = f"Attempt: {attempt}\nContent: {output}"
    
    response = call_llm(
        system_prompt=prompt,
        user_prompt=user_input
    )

    if response.startswith("APPROVED"):
        return "APPROVED", None

    return "REJECTED", response
