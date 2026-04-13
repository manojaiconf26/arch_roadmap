"""Test Generation & Execution Agent (TGEA).

Generates test cases from structured requirements and simulates their
execution using a Strands Agent with structured output.
"""

import json
import logging
from dataclasses import asdict
from typing import List, Tuple

from strands import Agent

from ai_testing_assistant.model_provider import get_model
from ai_testing_assistant.models import (
    AgentMetrics,
    StructuredRequirement,
    TestCase,
    TestCaseListModel,
)
from ai_testing_assistant.observability import extract_agent_metrics

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the Test Generation & Execution Agent. Your sole responsibility "
    "is to generate test cases from structured software requirements and "
    "simulate their execution.\n\n"
    "For each structured requirement you receive, generate at least one test "
    "case containing:\n"
    "- id: A unique test case identifier (e.g. TC-001, TC-002)\n"
    "- description: A clear description of what the test verifies\n"
    "- input_data: Realistic input data for the test\n"
    "- expected_output: The expected result of the test\n"
    "- requirement_id: The ID of the requirement this test covers "
    "(must match exactly one of the provided requirement IDs)\n"
    "- result: Simulate execution and set to 'pass' or 'fail'\n\n"
    "Every requirement must have at least one test case linked to it. "
    "Each test case must have a result of either 'pass' or 'fail'.\n"
    "If the input list of requirements is empty, return an empty list of "
    "test cases."
)


def generate_and_execute(
    requirements: List[StructuredRequirement],
) -> Tuple[List[TestCase], AgentMetrics]:
    """Generate test cases from structured requirements and simulate execution.

    Args:
        requirements: List of structured requirements to generate tests for.

    Returns:
        A tuple of (list of test cases with pass/fail results, agent metrics).
    """
    # Handle empty requirement list without invoking the agent
    if not requirements:
        logger.info("TGEA received empty requirements list; returning empty list.")
        return [], AgentMetrics(
            agent_name="TGEA",
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

    # Serialize requirements to JSON for the prompt
    requirements_json = json.dumps(
        [asdict(req) for req in requirements], indent=2
    )

    result = agent(
        f"Generate test cases for the following structured requirements and "
        f"simulate their execution. Each test case must have a result of "
        f"'pass' or 'fail'.\n\nRequirements:\n{requirements_json}",
        structured_output_model=TestCaseListModel,
    )

    # Convert Pydantic models to dataclasses
    test_cases: List[TestCase] = []
    if result.structured_output and result.structured_output.test_cases:
        for tc in result.structured_output.test_cases:
            # Ensure result is set to "pass" or "fail"
            tc_result = tc.result if tc.result in ("pass", "fail") else "fail"
            test_cases.append(
                TestCase(
                    id=tc.id,
                    description=tc.description,
                    input_data=tc.input_data,
                    expected_output=tc.expected_output,
                    requirement_id=tc.requirement_id,
                    result=tc_result,
                )
            )

    metrics = extract_agent_metrics("TGEA", result)
    logger.info("TGEA generated %d test cases.", len(test_cases))

    return test_cases, metrics
