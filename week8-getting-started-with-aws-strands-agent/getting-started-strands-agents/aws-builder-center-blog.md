# Building Multi-Agent Systems with AWS Strands: Sequential and Parallel Workflows

## Introduction

AI agents are transforming how we build intelligent applications, but creating production-ready agents shouldn't require months of complex orchestration code. In this post, I'll show you how to build a practical multi-agent system using AWS Strands Agents SDK with two real-world workflow patterns: sequential content creation and parallel batch processing.

## What is AWS Strands Agents Framework?

[AWS Strands Agents](https://strandsagents.com/) is an open-source SDK that takes a **model-driven approach** to building AI agents. Instead of writing complex orchestration logic, you define just three components:

1. **Model** - The LLM that powers agent reasoning
2. **System Prompt** - Instructions that define agent behavior  
3. **Tools** - Functions the agent can invoke to accomplish tasks

Strands is already used in production by multiple AWS teams including Amazon Q Developer, AWS Glue, and VPC Reachability Analyzer. It's designed to scale from simple single-agent use cases to complex multi-agent orchestrations.

### Key Capabilities

- **Model-Agnostic**: Works with Amazon Bedrock, Anthropic, Groq, Ollama, OpenAI, and more through LiteLLM
- **Tool Integration**: Supports thousands of Model Context Protocol (MCP) servers and custom tools
- **Multi-Agent Orchestration**: Build swarms, hierarchies, and graph-based workflows
- **Production-Ready**: Built-in OpenTelemetry instrumentation for observability
- **Flexible Deployment**: Run locally, on AWS Lambda, ECS, EKS, or Amazon Bedrock AgentCore

## What Pain Points Does Strands Solve?

### The Problem with Traditional Agent Frameworks

When AWS teams started building AI agents in early 2023, they relied on complex agent framework libraries for scaffolding and orchestration. The challenges were significant:

- **Months to Production**: It took months of tuning to get agents production-ready
- **Framework Overhead**: Complex orchestration logic hindered leveraging newer model capabilities
- **Rigid Workflows**: Frameworks imposed structure that didn't match how modern LLMs work
- **Slow Iteration**: Improvements in LLMs didn't translate to faster agent development

### The Strands Solution

Modern LLMs have native tool-use and reasoning capabilities. Strands embraces this by:

- **Trusting the Model**: Let LLMs handle planning, reasoning, and tool selection autonomously
- **Minimal Boilerplate**: Define agents in just a few lines of code
- **Faster Time to Market**: Ship new agents in days and weeks instead of months
- **Model-Driven Autonomy**: Agents dynamically direct their own steps without rigid orchestration

As stated in the [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/):

> "We found that relying on the latest models' capabilities to drive agents significantly reduced our time to market and improved the end user experience, compared to building agents with complex orchestration logic."

## Architecture: Two Practical Workflows

This project demonstrates two fundamental orchestration patterns using Strands with Groq's fast inference.

### Components

**2 Specialized Agents:**
- **Research Agent** - Uses `llama-3.3-70b-versatile` for information gathering
- **Data Processor Agent** - Uses `llama-3.1-8b-instant` for data structuring

**2 Core Tools:**
- `web_search_tool` - Information gathering
- `get_content_tool` - Fetch content from URLs

### Pattern 1: Sequential Content Creation Workflow

**Use Case**: Research reports, documentation generation, knowledge base building

```
Input: Topic
   │
   ▼
┌──────────────────┐
│  Research Agent  │  ← llama-3.3-70b-versatile
│                  │  ← Tools: web_search, get_content
└────────┬─────────┘
         │ Findings
         ▼
┌──────────────────┐
│ Data Processor   │  ← llama-3.1-8b-instant
│     Agent        │  ← Structures to JSON/CSV
└────────┬─────────┘
         │ Structured Data
         ▼
┌──────────────────┐
│ Direct File I/O  │  ← Python os/open/write
└────────┬─────────┘
         │
         ▼
Output: raw_research.txt
        processed_data.json
        content_document.md
```

**Benefits:**
- Predictable execution flow with clear dependencies
- Quality control at each step
- Context propagation between agents
- Resource-efficient single-threaded execution

### Pattern 2: Parallel Batch Processing Workflow

**Use Case**: High-throughput data processing, bulk operations, distributed analysis

```
Input: Batch Tasks [5 tasks]
   │
   ▼
┌──────────────────────────────────┐
│ ThreadPoolExecutor (max_workers=3)│
└──────────────────────────────────┘
   │
   ├─────────┬─────────┬─────────┐
   ▼         ▼         ▼         │
Research  Research   Data       │
 Agent     Agent   Processor    │
(Task 0)  (Task 1)  (Task 2)    │
   │         │         │         ▼
   │         │         │    Direct File I/O
   │         │         │       (Task 3)
   │         │         │         │
   └─────────┴─────────┴─────────┘
                 │
                 ▼
          Data Processor
            (Task 4)
                 │
                 ▼
         Collect & Summarize
                 │
                 ▼
         batch_summary.json
```

**Benefits:**
- High throughput with concurrent execution
- Fault isolation (one failure doesn't stop others)
- Horizontal scalability
- Reduced overall execution time

## LiteLLM: The Universal Model Provider

### Why LiteLLM with Strands?

One of Strands' most powerful features is **model flexibility**. LiteLLM provides a unified interface to 100+ LLM providers, enabling:

1. **Provider Independence**: Switch between Groq, Bedrock, OpenAI, Anthropic without code changes
2. **Model Specialization**: Use different models for different agents based on task complexity
3. **Cost Optimization**: Mix expensive and cheap models strategically
4. **Easy Migration**: Test locally with Ollama, deploy with Amazon Bedrock

### Implementation with Groq

```python
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel

# Research Agent: Powerful model for complex reasoning
research_model = LiteLLMModel(
    model_id="groq/llama-3.3-70b-versatile",
    params={
        "api_key": os.getenv("GROQ_API_KEY"),
        "max_tokens": 4000,
        "temperature": 0.7
    }
)

# Data Processor: Fast, cost-effective model
processor_model = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant",
    params={
        "api_key": os.getenv("GROQ_API_KEY"),
        "max_tokens": 4000,
        "temperature": 0.7
    }
)

# Define tools
@tool
def web_search_tool(query: str) -> str:
    """Search the web for information"""
    return f"Search results for '{query}': Found relevant information..."

# Create agents
research_agent = Agent(
    model=research_model,
    system_prompt="You are a research specialist...",
    tools=[web_search_tool, get_content_tool]
)

data_processor_agent = Agent(
    model=processor_model,
    system_prompt="You are a data processing specialist...",
    tools=[]
)
```

### Why Groq?

**Groq** offers exceptional performance with their custom LPU (Language Processing Unit) architecture:

- **Speed**: 10x faster inference than traditional GPUs
- **Cost-Effective**: Competitive pricing for high-throughput workloads
- **Open Models**: Access to Llama 3.3 70B and Llama 3.1 8B
- **Tool Calling**: Native support for function calling

### Provider Flexibility Example

```python
# Switch from Groq to Amazon Bedrock - one line change
model = LiteLLMModel(
    model_id="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
    params={"aws_region": "us-east-1"}
)

# Or use OpenAI
model = LiteLLMModel(
    model_id="gpt-4",
    params={"api_key": os.getenv("OPENAI_API_KEY")}
)

# Or test locally with Ollama
model = LiteLLMModel(
    model_id="ollama/llama3.2",
    params={"api_base": "http://localhost:11434"}
)
```

This abstraction is crucial for production systems where you need to:
- A/B test different models
- Implement fallback strategies
- Optimize costs by routing tasks to appropriate models
- Comply with regional data requirements

## Try It Yourself

### Prerequisites

1. **Get Groq API Key** (free tier available)
   - Sign up at [console.groq.com](https://console.groq.com)
   - Create an API key

2. **Install Dependencies**
   ```bash
   pip install strands-agents[litellm] strands-agents-tools
   ```

3. **Configure Environment**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

### Run Sequential Workflow

```python
from sequential_workflow import content_creation_workflow

result = content_creation_workflow(
    topic="Serverless Architecture on AWS",
    output_dir="output"
)

print(f"Created files: {result['files_created']}")
```

### Run Parallel Workflow

```python
from parallel_workflow import batch_processing_workflow

tasks = [
    {"type": "research", "query": "AWS Lambda best practices"},
    {"type": "research", "query": "Container orchestration with ECS"},
    {"type": "data_processing", "operation": "structure_findings", 
     "findings": ["Microservices", "Event-driven"], "format": "json"}
]

result = batch_processing_workflow(tasks, "batch_output")

print(f"Completed {result['successful_tasks']}/{result['total_tasks']} tasks")
```

### Full Demo

```bash
# Clone the repository
git clone <your-repo-url>
cd getting-started-strands-agents

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "GROQ_API_KEY=your_key" > .env

# Run demo
python main.py
```

### Expected Output

**Sequential Workflow:**
- `output/research/raw_research.txt` - Raw research findings
- `output/structured_data/processed_data.json` - Structured data
- `output/final_content/content_document.md` - Final document

**Parallel Workflow:**
- `batch_output/research_results/` - Individual research results
- `batch_output/processed_data/` - Processed data files
- `batch_output/batch_summary.json` - Aggregated summary

### Deploy to AWS

For production deployment, consider:

**AWS Lambda (Serverless)**
```python
# Strands' lightweight footprint fits Lambda constraints
# Use provisioned concurrency for cold start optimization
```

**Amazon ECS/EKS (Containers)**
```python
# Best for long-running agents and complex workflows
# Full control over resources and scaling
```

**Amazon Bedrock AgentCore**
```python
# Managed runtime for Strands agents
# Built-in scaling and observability
```

## Conclusion

AWS Strands Agents SDK represents a fundamental shift in how we build AI agents. By embracing a model-driven approach, Strands eliminates months of complex orchestration code and lets you focus on what matters: defining agent behavior and tools.

### Key Takeaways

1. **Simplicity Scales**: Three components (model, prompt, tools) are enough for production agents
2. **Model-Driven Wins**: Modern LLMs handle reasoning and planning better than rigid frameworks
3. **Provider Flexibility**: LiteLLM + Strands gives you freedom to choose the best model for each task
4. **Patterns Matter**: Sequential for complex workflows, parallel for high throughput
5. **Production-Ready**: Built-in observability and AWS integration from day one

### What's Next?

- **Explore Multi-Agent Patterns**: Try swarms, hierarchies, and graph-based orchestration
- **Add Observability**: Integrate OpenTelemetry for production monitoring
- **Scale with AWS**: Deploy on Lambda, ECS, or Bedrock AgentCore
- **Join the Community**: Contribute to [Strands on GitHub](https://github.com/strands-agents)

The combination of Strands' simplicity, LiteLLM's flexibility, and Groq's speed creates a powerful foundation for building production AI agents. Whether you're creating content pipelines or batch processors, Strands provides the tools to go from prototype to production in days, not months.

Start building your multi-agent system today and experience the power of model-driven agent development.

---

## Resources

- **Strands Agents**: [strandsagents.com](https://strandsagents.com/)
- **GitHub**: [github.com/strands-agents](https://github.com/strands-agents)
- **AWS Blog**: [Introducing Strands Agents](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)
- **Groq Console**: [console.groq.com](https://console.groq.com)
- **LiteLLM Docs**: [docs.litellm.ai](https://docs.litellm.ai)

---

*Have questions or want to share your Strands agent implementation? Join the discussion in the comments below or connect with the Strands community on GitHub.*
