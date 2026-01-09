# agents/critic.py
"""
Critic Agent
Approves or rejects executor output.
"""

from llm import call_llm
from typing import Tuple, Optional

def run_critic(output: str, prompt: str) -> Tuple[str, Optional[str]]:
    response = call_llm(
        system_prompt=prompt,
        user_prompt=output
    )

    if response.startswith("APPROVED"):
        return "APPROVED", None

    return "REJECTED", response
