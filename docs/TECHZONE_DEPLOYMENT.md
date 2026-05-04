# TechZone Environment Deployment Guide

This guide explains how to deploy Lendyr assets to the TechZone watsonx Orchestrate environment.

## Overview

The `deploy_to_techzone.sh` script automates the complete deployment process:
1. Sets up the TechZone environment in the Orchestrate CLI
2. Authenticates to the environment
3. Imports all tools, knowledge bases, connections, and agents
4. Handles agent dependencies automatically

## Prerequisites

- IBM watsonx Orchestrate ADK CLI installed (`pip install ibm-watsonx-orchestrate`)
- Access to a TechZone watsonx Orchestrate instance
- TechZone instance URL and API key

## Getting TechZone Credentials

### Instance URL
1. Log into your TechZone watsonx Orchestrate instance
2. Navigate to the service instance page
3. Copy the instance URL (e.g., `https://your-instance.watson-orchestrate.ibm.com`)

### API Key
1. In the TechZone Orchestrate UI, go to **Settings** → **API Keys**
2. Generate a new API key or use an existing one
3. Copy the API key (you'll need it during deployment)

## Running the Deployment

### Basic Usage

From the project root directory:

```bash
./scripts/deploy_to_techzone.sh
```

### What Happens During Deployment

1. **Environment Check**: Verifies the Orchestrate CLI is installed
2. **Environment Setup**: 
   - Prompts for TechZone instance URL
   - Prompts for environment type (default: `ibm_iam`)
   - Adds the environment to your CLI configuration
3. **Authentication**: Prompts for your API key to activate the environment
4. **Asset Import**: Imports in dependency order:
   - Tools (Python, OpenAPI, Flow)
   - Knowledge Bases
   - Connections
   - Agents (with automatic dependency resolution)

### Interactive Prompts

During execution, you'll be prompted for:

```
Enter TechZone instance URL: https://your-instance.watson-orchestrate.ibm.com
Enter environment type (ibm_iam/mcsp/cpd) [default: ibm_iam]: 
Please enter WXO API key: ************************************
```

## Environment Types

Choose the appropriate environment type for your TechZone instance:

- **`ibm_iam`** (default): For IBM Cloud-hosted instances using IBM IAM authentication
- **`mcsp`**: For AWS-hosted instances using Multi-Cloud SaaS Platform authentication
- **`cpd`**: For on-premises Cloud Pak for Data deployments

## What Gets Deployed

### Tools
- **Python Tools**: From `tools/*/tool_name.py` (with requirements.txt if present)
- **OpenAPI Tools**: From `tools/*/tool_name.json`
- **Flow Tools**: From `tools/*flow*.json`
- **Excludes**: Archived tools in `tools/archived_python_tools/`

### Knowledge Bases
- All `.yaml` and `.yml` files from `knowledge_bases/`

### Connections
- All `.yaml` and `.yml` files from `connections/`
- Note: Credentials must be configured separately after import

### Agents
- All `.yaml`, `.yml`, `.json`, and `.py` files from `agents/`
- Automatically handles agent-to-agent dependencies (collaborators)
- Uses multi-pass import (up to 5 passes) to resolve dependencies

## Example Output

```
========================================
Lendyr TechZone Deployment Script
========================================

✓ orchestrate CLI found

========================================
Step 1: Setting up TechZone Environment
========================================
ℹ Adding TechZone environment...
✓ TechZone environment added successfully

========================================
Step 2: Activating TechZone Environment
========================================
✓ TechZone environment activated
✓ Confirmed TechZone environment is active

========================================
Step 3: Importing Tools
========================================
ℹ Scanning for Python tools...
ℹ Importing Python tool: calculate_deferral_terms
✓ Imported Python tool: calculate_deferral_terms (with requirements)
...

========================================
TechZone Deployment Summary
========================================

Environment:     techzone
Tools:           15/15 successful
Knowledge Bases: 2/2 successful
Connections:     0/0 successful
Agents:          10/10 successful

Total:           27/27 successful, 0 failed

✓ All assets deployed successfully to TechZone!
```

## Post-Deployment Steps

### 1. Configure Connection Credentials

If you deployed connections, configure their credentials:

```bash
# Configure connection
orchestrate connections configure -a <app_id> --env draft --kind basic --type team

# Set credentials
orchestrate connections set-credentials -a <app_id> --env draft -u <username> -p <password>
```

### 2. Verify Deployments

Check that all assets were imported:

```bash
orchestrate tools list
orchestrate knowledge-bases list
orchestrate connections list
orchestrate agents list
```

### 3. Test Agents

Test agents in the draft environment:

```bash
orchestrate agents test -n lendyr_customer_care
```

### 4. Deploy to Live

Once tested, deploy agents to the live environment:

```bash
orchestrate agents deploy -n lendyr_customer_care
```

## Troubleshooting

### Environment Already Exists

If the TechZone environment already exists, the script will skip creation and proceed to activation.

### Authentication Expires

Authentication tokens expire after 2 hours. If you see authentication errors, reactivate:

```bash
orchestrate env activate techzone
```

### Import Failures

If specific assets fail to import:

1. Check the error messages in the output
2. Verify file syntax (YAML/JSON)
3. Ensure dependencies exist (e.g., tools referenced by agents)
4. Try importing manually:

```bash
# Import a specific tool
orchestrate tools import -k python -f tools/my_tool/my_tool.py

# Import a specific agent
orchestrate agents import -f agents/my_agent.yaml
```

### Agent Dependency Errors

The script automatically handles agent dependencies through multi-pass import. If an agent still fails after 5 passes:

1. Check that all collaborator agents exist
2. Verify collaborator names match exactly
3. Import collaborators manually first, then retry the dependent agent

## Switching Between Environments

To switch back to your local environment:

```bash
orchestrate env activate local
```

To switch to TechZone:

```bash
orchestrate env activate techzone
```

To list all environments:

```bash
orchestrate env list
```

## Re-running the Script

The script is idempotent and can be run multiple times:
- Existing environment will be reused
- Assets will be updated if they already exist
- New assets will be added

## Manual Environment Setup

If you prefer to set up the environment manually:

```bash
# Add environment
orchestrate env add -n techzone -u https://your-instance.watson-orchestrate.ibm.com -t ibm_iam

# Activate environment
orchestrate env activate techzone

# Import assets using the standard import script
./scripts/import_all_assets.sh
```

## Security Notes

- API keys are entered interactively and not stored in the script
- Environment configuration is stored in `~/.config/orchestrate/config.yaml`
- Authentication tokens are cached in `~/.cache/orchestrate/credentials.yaml`
- Tokens expire after 2 hours for security

## Support

For issues or questions:
- Review the watsonx Orchestrate ADK documentation
- Check error messages in script output
- Verify environment configuration: `orchestrate env list`
- Check active environment: `orchestrate env list | grep "(active)"`

## Related Documentation

- [Import Assets README](../scripts/IMPORT_ASSETS_README.md) - General asset import guide
- [Deployment Instructions](DEPLOYMENT_INSTRUCTIONS.md) - Overall deployment guide
- [Local Testing Guide](LOCAL_TESTING_GUIDE.md) - Testing locally before deployment

---

*Created with Bob - Your AI Development Assistant*