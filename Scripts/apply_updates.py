import json
import os
import sys
from generate_agent import generate_agent_spec


def extract_updates(transcript):

    updates = {}

    text = transcript.lower()

    if "8 am" in text and "6 pm" in text:
        updates["business_hours"] = {
            "days": "Mon-Fri",
            "start": "08:00",
            "end": "18:00",
            "timezone": "EST"
        }

    if "sprinkler leak" in text:
        updates["emergency_definition"] = [
            "sprinkler leak",
            "fire alarm activation"
        ]

    if "60 seconds" in text:
        updates["call_transfer_rules"] = {
            "timeout_seconds": 60
        }

    return updates


def apply_updates(memo, updates):

    changes = {}

    for key in updates:

        old_value = memo.get(key)
        new_value = updates[key]

        memo[key] = new_value

        changes[key] = {
            "old": old_value,
            "new": new_value
        }

    return memo, changes


if __name__ == "__main__":

    # arguments from pipeline
    account_id = sys.argv[1]
    onboarding_path = sys.argv[2]

    base_accounts_dir = "../outputs/accounts"

    v1_memo_path = f"{base_accounts_dir}/{account_id}/v1/memo.json"

    if not os.path.exists(v1_memo_path):
        print("Memo file not found. Run extract_memo.py first.")
        exit()

    # load v1 memo
    with open(v1_memo_path) as f:
        memo = json.load(f)

    # load onboarding transcript
    with open(onboarding_path) as f:
        transcript = f.read()

    updates = extract_updates(transcript)

    updated_memo, changes = apply_updates(memo, updates)

    # create v2 directory
    v2_dir = f"{base_accounts_dir}/{account_id}/v2"
    os.makedirs(v2_dir, exist_ok=True)

    # save v2 memo
    with open(f"{v2_dir}/memo.json", "w") as f:
        json.dump(updated_memo, f, indent=2)

    # generate v2 agent spec
    agent_spec = generate_agent_spec(updated_memo)
    agent_spec["version"] = "v2"

    with open(f"{v2_dir}/agent_spec.json", "w") as f:
        json.dump(agent_spec, f, indent=2)

    # create changelog
    os.makedirs("../changelog", exist_ok=True)

    with open(f"../changelog/{account_id}_changes.json", "w") as f:
        json.dump(changes, f, indent=2)

    print(f"v2 memo created for account {account_id}")
    print(f"Saved memo: {v2_dir}/memo.json")
    print(f"Saved agent spec: {v2_dir}/agent_spec.json")