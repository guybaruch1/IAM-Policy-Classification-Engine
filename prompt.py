"""Prompt construction utilities for policy classification.

The prompt enforces a JSON-only output with strict labels and a concise reason.
"""
from __future__ import annotations

import json


def build_prompt(policy: dict) -> str:
  policy_text = json.dumps(policy, indent=2, ensure_ascii=False)

  # Few-shot examples to guide deterministic outputs and JSON-only responses.
  examples = [
    {
      "policy": {
        "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
      },
      "classification": "Weak",
      "reason": "Allows all S3 actions on all resources (wildcard action+resource), violates least privilege."
    },
    {
      "policy": {
        "Statement": [{"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["arn:aws:s3:::my-bucket/*"]}]
      },
      "classification": "Strong",
      "reason": "Restricts actions to specific read operations and scopes resource to a single bucket."
    },
  ]

  example_text = ""
  for ex in examples:
    example_text += f"Policy:\n{json.dumps(ex['policy'])}\n-> {json.dumps({'classification': ex['classification'], 'reason': ex['reason']})}\n\n"

  prompt = f"""
You are a cloud security analyst. Analyze the IAM policy and classify it STRICTLY as either "Weak" or "Strong".

Rules:
- Only return a single JSON object and nothing else.
- The object must match the schema: {{"classification": "Weak"|"Strong", "reason": "<concise explanation>"}}
- `classification` must be exactly "Weak" or "Strong" (case-sensitive).
- `reason` must be a short, security-focused justification (one sentence preferred).
- Use deterministic settings (temperature=0) and avoid speculation.

Examples (for style):
{example_text}

NOW ANALYZE THE FOLLOWING POLICY and return JSON only.

POLICY:
{policy_text}
""".strip()

  return prompt


__all__ = ["build_prompt"]
