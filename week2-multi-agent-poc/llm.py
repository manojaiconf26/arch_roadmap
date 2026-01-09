# llm.py
"""
LLM abstraction layer.
All agents must go through this file.
"""

import json
import boto3
from groq import Groq
import os
from dotenv import load_dotenv

from config import (
    LLM_PROVIDER,
    GROQ_MODEL,
    BEDROCK_MODEL,
    BEDROCK_REGION,
    TEMPERATURE
)

# ---------- Clients ----------
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=BEDROCK_REGION
)

# ---------- Public Interface ----------
def call_llm(system_prompt: str, user_prompt: str) -> str:
    if LLM_PROVIDER == "groq":
        return _call_groq(system_prompt, user_prompt)
    elif LLM_PROVIDER == "bedrock":
        return _call_bedrock(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")

# ---------- Provider Implementations ----------
def _call_groq(system_prompt: str, user_prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def _call_bedrock(system_prompt: str, user_prompt: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": TEMPERATURE,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}]
            }
        ]
    }

    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL,
        body=json.dumps(body)
    )

    payload = json.loads(response["body"].read())
    return payload["content"][0]["text"].strip()
