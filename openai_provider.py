from openai import OpenAI
from providers import LLMProvider


class OpenAIProvider:
    def __init__(self, model, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt, max_tokens, temperature):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
