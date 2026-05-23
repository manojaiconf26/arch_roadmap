# Requirements Document

## Introduction

This document defines the requirements for the AI Research & Learning Assistant — a local-first, evaluation-rich agent system delivered as a Jupyter notebook (Google Colab or SageMaker compatible). Built on the Strands Agents framework, the assistant provides technical Q&A, learning roadmap generation, multi-turn conversations, local retrieval, technology comparison, instruction following, basic safety handling, and lightweight multimodal support. The system is designed as a lightweight tool for learning, experimentation, and agent evaluation — not a production-scale enterprise platform.

## Glossary

- **Assistant**: The AI Research & Learning Assistant agent built using the Strands Agents framework
- **Notebook**: The Jupyter notebook artifact that contains all code, tools, demos, and evaluation scenarios
- **Strands_Agent**: An instance of the `Agent` class from the `strands-agents` SDK configured with a system prompt, tools, and model provider
- **Custom_Tool**: A Python function decorated with `@tool` from the Strands Agents SDK that extends agent capabilities
- **Knowledge_Base**: A collection of local markdown files used as the retrieval source for grounding agent responses
- **Session_Manager**: The `FileSessionManager` from Strands Agents that persists conversation state to local files
- **Structured_Output**: Agent responses formatted according to a Pydantic model schema using the `structured_output_model` parameter
- **Model_Provider**: The LLM backend (Amazon Bedrock, Anthropic, OpenAI, Gemini, or LlamaAPI) used by the agent
- **Retrieval_Tool**: A Custom_Tool that searches and retrieves relevant content from the Knowledge_Base
- **Comparison_Tool**: A Custom_Tool that generates structured comparisons between technologies
- **Roadmap_Tool**: A Custom_Tool that generates structured learning plans with phases, timelines, and milestones
- **User**: The person interacting with the Assistant through the Notebook
- **Turn**: A single user-input and agent-response exchange within a conversation
- **Evaluation_Scenario**: A predefined test case in the Notebook that exercises a specific agent capability

## Requirements

### Requirement 1: Notebook Structure and Setup

**User Story:** As a developer, I want a well-structured Jupyter notebook with clear setup instructions, so that I can run the assistant locally in Google Colab or SageMaker with minimal friction.

#### Acceptance Criteria

1. THE Notebook SHALL contain a setup cell that installs `strands-agents` and `strands-agents-tools` packages with pinned versions
2. THE Notebook SHALL contain a configuration cell that allows the User to select and configure a Model_Provider
3. THE Notebook SHALL organize cells into logical sections: setup, configuration, tool definitions, knowledge base, agent creation, demos, and evaluation scenarios
4. THE Notebook SHALL include inline markdown documentation explaining each section's purpose
5. THE Notebook SHALL execute end-to-end without errors when a valid Model_Provider is configured
6. THE Notebook SHALL use only lightweight dependencies that are compatible with both Google Colab and SageMaker notebook environments

### Requirement 2: Technical Q&A

**User Story:** As a learner, I want to ask technical questions about AI, cloud, architecture, DevOps, MCP, Agentic AI, AWS, and Kubernetes, so that I receive concise and accurate explanations.

#### Acceptance Criteria

1. WHEN the User asks a technical question, THE Assistant SHALL provide a concise explanation relevant to the topic
2. WHEN the User asks a question outside the supported technical domains, THE Assistant SHALL indicate that the topic is outside its area of expertise
3. THE Assistant SHALL ground responses in factual information and avoid speculative claims
4. WHEN the User asks a follow-up question in the same session, THE Assistant SHALL incorporate prior context from the conversation

### Requirement 3: Learning Roadmap Generation

**User Story:** As a learner, I want to generate structured learning plans for technical topics, so that I have a clear path with phases, timelines, milestones, and learning goals.

#### Acceptance Criteria

