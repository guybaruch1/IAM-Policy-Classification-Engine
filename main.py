import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from llm_client import LLMClient
from classifier import PolicyClassifier
from prompt import build_prompt


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <policy.json>")
        sys.exit(1)

    # Load environment variables from .env
    load_dotenv()

    policy_path = Path(sys.argv[1])
    if not policy_path.exists():
        print(f"Policy file not found: {policy_path}")
        sys.exit(1)

    with open(policy_path, "r", encoding="utf-8") as f:
        policy = json.load(f)

    # Read configuration from environment (with safe defaults)
    model = os.getenv("HF_MODEL")
    api_token = os.getenv("HF_API_TOKEN")

    if not api_token:
        print("HF_API_TOKEN environment variable is required")
        sys.exit(1)

    # Create classifier pipeline
    llm = LLMClient(model=model, api_token=api_token)
    classifier = PolicyClassifier(llm)

    result = classifier.classify(policy)

    # Print result
    print(result.model_dump_json(indent=2))

    # Save output
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))


    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()