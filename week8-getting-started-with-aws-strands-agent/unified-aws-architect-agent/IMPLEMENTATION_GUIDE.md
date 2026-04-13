# Implementation Guide: AWS Solutions Architect Agent

## Overview

This guide demonstrates building a production-ready AWS Solutions Architect Agent that showcases all 5 advanced Strands Agent topics in a unified, practical use case.

## Problem Statement

**Challenge**: Build an AI agent that provides AWS architecture recommendations while maintaining:
- Safety controls to prevent costly mistakes
- Adaptability to different user expertise levels
- Cost awareness and budget constraints
- Session continuity across conversations
- Quality gates before delivering recommendations

**Solution**: A layered control system combining lifecycle management, hooks, runtime steering, session state, and evaluation gates.

---

## Architecture Deep Dive

### Control Hierarchy (4 Layers)

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: SYSTEM PROMPT                                  │
│ - Defines agent role (AWS Solutions Architect)          │
│ - Sets base behavior and responsibilities               │
│ - Static foundation for agent persona                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: RUNTIME STEERING                               │
│ - Verbosity: concise/detailed/expert                    │
│ - Risk Tolerance: cost-optimized/balanced/performance   │
│ - Tool Priority: docs-first/pricing-first/balanced      │
│ - Planning Depth: quick/thorough/comprehensive          │
│ - Adjustable WITHOUT redeployment                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: HOOKS (Event-Driven Control)                   │
│ - Pre-Tool: Validate AWS regions, inspect arguments     │
│ - Post-Tool: Normalize pricing data, validate outputs   │
│ - Pre-Response: Format based on user expertise          │
│ - Evaluation: Quality scoring, cost threshold checks    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: EVALUATION GATES                               │
│ - Cost threshold enforcement                            │
│ - Quality score validation                              │
│ - Retry vs Finalize decision                            │
│ - Fallback behavior triggers                            │
└─────────────────────────────────────────────────────────┘
```

---

## Topic 1: Agent Lifecycle

### Explicit Lifecycle Stages

The agent processes every query through 7 distinct stages:

```python
class LifecycleStage(Enum):
    INPUT_HANDLING = "input_handling"           # Parse and validate input
    PLANNING = "planning"                       # Create execution plan
    TOOL_SELECTION = "tool_selection"           # Choose appropriate tools
    TOOL_EXECUTION = "tool_execution"           # Execute selected tools
    EVALUATION = "evaluation"                   # Score output quality
    RESPONSE_FINALIZATION = "response_finalization"  # Prepare final response
    SESSION_UPDATE = "session_update"           # Update session state
```

### Implementation

**File**: `core/lifecycle.py`

Key features:
- **LifecycleTracker**: Monitors stage execution with timing
- **LifecycleEvent**: Records stage metadata and duration
- **Explicit stage boundaries**: Clear start/end markers

**Usage in main agent**:
```python
# Stage 1: Input Handling
self.lifecycle.start_stage(LifecycleStage.INPUT_HANDLING, {"query": query})
parsed_query = self._handle_input(query)
self.lifecycle.end_stage({"parsed": True})

# Stage 2: Planning
self.lifecycle.start_stage(LifecycleStage.PLANNING)
plan = self._create_plan(parsed_query)
self.lifecycle.end_stage({"plan": plan})
```

**Output**:
```
============================================================
LIFECYCLE: INPUT_HANDLING - STARTED
============================================================
Metadata: {'query': 'Design a REST API...'}
LIFECYCLE: INPUT_HANDLING - COMPLETED (2.45ms)
Result: {'parsed': True}
============================================================
```

### Lab Mapping
- **Lab 1**: Basic agent creation and result examination
- **Custom**: Explicit lifecycle stage tracking

---

## Topic 2: Agent Hooks (First-Class Control Surface)

### Four Hook Types

#### 1. Pre-Tool Hook: Validation & Inspection

**File**: `hooks/agent_hooks.py` - `PreToolValidationHook`

**Purpose**: Inspect and modify tool arguments before execution

**Example**:
```python
class PreToolValidationHook(HookProvider):
    def validate_tool_call(self, event: BeforeToolInvocationEvent):
        tool_input = event.tool_use.get("input", {})
        
        # Validate AWS region
        if "region" in tool_input:
            if tool_input["region"] not in self.allowed_regions:
                tool_input["region"] = "us-east-1"  # Override to safe default
                self.blocked_count += 1
