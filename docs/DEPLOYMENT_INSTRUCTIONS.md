# Deployment Instructions for Lendyr Agents

This guide explains how to deploy the updated agents and tools to watsonx Orchestrate after making changes.

## What Needs to be Deployed

After modifying agent YAML files or adding new tools, you need to deploy them to watsonx Orchestrate so the changes take effect.

### Files Modified in This Update:
- `agents/credit_score_agent.yaml` (NEW - created)
- `agents/lendyr_customer_care.yaml` (UPDATED - routing)
- `agents/loan_agent.yaml` (UPDATED - description)
- `tools/get_loan_details_openapi/get_loan_details_openapi.json` (NEW - created)

## Deployment Methods

### Method 1: Using the Import Script (Recommended)

The project includes an import script that can deploy all assets at once:

```bash
cd /Users/kk76/Public/lendyr
./scripts/import_all_assets.sh
```

This script will:
1. Import all agents from the `agents/` directory
2. Import all tools from the `tools/` directory
3. Import all knowledge bases from the `knowledge_bases/` directory
4. Import all connections from the `connections/` directory

**Note**: Check `scripts/IMPORT_ASSETS_README.md` for detailed information about the import script.

### Method 2: Using watsonx Orchestrate CLI

If you have the watsonx Orchestrate CLI installed, you can deploy individual components:

#### Deploy the New Credit Score Agent:
```bash
orchestrate agent import agents/credit_score_agent.yaml
```

#### Update Existing Agents:
```bash
orchestrate agent import agents/lendyr_customer_care.yaml
orchestrate agent import agents/loan_agent.yaml
```

#### Deploy the New Loan Details Tool:
```bash
orchestrate tool import tools/get_loan_details_openapi/
```

### Method 3: Using the Web UI

1. **Log in to watsonx Orchestrate**
   - Navigate to your watsonx Orchestrate instance
   - Go to the Agent Builder section

2. **Import the New Credit Score Agent**:
   - Click "Import Agent"
   - Select `agents/credit_score_agent.yaml`
   - Click "Import"

3. **Update Existing Agents**:
   - For each modified agent (lendyr_customer_care, loan_agent):
     - Find the agent in the list
     - Click "Import" or "Update"
     - Select the updated YAML file
     - Confirm the update

4. **Import the New Tool**:
   - Go to Tools section
   - Click "Import Tool"
   - Select `tools/get_loan_details_openapi/get_loan_details_openapi.json`
   - Click "Import"

## Verification Steps

After deployment, verify the changes are working:

### 1. Test Credit Score Agent Routing

Test that credit score queries route to the correct agent:

```
User: "What's my credit score?"
Expected: Routes to credit_score_agent (not loan_agent)
```

### 2. Test Credit Score Tool

Verify the credit score tool is working:

```
User: "Show me my credit score history"
Expected: Returns credit score data with history
Should NOT return "No loans found" error
```

### 3. Test Loan Agent Still Works

Verify loan queries still work correctly:

```
User: "What's my loan balance?"
Expected: Routes to loan_agent and returns loan information
```

### 4. Check Tool Performance

Monitor response times to verify the OpenAPI tools are faster:
- Authentication should be < 300ms
- Loan queries should be < 200ms
- Credit score queries should be < 200ms

## Troubleshooting

### Issue: "No loans found" error when asking about credit score

**Cause**: The agent is calling `get_loan_details` instead of `get_credit_score_history`

**Solution**: 
1. Verify the agents have been redeployed
2. Clear any caches in watsonx Orchestrate
3. Check that `credit_score_agent.yaml` is correctly imported
4. Verify the tool `get_credit_score_history` exists in the Tools section

### Issue: Credit score queries still route to loan_agent

**Cause**: The updated `lendyr_customer_care.yaml` hasn't been deployed

**Solution**:
1. Redeploy `lendyr_customer_care.yaml`
2. Verify the collaborators list includes `credit_score_agent`
3. Check the routing instructions in the deployed agent

### Issue: Tool not found errors

**Cause**: The new OpenAPI tools haven't been imported

**Solution**:
1. Import `tools/get_loan_details_openapi/get_loan_details_openapi.json`
2. Import `tools/get_credit_score_history/lendyr_openapi.json` (if not already present)
3. Verify tools appear in the Tools section of watsonx Orchestrate

## Rollback Procedure

If issues occur after deployment, you can rollback:

### Rollback Credit Score Agent:
```bash
orchestrate agent delete credit_score_agent
```

### Restore Previous Agent Versions:
```bash
# Use git to restore previous versions
git checkout HEAD~1 agents/lendyr_customer_care.yaml
git checkout HEAD~1 agents/loan_agent.yaml

# Then redeploy
orchestrate agent import agents/lendyr_customer_care.yaml
orchestrate agent import agents/loan_agent.yaml
```

### Restore Python Tools (if needed):
```bash
# Copy archived tools back
cp -r tools/archived_python_tools/get_loan_details tools/
cp tools/archived_python_tools/customer_auth_tool.py tools/

# Redeploy
orchestrate tool import tools/get_loan_details/
```

## Environment-Specific Deployment

### Draft Environment (Testing):
```bash
orchestrate agent import agents/credit_score_agent.yaml --environment draft
```

### Live Environment (Production):
```bash
orchestrate agent import agents/credit_score_agent.yaml --environment live
```

**Best Practice**: Always test in draft environment first, then promote to live.

## Post-Deployment Checklist

- [ ] All agents imported successfully
- [ ] All tools imported successfully
- [ ] Credit score queries route to credit_score_agent
- [ ] Loan queries route to loan_agent
- [ ] No "No loans found" errors for credit score queries
- [ ] Response times improved (check monitoring)
- [ ] All existing functionality still works
- [ ] Documentation updated

## Additional Resources

- **Import Script Documentation**: `scripts/IMPORT_ASSETS_README.md`
- **Implementation Summary**: `scripts/PYTHON_TOOLS_OPTIMIZATION_IMPLEMENTATION.md`
- **Archived Tools**: `tools/archived_python_tools/README.md`
- **CLI Commands Reference**: `docs/CLI_COMMANDS.md` (if exists)

## Support

If you encounter issues during deployment:
1. Check the watsonx Orchestrate logs
2. Verify all file paths are correct
3. Ensure you have proper permissions
4. Review the error messages carefully
5. Consult the watsonx Orchestrate documentation

---

**Last Updated**: 2026-05-04  
**Author**: Bob (AI Assistant)