# prompt engineering

def build_prompt(policy_json: str) -> str:
    return f"""
You are a cloud security analyst specializing in IAM policy risk assessment.

Your task is to analyze the following IAM policy and classify it strictly as either "Weak" or "Strong".

Classification guidelines:

A policy should be classified as "Weak" if one or more of the following apply:
- Uses wildcard actions (e.g., "*", "s3:*") without strong restrictions
- Uses wildcard resources ("*") without scoping
- Grants excessive permissions beyond least privilege
- Lacks security conditions such as Multi-Factor Authentication (MFA)
- Allows broad administrative actions without constraints

A policy should be classified as "Strong" if:
- Permissions follow the principle of least privilege
- Actions are specific and narrowly scoped
- Resources are explicitly defined
- Strong security conditions are enforced (e.g., MFA, IP restrictions)
- Access is limited to well-defined use cases

You must return a valid JSON object with the following structure and nothing else:

{{
  "classification": "Weak" | "Strong",
  "reason": "<concise security-focused explanation>"
}}

Do not include markdown, code blocks, or additional commentary.

IAM Policy to analyze:
{policy_json}
""".strip()
