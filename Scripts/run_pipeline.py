import os
import subprocess

demo_folder = "../dataset/demo_calls"
onboarding_folder = "../dataset/onboarding_calls"

demo_files = sorted(os.listdir(demo_folder))
onboarding_files = sorted(os.listdir(onboarding_folder))

print("Starting Clara batch pipeline...\n")

for demo_file, onboarding_file in zip(demo_files, onboarding_files):

    demo_path = os.path.join(demo_folder, demo_file)
    onboarding_path = os.path.join(onboarding_folder, onboarding_file)

    print(f"Processing account from {demo_file}")

    # Step 1 — Extract memo
    result = subprocess.run(
        ["python", "extract_memo.py", demo_path],
        capture_output=True,
        text=True
    )

    account_id = result.stdout.strip()

    if not account_id:
        print("Error: account_id not generated\n")
        continue

    print(f"Account created: {account_id}")

    # Step 2 — Generate v1 agent
    subprocess.run(["python", "generate_agent.py", account_id])

    # Step 3 — Apply onboarding updates
    subprocess.run(["python", "apply_updates.py", account_id, onboarding_path])

    print(f"Finished account {account_id}\n")

print("Batch pipeline completed.")