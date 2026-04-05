# Lendyr - watsonx Orchestrate Project

This is a watsonx Orchestrate Agent Development Kit (ADK) project for Lendyr.

## Project Structure

```
lendyr/
├── agents/          # Agent definition files (YAML)
├── tools/           # Tool implementation files (Python)
└── README.md        # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- watsonx Orchestrate ADK installed (`pip install ibm-watsonx-orchestrate`)
- Virtual environment activated

### Project Setup

1. Navigate to the project directory:
   ```bash
   cd ~/Public/lendyr
   ```

2. Activate your virtual environment (if not already active):
   ```bash
   source ~/.venv/bin/activate
   ```

### Working with Tools

Import a Python tool:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main tools import --kind python --file tools/your_tool.py
```

List imported tools:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main tools list
```

### Working with Agents

Import an agent:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main agents import --file agents/your_agent.yaml
```

List agents:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main agents list
```

### Testing Your Agent

Start the chat UI:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main chat start
```

Or use CLI chat:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main chat ask --agent your_agent_name
```

## Environment Management

Check active environment:
```bash
python3 -m ibm_watsonx_orchestrate.cli.main env list
```

The default local environment runs at `http://localhost:4321`

## Documentation

For more information, visit the [watsonx Orchestrate documentation](https://www.ibm.com/docs/en/watsonx/watson-orchestrate).