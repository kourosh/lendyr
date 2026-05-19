# Account Opening Agent - 401 Error Fix

## Problem
The webchat was showing a 401 error: "groq error: Invalid API Key" when trying to use the account opening agent.

## Root Cause
The webchat was configured to use `account_opening_agent_v2` (ID: `f3e9c7e8-463e-49fd-a9a9-c43afd9cfbf8`) which had an **incorrect model name**: `groq/gpt-oss-120b`

The correct model name should be: `groq/openai/gpt-oss-120b`

## Solution Applied

### 1. Updated Webchat Configuration
Changed `webchat/index.html` to use the correct agent:
- **Old Agent ID**: `f3e9c7e8-463e-49fd-a9a9-c43afd9cfbf8` (account_opening_agent_v2)
- **New Agent ID**: `ae64e337-aff7-483d-a0a1-174fc500bbba` (account_opening_agent)

### 2. Removed Incorrect Agent
Deleted `account_opening_agent_v2` which had the wrong model configuration.

### 3. Verified Correct Configuration
The `account_opening_agent` uses:
- **Model**: `groq/openai/gpt-oss-120b` ✅
- **Tools**: `open_account`, `schedule_appointment`
- **Collaborators**: `branch_locator_agent`

## Testing
1. Open `webchat/index.html` in a browser
2. The chat widget should now load without 401 errors
3. You can interact with the account opening agent

## Model Configuration Status
Both Groq models are properly registered in Orchestrate:
```
virtual-model/groq/openai/gpt-oss-120b  ✅
groq/openai/gpt-oss-120b                ✅
```

The `groq_credentials` connection exists and is configured.

## Files Modified
- `webchat/index.html` - Updated agent ID to use correct agent

## Files Removed
- None (agent removed via CLI)

## Next Steps
If you still encounter issues:
1. Verify your Groq API key is valid at https://console.groq.com/
2. Check the API key is set in the connection:
   ```bash
   orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=YOUR_ACTUAL_KEY"
   ```
3. Ensure the model was imported with the connection:
   ```bash
   orchestrate models import --file models/groq_gpt_oss_120b.yaml --app-id groq_credentials