```

**Output**:
```
🔍 PRE-TOOL HOOK: Validating aws_pricing_tool
   Arguments: {'service': 'lambda', 'region': 'ap-south-1'}
   ⚠️  WARNING: Region ap-south-1 not in allowed list
   ✓ Modified to: us-east-1
   ✓ Validation passed
```

#### 2. Post-Tool Hook: Normalization & Validation

**Purpose**: Validate and normalize tool outputs

```python
class PostToolNormalizationHook(HookProvider):
    def normalize_output(self, event: AfterToolInvocationEvent):
        # Validate output structure
        # Normalize pricing formats
        # Attach metadata
```

#### 3. Pre-Response Hook: Formatting

**Purpose**: Adjust response formatting based on user context

```python
class PreResponseFormattingHook(HookProvider):
    def format_response(self, event: AfterInvocationEvent):
        # Format for verbosity level
        # Adjust technical depth
```

#### 4. Evaluation Hook: Quality Gates

**Purpose**: Score outputs and decide retry vs finalize

```python
class EvaluationGateHook(HookProvider):
    def evaluate_response(self, event: AfterInvocationEvent):
        estimated_cost = 50.0
        quality_score = 0.85
        
        if estimated_cost <= self.cost_threshold and quality_score >= self.quality_threshold:
            return {"passed": True}
        return {"passed": False}  # Trigger retry
```

**Output**:
```
⚖️  EVALUATION HOOK: Checking quality gates
   ✓ Cost: $50.00 (threshold: $100.00)
   ✓ Quality: 0.85 (threshold: 0.70)
   ✅ EVALUATION PASSED - Finalizing response
```

### Lab Mapping
- **Lab 3**: Hook implementation patterns
- **Custom**: Evaluation and pre-response hooks

---

## Topic 3: Runtime Steering

### Steering Parameters

**File**: `steering/steering_config.py`

Four dimensions of runtime control:

#### 1. Verbosity Level
```python
class VerbosityLevel(Enum):
    CONCISE = "concise"      # Brief, technical answers
    DETAILED = "detailed"    # Step-by-step explanations
    EXPERT = "expert"        # Advanced technical depth
```

**Impact**: Controls response detail and explanation depth

#### 2. Risk Tolerance
```python
class RiskTolerance(Enum):
    COST_OPTIMIZED = "cost_optimized"    # Minimize costs
    BALANCED = "balanced"                # Balance cost and performance
    PERFORMANCE = "performance"          # Maximize performance
```

**Impact**: Influences service selection and architecture recommendations

#### 3. Tool Priority
```python
class ToolPriority(Enum):
    DOCS_FIRST = "docs_first"        # Prioritize documentation
    PRICING_FIRST = "pricing_first"  # Prioritize pricing info
    BALANCED = "balanced"            # Equal priority
```

**Impact**: Determines tool invocation order

#### 4. Planning Depth
```python
class PlanningDepth(Enum):
    QUICK = "quick"              # Fast, simple plans
    THOROUGH = "thorough"        # Detailed analysis
    COMPREHENSIVE = "comprehensive"  # Exhaustive evaluation
```

**Impact**: Controls planning thoroughness

### Dynamic Adjustment

```python
# Update steering at runtime
agent.update_steering(
    verbosity="concise",
    risk_tolerance="performance",
    tool_priority="docs_first",
    planning_depth="quick"
)
```

**Output**:
```
🎯 STEERING UPDATED: {
    'verbosity': 'concise',
    'risk_tolerance': 'performance',
    'tool_priority': 'docs_first',
    'planning_depth': 'quick'
}
```

### Steering → Prompt Translation

Steering parameters are converted to prompt guidance:

```python
def to_prompt_guidance(self) -> str:
    guidance = []
    
    if self.verbosity == VerbosityLevel.CONCISE:
        guidance.append("Provide concise, technical responses without lengthy explanations.")
    
    if self.risk_tolerance == RiskTolerance.COST_OPTIMIZED:
        guidance.append("Prioritize cost-effective solutions. Always mention pricing implications.")
    
    return "\n".join(guidance)
