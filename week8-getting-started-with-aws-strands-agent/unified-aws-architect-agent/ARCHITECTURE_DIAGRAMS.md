# Use Case Architecture Diagram

**Use Case**: AWS Solutions Architect Agent helping users design cloud architectures with complete control framework.

---

## 🏗️ Complete Architecture

```mermaid
graph TB
    User["👤 User<br/>(Beginner/Expert)"] --> Query["Query: Design REST API"]
    
    Query --> Agent["🤖 AWS Architect Agent"]
    
    subgraph Control Hierarchy
        Agent --> L1["📝 Layer 1: System Prompt<br/>Role: AWS Solutions Architect"]
        L1 --> L2["🎯 Layer 2: Runtime Steering<br/>Verbosity | Risk | Priority | Depth"]
        L2 --> L3["🔍 Layer 3: Hooks<br/>Pre-Tool | Post-Tool | Pre-Response | Evaluation"]
        L3 --> L4["⚖️ Layer 4: Evaluation Gates<br/>Cost < $100 | Quality > 0.7"]
    end
    
    L4 --> Lifecycle["🔄 Lifecycle Manager"]
    
    subgraph 7 Lifecycle Stages
        Lifecycle --> S1["1️⃣ Input Handling"]
        S1 --> S2["2️⃣ Planning"]
        S2 --> S3["3️⃣ Tool Selection"]
        S3 --> S4["4️⃣ Tool Execution"]
        S4 --> S5["5️⃣ Evaluation"]
        S5 --> S6["6️⃣ Response Finalization"]
        S6 --> S7["7️⃣ Session Update"]
    end
    
    S4 --> Tools["🛠️ AWS Tools<br/>Docs | Pricing"]
    Tools --> LLM["🧠 Claude LLM"]
    LLM --> Tools
    
    S7 --> Session["💾 Session Manager<br/>User Profile | History | State"]
    
    S6 --> Response["✅ Final Response<br/>Architecture + Cost + Metrics"]
    Response --> User
    
    style Agent fill:#e1f5ff
    style Response fill:#c8e6c9
```

---

## 🔄 Execution Sequence

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Steering
    participant Hooks
    participant LLM
    participant Session
    
    User->>Agent: "Design REST API for mobile app"
    
    Note over Agent: 4-Layer Control Hierarchy
    Agent->>Steering: Get config (verbosity=detailed, risk=cost_optimized)
    
    Note over Agent: Stage 1-3: Input → Planning → Tool Selection
    
    Agent->>Hooks: Pre-Tool Hook
    Hooks->>Hooks: Validate AWS region
    Hooks-->>Agent: ✓ Validated
    
    Note over Agent: Stage 4: Tool Execution
    Agent->>LLM: Invoke with AWS tools
    LLM->>LLM: Call aws_docs + aws_pricing
    LLM-->>Agent: Results
    
    Agent->>Hooks: Post-Tool Hook
    Hooks->>Hooks: Normalize pricing data
    Hooks-->>Agent: ✓ Normalized
    
    Note over Agent: Stage 5: Evaluation
    Agent->>Hooks: Evaluation Hook
    Hooks->>Hooks: Cost: $50 < $100 ✓
    Hooks->>Hooks: Quality: 0.85 > 0.7 ✓
    Hooks-->>Agent: ✅ PASSED
    
    Note over Agent: Stage 6: Response Finalization
    Agent->>Hooks: Pre-Response Hook
    Hooks->>Hooks: Format for beginner (detailed)
    Hooks-->>Agent: ✓ Formatted
    
    Note over Agent: Stage 7: Session Update
    Agent->>Session: Update state (turn++, add history)
    Session-->>Agent: ✓ Updated
    
    Agent-->>User: "Use API Gateway + Lambda...<br/>Cost: $45-60/month"
```

---

## 📝 Example Scenarios

### Scenario 1: Beginner User (Cost-Sensitive)
```
Input: "Design REST API for mobile app"
Steering: verbosity=detailed, risk=cost_optimized
Output: Step-by-step explanation with cost breakdown
Result: API Gateway + Lambda, $45-60/month
```

### Scenario 2: Expert User (Performance-Focused)
```
Input: "Design serverless data pipeline with DynamoDB Streams"
Steering: verbosity=concise, risk=performance
Output: Technical architecture with service configs
Result: DynamoDB Streams → Lambda → EventBridge → Step Functions
```

---

## 🔗 Related Documentation

- **Architecture Details**: [README.md](README.md)
- **Implementation Guide**: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

---

**Note**: These diagrams use Mermaid syntax and will render automatically on GitHub, GitLab, and many markdown viewers.
