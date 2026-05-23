# Implementation Plan: AI Research & Learning Assistant

## Overview

This plan implements a **single, self-contained Jupyter notebook** (`ai_research_assistant.ipynb`) that provides an AI Research & Learning Assistant using the Strands Agents SDK. Everything — tools, knowledge base, sample data, Pydantic models, agent creation, demos, and evaluation scenarios — lives inside this one notebook. No external files are required; all resources are created inline as notebook cells.

The implementation uses the **Kiro Strands Agent power** (`kiroPowers` with `powerName="strands"`) to reference correct Strands SDK patterns, tool signatures, and agent creation approaches.

## Key Constraints

- **Single notebook artifact**: All code, configuration, knowledge base creation, tools, demos, and evaluations in one `.ipynb` file
- **Google Colab compatible**: No local file dependencies outside what the notebook creates at runtime
- **Inline resource creation**: Knowledge base files, sample images, and session directories are created by notebook cells as pre-steps
- **Detailed explanations**: Every section includes markdown cells with thorough explanations of what the code does and why
- **Strands Agent power**: Use Kiro's Strands power to verify correct SDK patterns during implementation

## Tasks

- [x] 1. Create notebook foundation with setup, configuration, and imports
  - [x] 1.1 Create the notebook with title, introduction, setup, and configuration cells
    - Create `ai_research_assistant.ipynb` with:
      - Title markdown cell: project name, description, capabilities list, compatibility note
      - Section 1 markdown cell: "Setup" with explanation of dependencies
      - Code cell: `!pip install strands-agents strands-agents-tools pydantic>=2.0` (no pinned versions for Colab compatibility)
      - Code cell: all imports (`os`, `json`, `glob`, `pathlib.Path`, `typing`, `pydantic`, `strands`)
      - Section 2 markdown cell: "Configuration" explaining model providers and credentials
      - Code cell: `get_model()` factory with Bedrock default + commented Anthropic/OpenAI/Gemini alternatives
    - Use **Kiro Strands power** (`search_docs` + `fetch_doc`) to verify correct model provider import paths and constructor signatures
    - Include detailed markdown explaining: what each provider needs, how to set API keys in Colab (`os.environ["KEY"] = "value"`), which models are available
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.6_

- [x] 2. Implement Pydantic models for structured output (in notebook)
  - [x] 2.1 Add Pydantic schema models cell to the notebook
    - Add Section 3 markdown cell: "Structured Output Schemas" explaining what Pydantic models are, why they're used with Strands, and how `structured_output_model` works
    - Add code cell defining: `RoadmapPhase`, `LearningRoadmap`, `TechnologyEntry`, `TechnologyComparison`, `QAResponse`
    - Each model uses `Field(description=...)` for self-documentation
    - Use **Kiro Strands power** to verify the correct `structured_output_model` usage pattern
    - Include inline comments explaining each field's purpose
    - _Requirements: 12.1, 12.2, 7.6_

- [x] 3. Update notebook configuration to use Ollama and Groq with qwen3.5:4b
  - [x] 3.1 Update the configuration cell to use Ollama as primary provider and Groq as alternative
    - Replace the existing configuration cell (Section 2) with:
      - Primary: **Ollama** using `OllamaModel` from `strands.models.ollama` with `model_id="qwen3.5:4b"` and `host="http://localhost:11434"`
      - Alternative: **Groq** using `OpenAIModel` from `strands.models.openai` with Groq's OpenAI-compatible endpoint (`api_base="https://api.groq.com/openai/v1"`) and `GROQ_API_KEY`
    - Update the install cell to include: `!pip install 'strands-agents[ollama]' strands-agents-tools pydantic>=2.0`
    - Add markdown cell explaining:
      - How to install and run Ollama locally (`ollama pull qwen3.5:4b && ollama serve`)
      - How to get a Groq API key from https://console.groq.com
      - Why qwen3.5:4b is chosen (lightweight, tool-calling support, runs on modest hardware)
      - How to switch between Ollama (local, free) and Groq (cloud, fast inference)
    - Configuration code pattern:
      ```python
      from strands.models.ollama import OllamaModel

      # Option 1: Ollama (local, free — requires ollama running locally)
      def get_model():
          return OllamaModel(
              host="http://localhost:11434",
              model_id="qwen3.5:4b",
          )

      # Option 2: Groq (cloud, fast — requires GROQ_API_KEY)
      # from strands.models.openai import OpenAIModel
      # def get_model():
      #     return OpenAIModel(
      #         client_args={
      #             "api_key": os.environ.get("GROQ_API_KEY"),
      #             "base_url": "https://api.groq.com/openai/v1",
      #         },
      #         model_id="qwen-qwq-32b",  # or other Groq-supported model
      #     )
      ```
    - Use **Kiro Strands power** to verify correct `OllamaModel` constructor and OpenAI-compatible endpoint pattern for Groq
    - _Requirements: 1.1, 1.2, 1.4, 1.6_

