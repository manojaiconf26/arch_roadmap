"""Requirement Understanding Agent (RUA).

Parses raw software requirement text into structured requirement objects
using a Strands Agent with structured output.
"""

import logging
from typing import List, Tuple

from strands import Agent

from ai_testing_assistant.model_provider import get_model
from ai_testing_assistant.models import (
    AgentMetrics,
    RequirementListModel,
    StructuredRequirement,
)
from ai_testing_assistant.observability import extract_agent_metrics

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the Requirement Understanding Agent. Your sole responsibility is "
    "to parse raw software requirement text into a structured list of "
    "requirements.\n\n"
    "For each requirement you identify, extract:\n"
    "- id: A unique identifier (e.g. REQ-001, REQ-002)\n"
    "- description: A clear, concise description of the requirement\n"
    "- priority: One of 'high', 'medium', or 'low'\n"
    "- category: One of 'functional' or 'non-functional'\n\n"
    "If the input text is empty or contains no identifiable requirements, "
    "return an empty list of requirements.\n"
    "Be thorough — capture every distinct requirement from the text."
)


def parse_requirements(
    raw_text: str,
) -> Tuple[List[StructuredRequirement], AgentMetrics]:
    """Parse raw requirement text into structured requirement objects.

    Args:
        raw_text: The raw requirement text to parse.

    Returns:
        A tuple of (list of structured requirements, agent metrics).
    """
    # Handle empty/whitespace input without invoking the agent
    if not raw_text or raw_text.strip() == "":
        logger.info("RUA received empty/whitespace input; returning empty list.")
        return [], AgentMetrics(
            agent_name="RUA",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=0.0,
            cycle_count=0,
        )

    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        model=get_model(),
        callback_handler=None,
    )

    result = agent(
        f"Parse the following requirements text into structured requirements:\n\n{raw_text}",
        structured_output_model=RequirementListModel,
    )

    # Convert Pydantic models to dataclasses
    requirements: List[StructuredRequirement] = []
    if result.structured_output and result.structured_output.requirements:
        for req in result.structured_output.requirements:
            requirements.append(
                StructuredRequirement(
                    id=req.id,
                    description=req.description,
                    priority=req.priority,
                    category=req.category,
                )
            )

    metrics = extract_agent_metrics("RUA", result)
    logger.info("RUA parsed %d requirements.", len(requirements))

    return requirements, metrics
