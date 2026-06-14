"""Model provider configuration for the AI Testing Assistant.

Selects between Ollama (local), LiteLLM (Groq), and BedrockModel based
on the MODEL_PROVIDER environment variable.
"""

import os

from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()

# Default Groq model. Override with GROQ_MODEL_ID env var.
# Use a model that supports structured outputs (response_format with json_schema)
# to avoid the tool-call streaming fallback which is unreliable on Groq.
# Supported: "groq/openai/gpt-oss-120b", "groq/openai/gpt-oss-20b"
DEFAULT_GROQ_MODEL = "groq/openai/gpt-oss-20b"

# Default Ollama model. Override with OLLAMA_MODEL_ID env var.
# Good local options: qwen3:8b, gemma4:e4b, llama3.1:8b
DEFAULT_OLLAMA_MODEL = "qwen3:8b"

# Default Ollama host. Override with OLLAMA_HOST env var.
DEFAULT_OLLAMA_HOST = "http://localhost:11434"


def get_model():
    """Return the configured model provider based on environment.

    Reads MODEL_PROVIDER env var (default: "bedrock").
    - "ollama": returns an OllamaModel for local inference (no API costs).
      Uses OLLAMA_MODEL_ID and OLLAMA_HOST env vars for configuration.
    - "groq": returns a LiteLLMModel configured with GROQ_API_KEY.
      Uses GROQ_MODEL_ID env var to override the default model.
    - "bedrock" (or unset): returns a BedrockModel with Claude Sonnet.
    """
    provider = os.environ.get("MODEL_PROVIDER", "bedrock")

    if provider == "ollama":
        from strands.models.ollama import OllamaModel

        model_id = os.environ.get("OLLAMA_MODEL_ID", DEFAULT_OLLAMA_MODEL)
        host = os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

        return OllamaModel(
            host=host,
            model_id=model_id,
            max_tokens=4096,
            temperature=0.3,
        )

    if provider == "groq":
        from strands.models.litellm import LiteLLMModel

        model_id = os.environ.get("GROQ_MODEL_ID", DEFAULT_GROQ_MODEL)

        return LiteLLMModel(
            client_args={"api_key": os.environ["GROQ_API_KEY"]},
            model_id=model_id,
            params={"max_tokens": 4096, "temperature": 0.3},
        )

    return BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.3,
    )
