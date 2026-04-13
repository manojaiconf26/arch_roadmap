"""Eval Agent (EA).

Analyzes pipeline performance metrics collected from each agent invocation
and produces an efficiency evaluation report with actionable recommendations.
"""

import json
import logging
from dataclasses import asdict
from typing import Tuple

from strands import Agent

from ai_testing_assistant.model_provider import get_model
from ai_testing_assistant.models import (
    AgentMetrics,
    EvalReport,
    EvalReportModel,
    MetricsSummary,
    PipelineMetrics,
)
from ai_testing_assistant.observability import extract_agent_metrics

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the Eval Agent, responsible for analyzing the performance "
    "metrics of a multi-agent software testing pipeline.\n\n"
    "You will receive pipeline metrics containing per-agent token usage, "
    "latency, and cycle counts.\n\n"
    "Your responsibilities:\n\n"
    "**Metrics Summary:**\n"
    "- Calculate total tokens and total latency across all agents.\n"
    "- Provide a per-agent summary describing each agent's resource usage.\n"
    "- Note any efficiency observations (e.g. which agent dominates token "
    "usage or latency).\n\n"
    "**Efficiency Score (0.0–1.0):**\n"
    "- Rate the overall pipeline efficiency based on token usage patterns, "
    "latency distribution, and cycle counts.\n"
    "- A score of 1.0 means highly efficient; 0.0 means very inefficient.\n\n"
    "**Flagging Concerns:**\n"
    "- If any agent has disproportionately high token usage or latency "
    "relative to its task complexity, flag it with a specific concern.\n\n"
    "**Recommendations:**\n"
    "- Provide actionable recommendations for prompt tuning, cost "
    "optimization, or pipeline configuration improvements.\n"
    "- Be specific — reference agent names and metrics in your suggestions."
)


def evaluate(
    pipeline_metrics: PipelineMetrics,
) -> Tuple[EvalReport, AgentMetrics]:
    """Evaluate pipeline performance metrics and produce an efficiency report.

    Args:
        pipeline_metrics: Aggregated metrics from all agent invocations.

    Returns:
        A tuple of (eval report, agent metrics for the EA itself).
    """
    # Handle empty metrics without invoking the agent
    if not pipeline_metrics.agent_metrics:
        logger.info("EA received empty metrics; returning zero score.")
        return EvalReport(
            metrics_summary=MetricsSummary(
                total_tokens=0,
                total_latency_ms=0.0,
                per_agent_summary=[],
                efficiency_observations="No metrics available.",
            ),
            efficiency_score=0.0,
            recommendations=["Check pipeline execution — no agent metrics were collected."],
        ), AgentMetrics(
            agent_name="EA",
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

    metrics_json = json.dumps(asdict(pipeline_metrics), indent=2)

    prompt = (
        "Analyze the following pipeline metrics and produce an evaluation report.\n\n"
        "--- PIPELINE METRICS ---\n"
        f"{metrics_json}\n\n"
        "Provide your evaluation as an eval report with:\n"
        "- metrics_summary: total_tokens, total_latency_ms, per_agent_summary "
        "(list of strings), and efficiency_observations\n"
        "- efficiency_score: 0.0 to 1.0 overall pipeline efficiency\n"
        "- recommendations: list of actionable recommendations for cost and "
        "performance optimization"
    )

    result = agent(prompt, structured_output_model=EvalReportModel)

    # Convert Pydantic model to dataclass
    output = result.structured_output
    metrics_summary = None
    if output.metrics_summary:
        metrics_summary = MetricsSummary(
            total_tokens=output.metrics_summary.total_tokens,
            total_latency_ms=output.metrics_summary.total_latency_ms,
            per_agent_summary=list(output.metrics_summary.per_agent_summary),
            efficiency_observations=output.metrics_summary.efficiency_observations,
        )

    report = EvalReport(
        metrics_summary=metrics_summary,
        efficiency_score=output.efficiency_score,
        recommendations=list(output.recommendations),
    )

    metrics = extract_agent_metrics("EA", result)
    logger.info(
        "EA completed evaluation — efficiency score: %.2f, %d recommendations",
        report.efficiency_score,
        len(report.recommendations),
    )

    return report, metrics
