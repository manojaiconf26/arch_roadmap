"""Orchestrator for the AI Testing Assistant pipeline.

Coordinates the sequential execution of all four agents (RUA, TGEA, TVA, EA),
passing outputs from one agent as inputs to the next, collecting metrics,
and returning a complete PipelineResult.
"""

import logging

from ai_testing_assistant.agents.eval_agent import evaluate
from ai_testing_assistant.agents.requirement_agent import parse_requirements
from ai_testing_assistant.agents.test_gen_agent import generate_and_execute
from ai_testing_assistant.agents.validator_agent import validate
from ai_testing_assistant.input_handler import resolve_input
from ai_testing_assistant.models import PipelineMetrics, PipelineResult

logger = logging.getLogger(__name__)


def run_pipeline(input_value: str) -> PipelineResult:
    """Run the full AI Testing Assistant pipeline.

    Resolves the input, then invokes RUA, TGEA, TVA, and EA sequentially.
    Each agent's output feeds into the next. Metrics are collected from
    every invocation and aggregated into a PipelineMetrics object.

    Args:
        input_value: A file path (.txt/.md) or raw requirement text.

    Returns:
        A PipelineResult containing requirements, test cases, validation
        report, eval report, source file path, and pipeline metrics.

    Raises:
        RuntimeError: If any agent fails, with a message identifying which
            agent raised the error.
    """
    # --- Resolve input ---
    raw_text, source_file = resolve_input(input_value)

    pipeline_metrics = PipelineMetrics()

    # --- RUA: parse requirements ---
    try:
        requirements, rua_metrics = parse_requirements(raw_text)
    except Exception as exc:
        raise RuntimeError(
            f"Requirement Understanding Agent (RUA) failed: {exc}"
        ) from exc

    pipeline_metrics.agent_metrics.append(rua_metrics)
    pipeline_metrics.total_tokens += rua_metrics.total_tokens
    pipeline_metrics.total_latency_ms += rua_metrics.latency_ms

    # --- TGEA: generate and execute test cases ---
    try:
        test_cases, tgea_metrics = generate_and_execute(requirements)
    except Exception as exc:
        raise RuntimeError(
            f"Test Generation & Execution Agent (TGEA) failed: {exc}"
        ) from exc

    pipeline_metrics.agent_metrics.append(tgea_metrics)
    pipeline_metrics.total_tokens += tgea_metrics.total_tokens
    pipeline_metrics.total_latency_ms += tgea_metrics.latency_ms

    # --- TVA: validate outputs ---
    try:
        validation_report, tva_metrics = validate(raw_text, requirements, test_cases)
    except Exception as exc:
        raise RuntimeError(
            f"Test Validator Agent (TVA) failed: {exc}"
        ) from exc

    pipeline_metrics.agent_metrics.append(tva_metrics)
    pipeline_metrics.total_tokens += tva_metrics.total_tokens
    pipeline_metrics.total_latency_ms += tva_metrics.latency_ms

    # --- EA: evaluate pipeline efficiency ---
    try:
        eval_report, ea_metrics = evaluate(pipeline_metrics)
    except Exception as exc:
        raise RuntimeError(
            f"Eval Agent (EA) failed: {exc}"
        ) from exc

    pipeline_metrics.agent_metrics.append(ea_metrics)
    pipeline_metrics.total_tokens += ea_metrics.total_tokens
    pipeline_metrics.total_latency_ms += ea_metrics.latency_ms

    logger.info(
        "Pipeline complete — %d requirements, %d test cases, "
        "total tokens: %d, total latency: %.0f ms",
        len(requirements),
        len(test_cases),
        pipeline_metrics.total_tokens,
        pipeline_metrics.total_latency_ms,
    )

    return PipelineResult(
        requirements=requirements,
        test_cases=test_cases,
        validation_report=validation_report,
        eval_report=eval_report,
        source_file=source_file,
        metrics=pipeline_metrics,
    )
