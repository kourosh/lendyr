# Transaction Date Increment Cron Job

## Overview

This cron job automatically updates transaction dates in the Lendyr database to ensure the most recent transaction is always dated today. It runs daily at 11:59 PM Pacific Time.

## Problem Solved

Customer transactions were showing future dates (e.g., transactions dated May 5-8 when the current date is May 4). This happened because:
1. Transaction data was seeded with specific dates during initial setup
2. Unlike credit score history, there was no automated process to keep transaction dates current
3. The system simply displays transactions as stored in the database

## Solution

A daily cron job that:
- Finds the most recent transaction date in the database
- Calculates the difference between that date and today
- Adjusts all transaction dates by that difference
- Ensures the most recent transaction is always dated today
- Maintains the relative spacing between transactions

## Files Created

### Core Scripts
- **`scripts/increment_transaction_dates.py`** - Python script that performs the date updates
- **`scripts/cron_transaction_increment.sh`** - Bash wrapper for cron execution

### Deployment Files
- **`scripts/Dockerfile.transaction-cron`** - Docker container definition
- **`scripts/deploy_transaction_cron.sh`** - Automated deployment script

### Documentation
- **`docs/TRANSACTION_CRON_DEPLOYMENT.md`** - Comprehensive deployment guide
- **`docs/TRANSACTION_CRON_README.md`** - This file

## How It Works

### Algorithm

1. **Query Maximum Date**: Find the most recent transaction date
   ```sql
   SELECT MAX(created_at) FROM TRANSACTIONS
   ```

2. **Calculate Difference**: Determine days between max date and today
   ```python
   days_diff = (today - max_date).days
   ```

3. **Update All Dates**: Increment all transactions by the difference
   ```sql
   UPDATE TRANSACTIONS
   SET created_at = created_at + {days_diff} DAYS
   ```

### Example

**Before (May 4, 2026)**:
- Most recent transaction: May 8, 2026 (4 days in the future)
- Oldest transaction: May 3, 2026

**After running the job**:
- Most recent transaction: May 4, 2026 (today)
- Oldest transaction: April 29, 2026 (5 days ago)

All transactions maintain their relative spacing but shift to be current.

## Schedule

- **Frequency**: Daily
- **Time**: 11:59 PM Pacific Time
- **Cron Expression**: `59 23 * * *`
- **Time Zone**: `America/Los_Angeles`

## Quick Start

### Deploy to IBM Cloud Code Engine

```bash
# Run the automated deployment script
./scripts/deploy_transaction_cron.sh
```

This script will:
1. Build the Docker image
2. Push to IBM Container Registry
3. Create/update the Code Engine job
4. Run a test execution
5. Set up the daily cron schedule

### Manual Deployment

See [`docs/TRANSACTION_CRON_DEPLOYMENT.md`](./TRANSACTION_CRON_DEPLOYMENT.md) for detailed step-by-step instructions.

### Local Testing

```bash
# Set environment variables
export DRIVER="{IBM DB2 ODBC DRIVER}"
export DATABASE="BLUDB"
export DSN_HOSTNAME="your-hostname"
export DSN_PORT="50001"
export PROTOCOL="TCPIP"
export USERNAME="your-username"
export PASSWORD="your-password"
export SECURITY="SSL"

# Run the script
python3 scripts/increment_transaction_dates.py
```

## Monitoring

### View Job Runs

```bash
# List all job runs
ibmcloud ce jobrun list

# View specific run details
ibmcloud ce jobrun get --name <jobrun-name>

# View logs
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

### Manual Trigger

```bash
# Trigger job immediately (for testing)
ibmcloud ce jobrun submit \
  --job transaction-date-increment \
  --name manual-$(date +%s)
```

### Check Schedule

```bash
# View cron subscription
ibmcloud ce subscription cron get --name daily-transaction-update
```

## Integration with Other Cron Jobs

This job works alongside the existing credit history cron job:

| Job | Schedule | Purpose |
|-----|----------|---------|
| **Credit History** | Monthly (1st at midnight) | Increments credit scores by 1 month |
| **Transactions** | Daily (11:59 PM) | Keeps most recent transaction dated today |

Both jobs ensure the Lendyr demo data stays current and realistic.

## Troubleshooting

### Transactions Still Show Future Dates

1. Check if job ran successfully:
   ```bash
   ibmcloud ce jobrun list | grep transaction-date-increment
   ```

2. View the latest job logs:
   ```bash
   ibmcloud ce jobrun logs --jobrun <latest-jobrun-name>
   ```

3. Manually trigger the job:
   ```bash
   ibmcloud ce jobrun submit --job transaction-date-increment --name fix-$(date +%s)
   ```

### Job Fails to Execute

1. Check job configuration:
   ```bash
   ibmcloud ce job get --name transaction-date-increment
   ```

2. Verify DB2 credentials:
   ```bash
   ibmcloud ce secret get --name lendyr-db2-credentials
   ```

3. Review error logs:
   ```bash
   ibmcloud ce jobrun logs --jobrun <failed-jobrun-name>
   ```

## Cost

- **Execution Time**: ~1-2 seconds per run
- **CPU**: 0.25 vCPU
- **Memory**: 0.5 GB
- **Frequency**: Once per day
- **Estimated Monthly Cost**: < $1 USD

## Security

- DB2 credentials stored in Code Engine secrets (encrypted at rest)
- Job runs in isolated containers
- No credentials logged or exposed
- Read-only access to transaction data (only updates dates)

## Maintenance

### Update the Script

1. Modify `scripts/increment_transaction_dates.py`
2. Run deployment script:
   ```bash
   ./scripts/deploy_transaction_cron.sh
   ```

### Change Schedule

```bash
# Update cron schedule
ibmcloud ce subscription cron update \
  --name daily-transaction-update \
  --schedule "0 0 * * *"  # Example: midnight instead of 11:59 PM
```

### Disable Job

```bash
# Delete cron subscription (job remains, just won't run automatically)
ibmcloud ce subscription cron delete --name daily-transaction-update
```

### Re-enable Job

```bash
# Recreate cron subscription
ibmcloud ce subscription cron create \
  --name daily-transaction-update \
  --destination transaction-date-increment \
  --schedule "59 23 * * *" \
  --time-zone "America/Los_Angeles" \
  --destination-type job
```

## Related Documentation

- [Transaction Cron Deployment Guide](./TRANSACTION_CRON_DEPLOYMENT.md) - Detailed deployment instructions
- [Credit History Cron Deployment](./CREDIT_HISTORY_CRON_DEPLOYMENT.md) - Related cron job
- [Cron Deployment Summary](./CRON_DEPLOYMENT_SUMMARY.md) - Overview of all cron jobs

## Support

For issues or questions:
- Review the deployment guide
- Check IBM Cloud Code Engine documentation
- Contact the Lendyr development team

---

**Created**: May 4, 2026  
**Last Updated**: May 4, 2026  
**Version**: 1.0

# Made with Bob