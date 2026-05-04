# Credit History Cron Job Deployment Summary

## Deployment Date
May 4, 2026

## Deployed To
- **IBM Cloud Account**: Jason Leiby (Jason.Leiby@ibm.com)
- **Account ID**: Kourosh Karimkhany's Account (af05e647086dd5f0b8ec432b4bde5dac)
- **Region**: us-south
- **Resource Group**: Default

## Deployment Details

### Code Engine Project
- **Project Name**: lendyr-cron-jobs
- **Project ID**: 018ae2e4-7574-4764-8ee2-70c321c285e2
- **Status**: Active

### Container Image
- **Image**: us.icr.io/lendyr/lendyr-credit-history-cron:latest
- **Registry**: IBM Container Registry (us.icr.io)
- **Namespace**: lendyr
- **Build Status**: Succeeded
- **Image Digest**: sha256:0c83617abe16a7d193ecdd85af630f1b14ebd7f3343a8ca5d31305896e1fea6e

### Secrets Created
- **Registry Secret**: icr-lendyr (for pulling images from IBM Container Registry)
- **DB2 Credentials Secret**: lendyr-db2-credentials (contains DB2 connection details)

### Job Configuration
- **Job Name**: credit-history-increment
- **CPU**: 0.25 vCPU
- **Memory**: 0.5 GB
- **Max Execution Time**: 300 seconds (5 minutes)
- **Environment Variables**: Loaded from secret `lendyr-db2-credentials`

### Cron Subscription
- **Subscription Name**: monthly-credit-history
- **Schedule**: `0 0 1 * *` (Midnight on the 1st of every month)
- **Time Zone**: America/Los_Angeles (Pacific Time)
- **Destination**: credit-history-increment (job)
- **Status**: Ready

## Test Results

### Manual Test Run
- **Test Run Name**: test-run-1777901468
- **Status**: Succeeded
- **Records Updated**: 60 credit score history records
- **Execution Time**: ~1 second
- **Log Output**:
  ```
  [2026-05-04T13:31:21.629294] Starting credit score history date increment
  [2026-05-04T13:31:22.377306] Connected to database successfully
  [2026-05-04T13:31:22.377341] Executing date increment...
  [2026-05-04T13:31:22.616021] Successfully incremented 60 credit score history records
  [2026-05-04T13:31:22.616067] All credit score dates have been moved forward by one month
  [2026-05-04T13:31:22.654446] Credit score history date increment completed successfully
  ```

## What the Cron Job Does

The cron job automatically increments all credit score history dates by one month on the 1st of every month at midnight Pacific Time. This keeps the 6-month rolling window of credit history data current without manual intervention.

**Example**: If a customer has a credit score of 742 for April, after the job runs, that score becomes the May score.

## Monitoring and Management

### View Job Runs
```bash
ibmcloud ce jobrun list
```

### View Specific Job Run Details
```bash
ibmcloud ce jobrun get --name <jobrun-name>
```

### View Job Run Logs
```bash
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

### View Cron Subscription Status
```bash
ibmcloud ce subscription cron get --name monthly-credit-history
```

### Manually Trigger the Job (for testing)
```bash
ibmcloud ce jobrun submit --job credit-history-increment --name manual-test-$(date +%s)
```

### View Job Configuration
```bash
ibmcloud ce job get --name credit-history-increment
```

## Next Scheduled Run

The job will run automatically on **June 1, 2026 at 12:00 AM Pacific Time**.

## Troubleshooting

If the job fails:

1. Check the job run logs:
   ```bash
   ibmcloud ce jobrun logs --jobrun <failed-jobrun-name>
   ```

2. Verify DB2 credentials are correct:
   ```bash
   ibmcloud ce secret get --name lendyr-db2-credentials
   ```

3. Test database connectivity by running a manual job:
   ```bash
   ibmcloud ce jobrun submit --job credit-history-increment --name debug-run-$(date +%s)
   ```

4. Check Code Engine events:
   ```bash
   ibmcloud ce jobrun events --jobrun <jobrun-name>
   ```

## Rollback Procedure

If you need to roll back the date increment in the database:

```sql
-- Connect to DB2
db2 connect to BLUDB user 43cdccd2

-- Decrement all dates by one month
UPDATE "LENDYR-DEMO".CREDIT_SCORE_HISTORY
SET score_date = ADD_MONTHS(score_date, -1);

COMMIT;
```

## Files Modified During Deployment

- **scripts/Dockerfile.cron**: Added `libxml2` library dependency to fix import error

## Resources

- [IBM Cloud Code Engine Documentation](https://cloud.ibm.com/docs/codeengine)
- [Code Engine Jobs](https://cloud.ibm.com/docs/codeengine?topic=codeengine-job-plan)
- [Code Engine Cron Subscriptions](https://cloud.ibm.com/docs/codeengine?topic=codeengine-subscribing-cron)
- [Original Deployment Guide](./CREDIT_HISTORY_CRON_DEPLOYMENT.md)

## Contact

For issues or questions about this deployment, contact the Lendyr development team.