# LLM abstraction using Hugging Face Inference API.

"""LLM abstraction using Hugging Face Inference API.

This client expects an environment variable `HF_API_TOKEN` to be set.
It calls the HF Inference endpoint for a specified model and returns
the raw generated text.
"""
from __future__ import annotations

import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


class LLMClient:
    def __init__(self, model: str, api_token: str | None = None):
        self.model = model
        self.api_token = api_token or os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise RuntimeError("HF_API_TOKEN is required")

        self.client = InferenceClient(
            model=self.model,
            token=self.api_token
        )

    def generate(self, prompt: str, max_tokens: int = 300, temperature: float = 0.0) -> str:
        response = self.client.chat_completion(
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message["content"]