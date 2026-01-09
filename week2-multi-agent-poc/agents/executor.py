# agents/executor.py
"""
Executor Agent
--------------
Responsibility:
- Execute the plan
- Generate concrete output

Does NOT:
- Judge quality
- Change scope
"""

from llm import call_llm
from typing import Optional

def run_executor(plan: str, feedback: Optional[str], prompt: str) -> str:
    """
    Generates or revises output based on the plan and critic feedback.
    """

    user_prompt = f"""
    PLAN:
    {plan}
    """

    if feedback:
        user_prompt += f"""
        CRITIC FEEDBACK:
        {feedback}

        Revise the output strictly based on the feedback above.
        """

    return call_llm(
        system_prompt=prompt,
        user_prompt=user_prompt
    )