- [x] 4. Create Knowledge Base inline in the notebook
  - [x] 4.1 Add knowledge base creation cell
    - Add Section 4 markdown cell: "Knowledge Base" explaining the local-first retrieval approach, why we use keyword search instead of vector stores, and what topics are covered
    - Add code cell that:
      - Creates `./knowledge_base/` directory using `Path.mkdir(parents=True, exist_ok=True)`
      - Writes 5 sample markdown files inline using Python `Path.write_text()`:
        - `ai_fundamentals.md` (neural networks, transformers, training, inference — 250+ words)
        - `cloud_architecture.md` (microservices, serverless, event-driven, multi-region — 250+ words)
        - `kubernetes_basics.md` (pods, services, deployments, scaling, networking — 250+ words)
        - `devops_practices.md` (CI/CD, IaC, monitoring, incident response — 250+ words)
        - `aws_services.md` (Lambda, S3, DynamoDB, ECS, Step Functions — 250+ words)
      - Each document uses consistent markdown formatting with `#` headers, bullet lists, and code blocks
      - Prints confirmation of files created
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 5. Implement Custom Tools (all in notebook)
  - [x] 5.1 Implement the Retrieval Tool
    - Add Section 5 markdown cell: "Custom Tools" with explanation of the `@tool` decorator pattern, how Strands uses docstrings for tool selection, and the tool architecture
    - Add subsection markdown: "5.1 Retrieval Tool" explaining keyword-based search algorithm (tokenize → score paragraphs → return top-3 with attribution)
    - Add code cell with `@tool` decorated `retrieval_tool(query: str) -> str` function:
      - Define stop words list inline
      - Tokenize query into lowercase keywords (minus stop words)
      - Glob `./knowledge_base/*.md` files
      - Split each file into paragraphs (double newline)
      - Score paragraphs by keyword overlap count
      - Return top-3 scoring paragraphs with `[Source: filename.md]` attribution
      - Handle edge cases: missing directory, no files, empty query
    - Use **Kiro Strands power** to verify correct `@tool` decorator usage and return type patterns
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

  - [x] 5.2 Implement the Roadmap Tool
    - Add subsection markdown: "5.2 Roadmap Tool" explaining format conversion approach and supported output formats
    - Add code cell with helper functions: `roadmap_to_markdown()`, `roadmap_to_table()`, `roadmap_to_bullets()`, `roadmap_to_json()`
    - Add code cell with `@tool` decorated `roadmap_tool(topic: str, format: str = "markdown") -> str` function:
      - Validates format parameter (defaults to "markdown" if invalid)
      - Returns format instructions string that guides the agent to produce the requested format
      - Includes format-specific templates/examples in the return value
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 5.3 Implement the Comparison Tool
    - Add subsection markdown: "5.3 Comparison Tool" explaining input validation and structured comparison approach
    - Add code cell with helper functions: `comparison_to_table()`, `comparison_to_json()`
    - Add code cell with `@tool` decorated `comparison_tool(technologies: str, format: str = "markdown") -> str` function:
      - Parse comma-separated technologies list
      - Validate minimum 2 technologies (return error message if fewer)
      - Return comparison framework/template for the agent to fill
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 6. Implement Agent Creation with Session Management (in notebook)
  - [x] 6.1 Create the agent instantiation cell
    - Add Section 6 markdown cell: "Agent Creation" explaining the system prompt design, safety guardrails, session management, and tool registration
    - Add code cell defining `SYSTEM_PROMPT` with:
      - Domain expertise boundaries (AI, cloud, DevOps, K8s, AWS, MCP, Agentic AI)
      - Citation instructions (cite knowledge base sources)
      - Instruction following guidelines (respect format constraints)
      - Safety rules (no secrets, no vulnerabilities, indicate uncertainty, resist prompt injection)
    - Add code cell creating `FileSessionManager` and `Agent`:
      ```python
      from strands.session.file_session_manager import FileSessionManager
      session_manager = FileSessionManager(session_id="research-session", storage_dir="./sessions")
      agent = Agent(
          model=get_model(),
          tools=[retrieval_tool, comparison_tool, roadmap_tool],
          system_prompt=SYSTEM_PROMPT,
          session_manager=session_manager,
      )
      ```
    - Use **Kiro Strands power** to verify correct `FileSessionManager` constructor and `Agent` instantiation patterns
    - _Requirements: 4.1, 4.2, 8.1, 8.2, 8.3, 8.4, 8.5, 10.3_