```

### Lab Mapping
- **No existing lab** - Custom implementation based on experimental Strands steering feature
- Inspired by AWS documentation on model-driven approach

---

## Topic 4: Session Management

### Session State Structure

**File**: `sessions/session_state.py`

```python
@dataclass
class UserProfile:
    user_id: str
    expertise_level: str = "intermediate"  # beginner, intermediate, expert
    preferred_region: str = "us-east-1"
    cost_sensitivity: str = "balanced"     # low, balanced, high
    preferred_services: List[str] = None

@dataclass
class SessionState:
    session_id: str
    user_profile: UserProfile
    architecture_history: List[Dict[str, Any]]
    last_tool_used: str
    evaluation_history: List[Dict[str, Any]]
    turn_count: int
```

### Session Isolation

Each user gets isolated session state:

```python
# User Alice - Beginner, cost-sensitive
agent1 = AWSArchitectAgent(session_id="demo_001", user_id="alice")
agent1.session.update_profile(expertise_level="beginner", cost_sensitivity="high")

# User Bob - Expert, performance-focused
agent2 = AWSArchitectAgent(session_id="demo_002", user_id="bob")
agent2.session.update_profile(expertise_level="expert", cost_sensitivity="low")
```

### Multi-Turn Continuity

Session state persists across turns:

```python
def _update_session(self, query: str, response: str, evaluation: Dict[str, Any]):
    self.session.get_state().increment_turn()
    self.session.get_state().add_evaluation(evaluation)
    self.session.get_state().add_architecture({
        "query": query,
        "response": response[:100] + "..."
    })
```

### Session Context in Prompts

```python
def get_context_for_agent(self) -> str:
    profile = self.session_state.user_profile
    return f"""
User Context:
- Expertise Level: {profile.expertise_level}
- Preferred Region: {profile.preferred_region}
- Cost Sensitivity: {profile.cost_sensitivity}
- Turn Count: {self.session_state.turn_count}
"""
```

### Lab Mapping
- **Lab 5**: Session and conversation management
- **Custom**: User profile and architecture history tracking

---

## Topic 5: Internal Control Hierarchy

### Layered Control Demonstration

**File**: `main.py` - `AWSArchitectAgent` class

The control hierarchy is implemented through method composition:

```python
def _build_system_prompt(self) -> str:
    # Layer 1: Base system prompt (static)
    base_prompt = "You are an expert AWS Solutions Architect..."
    
    # Layer 2: Add steering guidance (dynamic)
    steering_guidance = self.steering.get_prompt_guidance()
    
    # Add session context
    session_context = self.session.get_context_for_agent()
    
    return base_prompt + "\n" + steering_guidance + "\n" + session_context
```

### Layer Interaction

1. **Prompt shapes** base behavior
2. **Steering adjusts** behavior dynamically
3. **Hooks enforce** validation rules
4. **Evaluation gates** final quality

### Override Mechanism

Higher layers can override lower layers:

```python
# Layer 2 (Steering) overrides Layer 1 (Prompt)
agent.update_steering(verbosity="concise")  # Changes prompt guidance

# Layer 3 (Hooks) can block Layer 2 decisions
# Pre-tool hook blocks invalid regions regardless of steering
```

### Audit Trail

```python
def print_control_hierarchy(self):
    print("Layer 1: SYSTEM PROMPT")
    print("  Role: AWS Solutions Architect")
    
    print("Layer 2: RUNTIME STEERING")
    print(f"  Config: {self.steering.get_config().to_dict()}")
    
    print("Layer 3: HOOKS")
    print(f"  Pre-Tool Validations: {self.pre_tool_hook.blocked_count}")
    
    print("Layer 4: EVALUATION GATES")
    print(f"  Cost Threshold: ${self.evaluation_hook.cost_threshold}")
```

### Lab Mapping
- **No existing lab** - Custom unified implementation
- Combines concepts from Labs 1, 3, 5

---

## Complete Integration Example

### Scenario 1: Beginner User

```python
agent = AWSArchitectAgent(session_id="demo_001", user_id="alice")

# Configure for beginner
agent.session.update_profile(
    expertise_level="beginner",
    cost_sensitivity="high"
)

