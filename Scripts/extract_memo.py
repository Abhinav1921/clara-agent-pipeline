import json
import uuid
import os
from schema import empty_account_memo
import sys

def extract_account_data(transcript):

    memo = empty_account_memo()

    # generate unique account id
    memo["account_id"] = str(uuid.uuid4())[:8]

    text = transcript.lower()

    # rule based extraction
    if "sprinkler" in text:
        memo["services_supported"].append("sprinkler services")

    if "fire alarm" in text:
        memo["services_supported"].append("fire alarm maintenance")

    if "emergency" in text:
        memo["emergency_definition"].append("caller mentioned emergency scenario")

    # if nothing extracted
    if memo["services_supported"] == []:
        memo["questions_or_unknowns"].append(
            "services_supported not mentioned"
        )

    return memo


if __name__ == "__main__":

    transcript_path = sys.argv[1]

    with open(transcript_path, "r") as f:
        transcript = f.read()

    memo = extract_account_data(transcript)

    account_id = memo["account_id"]

    base_dir = f"../outputs/accounts/{account_id}/v1"
    os.makedirs(base_dir, exist_ok=True)

    memo_path = f"{base_dir}/memo.json"

    with open(memo_path, "w") as f:
        json.dump(memo, f, indent=2)

    # IMPORTANT: pipeline captures this
    print(account_id)