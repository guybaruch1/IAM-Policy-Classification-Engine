from huggingface_provider import HuggingFaceProvider
from openai_provider import OpenAIProvider


class LLMClient:
    def __init__(self, provider, model, api_token):
        if provider == "huggingface":
            self.provider = HuggingFaceProvider(model, api_token)
        elif provider == "openai":
            self.provider = OpenAIProvider(model, api_token)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def generate(self, prompt: str,max_tokens: int = 512,temperature: float = 0.0) -> str:
        return self.provider.generate(prompt=prompt, max_tokens=max_tokens, temperature=temperature)





# # LLM abstraction using Hugging Face Inference API.

# """LLM abstraction using Hugging Face Inference API.

# This client expects an environment variable `HF_API_TOKEN` to be set.
# It calls the HF Inference endpoint for a specified model and returns
# the raw generated text.
# """
# from __future__ import annotations

# import os
# import time
# import requests
# from typing import Optional
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()


# class LLMClient:
#     def __init__(self, model: str, api_token: str):
#         self.model = model
#         self.api_token = api_token
#         if not self.api_token:
#             raise RuntimeError("API_TOKEN is required")

#         self.client = InferenceClient(model=self.model, token=self.api_token)

#     def generate(self, prompt: str, max_tokens: int = 300, temperature: float = 0.0) -> str:
#         try:
#             response = self.client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=temperature,
#                 max_tokens=max_tokens,
#             )
#             return response.choices[0].message["content"]
#         except Exception:
#             # fallback to text generation
#             output = self.client.text_generation(
#                 prompt,
#                 temperature=temperature,
#                 max_new_tokens=max_tokens,
#             )
#             return output
        
#         # response = self.client.chat_completion(
#         #     messages=[
#         #         {"role": "user", "content": prompt}
#         #     ],
#         #     max_tokens=max_tokens,
#         #     temperature=temperature
#         # )
#         # return response.choices[0].message["content"]