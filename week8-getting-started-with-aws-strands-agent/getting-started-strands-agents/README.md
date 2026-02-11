# Strands Agents Multi-Agent System

A simplified multi-agent system built with AWS Strands Agents SDK, demonstrating both sequential and parallel execution patterns using Groq API.

## Prerequisites

### Get Groq API Key
1. Sign up for a free account at [Groq Console](https://console.groq.com)
2. Navigate to API Keys section
3. Create a new API key
4. Copy the API key for configuration

## Architecture

### 2 Specialized Agents
1. **Research Agent** - Uses `llama-3.3-70b-versatile` for web search and information gathering
2. **Data Processor Agent** - Uses `llama-3.1-8b-instant` for parsing and transforming data

### 2 Core Tools
1. **Web Search** - Information gathering and content retrieval
2. **Get Content** - Fetch content from URLs

## Use Cases

### Sequential Execution: Content Creation Workflow
**Flow**: Research → Data Processing → File Output

```
Research Agent → Data Processor Agent → Direct File Operations
```

**Steps**:
1. Research Agent gathers information on a topic
2. Data Processor Agent structures the findings
3. Direct file operations save organized documentation

**Use Case**: Comprehensive content generation, report creation, knowledge base building

### Parallel Execution: Batch Processing Workflow
**Flow**: Multiple agents working simultaneously

```
Research Agent (Task 1) ┐
Research Agent (Task 2) ├─→ Concurrent Execution
Data Processor (Task 3) ┘
```

**Steps**:
1. Multiple agents process different tasks concurrently
2. ThreadPoolExecutor manages parallel execution
3. Results are collected and summarized

**Use Case**: High-throughput data processing, bulk operations, distributed analysis

## Files Structure

```
strands-agents/
├── research_agent.py          # Research specialist agent
├── data_processor_agent.py    # Data processing agent
├── sequential_workflow.py     # Content creation workflow
├── parallel_workflow.py       # Batch processing workflow
├── main.py                    # Demo script
├── .env                       # Environment configuration (create from .env.example)
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Or copy from example:
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

## Usage

### Run Demo
```bash
python main.py
```

### Sequential Workflow
```python
from sequential_workflow import content_creation_workflow

result = content_creation_workflow("AI in Healthcare", "output_dir")
```

### Parallel Workflow
```python
from parallel_workflow import batch_processing_workflow

tasks = [
    {"type": "research", "query": "Cloud Computing"},
    {"type": "data_processing", "operation": "structure_findings", "findings": [...]}
]

result = batch_processing_workflow(tasks, "batch_output")
```

## Key Features

- **Strands Agents SDK**: Model-driven approach with tool integration
- **Groq Integration**: Fast inference with llama models
- **Concurrent Execution**: ThreadPoolExecutor for parallel processing
- **Tool Integration**: Seamless tool calling within agents
- **Error Handling**: Robust error management and recovery
- **Observability**: Built-in logging and result tracking

## Models Used

- **Research Agent**: `groq/llama-3.3-70b-versatile` (4000 max tokens)
- **Data Processor Agent**: `groq/llama-3.1-8b-instant` (4000 max tokens)

## Benefits

### Sequential Workflow
- **Predictable Flow**: Clear dependency chain
- **Quality Control**: Each step validates previous results
- **Resource Efficiency**: Single-threaded execution
- **Complex Tasks**: Handles multi-step processes well

### Parallel Workflow  
- **High Throughput**: Process multiple tasks simultaneously
- **Scalability**: Easily add more workers
- **Fault Tolerance**: Individual task failures don't stop others
- **Time Efficiency**: Reduced overall execution time

## Troubleshooting

### API Key Issues
- Ensure `.env` file exists in project root
- Verify `GROQ_API_KEY` is set correctly
- Check API key is valid at [Groq Console](https://console.groq.com)

### Tool Calling Errors
- Models are optimized for tool calling
- Large content is handled by direct file operations
- Check max_tokens settings if issues persist