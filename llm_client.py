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