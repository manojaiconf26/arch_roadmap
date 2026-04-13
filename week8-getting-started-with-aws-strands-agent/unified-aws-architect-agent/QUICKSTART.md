# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
cd unified-aws-architect-agent
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

```bash
# Option 1: AWS CLI (Recommended)
aws configure

# Option 2: Environment Variables
cp .env.example .env
# Edit .env and add:
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
# AWS_REGION=us-east-1
```

### 3. Ensure Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access"
3. Request access to "Claude 3.5 Sonnet" if not already enabled

### 4. Run Demo

```bash
python main.py
```

## What You'll See

### Scenario 1: Beginner User
```
SCENARIO 1: BEGINNER USER - API DESIGN
================================================================================

CONTROL HIERARCHY
================================================================================
Layer 1: SYSTEM PROMPT
  Role: AWS Solutions Architect
  Status: Active

Layer 2: RUNTIME STEERING
  Config: {'verbosity': 'detailed', 'risk_tolerance': 'cost_optimized', ...}

Layer 3: HOOKS
  Pre-Tool Validations: 0
  Post-Tool Normalizations: 0
  Evaluations: 0

Layer 4: EVALUATION GATES
  Cost Threshold: $100.0
  Quality Threshold: 0.7
================================================================================

============================================================
LIFECYCLE: INPUT_HANDLING - STARTED
============================================================
LIFECYCLE: INPUT_HANDLING - COMPLETED (2.45ms)
============================================================

[... continues through all 7 lifecycle stages ...]

📝 RESPONSE:
[Detailed AWS architecture recommendation]

📊 LIFECYCLE SUMMARY:
Total Duration: 3245.67ms
Stages Executed: 7
```

## Understanding the Output

### 1. Control Hierarchy Display
Shows the 4 layers of control:
- **Layer 1**: System prompt (agent role)
- **Layer 2**: Runtime steering (current settings)
- **Layer 3**: Hooks (validation counts)
- **Layer 4**: Evaluation gates (thresholds)

### 2. Lifecycle Stages
Each stage shows:
- Stage name
- Start/end markers
- Duration in milliseconds
- Metadata

### 3. Hook Execution
Watch for these markers:
- 🔍 **PRE-TOOL HOOK**: Validation before tool execution
- 📊 **POST-TOOL HOOK**: Output normalization
- ✨ **PRE-RESPONSE HOOK**: Response formatting
- ⚖️ **EVALUATION HOOK**: Quality gates

### 4. Steering Updates
When steering changes:
```
🎯 STEERING UPDATED: {'verbosity': 'concise', 'risk_tolerance': 'performance'}
```

### 5. Session Updates
When session state changes:
```
👤 SESSION: Profile updated - {'expertise_level': 'expert'}
```

## Customizing Scenarios

### Change User Profile

```python
agent.session.update_profile(
    expertise_level="expert",      # beginner, intermediate, expert
    cost_sensitivity="low",        # low, balanced, high
    preferred_region="eu-west-1"
)
```

### Adjust Steering

```python
agent.update_steering(
    verbosity="concise",           # concise, detailed, expert
    risk_tolerance="performance",  # cost_optimized, balanced, performance
    tool_priority="docs_first",    # docs_first, pricing_first, balanced
    planning_depth="quick"         # quick, thorough, comprehensive
)
```

### Change Evaluation Thresholds

```python
agent.evaluation_hook.cost_threshold = 50.0      # Max cost in dollars
agent.evaluation_hook.quality_threshold = 0.8    # Min quality score (0-1)
```

## Testing Different Queries

### Cost-Sensitive Query
```python
agent.update_steering(risk_tolerance="cost_optimized")
result = agent.process_query(
    "Build a data pipeline under $100/month"
)
```

### Performance-Focused Query
```python
agent.update_steering(risk_tolerance="performance")
result = agent.process_query(
    "Design a high-throughput event processing system"
)
```

### Beginner-Friendly Query
```python
agent.update_steering(verbosity="detailed")
result = agent.process_query(
    "How do I deploy a simple website on AWS?"
)
```

## Exploring the Code

### 1. Start with `main.py`
- See complete integration
- Understand control flow
- Review scenario examples

### 2. Examine `core/lifecycle.py`
- Lifecycle stage definitions
- Event tracking
- Timing metrics

### 3. Review `hooks/agent_hooks.py`
- Four hook types
- Validation logic
- Evaluation gates

### 4. Study `steering/steering_config.py`
- Steering parameters
- Prompt guidance generation
- Runtime updates

### 5. Check `sessions/session_state.py`
- User profiles
- Session state structure
- Context management

## Common Issues

### API Key Error
```
ValueError: ANTHROPIC_API_KEY not found
```
**Solution**: Add your API key to `.env` file

### Import Error
```
ModuleNotFoundError: No module named 'strands'
```
**Solution**: Run `pip install -r requirements.txt`

### Hook Not Executing
**Check**: Hooks are registered in agent initialization
```python
hooks=[
    self.pre_tool_hook,
    self.post_tool_hook,
    self.pre_response_hook,
    self.evaluation_hook
]
```

## Next Steps

1. **Read IMPLEMENTATION_GUIDE.md** - Deep dive into each topic
2. **Modify scenarios** - Test different configurations
3. **Add custom hooks** - Implement your own validation logic
4. **Extend steering** - Add new behavioral dimensions
5. **Integrate real tools** - Connect to AWS APIs

## Learning Path

```
Day 1: Run demo, understand output
  ↓
Day 2: Read IMPLEMENTATION_GUIDE.md
  ↓
Day 3: Modify steering parameters
  ↓
Day 4: Create custom hooks
  ↓
Day 5: Build your own use case
```

## Support

- **Documentation**: See IMPLEMENTATION_GUIDE.md
- **Code Examples**: Check main.py scenarios
- **AWS Docs**: https://docs.aws.amazon.com/
- **Strands Docs**: https://strandsagents.com/

## Key Concepts Recap

| Concept | What It Does | Where to Find |
|---------|--------------|---------------|
| **Lifecycle** | Tracks agent execution stages | `core/lifecycle.py` |
| **Hooks** | Validates and controls behavior | `hooks/agent_hooks.py` |
| **Steering** | Adjusts behavior at runtime | `steering/steering_config.py` |
| **Session** | Manages user state | `sessions/session_state.py` |
| **Hierarchy** | Layers control mechanisms | `main.py` |

Happy learning! 🚀