agent.update_steering(
    verbosity="detailed",
    risk_tolerance="cost_optimized"
)

result = agent.process_query(
    "I need to build a REST API for my mobile app. What AWS services should I use?"
)
```

**Control Flow**:
1. **Layer 1 (Prompt)**: "You are an AWS Solutions Architect..."
2. **Layer 2 (Steering)**: "Provide detailed, step-by-step explanations. Prioritize cost-effective solutions."
3. **Layer 3 (Hooks)**: Validate regions, normalize pricing
4. **Layer 4 (Evaluation)**: Check cost < $100, quality > 0.7

**Output**:
```
Response: "For a mobile app REST API, I recommend starting with AWS Lambda and API Gateway...
[Detailed explanation with cost breakdown]
Estimated monthly cost: $45-60 for moderate traffic..."

Lifecycle Summary:
- Total Duration: 3,245ms
- Stages: 7
- Hooks Executed: 4
- Evaluation: PASSED
```

### Scenario 2: Expert User

```python
agent = AWSArchitectAgent(session_id="demo_002", user_id="bob")

agent.session.update_profile(
    expertise_level="expert",
    cost_sensitivity="low"
)

agent.update_steering(
    verbosity="concise",
    risk_tolerance="performance"
)

result = agent.process_query(
    "Design a serverless data processing pipeline with DynamoDB Streams"
)
```

**Output**:
```
Response: "Architecture: DynamoDB Streams → Lambda → EventBridge → Step Functions.
Use provisioned concurrency for Lambda, on-demand for DynamoDB.
Consider DLQ for failed events..."

[Concise, technical response without explanations]
```

---

## Key Takeaways

### 1. Lifecycle Visibility
- Explicit stages make debugging easier
- Timing metrics identify bottlenecks
- Clear separation of concerns

### 2. Hooks as Control Points
- Pre-tool: Prevent invalid operations
- Post-tool: Ensure data quality
- Evaluation: Enforce business rules

### 3. Runtime Steering
- Adjust behavior without redeployment
- User-specific customization
- A/B testing different strategies

### 4. Session Management
- User isolation prevents data leakage
- Context continuity improves UX
- History tracking enables learning

### 5. Control Hierarchy
- Layered approach provides flexibility
- Clear override semantics
- Audit trail for compliance

---

## Extending the Agent

### Add New Tools

```python
from strands_tools import tool

@tool
def aws_cost_calculator(service: str, usage: dict) -> dict:
    """Calculate AWS service costs"""
    # Implementation
    return {"monthly_cost": 45.0}

agent.agent.tools.append(aws_cost_calculator)
```

### Add Custom Hooks

```python
class SecurityValidationHook(HookProvider):
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(BeforeToolInvocationEvent, self.check_security)
    
    def check_security(self, event):
        # Validate security configurations
        pass
```

### Add Steering Dimensions

```python
class ComplianceLevel(Enum):
    STANDARD = "standard"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"

# Add to SteeringConfig
compliance: ComplianceLevel = ComplianceLevel.STANDARD
```

---

## Comparison with Course Labs

| Topic | Course Labs | This Implementation |
|-------|-------------|---------------------|
| **Lifecycle** | Lab 1 (basic) | Explicit 7-stage tracking |
| **Hooks** | Lab 3 (logging) | 4 hook types with validation |
| **Steering** | None | Complete runtime control |
| **Session** | Lab 5 (basic) | User profiles + history |
| **Hierarchy** | None | 4-layer unified system |

---

## Next Steps

1. **Add Real Tools**: Integrate AWS SDK for actual service queries
2. **Persistent Storage**: Use DynamoDB for session state
3. **Metrics Dashboard**: Visualize lifecycle and evaluation metrics
4. **Multi-Agent**: Add specialist agents for specific AWS services
5. **Evaluation Framework**: Implement LLM-as-judge for quality scoring

---

## Conclusion

This unified implementation demonstrates how all 5 advanced Strands Agent topics work together to create a production-ready system with:

- ✅ Clear lifecycle stages
- ✅ Comprehensive hook coverage
- ✅ Runtime behavioral control
- ✅ Session-scoped state
- ✅ Layered control hierarchy

The AWS Solutions Architect Agent serves as a practical template for building controlled, observable, and adaptable AI agents.
