"""
Evaluation script for IAM Policy Classification.

Runs multiple LLMs on a labeled dataset of IAM policies
and reports accuracy per model.
"""

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from logging_utils import setup_logging
from llm_client import LLMClient
from classifier import PolicyClassifier

# logging.getLogger("httpx").setLevel(logging.WARNING)


DATASET_PATH = Path("policies/labeled_policies.json")
OUTPUT_PATH = Path("outputs/evaluation_results.json")


MODELS = [
    {
        "provider": "huggingface",
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "env": "HF_API_TOKEN",
    },
    {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "env": "OPENAI_API_KEY",
    },
]


def load_dataset(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_model(model_cfg, dataset):
    provider = model_cfg["provider"]
    model_name = model_cfg["model"]
    env_var = model_cfg["env"]

    api_token = os.getenv(env_var)
    if not api_token:
        raise RuntimeError(f"Missing API key: {env_var}")

    llm = LLMClient(
        provider=provider,
        model=model_name,
        api_token=api_token,
    )
    classifier = PolicyClassifier(llm)

    correct = 0
    total = len(dataset)
    failures = 0

    for idx, sample in enumerate(dataset, start=1):
        policy = sample["policy"]
        label = sample["label"]

        try:
            result = classifier.classify(policy)
            prediction = result.classification

            if prediction == label:
                correct += 1

        except Exception as e:
            logging.error(
                f"[{provider}:{model_name}] Failed on sample {idx}: {e}"
            )
            failures += 1

    accuracy = correct / total if total > 0 else 0.0

    return {
        "provider": provider,
        "model": model_name,
        "accuracy": round(accuracy * 100, 2),
        "total_samples": total,
        "correct_predictions": correct,
        "failures": failures,
    }


def main():
    setup_logging()
    load_dotenv()

    logging.info("Starting evaluation")

    dataset = load_dataset(DATASET_PATH)
    logging.info(f"Loaded dataset with {len(dataset)} samples")

    results = []

    for model_cfg in MODELS:
        provider = model_cfg["provider"]
        model_name = model_cfg["model"]

        logging.info(
            f"Evaluating provider={provider}, model={model_name}"
        )

        try:
            metrics = evaluate_model(model_cfg, dataset)
            results.append(metrics)

            logging.info(
                f"Completed evaluation for {model_name} "
                f"(accuracy={metrics['accuracy']}%)"
            )

        except Exception as e:
            logging.error(
                f"Evaluation failed for {model_name}: {e}"
            )
            results.append({
                "provider": provider,
                "model": model_name,
                "error": str(e),
            })

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nEvaluation Results:")
    print(json.dumps(results, indent=2))
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
