"""Data models for the AI Testing Assistant pipeline.

Defines core dataclasses for inter-agent data passing, Pydantic wrapper
models for Strands structured output, and JSON serialization helpers.
"""

import json
from dataclasses import asdict, dataclass, field
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Core dataclasses
# ---------------------------------------------------------------------------

@dataclass
class StructuredRequirement:
    """A single structured requirement extracted by the RUA."""

    id: str                    # e.g. "REQ-001"
    description: str           # Requirement description
    priority: str              # "high", "medium", "low"
    category: str              # e.g. "functional", "non-functional"


@dataclass
class TestCase:
    """A test case generated and executed by the TGEA."""

    id: str                    # e.g. "TC-001"
    description: str           # Test case description
    input_data: str            # Input for the test
    expected_output: str       # Expected result
    requirement_id: str        # Linked requirement ID
    result: Optional[str] = None  # "pass" or "fail" after execution


@dataclass
class ValidationReport:
    """Functional validation report produced by the TVA."""

    rua_score: float           # 0.0 to 1.0 — RUA parsing accuracy
    tgea_score: float          # 0.0 to 1.0 — TGEA test case relevance
    coverage_assessment: str   # Semantic coverage summary
    uncovered_requirements: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)


@dataclass
class MetricsSummary:
    """Summary of pipeline metrics produced by the EA."""

    total_tokens: int = 0
    total_latency_ms: float = 0.0
    per_agent_summary: List[str] = field(default_factory=list)
    efficiency_observations: str = ""


@dataclass
class EvalReport:
    """Evaluation report produced by the EA."""

    metrics_summary: Optional[MetricsSummary] = None
    efficiency_score: float = 0.0      # 0.0 to 1.0
    recommendations: List[str] = field(default_factory=list)


@dataclass
class AgentMetrics:
    """Metrics extracted from a single agent invocation."""

    agent_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    cycle_count: int


@dataclass
class PipelineMetrics:
    """Aggregated metrics across all agent invocations."""

    agent_metrics: List[AgentMetrics] = field(default_factory=list)
    total_tokens: int = 0
    total_latency_ms: float = 0.0


@dataclass
class PipelineResult:
    """Complete result returned by the orchestrator."""

    requirements: List[StructuredRequirement] = field(default_factory=list)
    test_cases: List[TestCase] = field(default_factory=list)
    validation_report: Optional[ValidationReport] = None
    eval_report: Optional[EvalReport] = None
    source_file: str = ""
    metrics: Optional[PipelineMetrics] = None


# ---------------------------------------------------------------------------
# Pydantic wrapper models (for Strands structured output)
# ---------------------------------------------------------------------------

class RequirementModel(BaseModel):
    """Pydantic model for a single structured requirement."""

    id: str = Field(description="Requirement identifier, e.g. REQ-001")
    description: str = Field(description="Requirement description")
    priority: str = Field(description="Priority: high, medium, or low")
    category: str = Field(description="Category: functional or non-functional")


class RequirementListModel(BaseModel):
    """Pydantic model wrapping a list of requirements."""

    requirements: List[RequirementModel]


class TestCaseModel(BaseModel):
    """Pydantic model for a single test case."""

    id: str = Field(description="Test case identifier, e.g. TC-001")
    description: str = Field(description="Test case description")
    input_data: str = Field(description="Input for the test")
    expected_output: str = Field(description="Expected result")
    requirement_id: str = Field(description="Linked requirement ID")
    result: Optional[str] = Field(default=None, description="pass or fail")


class TestCaseListModel(BaseModel):
    """Pydantic model wrapping a list of test cases."""

    test_cases: List[TestCaseModel]


class ValidationReportModel(BaseModel):
    """Pydantic model for the TVA validation report."""

    rua_score: float = Field(description="RUA parsing accuracy score 0.0 to 1.0")
    tgea_score: float = Field(description="TGEA test case relevance score 0.0 to 1.0")
    coverage_assessment: str = Field(default="", description="Semantic coverage summary")
    uncovered_requirements: List[str] = Field(default_factory=list)
    issues: List[str] = Field(default_factory=list, description="Identified issues with agent outputs")


class MetricsSummaryModel(BaseModel):
    """Pydantic model for the EA metrics summary."""

    total_tokens: int = Field(default=0, description="Total tokens used across all agents")
    total_latency_ms: float = Field(default=0.0, description="Total latency in milliseconds")
    per_agent_summary: List[str] = Field(default_factory=list, description="Summary per agent")
    efficiency_observations: str = Field(default="", description="Observations about pipeline efficiency")


class EvalReportModel(BaseModel):
    """Pydantic model for the EA evaluation report."""

    metrics_summary: Optional[MetricsSummaryModel] = Field(default=None)
    efficiency_score: float = Field(default=0.0, description="Overall pipeline efficiency 0.0 to 1.0")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations for cost and performance")


# ---------------------------------------------------------------------------
# JSON serialization helpers
# ---------------------------------------------------------------------------

def serialize(obj) -> str:
    """Serialize a dataclass instance to a JSON string."""
    return json.dumps(asdict(obj))


def deserialize_requirement(json_str: str) -> StructuredRequirement:
    """Deserialize a JSON string to a StructuredRequirement."""
    return StructuredRequirement(**json.loads(json_str))


def deserialize_test_case(json_str: str) -> TestCase:
    """Deserialize a JSON string to a TestCase."""
    return TestCase(**json.loads(json_str))
