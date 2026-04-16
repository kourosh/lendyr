# Deployment Steps for Customer ID Fix

## Prerequisites
- IBM Cloud CLI installed
- Orchestrate ADK installed
- Docker installed (for API deployment)
- Access to IBM Cloud account

**Note:** If Docker is not installed, you can skip Step 1 (API deployment) and only update the agents. The API is already deployed and running.

## Step 1: Deploy Updated API to IBM Cloud

```bash
# Navigate to the lendyr_code_engine directory where .env file is located
cd ~/Public/lendyr/lendyr_code_engine

# Run the deployment script
../scripts/deploy-ibm.sh
```

**Expected Output:**
- Docker image built successfully
- Image pushed to IBM Container Registry  
- Code Engine application updated
- New API URL displayed

## Step 2: Verify API Deployment

Test the new customer_id-based endpoints:

```bash
# Test customer lookup by ID
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301

# Test authentication (should return customer_id)
curl -X POST https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/auth/validate \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 846301, "pin": "12345"}'
```

## Step 3: Import Tools

```bash
# Navigate back to project root
cd ~/Public/lendyr

# Import the customer_id-based tools
orchestrate tools import \
  --kind openapi \
  --file tools/lendyr_openapi_customer_id.json
```

**Note:** You may see warnings about existing tools - this is normal.

## Step 4: Create/Update Agents

### Option A: If agents don't exist yet (first time)

```bash
# Import agents in order (dependencies first)
orchestrate agents import --file agents/account_agent.yaml
orchestrate agents import --file agents/loan_deferral_agent.yaml
orchestrate agents import --file agents/lendyr_customer_care.yaml
```

### Option B: If agents already exist (updating)

```bash
# Remove existing agents
orchestrate agents remove --name account_agent --kind native
orchestrate agents remove --name loan_deferral_agent --kind native
orchestrate agents remove --name lendyr_customer_care --kind native

# Recreate with updated configuration
orchestrate agents create --file agents/account_agent.yaml
orchestrate agents create --file agents/loan_deferral_agent.yaml
orchestrate agents create --file agents/lendyr_customer_care.yaml
```

## Step 5: Verify Agent Configuration

```bash
# List all agents
orchestrate agents list

# Check specific agent details
orchestrate agents get loan_deferral_agent
```

## Step 6: Test the Fix

### Start Interactive Chat

```bash
orchestrate chat ask --agent-name lendyr_customer_care
```

### Test Script

1. **User:** "Hi, I need help with my loan payment"
2. **Agent:** Asks for customer ID
3. **User:** "846301"
4. **Agent:** Asks for PIN
5. **User:** "12345"
6. **Agent:** Authenticates successfully
7. **User:** "I need to defer my next loan payment"
8. **Agent:** Routes to loan_deferral_agent
9. **Loan Agent:** Shows eligibility and deferral terms
10. **User:** "Yes, I agree"
11. **Loan Agent:** **Should process successfully without "Customer not found" error** ✅

## Troubleshooting

### Issue: ".env file not found"
**Solution:** Make sure you're in the `lendyr_code_engine` directory when running the deploy script:
```bash
cd ~/Public/lendyr/lendyr_code_engine
../scripts/deploy-ibm.sh
```

### Issue: "No agent found"
**Solution:** The agents haven't been created yet. Use Option A above to create them.

### Issue: "Failed to find tool"
**Solution:** Import the tools first (Step 3) before creating agents.

### Issue: "Failed to find collaborator"
**Solution:** Create agents in the correct order - dependencies first:
1. account_agent (no dependencies)
2. loan_deferral_agent (no dependencies)
3. lendyr_customer_care (depends on the above)

## Quick Command Reference

```bash
# Deploy API
cd ~/Public/lendyr/lendyr_code_engine && ../scripts/deploy-ibm.sh

# Import tools
cd ~/Public/lendyr
orchestrate tools import --kind openapi --file tools/lendyr_openapi_customer_id.json

# Create agents (in order)
orchestrate agents create --file agents/account_agent.yaml
orchestrate agents create --file agents/loan_deferral_agent.yaml
orchestrate agents create --file agents/lendyr_customer_care.yaml

# Test
orchestrate chat ask --agent-name lendyr_customer_care
```

## Success Criteria

✅ API deployed with new customer_id endpoints  
✅ Tools imported successfully  
✅ All agents created without errors  
✅ Loan deferral completes without "Customer not found" error  
✅ Customer ID 846301 (Brian Nguyen) can successfully defer loan payment  