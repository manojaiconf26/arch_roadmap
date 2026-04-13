# AWS Solutions Architect Agent: Complete Control Framework

A production-ready AI agent demonstrating the complete control hierarchy for AWS architecture recommendations.

## Problem Statement

Design an intelligent AWS Solutions Architect Agent that:
- Provides accurate, cost-effective architecture recommendations
- Adapts to user expertise levels (beginner/expert)
- Maintains safety controls to prevent costly mistakes
- Remembers user preferences across sessions
- Validates recommendations before delivery

## Architecture Overview

```
User Query
    ↓
┌─────────────────────────────────────────────┐
│         CONTROL HIERARCHY                    │
├─────────────────────────────────────────────┤
│ Layer 1: System Prompt (Architect Persona)  │
│ Layer 2: Runtime Steering (Verbosity/Risk)  │
│ Layer 3: Hooks (Validation Gates)           │
│ Layer 4: Evaluation (Quality/Cost Gates)    │
└─────────────────────────────────────────────┘
    ↓
Agent Lifecycle
    ↓
Response
```

## Topics Covered

### 1. Agent Lifecycle (Lab 1 + Custom)
- Input handling and parsing
- Planning and reasoning phase
- Tool selection logic
- Tool execution
- Evaluation gates
- Response finalization
- Session state update

### 2. Agent Hooks (Lab 3 + Custom)
- **Pre-Tool Hook**: Validate AWS service availability, inspect arguments
- **Post-Tool Hook**: Normalize pricing data, validate outputs
- **Pre-Response Hook**: Format based on user expertise level
- **Evaluation Hook**: Cost threshold checks, quality scoring

### 3. Runtime Steering (Custom)
- **Verbosity Levels**: concise/detailed/expert
- **Risk Tolerance**: cost-optimized/balanced/performance
- **Tool Prioritization**: docs-first/pricing-first/balanced
- **Planning Depth**: quick/thorough/comprehensive

### 4. Session Management (Lab 5)
- User ID tracking
- Preferred AWS region
- Expertise level
- Architecture history
- Cost preferences
- Multi-turn context

### 5. Control Hierarchy (Unified)
- Layered control demonstration
- Clear separation of concerns
- Override mechanisms
- Audit trail

## Project Structure

```
unified-aws-architect-agent/
├── core/
│   ├── agent.py              # Main agent with lifecycle
│   └── lifecycle.py          # Explicit lifecycle stages
├── hooks/
│   ├── pre_tool_hooks.py     # Service validation, argument inspection
│   ├── post_tool_hooks.py    # Output normalization, validation
│   ├── pre_response_hooks.py # Formatting adjustments
│   └── evaluation_hooks.py   # Quality and cost gates
├── steering/
│   ├── steering_config.py    # Runtime steering parameters
│   └── steering_manager.py   # Dynamic behavior adjustment
├── evaluation/
│   ├── evaluator.py          # Quality and cost evaluation
│   └── gates.py              # Decision gates (retry/finalize)
├── tools/
│   ├── aws_docs_tool.py      # AWS documentation search
│   └── aws_pricing_tool.py   # AWS pricing calculator
├── sessions/
│   └── session_state.py      # Session management
├── main.py                   # Complete demo
├── requirements.txt
└── .env.example
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
# OR set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# Run complete demo
python main.py
```

## Example Scenarios

### Scenario 1: Beginner User
```
User: "I need to build an API for my mobile app"

Steering: verbosity=detailed, risk=cost-optimized
Output: Step-by-step explanation with cost estimates
```

### Scenario 2: Expert User
```
User: "Design a serverless API with DynamoDB"

Steering: verbosity=concise, risk=performance
Output: Technical architecture with service configurations
```

### Scenario 3: Cost-Sensitive
```
User: "Build a data pipeline under $100/month"

Steering: risk=cost-optimized, tool_priority=pricing-first
Evaluation: Cost gate blocks recommendations over budget
```

## Key Features

- ✅ Explicit lifecycle stages with tracing
- ✅ Four-layer control hierarchy
- ✅ Runtime steering without redeployment
- ✅ Session-scoped state management
- ✅ Quality and cost evaluation gates
- ✅ AWS service validation
- ✅ Multi-turn conversation support
- ✅ Audit trail for all decisions

## Metrics & Observability

- Lifecycle stage timing
- Hook execution counts
- Steering parameter changes
- Evaluation gate decisions
- Tool usage patterns
- Session state evolution

## Learning Path

1. Start with `main.py` - See complete integration
2. Explore `core/lifecycle.py` - Understand agent flow
3. Review `hooks/` - See control points
4. Examine `steering/` - Runtime adjustments
5. Study `evaluation/` - Quality gates
6. Test scenarios - Hands-on learning
