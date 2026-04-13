"""Test Validator Agent (TVA).

Functionally validates the outputs of the RUA and TGEA using an
LLM-as-judge approach. Evaluates parsing accuracy, test case semantic
relevance, and requirement coverage.
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
    ValidationReport,
    ValidationReportModel,
)
from ai_testing_assistant.observability import extract_agent_metrics

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the Test Validator Agent, acting as an LLM-as-judge for "
    "functional validation of a software testing pipeline.\n\n"
    "You will receive three inputs:\n"
    "1. The original raw requirement text\n"
    "2. Structured requirements produced by the Requirement Understanding Agent (RUA)\n"
    "3. Test cases produced by the Test Generation & Execution Agent (TGEA)\n\n"
    "Your responsibilities:\n\n"
    "**RUA Evaluation (rua_score 0.0–1.0):**\n"
    "- Assess whether the structured requirements accurately reflect the "
    "content of the original raw text.\n"
    "- Check that each requirement has a valid id, description, priority, "
    "and category.\n"
    "- Check that no requirements from the raw text were missed.\n\n"
    "**TGEA Evaluation (tgea_score 0.0–1.0):**\n"
    "- Assess whether each test case semantically relates to the requirement "
    "it claims to cover.\n"
    "- Check that test inputs and expected outputs are realistic.\n"
    "- Check that every test case has a result of 'pass' or 'fail'.\n\n"
    "**Coverage Assessment:**\n"
    "- Identify any requirement IDs that have no semantically relevant test "
    "cases and list them in uncovered_requirements.\n"
    "- Provide a brief coverage_assessment summary.\n\n"
    "**Issues:**\n"
    "- List any specific issues found with the RUA or TGEA outputs.\n\n"
    "Be thorough and objective in your evaluation."
)


def validate(
    raw_text: str,
    requirements: List[StructuredRequirement],
    test_cases: List[TestCase],
) -> Tuple[ValidationReport, AgentMetrics]:
    """Validate the outputs of the RUA and TGEA using LLM-as-judge.

    Args:
        raw_text: The original raw requirement text.
        requirements: Structured requirements produced by the RUA.
        test_cases: Test cases produced by the TGEA.

    Returns:
        A tuple of (validation report, agent metrics).
    """
    # Handle empty inputs — nothing to validate
    if not requirements and not test_cases:
        logger.info("TVA received empty requirements and test cases; returning zero scores.")
        return ValidationReport(
            rua_score=0.0,
            tgea_score=0.0,
            coverage_assessment="No requirements or test cases to validate.",
            uncovered_requirements=[],
            issues=[],
        ), AgentMetrics(
            agent_name="TVA",
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

    requirements_json = json.dumps(
        [asdict(req) for req in requirements], indent=2
    )
    test_cases_json = json.dumps(
        [asdict(tc) for tc in test_cases], indent=2
    )

    prompt = (
        "Evaluate the following pipeline outputs for functional correctness.\n\n"
        "--- ORIGINAL RAW REQUIREMENT TEXT ---\n"
        f"{raw_text}\n\n"
        "--- STRUCTURED REQUIREMENTS (RUA output) ---\n"
        f"{requirements_json}\n\n"
        "--- TEST CASES (TGEA output) ---\n"
        f"{test_cases_json}\n\n"
        "Provide your evaluation as a validation report with:\n"
        "- rua_score: 0.0 to 1.0 for RUA parsing accuracy\n"
        "- tgea_score: 0.0 to 1.0 for TGEA test case relevance\n"
        "- coverage_assessment: brief summary of requirement coverage\n"
        "- uncovered_requirements: list of requirement IDs with no relevant test cases\n"
        "- issues: list of specific issues found"
    )

    result = agent(prompt, structured_output_model=ValidationReportModel)

    # Convert Pydantic model to dataclass
    output = result.structured_output
    report = ValidationReport(
        rua_score=output.rua_score,
        tgea_score=output.tgea_score,
        coverage_assessment=output.coverage_assessment,
        uncovered_requirements=list(output.uncovered_requirements),
        issues=list(output.issues),
    )

    metrics = extract_agent_metrics("TVA", result)
    logger.info(
        "TVA completed validation — RUA score: %.2f, TGEA score: %.2f",
        report.rua_score,
        report.tgea_score,
    )

    return report, metrics
