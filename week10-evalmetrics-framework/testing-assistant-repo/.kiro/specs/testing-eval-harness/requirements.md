# Requirements Document

## Introduction

The Testing Eval Harness is a separate project that evaluates the AI Software Testing Assistant agents (Phase 1) across multiple dimensions: agent output quality, operational performance, security, and deployment readiness. It uses the Strands Evals SDK, operational metrics via CloudWatch, quality metrics, promptfoo for functional and red-team testing, and Bedrock AgentCore for production deployment with runtime evaluations.

## Glossary

- **Phase 1 Agents**: The four agents from the AI Software Testing Assistant — RUA, TGEA, TVA, and EA — deployed as a sequential pipeline.
- **Strands Evals SDK**: A Python SDK for evaluating conversational agents using LLM-as-judge evaluators, simulators, and experiments.
- **Evaluator**: A component that assesses agent output quality by scoring responses against rubrics or criteria.
- **Simulator**: A component that generates realistic multi-turn conversations to test agents.
- **Experiment**: A test run that combines cases, a task function, and evaluators to produce evaluation reports.
- **Operational Metrics**: Quantitative measurements of agent performance including cost per request, latency, TTFT, TTLT, tokens per second, and error rates.
- **Quality Metrics**: LLM-judged assessments of agent output including faithfulness, helpfulness, relevance, and coherence.
- **Promptfoo**: An open-source tool for testing LLM applications with functional assertions and red-team attack generation.
- **Red Teaming**: Adversarial testing that attempts to make agents produce harmful, incorrect, or policy-violating outputs.
- **Bedrock AgentCore**: AWS managed runtime for deploying and scaling Strands agents with built-in observability.
- **AgentCore Runtime Evals**: Evaluation capabilities provided by the AgentCore platform for deployed agents.
- **CloudWatch**: AWS monitoring service used to publish and visualize custom operational metrics.
- **TTFT**: Time to First Token — how quickly a model begins generating a response.
- **TTLT**: Time to Last Token — total time to complete response generation.

## Requirements

### Requirement 1

**User Story:** As a QA engineer, I want to evaluate each Phase 1 agent's output quality using the Strands Evals SDK, so that I can measure helpfulness, faithfulness, and tool usage accuracy.

#### Acceptance Criteria

1. WHEN the eval harness runs against the RUA agent, THE eval harness SHALL use the HelpfulnessEvaluator and FaithfulnessEvaluator to score the structured requirement output.
2. WHEN the eval harness runs against the TGEA agent, THE eval harness SHALL use the HelpfulnessEvaluator, ToolSelectionEvaluator, and a custom OutputEvaluator to score test case quality.
3. WHEN the eval harness runs against the TVA agent, THE eval harness SHALL use the FaithfulnessEvaluator and a custom OutputEvaluator to score functional validation accuracy.
4. WHEN the eval harness runs a full pipeline session, THE eval harness SHALL use the GoalSuccessRateEvaluator and TrajectoryEvaluator to assess end-to-end goal achievement.
5. WHEN the eval harness completes an evaluation experiment, THE eval harness SHALL produce a structured report containing per-evaluator scores and reasoning for each agent.

### Requirement 2

**User Story:** As a developer, I want to track operational metrics for each agent invocation, so that I can monitor cost, latency, and throughput in production.

#### Acceptance Criteria

1. WHEN an agent is invoked, THE eval harness SHALL measure and record cost per request based on input and output token counts and model pricing.
2. WHEN an agent is invoked with streaming enabled, THE eval harness SHALL measure Time to First Token and Time to Last Token separately.
3. WHEN an agent is invoked, THE eval harness SHALL calculate tokens per second throughput for the response.
4. WHEN operational metrics are collected, THE eval harness SHALL publish custom metrics to Amazon CloudWatch with dimensions for agent name and model provider.
5. WHEN operational metrics are collected, THE eval harness SHALL record error rates and throttling events per agent.

### Requirement 3

**User Story:** As a QA engineer, I want to measure quality metrics for agent outputs, so that I can track faithfulness, relevance, and coherence over time.

#### Acceptance Criteria

1. WHEN the eval harness evaluates an agent response, THE eval harness SHALL compute a faithfulness score measuring factual accuracy relative to the input context.
2. WHEN the eval harness evaluates an agent response, THE eval harness SHALL compute a relevance score measuring how well the output addresses the input query.
3. WHEN the eval harness evaluates an agent response, THE eval harness SHALL compute a coherence score measuring logical consistency and readability of the output.
4. WHEN quality metrics are computed, THE eval harness SHALL store results in a structured format that supports trend analysis across evaluation runs.

### Requirement 4

**User Story:** As a security engineer, I want to run functional and red-team evaluations using promptfoo, so that I can verify agent correctness and identify vulnerabilities.

#### Acceptance Criteria

1. WHEN the eval harness runs promptfoo functional tests, THE eval harness SHALL execute assertion-based test cases that verify each agent produces expected output structures.
2. WHEN the eval harness runs promptfoo red-team tests, THE eval harness SHALL generate adversarial inputs including prompt injection, jailbreak attempts, and policy-violating content.
3. WHEN a red-team test identifies a vulnerability, THE eval harness SHALL record the attack type, input, agent response, and severity in the evaluation report.
4. WHEN promptfoo evaluations complete, THE eval harness SHALL produce a pass/fail summary with detailed results per test case.

### Requirement 5

**User Story:** As a developer, I want to deploy the Phase 1 agents to Bedrock AgentCore and run E2E validation, so that I can verify production readiness.

#### Acceptance Criteria

1. WHEN the agents are deployed to AgentCore, THE eval harness SHALL verify each agent is accessible via the AgentCore runtime API.
2. WHEN the agents are deployed to AgentCore, THE eval harness SHALL run the Strands Evals SDK evaluators against the deployed agents and compare results to local evaluation baselines.
3. WHEN the agents are deployed to AgentCore, THE eval harness SHALL run promptfoo functional and red-team tests against the deployed endpoints.
4. WHEN AgentCore runtime evals are available, THE eval harness SHALL execute AgentCore-native evaluation capabilities and include results in the evaluation report.
5. WHEN E2E validation completes, THE eval harness SHALL produce a deployment readiness report containing all evaluation results from strands evals, promptfoo, and agentcore runtime evals.
