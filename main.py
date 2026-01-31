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




    
#     setup_logging()
#     logging.info("Starting IAM Policy Classification")

#     # Models to evaluate
#     models = [
#     {
#         "provider": "huggingface",
#         "model": "meta-llama/Meta-Llama-3-8B-Instruct",
#         "env": "HF_API_TOKEN",
#     },
#     {
#         "provider": "openai",
#         "model": "gpt-3.5-turbo",
#         "env": "OPENAI_API_KEY",
#     },
# ]

#     if len(sys.argv) < 2:
#         logging.error("No policy file provided")
#         sys.exit(1)

#     # Load environment variables from .env
#     load_dotenv()

#     policy_path = Path(sys.argv[1])
#     if not policy_path.exists():
#         logging.error(f"Policy file not found: {policy_path}")
#         sys.exit(1)

#     with open(policy_path, "r", encoding="utf-8") as f:
#         policy = json.load(f)
    
#     logging.info(f"Loaded policy from {policy_path}")

#     results = []
#     api_token = os.getenv("HF_API_TOKEN")

#     results = []

#     for cfg in models:
#         provider = cfg["provider"]
#         model_name = cfg["model"]
#         env_var = cfg["env"]

#         logging.info(
#             f"Running classification with provider={provider}, model={model_name}"
#         )

#         api_token = os.getenv(env_var)
#         if not api_token:
#             error_msg = f"Missing API key: environment variable {env_var} is not set"
#             logging.error(error_msg)
#             results.append({
#                 "provider": provider,
#                 "model": model_name,
#                 "error": error_msg,
#             })
#             continue

#         try:
#             llm = LLMClient(
#                 provider=provider,
#                 model=model_name,
#                 api_token=api_token,
#             )

#             classifier = PolicyClassifier(llm)
#             result = classifier.classify(policy)

#             logging.info(
#                 f"Model {model_name} ({provider}) completed successfully"
#             )

#             results.append({
#                 "provider": provider,
#                 "model": model_name,
#                 "classification": result.classification,
#                 "reason": result.reason,
#             })

#         except Exception as e:
#             logging.error(
#                 f"Model {model_name} ({provider}) failed: {e}"
#             )
#             results.append({
#                 "provider": provider,
#                 "model": model_name,
#                 "error": str(e),
#             })


#     final_output = {
#         "policy": policy,
#         "results": results,
#     }

#     print(json.dumps(final_output, indent=2))

    # for model_name in models:
    #     logging.info(f"Running classification with model: {model_name}")

    #     try:
    #         llm = LLMClient(model=model_name, api_token=api_token)
    #         classifier = PolicyClassifier(llm)

    #         result = classifier.classify(policy)

    #         logging.info(f"Model {model_name} completed successfully")

    #         results.append({
    #             "model": model_name,
    #             "classification": result.classification,
    #             "reason": result.reason,
    #         })

    #     except Exception as e:
    #         logging.error(f"Model {model_name} failed: {e}")
    #         results.append({
    #             "model": model_name,
    #             "error": str(e),
    #         })
    
    # final_output = {
    #     "policy": policy,
    #     "results": results,
    # }

    # print(json.dumps(final_output, indent=2))



    # # Read configuration from environment (with safe defaults)
    # model = os.getenv("HF_MODEL")
    # api_token = os.getenv("HF_API_TOKEN")

    # if not api_token:
    #     logging.error("HF_API_TOKEN is not set")
    #     sys.exit(1)

    # logging.info(f"Using model: {model}")

    # # Create classifier pipeline
    # llm = LLMClient(model=model, api_token=api_token)
    # classifier = PolicyClassifier(llm)

    # try:
    #     logging.info("Running classification")
    #     result = classifier.classify(policy)
    #     logging.info("Classification completed successfully")
    # except Exception as e:
    #     logging.error(f"Classification failed: {e}")
    #     sys.exit(1)

    # final_output = {
    # "policy": policy,
    # "classification": result.classification,
    # "reason": result.reason,
    # }

    # # Print result
    # print(json.dumps(final_output, indent=2))

    # # Save output
    # out_dir = Path("outputs")
    # out_dir.mkdir(exist_ok=True)
    # out_path = out_dir / "result.json"
    # with open(out_path, "w", encoding="utf-8") as f:
    #     json.dump(final_output, f, indent=2)

    # print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()