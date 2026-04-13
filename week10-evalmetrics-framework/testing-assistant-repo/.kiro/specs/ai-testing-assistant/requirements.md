# Requirements Document

## Introduction

The AI Software Testing Assistant is a Python-based multi-agent system built on the Strands agent framework. The system reads software requirements, generates test cases from those requirements, simulates test execution, validates the quality of the generated tests, and evaluates the overall pipeline performance. It comprises four specialized agents orchestrated sequentially: a Requirement Understanding Agent, a Test Generation & Execution Agent, a Test Validator Agent, and an Eval Agent.

## Glossary

- **Strands Agent Framework**: A Python framework for building AI agents with tool-use capabilities and structured message passing.
- **Requirement Understanding Agent (RUA)**: An agent responsible for parsing raw software requirements text and producing structured requirement objects.
- **Test Generation & Execution Agent (TGEA)**: An agent responsible for generating test cases from structured requirements and simulating their execution.
- **Test Validator Agent (TVA)**: An LLM-powered agent responsible for functionally validating the outputs of the RUA and TGEA — checking parsing accuracy, test case relevance, and meaningful requirement coverage.
- **Structured Requirement**: A dictionary or data object containing a requirement identifier, description, priority, and category extracted from raw text.
- **Test Case**: A dictionary or data object containing a test identifier, description, input data, expected output, linked requirement identifier, and execution result.
- **Validation Report**: A data object containing per-agent functional correctness scores, a semantic coverage assessment, and identified issues with agent outputs.
- **Orchestrator**: A Python module that coordinates the sequential execution of the three agents, passing outputs from one agent as inputs to the next.
- **Requirements Input**: A file path (to a `.txt` or `.md` file) or raw text string provided by the user as the source of software requirements.
- **Requirements File**: A persisted `.txt` file containing the raw requirement text, stored in a configurable output directory for reference by downstream agents.
- **LiteLLM**: A unified Python interface for multiple LLM providers, used in Strands to access Groq models for local development.
- **BedrockModel**: The Strands SDK model provider class for Amazon Bedrock, used for production deployment with Claude Sonnet.
- **Coverage Metric**: A numerical ratio representing the proportion of structured requirements that have at least one linked test case.
- **Pipeline Metrics**: An aggregate data object containing per-agent token usage, latency, and cycle counts collected from Strands AgentResult metrics.
- **AgentResult**: The object returned by a Strands Agent invocation, containing the agent's response, structured output, metrics, and traces.
- **OpenTelemetry**: An open-source observability framework for generating, collecting, and exporting telemetry data (traces, metrics, logs).
- **Eval Agent (EA)**: An agent responsible for analyzing the performance metrics collected from each agent invocation and evaluating pipeline efficiency.
- **Eval Report**: A data object containing per-agent metrics analysis, overall pipeline efficiency score, and actionable recommendations for cost and performance optimization.

## Requirements

### Requirement 1

**User Story:** As a QA engineer, I want to provide raw requirement text and receive structured requirement objects, so that I can use them as input for downstream test generation.

#### Acceptance Criteria

1. WHEN the Requirement Understanding Agent receives raw requirement text, THE Requirement Understanding Agent SHALL parse the text and return a list of structured requirement objects each containing an identifier, description, priority, and category.
2. WHEN the Requirement Understanding Agent receives empty or whitespace-only input, THE Requirement Understanding Agent SHALL return an empty list of structured requirements.
3. WHEN a structured requirement is serialized to JSON and deserialized back, THE system SHALL produce an object equivalent to the original structured requirement.

### Requirement 2

**User Story:** As a QA engineer, I want test cases generated from structured requirements, so that I can verify software behavior against those requirements.

#### Acceptance Criteria

1. WHEN the Test Generation & Execution Agent receives a list of structured requirements, THE Test Generation & Execution Agent SHALL generate at least one test case per structured requirement, each containing a test identifier, description, input data, expected output, and linked requirement identifier.
2. WHEN the Test Generation & Execution Agent generates test cases, THE Test Generation & Execution Agent SHALL simulate execution of each test case and assign a pass or fail result to each test case.
3. WHEN the Test Generation & Execution Agent receives an empty list of structured requirements, THE Test Generation & Execution Agent SHALL return an empty list of test cases.

### Requirement 3

**User Story:** As a QA engineer, I want the outputs of all pipeline agents functionally validated, so that I can trust the parsing accuracy and test case relevance.

#### Acceptance Criteria

1. WHEN the Test Validator Agent receives the structured requirements, test cases, and the original raw text, THE Test Validator Agent SHALL produce a validation report containing a functional correctness score for the RUA output and a functional correctness score for the TGEA output.
2. WHEN the Test Validator Agent evaluates the RUA output, THE Test Validator Agent SHALL assess whether the structured requirements accurately reflect the content of the original raw text.
3. WHEN the Test Validator Agent evaluates the TGEA output, THE Test Validator Agent SHALL assess whether each test case semantically relates to the requirement it claims to cover and whether the test inputs and expected outputs are realistic.
4. WHEN the Test Validator Agent identifies requirements with no semantically relevant test cases, THE Test Validator Agent SHALL list those requirement identifiers as uncovered in the validation report.