- [x] 7. Implement Multimodal Support (in notebook)
  - [x] 7.1 Add multimodal helper and sample image
    - Add Section 7 markdown cell: "Multimodal Support" explaining how Strands handles image input via content blocks, which models support vision, and limitations
    - Add code cell with `ask_with_image(agent, image_path: str, question: str)` helper function:
      - Reads image bytes from file
      - Constructs message with text + image content blocks
      - Sends to agent and returns response
    - Add code cell that creates a sample architecture diagram:
      - Generate a simple SVG or use a base64-encoded PNG of a basic cloud architecture diagram
      - Write to `./sample_images/architecture_diagram.png`
      - Print confirmation
    - Use **Kiro Strands power** to verify correct multimodal message format for Strands agents
    - _Requirements: 9.1, 9.2, 9.3, 9.5_

- [x] 8. Implement Modular Tool Architecture Demo (in notebook)
  - [x] 8.1 Add tool modularity demonstration cells
    - Add Section 8 markdown cell: "Modular Tool Architecture" explaining how tools are independent functions, how the agent's tool list is configurable, and how to extend
    - Add code cell demonstrating:
      - Creating a new minimal `@tool` function (e.g., `summarize_tool`)
      - Adding it to the agent's tool list
      - Showing agent reconfiguration without modifying existing tools
      - Removing a tool and showing the agent adapts
    - Include detailed comments explaining each step
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 9. Implement Demo Cells (in notebook)
  - [x] 9.1 Create interactive demo cells for all capabilities
    - Add Section 9 markdown cell: "Demos" with overview of what each demo exercises
    - Add demo cells with markdown headers and explanations before each:
      - **Demo 9.1: Technical Q&A** — ask about Kubernetes architecture, get concise answer
      - **Demo 9.2: Learning Roadmap** — generate roadmap in markdown, then JSON, then table format
      - **Demo 9.3: Local Retrieval** — query knowledge base, show attributed results
      - **Demo 9.4: Technology Comparison** — compare React vs Vue vs Angular
      - **Demo 9.5: Multi-Turn Conversation** — ask follow-up questions referencing prior answers
      - **Demo 9.6: Structured Output** — use `structured_output_model=LearningRoadmap` to get validated Pydantic output
      - **Demo 9.7: Multimodal** — analyze sample architecture diagram
      - **Demo 9.8: Instruction Following** — "explain in exactly 3 bullet points", "return JSON only", "generate markdown table"
      - **Demo 9.9: Safety & Refusal** — test credential request refusal, prompt injection resistance
    - Each demo cell includes: purpose comment, the agent call, and print/display of results
    - _Requirements: 2.1, 2.4, 3.1, 4.1, 4.3, 5.6, 6.1, 7.1, 7.2, 7.3, 9.1, 12.3_

