# Transaction Date Increment Cron Job Deployment Guide

## Overview

This guide explains how to deploy a daily cron job that automatically updates transaction dates in the Lendyr database. The job ensures that the most recent transaction is always dated today, with older transactions maintaining their relative spacing.

## What This Cron Job Does

The transaction date increment job:
- Runs **daily at 11:59 PM Pacific Time**
- Finds the most recent transaction date in the database
- Calculates the difference between that date and today
- Increments all transaction dates by that difference
- Ensures the most recent transaction is always dated today

**Example**: If the most recent transaction is dated May 8, 2026, and today is May 4, 2026, the job will subtract 4 days from all transaction dates, making the most recent transaction dated May 4, 2026.

## Prerequisites

Before deploying, ensure you have:

1. **IBM Cloud CLI** installed and configured
2. **IBM Cloud Code Engine plugin** installed
3. **IBM Container Registry access** configured
4. **DB2 credentials** from the existing deployment
5. Access to the **lendyr-cron-jobs** Code Engine project (or create a new one)

## Files Created

- `scripts/increment_transaction_dates.py` - Python script that updates transaction dates
- `scripts/cron_transaction_increment.sh` - Bash wrapper for the cron job
- `scripts/Dockerfile.transaction-cron` - Docker container definition
- `docs/TRANSACTION_CRON_DEPLOYMENT.md` - This deployment guide

## Deployment Steps

### Step 1: Set Up IBM Cloud CLI

```bash
# Login to IBM Cloud
ibmcloud login --sso

# Target the correct account and region
ibmcloud target -r us-south -g Default

# Select or create Code Engine project
ibmcloud ce project select --name lendyr-cron-jobs
# OR create new project:
# ibmcloud ce project create --name lendyr-cron-jobs
```

### Step 2: Build and Push Docker Image

```bash
# Navigate to project root
cd /path/to/lendyr

# Build the Docker image
docker build -f scripts/Dockerfile.transaction-cron -t lendyr-transaction-cron:latest .

# Tag for IBM Container Registry
docker tag lendyr-transaction-cron:latest us.icr.io/lendyr/lendyr-transaction-cron:latest

# Login to IBM Container Registry
ibmcloud cr login

# Push the image
docker push us.icr.io/lendyr/lendyr-transaction-cron:latest
```

### Step 3: Create DB2 Credentials Secret (if not already exists)

If you already have the `lendyr-db2-credentials` secret from the credit history cron job, skip this step.

```bash
# Create secret with DB2 credentials
ibmcloud ce secret create --name lendyr-db2-credentials \
  --from-env-file lendyr_code_engine/.env
```

### Step 4: Create the Code Engine Job

```bash
# Create the job
ibmcloud ce job create \
  --name transaction-date-increment \
  --image us.icr.io/lendyr/lendyr-transaction-cron:latest \
  --registry-secret icr-lendyr \
  --cpu 0.25 \
  --memory 0.5G \
  --maxexecutiontime 300 \
  --env-from-secret lendyr-db2-credentials
```

### Step 5: Test the Job

```bash
# Submit a test run
ibmcloud ce jobrun submit \
  --job transaction-date-increment \
  --name test-run-$(date +%s)

# Wait a few seconds, then check the logs
ibmcloud ce jobrun logs --jobrun test-run-XXXXXXXXXX
```

Expected output:
```
[2026-05-04T23:59:00.000000] Starting transaction date increment
[2026-05-04T23:59:00.500000] Connected to database successfully
[2026-05-04T23:59:00.500050] Current max transaction date: 2026-05-08 14:19:09
[2026-05-04T23:59:00.500100] Today's date: 2026-05-04 23:59:59
[2026-05-04T23:59:00.500150] Days to add: -4
[2026-05-04T23:59:00.500200] Executing date increment...
[2026-05-04T23:59:01.000000] Successfully updated 2057 transaction records
[2026-05-04T23:59:01.000050] All transaction dates have been moved forward by -4 days
[2026-05-04T23:59:01.000100] Most recent transaction is now dated: 2026-05-04 23:59:59
[2026-05-04T23:59:01.000150] Transaction date increment completed successfully
```

### Step 6: Create Cron Subscription

```bash
# Create daily cron subscription (runs at 11:59 PM Pacific Time)
ibmcloud ce subscription cron create \
  --name daily-transaction-update \
  --destination transaction-date-increment \
  --schedule "59 23 * * *" \
  --time-zone "America/Los_Angeles" \
  --destination-type job
```

### Step 7: Verify Deployment

```bash
# Check subscription status
ibmcloud ce subscription cron get --name daily-transaction-update

# List all jobs
ibmcloud ce job list

# Check job configuration
ibmcloud ce job get --name transaction-date-increment
```

