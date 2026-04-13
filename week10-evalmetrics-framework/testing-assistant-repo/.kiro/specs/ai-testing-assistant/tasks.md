# Implementation Plan

- [x] 1. Set up project structure and dependencies





  - Create directory structure: `ai_testing_assistant/`, `ai_testing_assistant/agents/`, `tests/`
  - Create `__init__.py` files for all packages
  - Create `requirements.txt` with `strands-agents`, `strands-agents[litellm]`, `strands-agents-tools`, `pydantic`, `pytest`, `hypothesis`
  - _Requirements: 5.1, 6.1, 10.1_

- [x] 2. Implement model provider configuration






  - [x] 2.1 Create `model_provider.py` with `get_model()` function

    - Read `MODEL_PROVIDER` env var (default: "bedrock")
    - When "groq": return `LiteLLMModel` with `groq/` prefix model ID and `GROQ_API_KEY` from env
    - When "bedrock": return `BedrockModel` with Claude Sonnet model ID
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 3. Implement data models






  - [x] 3.1 Create core dataclasses and Pydantic models in `models.py`

    - Implement `StructuredRequirement`, `TestCase`, `ValidationReport`, `PipelineResult` dataclasses
    - Implement `RequirementModel`, `RequirementListModel`, `TestCaseModel`, `TestCaseListModel`, `ValidationReportModel` Pydantic models
    - Implement `EvalReport`, `MetricsSummary` dataclasses and `EvalReportModel`, `MetricsSummaryModel` Pydantic models
    - Implement `AgentMetrics` and `PipelineMetrics` dataclasses for observability
    - Add JSON serialization helpers using `dataclasses.asdict()` and `json.dumps()`
    - `PipelineResult` includes `source_file: str` field for the requirements file path
    - _Requirements: 1.3, 5.2, 5.3, 5.4, 7.1_
  - [ ]* 3.2 Write property test: StructuredRequirement round-trip serialization
    - **Property 1: Structured requirement round-trip serialization**
    - **Validates: Requirements 1.3, 5.3**
  - [ ]* 3.3 Write property test: TestCase round-trip serialization
    - **Property 2: Test case round-trip serialization**
    - **Validates: Requirements 5.4**

- [x] 4. Implement input handler












  - [x] 4.1 Create `input_handler.py` with `resolve_input(input_value, output_dir)` function

    - If `input_value` is an existing file path (`.txt` or `.md`), read and return its contents along with the path
    - If `input_value` is raw text, write it to a timestamped file in `output_dir` and return the text and file path
    - Raise `FileNotFoundError` with a clear message if a path-like value does not exist
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  - [ ]* 4.2 Write unit tests for input handler
    - Test reading from an existing `.txt` file
    - Test writing raw text to a new file
    - Test error on non-existent file path
    - _Requirements: 8.1, 8.2, 8.3_

- [x] 5. Implement observability module




  - [x] 5.1 Create `observability.py` with logging configuration and metrics extraction


    - Implement `configure_logging()` function to set up the `strands` logger hierarchy
    - Implement `extract_agent_metrics(agent_name, result)` to pull token usage, latency, and cycle count from `AgentResult.metrics`
    - Implement optional `setup_tracing()` function wrapping `StrandsTelemetry.setup_otlp_exporter()`
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 6. Implement Requirement Understanding Agent






  - [x] 6.1 Create `agents/requirement_agent.py` with `parse_requirements(raw_text: str)` function

    - Construct a Strands `Agent` using `get_model()` with a focused system prompt for requirement parsing
    - Use `structured_output_model=RequirementListModel` for validated responses
    - Handle empty/whitespace input by returning an empty list before invoking the agent
    - Return `List[StructuredRequirement]` by converting Pydantic models to dataclasses
    - Extract and return agent metrics alongside the result
    - _Requirements: 1.1, 1.2, 6.1, 6.2, 7.2, 10.4_
  - [ ]* 6.2 Write property test: Whitespace-only input yields empty requirements
    - **Property 3: Whitespace-only input yields empty requirements**
    - **Validates: Requirements 1.2**
  - [ ]* 6.3 Write unit tests for Requirement Understanding Agent
    - Test parsing a known requirement text produces expected structured output
    - Test empty string input returns empty list
    - _Requirements: 1.1, 1.2_

- [x] 7. Checkpoint - Make sure all tests are passing





  - Ensure all tests pass, ask the user if questions arise.


