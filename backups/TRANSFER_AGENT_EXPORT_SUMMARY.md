# Transfer Agent Export Summary

**Date**: April 26, 2026
**Environment**: Local watsonx Orchestrate

## Exported Files

### 1. Agent Export (Full Package)
- **File**: `transfer_agent_export.zip` (14KB)
- **Contents**:
  - `agents/native/transfer_agent.yaml` - Agent configuration
  - `tools/get_accounts_by_customer_id/lendyr_openapi.json` - Account retrieval tool
  - `tools/transfer_money_by_customer_id/lendyr_openapi.json` - Transfer execution tool

### 2. Individual Tool Exports
- **File**: `get_accounts_by_customer_id_tool.zip` (3.4KB)
- **File**: `transfer_money_by_customer_id_tool.zip` (6.2KB)

## Current Agent Configuration

### Key Settings
- **Name**: transfer_agent
- **Kind**: native
- **LLM**: groq/openai/gpt-oss-120b
- **Style**: default
- **Context Variables**: customer_id
- **Tools**: 
  - get_accounts_by_customer_id
  - transfer_money_by_customer_id

### Known Issue
The agent is returning raw JSON responses instead of natural language:

**Problem Behavior**:
```json
{
  "raw_response": "[{\"account_id\":1,\"customer_id\":846301,...}]"
}
```

**Expected Behavior**:
"Done! I've transferred $500 from your checking to savings. Your checking now has $747.80 and savings has $3,700.50."

### Agent Instructions (Lines 24-27)
The agent has explicit instructions to NOT show raw JSON:
```yaml
### Step 1: Get Account Information (SILENTLY)
- Call get_accounts_by_customer_id immediately
- DO NOT show the raw JSON response to the customer
- Parse the response internally to understand available accounts and balances
```

### Additional Rules (Lines 64-65)
```yaml
1. NEVER return raw JSON or tool output to the customer
2. ALWAYS parse tool responses internally before responding
```

## Troubleshooting Steps

### Potential Causes
1. **LLM Model Issue**: The `groq/openai/gpt-oss-120b` model may not be following instructions properly
2. **Tool Response Format**: The tool might be returning data in a format the LLM can't parse
3. **Agent Style**: The `default` style might need to be changed to `react` or another style
4. **Instructions Clarity**: The instructions might need to be more explicit about response formatting

### Recommended Fixes

#### Option 1: Change LLM Model
Try a different model that better follows instructions:
- `ibm/granite-3-8b-instruct`
- `meta-llama/llama-3-1-70b-instruct`
- `anthropic/claude-3-5-sonnet-20241022`

#### Option 2: Modify Agent Style
Change from `default` to `react` style for better tool handling:
```yaml
style: react
```

#### Option 3: Add Structured Output
Add structured output schema to force proper formatting:
```yaml
structured_output:
  type: object
  properties:
    message:
      type: string
      description: Natural language response to customer
    transfer_completed:
      type: boolean
```

#### Option 4: Strengthen Instructions
Add more explicit formatting rules at the top of instructions:
```yaml
instructions: |-
  ## CRITICAL: RESPONSE FORMAT
  - You MUST respond in natural, conversational language
  - You MUST NEVER return raw JSON, arrays, or tool outputs
  - You MUST parse all tool responses internally before responding
  - Example: "Done! I've transferred $500..." NOT "[{...}]"
  
  [rest of instructions...]
```

## Next Steps

1. **Test with Different LLM**: Import agent with a different model
2. **Modify Instructions**: Strengthen the response format requirements
3. **Change Style**: Try `react` style instead of `default`
4. **Add Output Schema**: Use structured_output to enforce format
5. **Test Locally**: Use `orchestrate chat ask` to test changes before deploying

## Import Commands

To re-import the full agent package:
```bash
orchestrate agents import -f backups/transfer_agent_export.zip
```

To import just the agent YAML (after modifications):
```bash
orchestrate agents import -f backups/transfer_agent_export/agents/native/transfer_agent.yaml
```

To import individual tools:
```bash
orchestrate tools import -k openapi -f backups/transfer_agent_export/tools/get_accounts_by_customer_id/lendyr_openapi.json
orchestrate tools import -k openapi -f backups/transfer_agent_export/tools/transfer_money_by_customer_id/lendyr_openapi.json
```

## Files Location
All exports are in: `/Users/kk76/Public/lendyr/backups/`