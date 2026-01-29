import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from llm_client import LLMClient
from classifier import PolicyClassifier
from prompt import build_prompt


def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python main.py <policy.json>")
    #     sys.exit(2)

    # load_dotenv()

    # policy_path = Path(sys.argv[1])
    # if not policy_path.exists():
    #     print(f"Policy file not found: {policy_path}")
    #     sys.exit(2)

    # with open(policy_path, "r", encoding="utf-8") as fh:
    #     policy = json.load(fh)

    # # Create LLM client from env
    # model = os.getenv("HF_MODEL")
    # client = LLMClient(model=model)
    # classifier = PolicyClassifier(client)

    # result = classifier.classify(policy)

    # out_dir = Path("outputs")
    # out_dir.mkdir(exist_ok=True)
    # out_path = out_dir / "result.json"
    # with open(out_path, "w", encoding="utf-8") as fh:
    #     fh.write(result.json(indent=2))

    # print("Classification result:")
    # print(result.json(indent=2))
    # print(f"Saved to: {out_path}")

    policy_path = sys.argv[1]
    with open(policy_path) as f:
        policy = json.load(f)

    prompt = build_prompt(json.dumps(policy))

    llm = LLMClient("meta-llama/Meta-Llama-3-8B-Instruct")

    result = llm.generate(prompt)

    print(result)

if __name__ == "__main__":
    main()