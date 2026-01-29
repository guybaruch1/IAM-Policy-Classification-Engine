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


# class LLMClient:
# 	def __init__(self, model: Optional[str] = None, api_token: Optional[str] = None, timeout: int = 30):
# 		self.model = model or os.getenv("HF_MODEL", "gpt2")
# 		self.api_token = api_token or os.getenv("HF_API_TOKEN")
# 		if not self.api_token:
# 			raise RuntimeError("HF_API_TOKEN environment variable is required")
# 		self.endpoint = f"https://api-inference.huggingface.co/models/{self.model}"
# 		self.timeout = timeout

# 	def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.0, retries: int = 2) -> str:
# 		headers = {"Authorization": f"Bearer {self.api_token}", "Accept": "application/json"}
# 		payload = {
# 			"inputs": prompt,
# 			"parameters": {"max_new_tokens": max_tokens, "temperature": temperature},
# 		}

# 		for attempt in range(retries + 1):
# 			resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=self.timeout)
# 			if resp.status_code == 200:
# 				try:
# 					data = resp.json()
# 				except ValueError:
# 					return resp.text

# 				# Hugging Face may return a list of outputs or a dict with "generated_text"
# 				if isinstance(data, list):
# 					texts = []
# 					for item in data:
# 						if isinstance(item, dict) and "generated_text" in item:
# 							texts.append(item["generated_text"])
# 						elif isinstance(item, str):
# 							texts.append(item)
# 					return "\n".join(texts)

# 				if isinstance(data, dict):
# 					if "error" in data:
# 						raise RuntimeError(f"Model error: {data['error']}")
# 					if "generated_text" in data:
# 						return data["generated_text"]
# 					return str(data)

# 				return str(data)

# 			# Retry on rate-limit / transient server errors
# 			if resp.status_code in (429, 503) and attempt < retries:
# 				time.sleep(1 + attempt * 2)
# 				continue

# 			raise RuntimeError(f"HF request failed: {resp.status_code} {resp.text}")


# __all__ = ["LLMClient"]

class LLMClient:
    def __init__(self, model_name: str):
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            raise RuntimeError("HUGGINGFACE_TOKEN is not set")

        self.client = InferenceClient(
            model=model_name,
            token=token
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.0
        )

        return response.choices[0].message["content"]