# AI Testing Assistant

A multi-agent pipeline built on the Strands Agents SDK that reads software requirements, generates test cases, validates quality, and evaluates pipeline performance.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Model Provider Configuration

The app supports two model providers, controlled by the `MODEL_PROVIDER` environment variable.

### AWS Bedrock (default)

Ensure your AWS credentials are configured (`aws configure`, env vars, or IAM role). No additional setup needed.

### Groq (local development)

Set the following in your `.env` file or export them:

```
MODEL_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
```

## Usage

Run the pipeline with a requirements file:

```bash
python -m ai_testing_assistant path/to/requirements.txt
python -m ai_testing_assistant requirements/swag_labs_requirements.txt
```

Or pass raw requirement text directly:

```bash
python -m ai_testing_assistant "The system shall allow users to log in with email and password. The system shall send a confirmation email after registration."
```

The pipeline runs four agents sequentially:

1. **Requirement Understanding Agent (RUA)** — parses raw text into structured requirements
2. **Test Generation & Execution Agent (TGEA)** — generates and simulates test cases
3. **Test Validator Agent (TVA)** — validates parsing accuracy and test relevance
4. **Eval Agent (EA)** — analyzes pipeline metrics and recommends optimizations

Output is printed as formatted JSON containing structured requirements, test cases, validation report, eval report, and pipeline metrics.