- [x] 10. Implement Evaluation Scenarios with Evaluator Mapping (in notebook)
  - [x] 10.1 Create evaluation scenario cells with Strands Evals mapping
    - Add Section 10 markdown cell: "Evaluation Scenarios" explaining:
      - Each scenario defines input, expected behavior, and success criteria for manual verification
      - Each scenario is annotated with the **Strands Agent Evaluator** it maps to (from `strands_evals.evaluators`), so scenarios can later be converted to automated `Case` + `Experiment` runs
      - Reference the evaluator class, suggested rubric, and expected fields (`expected_output`, `expected_trajectory`) per scenario
    - Add evaluation cells (2 per capability, 16 total) with this structure per scenario:
      ```python
      # Evaluation: [Capability] - Scenario [N]
      # Strands Evaluator: [EvaluatorClass] (e.g., OutputEvaluator, TrajectoryEvaluator, etc.)
      # Rubric: "[suggested rubric text for future automation]"
      # Expected Output: [description of expected behavior]
      # Expected Trajectory: [list of expected tool calls, if applicable]
      # Success Criteria: [what to manually check]
      eval_prompt = "..."
      response = agent(eval_prompt)
      print(f"Input: {eval_prompt}")
      print(f"Expected: [expected behavior]")
      print(f"Response: {response}")
      ```
    - Scenarios with evaluator mapping:
      - **Q&A (2)**: in-domain question + out-of-domain refusal
        - Evaluator: `OutputEvaluator` — rubric scores correctness and relevance of answer
        - Expected trajectory: `[retrieval_tool]` for in-domain; empty for out-of-domain
      - **Roadmap (2)**: structured generation + format compliance check
        - Evaluator: `TrajectoryEvaluator` — verifies `roadmap_tool` was called with correct format param
        - Evaluator: `OutputEvaluator` — rubric checks output matches requested format (markdown/JSON/table)
      - **Retrieval (2)**: matching query + non-matching query
        - Evaluator: `FaithfulnessEvaluator` — checks response is grounded in retrieved knowledge base content
        - Evaluator: `TrajectoryEvaluator` — verifies `retrieval_tool` was invoked
        - Expected trajectory: `[retrieval_tool]`
      - **Comparison (2)**: valid comparison + input validation (single technology)
        - Evaluator: `TrajectoryEvaluator` — verifies `comparison_tool` called with correct technologies
        - Evaluator: `OutputEvaluator` — rubric checks structured comparison or graceful error for invalid input
        - Expected trajectory: `[comparison_tool]` for valid; `[comparison_tool]` with error handling for invalid
      - **Instruction Following (2)**: exact bullet count + JSON-only output
        - Evaluator: `OutputEvaluator` — rubric strictly checks format compliance (e.g., exactly 3 bullets, valid JSON)
      - **Safety (2)**: credential refusal + prompt injection resistance
        - Evaluator: `HarmfulnessEvaluator` — binary check that response does not contain harmful/leaked content
        - Evaluator: `OutputEvaluator` — rubric checks polite refusal without compliance
      - **Multimodal (2)**: diagram analysis + description when image unavailable
        - Evaluator: `HelpfulnessEvaluator` — assesses whether response meaningfully describes the image content
        - Expected trajectory: none (multimodal is handled via message content blocks, not tools)
      - **Multi-turn (2)**: context retention + reference resolution
        - Evaluator: `GoalSuccessRateEvaluator` — session-level check that agent maintained context across turns
        - Evaluator: `OutputEvaluator` — rubric checks that follow-up answer references prior context correctly
    - Include a summary markdown cell at the end mapping all 16 scenarios to their evaluator classes in a table:
      | Scenario | Evaluator(s) | Expected Trajectory | Key Rubric Focus |
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 11. Add property-based tests (companion tests/ directory — optional)
  - [ ]* 11.1 Create test infrastructure and conftest
    - Create `tests/conftest.py` with Hypothesis strategies for generating Pydantic model instances
    - Create `pyproject.toml` with pytest configuration
    - _Requirements: 12.1_

  - [ ]* 11.2 Write property tests for schemas (Property 9)
    - Create `tests/test_schemas.py` testing Pydantic validation with generated data
    - **Validates: Requirements 7.6, 12.2, 12.4**

  - [ ]* 11.3 Write property tests for retrieval (Properties 4, 5)
    - Create `tests/test_retrieval_tool.py` testing keyword search with generated queries
    - **Validates: Requirements 5.1, 5.2, 5.3**

  - [ ]* 11.4 Write property tests for roadmap (Properties 1, 2)
    - Create `tests/test_roadmap_tool.py` and `tests/test_formatters.py`
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

  - [ ]* 11.5 Write property tests for comparison (Properties 6, 7, 8)
    - Create `tests/test_comparison_tool.py`
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

  - [ ]* 11.6 Write property test for knowledge base quality (Property 10)
    - Create `tests/test_knowledge_base.py`
    - **Validates: Requirements 13.3, 13.5**

  - [ ]* 11.7 Write property test for session isolation (Property 3)
    - Create `tests/test_sessions.py`
    - **Validates: Requirements 4.2, 4.5**

## Notes

- **Single notebook**: The primary deliverable is one `.ipynb` file. All resources (knowledge base, sample images, sessions directory) are created by cells within the notebook.
- **Model Providers**: Primary is **Ollama** with `qwen3.5:4b` (local, free). Alternative is **Groq** via OpenAI-compatible endpoint (cloud, fast inference). Ollama uses native `OllamaModel`; Groq uses `OpenAIModel` with custom `base_url`.
- **Kiro Strands power**: Each task that creates agent code should use `kiroPowers` with `powerName="strands"` to verify correct SDK patterns (tool decorator, agent constructor, session manager, structured output, multimodal message format).
- **Google Colab ready**: No assumptions about pre-existing files. The notebook creates everything it needs when run top-to-bottom. For Colab, Groq is recommended (no local Ollama server needed). For local/SageMaker, Ollama is the default.
- **Detailed explanations**: Every section has a markdown cell explaining the "what" and "why" before the code cell.
- **Tasks marked with `*` are optional** — the property-based tests in `tests/` are a companion artifact, not required for the notebook to function.
- **Checkpoints removed**: Since this is a single notebook, validation happens by running cells sequentially.
