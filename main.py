import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from llm_client import LLMClient
from classifier import PolicyClassifier
from prompt import build_prompt
import logging
from logging_utils import setup_logging


# ========================
# Configuration
# ========================

LLM_PROVIDER = "huggingface"  # "huggingface" or "openai"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

PROVIDER_API_ENV = {
    "huggingface": "HF_API_TOKEN",
    "openai": "OPENAI_API_KEY",
}


def main():
    setup_logging()
    logging.info("Starting IAM Policy Classification")

    if len(sys.argv) < 2:
        logging.error("No policy file provided")
        sys.exit(1)

    load_dotenv()

    policy_path = Path(sys.argv[1])
    if not policy_path.exists():
        logging.error(f"Policy file not found: {policy_path}")
        sys.exit(1)

    with open(policy_path, "r", encoding="utf-8") as f:
        policy = json.load(f)

    logging.info(f"Loaded policy from {policy_path}")

    # Resolve API token by provider
    api_env_var = PROVIDER_API_ENV.get(LLM_PROVIDER)
    if not api_env_var:
        logging.error(f"Unsupported provider: {LLM_PROVIDER}")
        sys.exit(1)

    api_token = os.getenv(api_env_var)
    if not api_token:
        logging.error(f"Missing API key: environment variable {api_env_var} is not set")
        sys.exit(1)

    logging.info(
        f"Running classification with provider={LLM_PROVIDER}, model={MODEL_NAME}"
    )

    try:
        llm = LLMClient(
            provider=LLM_PROVIDER,
            model=MODEL_NAME,
            api_token=api_token,
        )

        classifier = PolicyClassifier(llm)
        result = classifier.classify(policy)

        logging.info("Classification completed successfully")

    except Exception as e:
        logging.error(f"Classification failed: {e}")
        sys.exit(1)

    # ===== Final output =====
    final_output = {
        "policy": policy,
        "classification": result.classification,
        "reason": result.reason,
    }

    print(json.dumps(final_output, indent=2))


if __name__ == "__main__":
    main()