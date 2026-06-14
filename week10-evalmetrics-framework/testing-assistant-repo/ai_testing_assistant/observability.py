"""Observability module for the AI Testing Assistant.

Provides logging configuration, agent metrics extraction from Strands
AgentResult objects, and optional OpenTelemetry tracing setup.
"""

import logging
from typing import Optional

from ai_testing_assistant.models import AgentMetrics


def configure_logging(level: int = logging.INFO) -> None:
    """Configure Python logging for the application and strands loggers.

    Sets up both the application logger (``ai_testing_assistant``) and the
    ``strands`` logger with stream handlers so that pipeline progress and
    agent execution details are visible during runs.

    Args:
        level: The logging level to apply (default ``logging.INFO``).
    """
    fmt = logging.Formatter("%(levelname)s | %(name)s | %(message)s")

    for logger_name in ("ai_testing_assistant", "strands"):
        lgr = logging.getLogger(logger_name)
        lgr.setLevel(level)
        if not lgr.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(fmt)
            lgr.addHandler(handler)


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

    # Handle both dict-like and object-like access for usage/metrics
    if isinstance(accumulated_usage, dict):
        input_tokens = accumulated_usage.get("inputTokens", 0)
        output_tokens = accumulated_usage.get("outputTokens", 0)
        total_tokens = accumulated_usage.get("totalTokens", 0)
    else:
        input_tokens = getattr(accumulated_usage, "inputTokens", 0) or 0
        output_tokens = getattr(accumulated_usage, "outputTokens", 0) or 0
        total_tokens = getattr(accumulated_usage, "totalTokens", 0) or 0

    if isinstance(accumulated_metrics, dict):
        latency_ms = accumulated_metrics.get("latencyMs", 0.0)
    else:
        latency_ms = getattr(accumulated_metrics, "latencyMs", 0.0) or 0.0

    cycle_count = getattr(metrics, "cycle_count", 0) or 0

    return AgentMetrics(
        agent_name=agent_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency_ms=latency_ms,
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
