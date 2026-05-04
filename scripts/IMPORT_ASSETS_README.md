# Lendyr Asset Import Script

This script automates the import of all Lendyr project assets into watsonx Orchestrate in the correct dependency order.

## Overview

The `import_all_assets.sh` script imports project assets in the following order:

1. **Tools** - OpenAPI, Python, and Flow tools (no dependencies)
2. **Knowledge Bases** - Knowledge base configurations
3. **Connections** - Authentication and connection configurations
4. **Agents** - AI agents (depend on tools, knowledge bases, and connections)
   - Uses multi-pass import to handle agent-to-agent dependencies (collaborators)
   - Automatically retries agents with unmet dependencies up to 5 times

## Prerequisites

- IBM watsonx Orchestrate ADK CLI installed and configured
- Active Orchestrate environment set up
- Proper authentication credentials configured

## Usage

### Basic Usage

Run the script from the project root or scripts directory:

```bash
# From project root
./scripts/import_all_assets.sh

# From scripts directory
cd scripts
./import_all_assets.sh
```

### What Gets Imported

#### Tools (`tools/` directory)
- **Python Tools**: Scans for `.py` files in subdirectories
  - Automatically includes `requirements.txt` if present
  - Example: `tools/calculate_deferral_terms/calculate_deferral_terms.py`
  
- **OpenAPI Tools**: Scans for `.json` files in subdirectories
  - Example: `tools/customer_auth_tool/customer_auth_openapi.json`
  
- **Flow Tools**: Scans for JSON files with "flow" in the name at root level
  - Example: `tools/customer_authentication_flow.py`

#### Knowledge Bases (`knowledge_bases/` directory)
- Imports all `.yaml` and `.yml` files
- Example: `knowledge_bases/lendyr_overlimit_transfers_knowledge_base.yaml`

#### Connections (`connections/` directory)
- Imports all `.yaml` and `.yml` files
- Note: Connection credentials must be configured separately after import

#### Agents (`agents/` directory)
- Imports all `.yaml`, `.yml`, `.json`, and `.py` files
- Example: `agents/lendyr_customer_care.yaml`

## Output

The script provides:
- Color-coded progress messages (green for success, red for errors, yellow for warnings)
- Real-time import status for each asset
- Summary report showing:
  - Number of tools imported
  - Number of knowledge bases imported
  - Number of connections imported
  - Number of agents imported
  - Total success/failure count

### Example Output

```
========================================
Lendyr Asset Import Script
========================================

✓ orchestrate CLI found

========================================
Step 1: Importing Tools
========================================
ℹ Scanning for Python tools...
ℹ Importing Python tool: calculate_deferral_terms
✓ Imported Python tool: calculate_deferral_terms (with requirements)
...

========================================
Step 4: Importing Agents
========================================
ℹ Importing agents in multiple passes to handle dependencies...
ℹ Importing agent: loan_deferral_agent.yaml
✓ Imported agent: loan_deferral_agent.yaml
ℹ Importing agent: loan_agent.yaml
⚠ Agent loan_agent.yaml has unmet dependencies, will retry
ℹ Pass 2: Retrying failed agents...
ℹ Importing agent: loan_agent.yaml
✓ Imported agent: loan_agent.yaml
...

========================================
Import Summary
========================================

Tools:           18/18 successful
Knowledge Bases: 2/2 successful
Connections:     0/0 successful
Agents:          10/10 successful

Total:           30/30 successful, 0 failed

✓ All assets imported successfully!
```

## Error Handling

- The script exits immediately if the `orchestrate` CLI is not found
- Each import operation is tracked individually
- Failed imports are reported but don't stop the script
- **Agent dependency handling**: Agents with unmet collaborator dependencies are automatically retried in subsequent passes (up to 5 passes)
- Exit code 0 indicates all imports succeeded
- Exit code 1 indicates one or more imports failed

## Agent Dependency Resolution

The script intelligently handles agent-to-agent dependencies (collaborators):

1. **First Pass**: Attempts to import all agents
2. **Subsequent Passes**: Retries agents that failed due to missing collaborators
3. **Automatic Detection**: Identifies dependency errors and queues agents for retry
4. **Progress Tracking**: Stops retrying if no progress is made to avoid infinite loops
5. **Maximum 5 Passes**: Prevents excessive retries while allowing complex dependency chains

**Example Dependency Chain:**
- `loan_deferral_agent` (no dependencies) → imports in pass 1
- `loan_agent` (depends on `loan_deferral_agent`) → imports in pass 2
- `lendyr_customer_care` (depends on `loan_agent`) → imports in pass 3

## Directory Structure Expected

```
lendyr/
├── tools/
│   ├── calculate_deferral_terms/
│   │   ├── calculate_deferral_terms.py
│   │   └── requirements.txt
│   ├── customer_auth_tool/
│   │   └── customer_auth_openapi.json
│   └── customer_authentication_flow.py
├── knowledge_bases/
│   ├── lendyr_overlimit_transfers_knowledge_base.yaml
│   └── Lendyr_agent_assist_4368Rc.yaml
├── connections/
│   └── (connection YAML files)
├── agents/
│   ├── lendyr_customer_care.yaml
│   ├── account_agent.yaml
│   └── (other agent files)
└── scripts/
    └── import_all_assets.sh
```

## Post-Import Steps

After running the import script:

1. **Configure Connection Credentials**: If you imported connections, set up their credentials:
   ```bash
   orchestrate connections configure -a <app_id> --env draft --kind <auth_type> --type team
   orchestrate connections set-credentials -a <app_id> --env draft -u <username> -p <password>
   ```

2. **Verify Imports**: Check that all assets were imported correctly:
   ```bash
   orchestrate tools list
   orchestrate knowledge-bases list
   orchestrate connections list
   orchestrate agents list
   ```

3. **Test Agents**: Test your agents in draft environment before deploying to live:
   ```bash
   orchestrate agents test -n <agent_name>
   ```

4. **Deploy to Live**: Once tested, deploy agents to live environment:
   ```bash
   orchestrate agents deploy -n <agent_name>
   ```

## Troubleshooting

### Script Not Executable
```bash
chmod +x scripts/import_all_assets.sh
```

### Orchestrate CLI Not Found
Install the IBM watsonx Orchestrate ADK:
```bash
pip install ibm-watsonx-orchestrate
```

### Authentication Errors
Ensure you're logged in and have an active environment:
```bash
orchestrate login
orchestrate env list
orchestrate env use <environment_name>
```

### Import Failures
- Check that file formats are correct (YAML/JSON syntax)
- Verify that referenced dependencies exist (e.g., tools referenced by agents)
- Review error messages for specific issues
- Try importing individual assets manually to debug

## Manual Import Commands

If you need to import assets individually:

```bash
# Import a tool
orchestrate tools import -k python -f tools/my_tool/my_tool.py -r tools/my_tool/requirements.txt
orchestrate tools import -k openapi -f tools/my_tool/openapi.json

# Import a knowledge base
orchestrate knowledge-bases import -f knowledge_bases/my_kb.yaml

# Import a connection
orchestrate connections import -f connections/my_connection.yaml

# Import an agent
orchestrate agents import -f agents/my_agent.yaml
```

## Notes

- The script uses `set -e` to exit on errors during execution
- All paths are relative to the project root directory
- The script automatically detects the project root from the script location
- Color output works in most modern terminals

## Support

For issues or questions:
- Review the watsonx Orchestrate ADK documentation
- Check the error messages in the script output
- Verify your environment configuration with `orchestrate env list`