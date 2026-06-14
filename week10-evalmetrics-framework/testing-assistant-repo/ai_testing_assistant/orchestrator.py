"""Orchestrator for the AI Testing Assistant pipeline.

Coordinates the sequential execution of all four agents (RUA, TGEA, TVA, EA),
passing outputs from one agent as inputs to the next, collecting metrics,
and returning a complete PipelineResult.
"""

import logging
import time

from ai_testing_assistant.agents.eval_agent import evaluate
from ai_testing_assistant.agents.requirement_agent import parse_requirements
from ai_testing_assistant.agents.test_gen_agent import generate_and_execute
from ai_testing_assistant.agents.validator_agent import validate
from ai_testing_assistant.input_handler import resolve_input
from ai_testing_assistant.models import PipelineMetrics, PipelineResult

logger = logging.getLogger(__name__)

# Max retries and base delay for rate-limit errors (Groq free tier: 8K TPM)
_MAX_RETRIES = 3
_BASE_DELAY_S = 30


def _run_with_retry(agent_fn, agent_label, *args):
    """Run an agent function with retry on rate-limit errors.

    Retries up to _MAX_RETRIES times with increasing backoff when a
    RateLimitError is detected, giving the TPM window time to reset.
    """
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            return agent_fn(*args)
        except Exception as exc:
            if "RateLimitError" in type(exc).__name__ or "rate_limit" in str(exc).lower():
                if attempt < _MAX_RETRIES:
                    delay = _BASE_DELAY_S * attempt
                    logger.warning(
                        "%s hit rate limit (attempt %d/%d). Waiting %ds before retry...",
                        agent_label, attempt, _MAX_RETRIES, delay,
                    )
                    time.sleep(delay)
                    continue
            raise RuntimeError(f"{agent_label} failed: {exc}") from exc


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
    logger.info("Input resolved — %d characters from %s", len(raw_text), source_file or "raw text")

    pipeline_metrics = PipelineMetrics()
    pipeline_start = time.time()

    # --- RUA: parse requirements ---
    logger.info("[1/4] Running Requirement Understanding Agent (RUA)...")
    step_start = time.time()
    requirements, rua_metrics = _run_with_retry(
        parse_requirements, "Requirement Understanding Agent (RUA)", raw_text
    )
    logger.info("[1/4] RUA complete — %d requirements parsed (%.1fs)",
                len(requirements), time.time() - step_start)

    pipeline_metrics.agent_metrics.append(rua_metrics)
    pipeline_metrics.total_tokens += rua_metrics.total_tokens
    pipeline_metrics.total_latency_ms += rua_metrics.latency_ms

    # --- TGEA: generate and execute test cases ---
    logger.info("[2/4] Running Test Generation & Execution Agent (TGEA)...")
    step_start = time.time()
    test_cases, tgea_metrics = _run_with_retry(
        generate_and_execute, "Test Generation & Execution Agent (TGEA)", requirements
    )
    logger.info("[2/4] TGEA complete — %d test cases generated (%.1fs)",
                len(test_cases), time.time() - step_start)

    pipeline_metrics.agent_metrics.append(tgea_metrics)
    pipeline_metrics.total_tokens += tgea_metrics.total_tokens
    pipeline_metrics.total_latency_ms += tgea_metrics.latency_ms

    # --- TVA: validate outputs ---
    logger.info("[3/4] Running Test Validator Agent (TVA)...")
    step_start = time.time()
    validation_report, tva_metrics = _run_with_retry(
        validate, "Test Validator Agent (TVA)", raw_text, requirements, test_cases
    )
    logger.info("[3/4] TVA complete — RUA score: %.2f, TGEA score: %.2f (%.1fs)",
                validation_report.rua_score, validation_report.tgea_score,
                time.time() - step_start)

    pipeline_metrics.agent_metrics.append(tva_metrics)
    pipeline_metrics.total_tokens += tva_metrics.total_tokens
    pipeline_metrics.total_latency_ms += tva_metrics.latency_ms

    # --- EA: evaluate pipeline efficiency ---
    logger.info("[4/4] Running Eval Agent (EA)...")
    step_start = time.time()
    eval_report, ea_metrics = _run_with_retry(
        evaluate, "Eval Agent (EA)", pipeline_metrics
    )
    logger.info("[4/4] EA complete — efficiency score: %.2f (%.1fs)",
                eval_report.efficiency_score, time.time() - step_start)

    pipeline_metrics.agent_metrics.append(ea_metrics)
    pipeline_metrics.total_tokens += ea_metrics.total_tokens
    pipeline_metrics.total_latency_ms += ea_metrics.latency_ms

    total_time = time.time() - pipeline_start
    logger.info(
        "Pipeline complete — %d requirements, %d test cases, "
        "total tokens: %d, total time: %.1fs",
        len(requirements),
        len(test_cases),
        pipeline_metrics.total_tokens,
        total_time,
    )

    return PipelineResult(
        requirements=requirements,
        test_cases=test_cases,
        validation_report=validation_report,
        eval_report=eval_report,
        source_file=source_file,
        metrics=pipeline_metrics,
    )
