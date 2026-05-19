# Import All Assets Script - Updated for Orchestrate CLI

## Overview

The `import_all_assets.sh` script has been updated with the correct Orchestrate CLI commands based on the official documentation. This script imports all Lendyr Bank assets in the correct dependency order.

## What It Does

The script imports assets in this order:

1. **Tools** (Python, OpenAPI, Flow)
2. **Knowledge Bases**
3. **Connections**
4. **Agents** (with dependency resolution)
5. **Cleanup** (removes AskOrchestrate agent)

## Correct CLI Commands Used

### Tools
```bash
# Python tools
orchestrate tools import -k python -f <file.py> -r <requirements.txt>

# OpenAPI tools
orchestrate tools import -k openapi -f <spec.json>

# Flow tools
orchestrate tools import -k flow -f <flow.json>
```

### Knowledge Bases
```bash
orchestrate knowledge_bases import -f <kb.yaml>
```

### Connections
```bash
orchestrate connections import -f <connection.yaml>
```

### Agents
```bash
orchestrate agents import -f <agent.yaml>
```

## Usage

### Basic Usage
```bash
cd /Users/kk76/Public/lendyr
./scripts/import_all_assets.sh
```

### Make Executable (if needed)
```bash
chmod +x scripts/import_all_assets.sh
```

## Features

### 1. Automatic Discovery
- Scans directories for all asset types
- Detects Python tools with requirements.txt
- Finds OpenAPI specs in subdirectories
- Identifies Flow tools by naming pattern

### 2. Dependency Resolution
- Imports agents in multiple passes
- Handles collaborator dependencies
- Retries failed imports up to 5 times
- Stops if no progress is made

### 3. Error Handling
- Continues on individual failures
- Tracks success/failure counts
- Shows detailed error messages
- Returns appropriate exit codes

### 4. Color-Coded Output
- 🔵 Blue: Section headers and info
- ✅ Green: Success messages
- ❌ Red: Error messages
- ⚠️  Yellow: Warning messages

## Directory Structure Expected

```
lendyr/
├── tools/
│   ├── tool_name/
│   │   ├── tool_name.py          # Python tool
│   │   └── requirements.txt      # Optional
│   ├── another_tool/
│   │   └── spec.json             # OpenAPI tool
│   └── flow_tool.json            # Flow tool (root level)
├── knowledge_bases/
│   ├── kb1.yaml
│   └── kb2.yaml
├── connections/
│   ├── conn1.yaml
│   └── conn2.yaml
└── agents/
    ├── agent1.yaml
    ├── agent2.yaml
    └── main_agent.yaml
```

## Account Opening Assets

The script will automatically import the new account opening assets:

### Tools
- `tools/collect_account_info/collect_account_info.py` - Account info collection with dropdown
- `tools/collect_account_info_form/collect_account_info_form.py` - Alternative form approach
- `tools/schedule_appointment/schedule_appointment.py` - Appointment scheduling

### Agents
- `agents/account_opening_agent.yaml` - Account opening specialist
- `agents/lendyr_customer_care.yaml` - Updated main agent with routing

## Output Example

```
========================================
Lendyr Asset Import Script
========================================

✓ orchestrate CLI found

========================================
Step 1: Importing Tools
========================================

ℹ Scanning for Python tools...
ℹ Importing Python tool: collect_account_info
✓ Imported Python tool: collect_account_info (with requirements)
ℹ Importing Python tool: schedule_appointment
✓ Imported Python tool: schedule_appointment

ℹ Scanning for OpenAPI tools...
ℹ Importing OpenAPI tool: customer_auth_tool
✓ Imported OpenAPI tool: customer_auth_tool

ℹ Tools imported: 25/25 successful, 0 failed

========================================
Step 2: Importing Knowledge Bases
========================================

ℹ Scanning for knowledge base files...
ℹ Importing knowledge base: lendyr_branch_locations.yaml
✓ Imported knowledge base: lendyr_branch_locations.yaml

ℹ Knowledge bases imported: 3/3 successful, 0 failed

========================================
Step 3: Importing Connections
========================================

⚠ Connections directory not found: /path/to/connections

========================================
Step 4: Importing Agents
========================================

ℹ Importing agents in multiple passes to handle dependencies...
ℹ Importing agent: account_opening_agent.yaml
✓ Imported agent: account_opening_agent.yaml
ℹ Importing agent: lendyr_customer_care.yaml
✓ Imported agent: lendyr_customer_care.yaml

ℹ Agents imported: 12/12 successful, 0 failed

========================================
Step 5: Deleting AskOrchestrate Agent
========================================

ℹ Removing AskOrchestrate agent...
✓ Deleted AskOrchestrate agent

========================================
Import Summary
========================================

Tools:           25/25 successful
Knowledge Bases: 3/3 successful
Connections:     0/0 successful
Agents:          12/12 successful

Total:           40/40 successful, 0 failed

✓ All assets imported successfully!
```

## Troubleshooting

### "orchestrate CLI not found"
Install the IBM watsonx Orchestrate ADK:
```bash
pip install ibm-watsonx-orchestrate
```

### "Failed to find collaborator"
This is normal - the script will retry in subsequent passes. If it persists after 5 passes, check agent dependencies.

### Permission Denied
Make the script executable:
```bash
chmod +x scripts/import_all_assets.sh
```

### Import Failures
Check the error details shown in red. Common issues:
- Invalid YAML/JSON syntax
- Missing required fields
- Invalid tool/agent references
- Network connectivity issues

## Best Practices

1. **Run from project root**: Always run from `/Users/kk76/Public/lendyr`
2. **Check output**: Review the summary to ensure all assets imported
3. **Fix failures**: Address any failed imports before deploying
4. **Test after import**: Verify agents work correctly after import
5. **Version control**: Commit working configurations before changes

## Integration with CI/CD

The script returns appropriate exit codes:
- `0` - All assets imported successfully
- `1` - Some assets failed to import

Example CI/CD usage:
```bash
#!/bin/bash
if ./scripts/import_all_assets.sh; then
    echo "Deployment successful"
    # Continue with testing
else
    echo "Deployment failed"
    exit 1
fi
```

## Changes from Previous Version

### Fixed Commands
- ✅ `orchestrate tools import` (was `orchestrate tool import`)
- ✅ `orchestrate agents import` (was `orchestrate agent import`)
- ✅ `orchestrate knowledge_bases import` (was `orchestrate knowledge-bases import`)

### Maintained Features
- ✅ Multi-pass agent import with dependency resolution
- ✅ Automatic tool type detection
- ✅ Color-coded output
- ✅ Comprehensive error handling
- ✅ Summary statistics

## Related Documentation

- `docs/ACCOUNT_OPENING_COMPLETE_SUMMARY.md` - Account opening implementation
- `docs/ACCOUNT_OPENING_DROPDOWN_IMPLEMENTATION.md` - Dropdown menu guide
- `scripts/IMPORT_ASSETS_README.md` - Original import documentation

## Support

For issues or questions:
1. Check the Orchestrate documentation MCP server
2. Review error messages in the script output
3. Verify asset file syntax (YAML/JSON)
4. Ensure all dependencies are available

---

**Last Updated**: 2026-05-07  
**Script Version**: 2.0 (Orchestrate CLI v2.9.0 compatible)