- [x] 8. Implement Test Generation & Execution Agent





  - [x] 8.1 Create `agents/test_gen_agent.py` with `generate_and_execute(requirements)` function

    - Construct a Strands `Agent` using `get_model()` with a system prompt for test case generation and simulated execution
    - Use `structured_output_model=TestCaseListModel` for validated responses
    - Handle empty requirement list by returning an empty list before invoking the agent
    - Ensure each test case has a `result` field set to "pass" or "fail"
    - Extract and return agent metrics alongside the result
    - _Requirements: 2.1, 2.2, 2.3, 6.1, 6.2, 7.2, 10.4_
  - [ ]* 8.2 Write property test: Test generation covers all requirements
    - **Property 4: Test generation covers all requirements**
    - **Validates: Requirements 2.1, 2.2**
  - [ ]* 8.3 Write unit tests for Test Generation & Execution Agent
    - Test generating test cases from a known requirement list
    - Test empty requirement list returns empty test case list
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 9. Implement Test Validator Agent





  - [x] 9.1 Create `agents/validator_agent.py` with `validate(raw_text, requirements, test_cases)` function


    - Construct a Strands `Agent` using `get_model()` with a system prompt for LLM-as-judge functional validation
    - Use `structured_output_model=ValidationReportModel` for validated responses
    - Pass the original raw text, structured requirements, and test cases as context
    - The agent evaluates: RUA parsing accuracy and TGEA test case semantic relevance
    - The agent identifies requirements with no semantically relevant test cases
    - Extract and return agent metrics alongside the result
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 7.2, 10.4_
  - [ ]* 9.2 Write unit tests for Test Validator Agent
    - Test validation of a well-formed pipeline produces scores for RUA and TGEA
    - Test validation identifies obviously mismatched test cases
    - _Requirements: 3.1, 3.2, 3.3_

- [x] 10. Implement Eval Agent





  - [x] 10.1 Create `agents/eval_agent.py` with `evaluate(pipeline_metrics: PipelineMetrics) -> EvalReport` function


    - Construct a Strands `Agent` using `get_model()` with a system prompt for metrics analysis and efficiency evaluation
    - Use `structured_output_model=EvalReportModel` for validated responses
    - Pass the pipeline metrics (per-agent token usage, latency, cycle counts) as context
    - The agent analyzes token efficiency, latency patterns, and cycle counts per agent
    - The agent produces an efficiency score and actionable recommendations for cost optimization and prompt tuning
    - Handle empty metrics by returning zero efficiency score with a recommendation to check pipeline execution
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 6.1, 6.2, 10.4_
  - [ ]* 10.2 Write unit tests for Eval Agent
    - Test evaluation of complete metrics produces efficiency score and recommendations
    - Test evaluation flags agents with disproportionate token usage
    - Test empty metrics returns zero score
    - _Requirements: 9.1, 9.2, 9.4_

- [x] 11. Checkpoint - Make sure all tests are passing





  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Implement orchestrator and wire everything together







  - [ ] 12.1 Create `orchestrator.py` with `run_pipeline(input_value: str)` function
    - Call `resolve_input()` to get raw text and source file path
    - Invoke RUA, TGEA, TVA, EA sequentially, passing outputs as inputs
    - Pass raw text + requirements + test cases to TVA for functional validation
    - Pass collected PipelineMetrics to EA for efficiency analysis
    - Collect `AgentMetrics` from each agent invocation and aggregate into `PipelineMetrics`
    - Return `PipelineResult` with requirements, test cases, validation report, eval report, source file, and metrics
    - Wrap each agent call in try/except and re-raise with agent-identifying error message
    - _Requirements: 4.1, 4.2, 4.3, 7.1, 8.1, 8.2, 9.1_
  - [ ]* 12.2 Write property test: Orchestrator error identification
    - **Property 5: Orchestrator error identification**
    - **Validates: Requirements 4.3**
  - [ ]* 12.3 Write unit tests for orchestrator
    - Test full pipeline with known input produces a complete PipelineResult including eval report
    - Test error propagation identifies the failing agent
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 13. Create main entry point





  - [x] 13.1 Create `__main__.py` or `main.py` with a CLI entry point


    - Accept a file path or raw text as a CLI argument
    - Call `run_pipeline()` and print the result as formatted JSON
    - Configure logging via `configure_logging()` before pipeline execution
    - _Requirements: 4.1, 7.3, 8.1, 8.2_

- [x] 14. Final Checkpoint - Make sure all tests are passing





  - Ensure all tests pass, ask the user if questions arise.
