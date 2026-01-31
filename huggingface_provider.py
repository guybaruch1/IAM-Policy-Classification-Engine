from huggingface_hub import InferenceClient
from providers import LLMProvider


class HuggingFaceProvider:
    def __init__(self, model, api_token):
        self.client = InferenceClient(model=model, token=api_token)

    def generate(self, prompt, max_tokens, temperature):
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message["content"]