## Monitoring and Management

### View Job Runs

```bash
# List all job runs
ibmcloud ce jobrun list

# View specific job run details
ibmcloud ce jobrun get --name <jobrun-name>

# View job run logs
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

### Manually Trigger the Job

```bash
# For testing or immediate execution
ibmcloud ce jobrun submit \
  --job transaction-date-increment \
  --name manual-run-$(date +%s)
```

### Update the Job

If you need to update the script:

```bash
# 1. Rebuild and push the Docker image
docker build -f scripts/Dockerfile.transaction-cron -t lendyr-transaction-cron:latest .
docker tag lendyr-transaction-cron:latest us.icr.io/lendyr/lendyr-transaction-cron:latest
docker push us.icr.io/lendyr/lendyr-transaction-cron:latest

# 2. Update the job to use the new image
ibmcloud ce job update \
  --name transaction-date-increment \
  --image us.icr.io/lendyr/lendyr-transaction-cron:latest
```

## Troubleshooting

### Job Fails to Run

1. Check the job run logs:
   ```bash
   ibmcloud ce jobrun logs --jobrun <failed-jobrun-name>
   ```

2. Verify DB2 credentials:
   ```bash
   ibmcloud ce secret get --name lendyr-db2-credentials
   ```

3. Test database connectivity:
   ```bash
   ibmcloud ce jobrun submit --job transaction-date-increment --name debug-$(date +%s)
   ```

### Transactions Still Show Future Dates

1. Check if the job ran successfully:
   ```bash
   ibmcloud ce jobrun list | grep transaction-date-increment
   ```

2. Verify the cron schedule:
   ```bash
   ibmcloud ce subscription cron get --name daily-transaction-update
   ```

3. Manually trigger the job:
   ```bash
   ibmcloud ce jobrun submit --job transaction-date-increment --name fix-$(date +%s)
   ```

### Rollback Procedure

If you need to manually adjust transaction dates:

```sql
-- Connect to DB2
db2 connect to BLUDB user <username>

-- Move all transactions back by N days
UPDATE "LENDYR-DEMO".TRANSACTIONS
SET created_at = created_at - 5 DAYS;

COMMIT;
```

## Local Testing

To test the script locally before deploying:

```bash
# 1. Set up environment variables
export DRIVER="{IBM DB2 ODBC DRIVER}"
export DATABASE="BLUDB"
export DSN_HOSTNAME="your-hostname"
export DSN_PORT="50001"
export PROTOCOL="TCPIP"
export USERNAME="your-username"
export PASSWORD="your-password"
export SECURITY="SSL"

# 2. Run the script
python3 scripts/increment_transaction_dates.py
```

## Cron Schedule Reference

The cron schedule `59 23 * * *` means:
- **59**: Minute (11:59 PM)
- **23**: Hour (23:00 = 11 PM in 24-hour format)
- **\***: Every day of the month
- **\***: Every month
- **\***: Every day of the week

Time zone: `America/Los_Angeles` (Pacific Time)

## Integration with Credit History Cron

This job complements the existing credit history cron job:

| Job | Schedule | Purpose |
|-----|----------|---------|
| **Credit History** | 1st of month at midnight | Increments credit score history by 1 month |
| **Transactions** | Daily at 11:59 PM | Keeps most recent transaction dated today |

Both jobs work together to keep the demo data current and realistic.

## Cost Considerations

- **Job Execution**: ~1-2 seconds per run
- **CPU**: 0.25 vCPU
- **Memory**: 0.5 GB
- **Frequency**: Once per day
- **Estimated Monthly Cost**: < $1 USD

## Security Notes

- DB2 credentials are stored in Code Engine secrets
- Secrets are encrypted at rest
- Job runs in isolated containers
- No credentials are logged or exposed

## Next Steps

After deployment:
1. Monitor the first few automatic runs
2. Verify transaction dates are updating correctly
3. Check application behavior with current dates
4. Document any issues or adjustments needed

## Support

For issues or questions:
- Check IBM Cloud Code Engine documentation
- Review job run logs for error details
- Contact the Lendyr development team

## Related Documentation

- [Credit History Cron Deployment](./CREDIT_HISTORY_CRON_DEPLOYMENT.md)
- [Cron Deployment Summary](./CRON_DEPLOYMENT_SUMMARY.md)
- [IBM Cloud Code Engine Jobs](https://cloud.ibm.com/docs/codeengine?topic=codeengine-job-plan)
- [IBM Cloud Code Engine Cron](https://cloud.ibm.com/docs/codeengine?topic=codeengine-subscribing-cron)

---

**Deployment Date**: May 4, 2026  
**Last Updated**: May 4, 2026  
**Version**: 1.0

# Made with Bob