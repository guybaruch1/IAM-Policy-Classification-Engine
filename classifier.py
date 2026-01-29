"""Policy classification pipeline that composes prompts, calls the LLM client,
and validates the structured output.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from prompt import build_prompt
from schemas import ClassificationOutput


def _extract_json(text: str) -> Dict[str, Any]:
    """Try to extract a JSON object from a text blob.

    This is tolerant to a model returning explanations around JSON.
    """
    text = text.strip()
    # quick attempt: find first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output")

    candidate = text[start : end + 1]
    return json.loads(candidate)


class PolicyClassifier:
    def __init__(self, llm_client):
        self.llm = llm_client

    def classify(self, policy: Dict[str, Any]) -> ClassificationOutput:
        prompt = build_prompt(policy)
        raw = self.llm.generate(prompt, max_tokens=300, temperature=0.0)

        # Parse JSON out of model output and validate
        try:
            parsed = _extract_json(raw)
        except Exception:
            # If extraction fails, raise a helpful error including raw output
            raise RuntimeError(f"Failed to parse JSON from model output: {raw}")

        # Validate structure with pydantic
        return ClassificationOutput.parse_obj(parsed)


__all__ = ["PolicyClassifier"]