### Requirement 4

**User Story:** As a developer, I want a simple orchestrator that runs the three agents sequentially, so that I can execute the full pipeline with a single invocation.

#### Acceptance Criteria

1. WHEN the orchestrator receives raw requirement text, THE orchestrator SHALL invoke the Requirement Understanding Agent, then the Test Generation & Execution Agent, then the Test Validator Agent in sequence, passing each agent's output as input to the next agent.
2. WHEN the orchestrator completes the pipeline, THE orchestrator SHALL return a dictionary containing the structured requirements, the test cases, and the validation report.
3. IF any agent in the pipeline raises an error, THEN THE orchestrator SHALL propagate the error with a message identifying which agent failed.

### Requirement 5

**User Story:** As a developer, I want each agent to have a clear modular interface, so that I can extend or replace individual agents independently.

#### Acceptance Criteria

1. THE system SHALL define each agent as a separate Python module with a single public entry-point function that accepts typed input and returns typed output.
2. THE system SHALL use Python dataclasses or typed dictionaries to define the input and output schemas for each agent.
3. WHEN a structured requirement is serialized to JSON using the system's serializer and then deserialized using the system's deserializer, THE system SHALL produce a structured requirement equivalent to the original.
4. WHEN a test case is serialized to JSON using the system's serializer and then deserialized using the system's deserializer, THE system SHALL produce a test case equivalent to the original.

### Requirement 6

**User Story:** As a developer, I want the system to use the Strands agent framework for agent construction, so that I can leverage its tool-use and message-passing capabilities.

#### Acceptance Criteria

1. THE system SHALL construct each agent using the Strands Agent class with a system prompt describing the agent's role and responsibilities.
2. WHEN an agent is invoked, THE system SHALL pass the input through the Strands agent's callable interface and parse the agent's response into the expected output schema.

### Requirement 8

**User Story:** As a QA engineer, I want to provide requirements as either a file path or raw text, so that I can use whichever input method is convenient.

#### Acceptance Criteria

1. WHEN the user provides a file path to a `.txt` or `.md` file, THE system SHALL read the file contents and use them as the raw requirement text for the pipeline.
2. WHEN the user provides raw text content instead of a file path, THE system SHALL write the text to a file in the output directory and use the file path for reference by downstream agents.
3. WHEN the user provides a file path that does not exist, THE system SHALL raise an error with a message indicating the file was not found.
4. WHEN the system writes raw text to a file, THE system SHALL store the file in a configurable output directory with a timestamped filename.

### Requirement 7

**User Story:** As a developer, I want the pipeline to collect and expose observability metrics from each agent invocation, so that I can monitor performance and debug issues.

#### Acceptance Criteria

1. WHEN the orchestrator completes the pipeline, THE orchestrator SHALL include a pipeline metrics object in the result containing per-agent token usage, latency, and cycle count.
2. WHEN an agent is invoked, THE system SHALL extract token usage (input tokens, output tokens, total tokens) and latency from the Strands AgentResult metrics attribute.
3. THE system SHALL configure Python logging for the strands logger hierarchy to enable operational visibility into agent execution.
4. WHERE OpenTelemetry tracing is enabled, THE system SHALL export distributed traces for each agent invocation using the Strands StrandsTelemetry helper.

### Requirement 9

**User Story:** As a developer, I want the pipeline's performance metrics evaluated by a dedicated Eval Agent, so that I can understand the efficiency of each agent and optimize costs.

#### Acceptance Criteria

1. WHEN the Eval Agent receives pipeline metrics, THE Eval Agent SHALL analyze per-agent token usage, latency, and cycle count and produce an eval report containing a metrics summary with efficiency observations.
2. WHEN the Eval Agent identifies an agent with disproportionately high token usage or latency relative to its task complexity, THE Eval Agent SHALL flag the agent in the eval report with a specific efficiency concern.
3. WHEN the Eval Agent produces an eval report, THE Eval Agent SHALL include actionable recommendations for prompt tuning, cost optimization, or pipeline configuration improvements.
4. WHEN the Eval Agent receives an empty pipeline metrics object, THE Eval Agent SHALL return an eval report with zero scores and a recommendation to check the pipeline execution.

### Requirement 10

**User Story:** As a developer, I want to switch between Groq (via LiteLLM) for local testing and Amazon Bedrock for AWS deployment, so that I can develop locally with fast iteration and deploy to production with managed infrastructure.

#### Acceptance Criteria

1. THE system SHALL provide a `get_model()` function that returns a Strands model provider based on the `MODEL_PROVIDER` environment variable.
2. WHEN `MODEL_PROVIDER` is set to "groq", THE system SHALL return a LiteLLMModel configured with the Groq API key from the `GROQ_API_KEY` environment variable.
3. WHEN `MODEL_PROVIDER` is set to "bedrock" or is not set, THE system SHALL return a BedrockModel configured with Claude Sonnet as the default model.
4. THE system SHALL use the configured model provider for all agent constructions without requiring changes to agent code.
