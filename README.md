# Fitness Concierge: Personalized Planning Agent powered by Google ADK and Gemini

## Overview

Fitness Concierge is a personalized end-to-end fitness planning agent built with Google's Agent Development Kit (ADK) that leverages the power of Gemini. This multi-agent system seeks to understand an individual's goals and experiences by coordinating specialized agents for meal and workout plans. It uses MCP tools for nutrition data, and exposes interactive evaluation and deployment utilities.

---

## Architecture 🔧

- **Root agent (Coordinator)**: Receptionist orchestrating the fitness planning journey.
- **Workout agent**: Creates initial training program.
- **Workout reviser agent**: Iteratively revises training program.
- **Meal agent**: Creates initial meal plan and uses MCP tools for food lookups.
- **Meal reviser agent**: Iteratively revises meal plan.

---

## Getting Started

### Prerequisites ⚙️

- Python >= 3.12
- Node.js + npm (for MCP server build and dataset conversion)
- [uv](https://docs.astral.sh/uv/) package manager
- Google API Key from [Google AI Studio](https://aistudio.google.com/app/api-keys)
- (Optional) [GCP](https://console.cloud.google.com/welcome/new) account for deployment via Vertex AI Agent Engine

### Setup 📥

```bash
# Clone the repo
git clone <repo-url>
cd fitness_concierge

# Create and activate virtual environment
uv venv
source .venv/bin/active

# Install dependencies
uv sync
```

### Setup the MCP nutrition server and dataset:

```bash
bash scripts/setup_mcp_opennutrition.sh
```

This will clone/build the `mcp-opennutrition` microservice and prepare local food data.

### Environment Variables

```bash
# API Key
GOOGLE_API_KEY=your_google_api_key

# Google Cloud Console
GOOGLE_CLOUD_LOCATION=your_google_cloud_location
GOOGLE_CLOUD_PROJECT=your_google_cloud_project

# Required for Vertex AI deployment (1 to activate)
GOOGLE_GENAI_USE_VERTEXAI=0
```

---

## Running with ADK Web Interface 🌐

```bash
adk web src
```

Open the URL shown in the terminal and select `fitness_agent` to start.

_Tip: For local CLI interaction, use the provided script:_

```bash
uv run scripts/run_with_plugins.py
```

---

## Project Structure 📁

```
fitness_concierge/
├── src/
│   └── fitness_agent/
│       ├── agent.py               # Root fitness concierge agent
│       ├── sub_agents/            # ADK-compatible agent definitions
│       │   ├── meal/              # Meal planning and revision
│       │   └── workout/           # Workout planning and revision
│       ├── infra/                 # Infrastructure / integrations
│       ├── app.py                 # ADK / web app entrypoint
│       └── config.py              # Configuration definitions
│
├── scripts/
│   ├── deploy/                    # Scripts for Vertex AI deployment and testing
│   ├── eval/
│   │   ├── data/                  # JSON scripts for input and configurations
│   │   └── run_eval.py            # Evaluation script
│   ├── run_with_plugins.py        # Local script run with tool loggings
│   └── setup_mcp_opennutrition.sh # MCP server setup script
│
├── deploy_agent/                  # Agent deployment artifacts
├── mcp-opennutrition/             # MCP server integration (OpenNutrition)
└── notebook/                      # Demo notebook

```

---

## Evaluation 🧪

To run evaluation using ADK's User Simulation, navigate to `scripts/data/` and update the relevant `.json` files to add new conversation scenarios or adjust evaluation configurations.

Once ready, run the evaluation script:

```bash
uv run scripts/run_eval.py
```

An example of the evaluation output is available in the `notebook/` under the **Agent Evaluation** section.

---

## Deployment 🚀

- The repository contains a helper to deploy to Vertex AI via ADK:

```bash
uv run scripts/deploy/deploy_vertex.py
```

- Ensure you are authenticated with Google Cloud and have required IAM permissions.
- For alternative deployment targets, use the ADK CLI (`adk deploy ...`) and follow provider docs.
