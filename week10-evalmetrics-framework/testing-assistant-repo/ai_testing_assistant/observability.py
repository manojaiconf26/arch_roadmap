"""Observability module for the AI Testing Assistant.

Provides logging configuration, agent metrics extraction from Strands
AgentResult objects, and optional OpenTelemetry tracing setup.
"""

import logging
from typing import Optional

from ai_testing_assistant.models import AgentMetrics


def configure_logging(level: int = logging.INFO) -> None:
    """Configure Python logging for the strands logger hierarchy.

    Sets up the ``strands`` logger with a stream handler and a concise
    format so that agent execution details are visible during pipeline
    runs.

    Args:
        level: The logging level to apply (default ``logging.INFO``).
    """
    logger = logging.getLogger("strands")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)


def extract_agent_metrics(agent_name: str, result) -> AgentMetrics:
    """Extract token usage, latency, and cycle count from an AgentResult.

    Reads the ``metrics`` attribute of a Strands ``AgentResult`` and maps
    the values into an :class:`AgentMetrics` dataclass.

    Args:
        agent_name: Human-readable name for the agent (e.g. ``"RUA"``).
        result: A Strands ``AgentResult`` instance.

    Returns:
        An :class:`AgentMetrics` populated from the result's metrics.
    """
    metrics = getattr(result, "metrics", None)

    if metrics is None:
        return AgentMetrics(
            agent_name=agent_name,
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=0.0,
            cycle_count=0,
        )

    accumulated_usage = getattr(metrics, "accumulated_usage", {}) or {}
    accumulated_metrics = getattr(metrics, "accumulated_metrics", {}) or {}
    agent_invocations = getattr(metrics, "agent_invocations", []) or []

    cycle_count = 0
    if agent_invocations:
        last_invocation = agent_invocations[-1]
        cycles = getattr(last_invocation, "cycles", []) or []
        cycle_count = len(cycles)

    return AgentMetrics(
        agent_name=agent_name,
        input_tokens=accumulated_usage.get("inputTokens", 0),
        output_tokens=accumulated_usage.get("outputTokens", 0),
        total_tokens=accumulated_usage.get("totalTokens", 0),
        latency_ms=accumulated_metrics.get("latencyMs", 0.0),
        cycle_count=cycle_count,
    )


def setup_tracing() -> Optional[object]:
    """Set up OpenTelemetry tracing via the Strands StrandsTelemetry helper.

    This is optional — it only activates when the required dependencies
    are installed. Returns the telemetry instance on success, or ``None``
    if the import fails.
    """
    try:
        from strands.telemetry import StrandsTelemetry

        telemetry = StrandsTelemetry()
        telemetry.setup_otlp_exporter()
        return telemetry
    except ImportError:
        logging.getLogger("strands").warning(
            "OpenTelemetry dependencies not installed; tracing disabled."
        )
        return None
    except Exception:
        logging.getLogger("strands").warning(
            "Failed to set up OpenTelemetry tracing; tracing disabled.",
            exc_info=True,
        )
        return None
