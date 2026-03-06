import json
import os
import sys

def generate_prompt(memo):

    hours = memo["business_hours"]

    prompt = f"""
You are Clara, the AI receptionist for {memo['company_name']}.

BUSINESS HOURS:
{hours['days']} {hours['start']} - {hours['end']} {hours['timezone']}

BUSINESS HOURS FLOW:
1. Greet the caller professionally
2. Ask the purpose of the call
3. Collect the caller's name and phone number
4. Route or transfer the call according to the request
5. If transfer fails apologize and assure follow up
6. Ask if the caller needs anything else
7. Close the call politely

AFTER HOURS FLOW:
1. Greet the caller
2. Ask purpose of call
3. Confirm whether the issue is an emergency
4. If emergency collect:
   - name
   - phone number
   - address
5. Attempt emergency transfer
6. If transfer fails apologize and assure quick follow up
7. Ask if they need anything else
8. Close the call politely
"""

    return prompt


def generate_agent_spec(memo):

    agent_spec = {
        "agent_name": memo["company_name"] + " AI Receptionist",
        "voice_style": "professional",
        "version": "v1",
        "system_prompt": generate_prompt(memo),
        "variables": {
            "timezone": memo["business_hours"]["timezone"],
            "business_hours": memo["business_hours"],
            "office_address": memo["office_address"]
        },
        "call_transfer_protocol": "Attempt transfer based on routing rules",
        "transfer_failure_protocol": "Apologize and log the request for follow up"
    }

    return agent_spec


if __name__ == "__main__":

    account_id = sys.argv[1]

    memo_path = f"../outputs/accounts/{account_id}/v1/memo.json"

    if not os.path.exists(memo_path):
        print("Memo file not found. Run extract_memo.py first.")
        exit()

    with open(memo_path) as f:
        memo = json.load(f)

    agent_spec = generate_agent_spec(memo)

    agent_path = f"../outputs/accounts/{account_id}/v1/agent_spec.json"

    with open(agent_path, "w") as f:
        json.dump(agent_spec, f, indent=2)

    print(f"Agent spec generated for account {account_id}")