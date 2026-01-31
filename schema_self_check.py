"""
Manual sanity checks for the ClassificationOutput schema.

This script demonstrates how invalid LLM outputs are rejected
by the schema validation logic.

"""

from pydantic import ValidationError
from schemas import ClassificationOutput


def run_case(name: str, data: dict):
    print(f"\n=== Test case: {name} ===")
    print("Input:")
    print(data)

    try:
        result = ClassificationOutput(**data)
        print("❌ Unexpected success")
        print("Parsed result:", result)
    except ValidationError as e:
        print("✅ ValidationError caught as expected")
        print("Error details:")
        print(e)


def main():
    # Case 1: Invalid classification label
    run_case(
        "Invalid classification value",
        {
            "classification": "Medium",
            "reason": "This policy has some issues."
        }
    )

    # Case 2: Missing required field
    run_case(
        "Missing reason field",
        {
            "classification": "Weak"
        }
    )

    # Case 3: Reason too short
    run_case(
        "Reason too short",
        {
            "classification": "Strong",
            "reason": "Ok"
        }
    )

    # Case 4: Valid output (should pass)
    run_case(
        "Valid output",
        {
            "classification": "Weak",
            "reason": "Grants unrestricted access to all actions and resources."
        }
    )


if __name__ == "__main__":
    main()
