Clara AI Agent Automation Pipeline
Overview

This project implements an automated pipeline that converts demo and onboarding call transcripts into structured configurations for an AI phone agent. The system simulates how Clara automatically creates and updates AI receptionist agents using information gathered from customer calls.

The pipeline extracts business information from transcripts, generates an AI agent configuration, applies updates from onboarding calls, and maintains version history of the agent configuration.

Additionally, the pipeline is integrated with an automation workflow using n8n, which exposes a webhook endpoint that can trigger the automation process.



Problem Statement

Businesses often provide configuration information for AI phone agents during demo and onboarding calls. Converting these conversations into structured configurations manually can be time-consuming and error-prone.

This project automates that process by:

Extracting relevant information from transcripts

Generating AI agent configuration files

Applying updates after onboarding

Maintaining version control of configurations

Triggering the automation workflow using n8n





System Architecture

The automation pipeline follows this workflow:

Transcript Input
       │
       ▼
Memo Extraction
       │
       ▼
Agent Specification Generation
       │
       ▼
Onboarding Updates
       │
       ▼
Versioning (v1 → v2)
       │
       ▼
Changelog Generation
       │
       ▼
Automation Trigger via n8n





Project Structure:


Clara_Agent_pipeline
├── dataset
│   ├── demo_calls
│   └── onboarding_calls
│
├── scripts
│   ├── extract_memo.py
│   ├── generate_agent.py
│   ├── apply_updates.py
│   ├── run_pipeline.py
│   └── schema.py
│
├── outputs
│   └── accounts
│       └── <account_id>
│           ├── v1
│           │   ├── memo.json
│           │   └── agent_spec.json
│           └── v2
│               ├── memo.json
│               └── agent_spec.json
│
├── changelog
│   └── <account_id>_changes.json
│
├── workflows
│   └── n8n_workflow.json
    └── workflow_diagram.png
│
└── README.md




Workflow Explanation
Step 1 — Demo Call Processing

Demo call transcripts contain basic business information such as:

services offered

emergency definitions

customer interaction details

The script extract_memo.py processes the transcript and generates a structured memo.



Step 2 — Agent Configuration Generation

The script generate_agent.py converts the extracted memo into an AI agent configuration.

This configuration includes:

system prompt

business hours

routing instructions

transfer behavior


Step 3 — Onboarding Updates

During onboarding calls, customers may update configuration details such as:

business hours

emergency definitions

call routing rules

The script apply_updates.py reads onboarding transcripts and applies these updates.

Step 4 — Versioning


After applying updates, a new version of the configuration is created.

memo.json (v2)
agent_spec.json (v2)

This ensures configuration changes are tracked across versions.

Step 5 — Changelog Generation

All updates applied during onboarding are recorded in a changelog.

Example:

changelog/<account_id>_changes.json

This file tracks the differences between v1 and v2 configurations.



Step 6 — Batch Pipeline Execution

The script run_pipeline.py processes multiple transcripts automatically.

Example:

python run_pipeline.py

The pipeline will process all demo and onboarding transcripts and generate configurations for multiple accounts.


n8n Workflow Automation

The project includes an automation workflow using n8n.

The workflow exposes a webhook endpoint that can trigger the automation pipeline.

Webhook endpoint:

POST /run-pipeline

Example trigger:

Invoke-WebRequest -Uri "http://localhost:5678/webhook-test/run-pipeline" -Method POST

This webhook can be used to trigger the pipeline automatically from external systems.

Technologies Used

Python

JSON

n8n (workflow automation)

Rule-based text extraction


Key Features

Automated transcript parsing

Structured memo generation

AI agent configuration creation

Version control for configuration updates

Changelog tracking

Batch processing of transcripts

Workflow orchestration using n8n

Limitations

The extraction process is rule-based rather than using a large language model.

The dataset used in this project contains simulated transcripts.

The AI agent configuration is simplified for demonstration purposes.

Future Improvements

Possible improvements for this system include:

Integrating speech-to-text for real call recordings

Using LLMs for richer information extraction

Adding a monitoring dashboard for agent configurations

Integrating directly with telephony APIs