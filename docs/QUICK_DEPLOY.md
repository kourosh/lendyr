# Quick Deployment Guide - Customer ID Fix

## Fixed: Tool Name Format Issue

**Problem:** Agent YAML files were using double underscores `__` for path parameters, but the actual imported tool names use single underscores `_`.

**Solution:** Updated all agent YAML files to use correct tool names with single underscores.

## Deployment Commands

### 1. Import Tools (REQUIRED FIRST)

```bash
cd ~/Public/lendyr

orchestrate tools import --kind openapi --file tools/lendyr_openapi_customer_id.json
```

### 2. Import Agents (in dependency order)

```bash
# Import all 5 collaborator agents first (no dependencies)
orchestrate agents import --file agents/account_agent.yaml
orchestrate agents import --file agents/card_agent.yaml
orchestrate agents import --file agents/loan_agent.yaml
orchestrate agents import --file agents/lendyr_disputes_agent.yaml
orchestrate agents import --file agents/loan_deferral_agent.yaml

# Import orchestrator agent last (depends on all collaborators)
orchestrate agents import --file agents/lendyr_customer_care.yaml
```

**Note:** Use `import` (not `create`) when loading from YAML files.

### 3. Test the Fix

```bash
orchestrate chat ask --agent-name lendyr_customer_care
```

**Test Scenario:**
1. Provide customer ID: `846301`
2. Provide PIN: `12345`
3. Say: "I need to defer my next loan payment"
4. Approve the deferral terms
5. **Expected:** Deferral processes successfully without "Customer not found" error

## If Agents Already Exist

If you get errors about agents already existing, remove them first:

```bash
orchestrate agents remove --name account_agent --kind native
orchestrate agents remove --name loan_deferral_agent --kind native
orchestrate agents remove --name lendyr_customer_care --kind native
```

Then run the import commands above.

## Common Errors Fixed

❌ **Wrong:** `orchestrate agents create --file agents/account_agent.yaml`
- Error: "ValueError: --name is required for non-custom agents"

✅ **Correct:** `orchestrate agents import --file agents/account_agent.yaml`

---

❌ **Wrong:** `orchestrate skills import-api`
- Error: Command not found

✅ **Correct:** `orchestrate tools import --kind openapi`

---

❌ **Wrong:** `orchestrate agents delete`
- Error: Command not found

✅ **Correct:** `orchestrate agents remove --name <name> --kind native`