1. WHEN the User requests a learning roadmap, THE Roadmap_Tool SHALL generate a structured plan containing phases, timelines, milestones, and learning goals
2. WHEN the User specifies markdown format, THE Roadmap_Tool SHALL return the roadmap as formatted markdown with headers and bullet lists
3. WHEN the User specifies JSON format, THE Roadmap_Tool SHALL return the roadmap as a valid JSON object conforming to a defined Pydantic schema
4. WHEN the User specifies table format, THE Roadmap_Tool SHALL return the roadmap as a markdown table with columns for phase, timeline, milestone, and goals
5. WHEN the User specifies bullet list format, THE Roadmap_Tool SHALL return the roadmap as a hierarchical bullet list
6. IF the User provides an ambiguous or overly broad topic, THEN THE Assistant SHALL request clarification before generating the roadmap

### Requirement 4: Multi-Turn Conversation Support

**User Story:** As a user, I want to have multi-turn conversations with the assistant, so that I can refine questions, build on previous answers, and explore topics iteratively.

#### Acceptance Criteria

1. THE Strands_Agent SHALL maintain conversation context across multiple Turns within a session
2. THE Session_Manager SHALL persist conversation history to local files using `FileSessionManager`
3. WHEN the User references a previous response, THE Assistant SHALL resolve the reference using conversation history
4. WHEN the User requests modification of a previous response, THE Assistant SHALL generate a revised response incorporating the requested changes
5. WHEN a new session is started, THE Session_Manager SHALL create a new conversation context independent of previous sessions
6. IF the conversation history exceeds the model context window, THEN THE Assistant SHALL summarize earlier context to maintain coherence

### Requirement 5: Local Retrieval Tool

**User Story:** As a researcher, I want the assistant to retrieve information from my local markdown documents, so that responses are grounded in my own notes and reference materials.

#### Acceptance Criteria

1. THE Retrieval_Tool SHALL search local markdown files in the Knowledge_Base directory for content relevant to the User query
2. WHEN relevant content is found, THE Retrieval_Tool SHALL return the matching text passages with source file attribution
3. WHEN no relevant content is found, THE Retrieval_Tool SHALL indicate that no matching documents were found in the Knowledge_Base
4. THE Knowledge_Base SHALL include sample markdown documents covering AI, cloud architecture, and DevOps topics
5. THE Retrieval_Tool SHALL operate without external databases or vector stores, using local file-based search only
6. WHEN the Retrieval_Tool returns content, THE Assistant SHALL cite the source document in the response

### Requirement 6: Technology Comparison Tool

**User Story:** As a developer, I want to compare frameworks, tools, or technologies side by side, so that I can make informed decisions about which to adopt.

#### Acceptance Criteria

1. WHEN the User requests a technology comparison, THE Comparison_Tool SHALL generate a structured comparison summary
2. THE Comparison_Tool SHALL include categories such as strengths, weaknesses, use cases, and ecosystem maturity for each compared technology
3. WHEN the User specifies a table format, THE Comparison_Tool SHALL return the comparison as a markdown table
4. WHEN the User specifies JSON format, THE Comparison_Tool SHALL return the comparison as a valid JSON object
5. IF the User provides fewer than two technologies to compare, THEN THE Comparison_Tool SHALL request at least two items for comparison

### Requirement 7: Instruction Following

**User Story:** As a user, I want the assistant to reliably follow formatting and constraint instructions, so that I receive responses in the exact format and style I specify.

#### Acceptance Criteria

1. WHEN the User specifies a bullet point count (e.g., "exactly 3 bullet points"), THE Assistant SHALL return a response with exactly that number of bullet points
2. WHEN the User requests JSON-only output, THE Assistant SHALL return only valid JSON without additional prose
3. WHEN the User requests a markdown table, THE Assistant SHALL return a properly formatted markdown table
4. WHEN the User requests a concise response, THE Assistant SHALL limit the response to three sentences or fewer
5. WHEN the User requests a beginner-friendly explanation, THE Assistant SHALL avoid jargon and use simple language with analogies
6. THE Structured_Output SHALL use Pydantic models to enforce response schemas when structured output is requested

### Requirement 8: Basic Safety and Refusal Handling

**User Story:** As a user, I want the assistant to refuse unsafe or inappropriate requests, so that I am protected from harmful guidance, hallucinated information, and credential exposure.

#### Acceptance Criteria

