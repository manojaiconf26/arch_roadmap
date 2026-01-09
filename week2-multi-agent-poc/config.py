# config.py
"""
Central configuration for LLM provider selection.
"""

# Select provider: "groq" or "bedrock"
LLM_PROVIDER = "groq"

# ---------- Groq ----------
GROQ_MODEL = "llama-3.1-8b-instant"

# ---------- Amazon Bedrock ----------
BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
BEDROCK_REGION = "us-east-1"

# ---------- Shared ----------
TEMPERATURE = 0.2
MAX_CRITIC_RETRIES = 3
