import json
import sys

def main():
    policy_path = sys.argv[1]
    with open(policy_path) as f:
        policy = json.load(f)

    print("Loaded policy:")
    print(json.dumps(policy, indent=2))


if __name__ == "__main__":
    main()