1. WHEN the User requests secrets, credentials, API keys, or passwords, THE Assistant SHALL refuse the request and explain why
2. WHEN the User requests guidance that could cause security vulnerabilities or system damage, THE Assistant SHALL refuse and suggest a safe alternative
3. WHEN the User asks a question the Assistant cannot answer with confidence, THE Assistant SHALL indicate uncertainty rather than generating hallucinated information
4. WHEN the User submits a malicious prompt injection attempt, THE Assistant SHALL refuse to comply and maintain normal operation
5. THE Assistant SHALL include a system prompt with safety guardrails that define refusal boundaries

### Requirement 9: Lightweight Multimodal Support

**User Story:** As a learner, I want to provide architecture diagrams, screenshots, or flowcharts to the assistant, so that it can summarize visual content and explain high-level workflows.

#### Acceptance Criteria

1. WHEN the User provides an image of an architecture diagram, THE Assistant SHALL identify and list the major components depicted
2. WHEN the User provides an image of a flowchart, THE Assistant SHALL describe the high-level workflow steps
3. WHEN the User provides a screenshot, THE Assistant SHALL summarize the visible content and context
4. IF the provided image is unreadable or too low resolution, THEN THE Assistant SHALL indicate that the image quality is insufficient for analysis
5. THE Notebook SHALL include at least one sample architecture diagram for demonstrating multimodal capabilities

### Requirement 10: Modular Tool Architecture

**User Story:** As a developer, I want the tools to be modular and reusable, so that I can extend the assistant with new capabilities without modifying existing code.

#### Acceptance Criteria

1. THE Notebook SHALL define each Custom_Tool as an independent Python function decorated with `@tool`
2. THE Custom_Tool definitions SHALL include descriptive docstrings that the Strands_Agent uses for tool selection
3. THE Strands_Agent SHALL be instantiated with a configurable list of tools passed via the `tools` parameter
4. WHEN a new Custom_Tool is added to the tools list, THE Strands_Agent SHALL incorporate the tool without changes to existing tool definitions
5. THE Notebook SHALL demonstrate adding and removing tools from the agent configuration

### Requirement 11: Evaluation Scenarios

**User Story:** As a developer, I want predefined evaluation scenarios in the notebook, so that I can systematically test agent capabilities across Q&A, retrieval, instruction following, safety, and multimodal tasks.

#### Acceptance Criteria

1. THE Notebook SHALL include at least two Evaluation_Scenarios for each major capability: Q&A, roadmap generation, multi-turn conversation, retrieval, comparison, instruction following, safety, and multimodal
2. EACH Evaluation_Scenario SHALL define an input prompt, expected behavior description, and success criteria
3. THE Notebook SHALL organize Evaluation_Scenarios in a dedicated section after the demo cells
4. THE Evaluation_Scenarios SHALL be executable as standard notebook cells producing observable outputs
5. WHEN an Evaluation_Scenario is executed, THE Notebook SHALL display the agent response alongside the expected behavior for manual comparison

### Requirement 12: Structured Output Support

**User Story:** As a developer, I want the assistant to produce structured outputs using Pydantic models, so that I can programmatically consume and validate agent responses.

#### Acceptance Criteria

1. THE Notebook SHALL define Pydantic models for roadmap, comparison, and Q&A response schemas
2. WHEN the Strands_Agent is configured with a `structured_output_model`, THE Assistant SHALL return responses conforming to the specified Pydantic schema
3. THE Notebook SHALL demonstrate switching between free-form and structured output modes
4. IF the agent response does not conform to the specified schema, THEN THE Notebook SHALL display a validation error with details

### Requirement 13: Sample Knowledge Base

**User Story:** As a user, I want sample local documents included in the notebook, so that I can immediately test retrieval capabilities without creating my own content.

#### Acceptance Criteria

1. THE Notebook SHALL include at least five sample markdown documents covering distinct technical topics
2. THE sample documents SHALL cover topics including: AI fundamentals, cloud architecture patterns, Kubernetes basics, DevOps practices, and AWS services
3. EACH sample document SHALL contain at least 200 words of substantive technical content
4. THE Notebook SHALL include a cell that creates the Knowledge_Base directory and writes sample documents to local storage
5. THE sample documents SHALL use consistent markdown formatting with headers, lists, and code blocks where appropriate
