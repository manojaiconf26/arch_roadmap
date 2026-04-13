"""Model provider configuration for the AI Testing Assistant.

Selects between LiteLLM (Groq) and BedrockModel based on the
MODEL_PROVIDER environment variable.
"""

import os

from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()


def get_model():
    """Return the configured model provider based on environment.

    Reads MODEL_PROVIDER env var (default: "bedrock").
    - "groq": returns a LiteLLMModel configured with GROQ_API_KEY.
    - "bedrock" (or unset): returns a BedrockModel with Claude Sonnet.
    """
    provider = os.environ.get("MODEL_PROVIDER", "bedrock")

    if provider == "groq":
        from strands.models.litellm import LiteLLMModel

        return LiteLLMModel(
            client_args={"api_key": os.environ["GROQ_API_KEY"]},
            model_id="groq/llama-3.3-70b-versatile",
            params={"max_tokens": 4096, "temperature": 0.3},
        )

    return BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.3,
    )
