# Credit History Date Increment Cron Job Deployment Guide

## Overview

This document provides instructions for deploying a monthly cron job that increments credit score history dates by one month. This keeps the 6 months of historical credit data current without requiring manual updates.

## What It Does

The cron job runs on the 1st of every month at midnight and:
1. Connects to the Lendyr DB2 database
2. Increments all `score_date` values in the `CREDIT_SCORE_HISTORY` table by one month
3. Logs the operation results
4. Maintains the rolling 6-month window of credit history data

**Example**: If April's credit score is 742, after running the job, that score becomes May's score.

## Files Involved

- **`scripts/increment_credit_history_dates.py`** - Python script that performs the database update
- **`scripts/cron_credit_history_increment.sh`** - Bash wrapper script for cron execution
- **`lendyr_code_engine/.env`** - Environment variables (DB2 connection details)

## Prerequisites

1. IBM Cloud account with access to the Lendyr DB2 database
2. Python 3.8+ installed
3. `ibm_db` Python package installed
4. DB2 connection credentials configured in environment variables

## Deployment Options

### Option 1: IBM Cloud Code Engine (Recommended)

IBM Cloud Code Engine supports scheduled jobs that can run on a cron schedule.

#### Step 1: Create a Code Engine Project

```bash
# Login to IBM Cloud
ibmcloud login

# Target your resource group
ibmcloud target -g <resource-group-name>

# Create or select a Code Engine project
ibmcloud ce project create --name lendyr-cron-jobs
ibmcloud ce project select --name lendyr-cron-jobs
```

#### Step 2: Build and Push Container Image

Create a `Dockerfile` for the cron job:

```dockerfile
FROM python:3.11-slim

# Install DB2 dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install IBM DB2 driver
RUN wget https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/linuxx64_odbc_cli.tar.gz \
    && tar -xzf linuxx64_odbc_cli.tar.gz -C /opt \
    && rm linuxx64_odbc_cli.tar.gz

ENV IBM_DB_HOME=/opt/clidriver
ENV LD_LIBRARY_PATH=/opt/clidriver/lib:$LD_LIBRARY_PATH

# Install Python dependencies
COPY scripts/requirements_cron.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy script
COPY scripts/increment_credit_history_dates.py /app/increment_credit_history_dates.py

WORKDIR /app

CMD ["python", "increment_credit_history_dates.py"]
```

Create `scripts/requirements_cron.txt`:

```
ibm_db>=3.1.0
python-dotenv>=1.0.0
```

Build and push the image:

```bash
# Build the image
ibmcloud ce build create --name credit-history-cron-build \
  --source . \
  --dockerfile Dockerfile \
  --image us.icr.io/<namespace>/lendyr-credit-history-cron:latest

# Or use Docker directly
docker build -t us.icr.io/<namespace>/lendyr-credit-history-cron:latest .
docker push us.icr.io/<namespace>/lendyr-credit-history-cron:latest
```

#### Step 3: Create Environment Variables

```bash
# Create a secret for DB2 credentials
ibmcloud ce secret create --name lendyr-db2-credentials \
  --from-literal DB2_HOST=<your-db2-host> \
  --from-literal DB2_PORT=<your-db2-port> \
  --from-literal DB2_DATABASE=<your-db2-database> \
  --from-literal DB2_USERNAME=<your-db2-username> \
  --from-literal DB2_PASSWORD=<your-db2-password>
```

#### Step 4: Create the Scheduled Job

```bash
# Create a job that runs on the 1st of every month at midnight UTC
ibmcloud ce job create --name credit-history-increment \
  --image us.icr.io/<namespace>/lendyr-credit-history-cron:latest \
  --env-from-secret lendyr-db2-credentials \
  --cpu 0.25 \
  --memory 0.5G \
  --maxexecutiontime 300

# Create a subscription to run the job monthly
ibmcloud ce subscription cron create --name monthly-credit-history \
  --destination credit-history-increment \
  --schedule "0 0 1 * *" \
  --time-zone "America/Los_Angeles"
```

#### Step 5: Test the Job

```bash
# Run the job manually to test
ibmcloud ce jobrun submit --job credit-history-increment --name test-run-$(date +%s)

# Check the logs
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

### Option 2: Traditional Cron on Linux Server

If deploying to a traditional Linux server with cron:

#### Step 1: Install Dependencies

```bash
# Install Python and pip
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install DB2 driver
wget https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/linuxx64_odbc_cli.tar.gz
tar -xzf linuxx64_odbc_cli.tar.gz -C /opt
export IBM_DB_HOME=/opt/clidriver
export LD_LIBRARY_PATH=/opt/clidriver/lib:$LD_LIBRARY_PATH

# Install Python dependencies
pip3 install ibm_db python-dotenv
```

#### Step 2: Configure Environment Variables

Create `/etc/lendyr/.env`:

```bash
DB2_HOST=your-db2-host
DB2_PORT=50000
DB2_DATABASE=your-database
DB2_USERNAME=your-username
DB2_PASSWORD=your-password
```

Secure the file:

```bash
sudo chmod 600 /etc/lendyr/.env
sudo chown root:root /etc/lendyr/.env
```

#### Step 3: Deploy Scripts

```bash
# Copy scripts to a permanent location
sudo mkdir -p /opt/lendyr/scripts
sudo cp scripts/increment_credit_history_dates.py /opt/lendyr/scripts/
sudo cp scripts/cron_credit_history_increment.sh /opt/lendyr/scripts/
sudo chmod +x /opt/lendyr/scripts/cron_credit_history_increment.sh

# Update the wrapper script to use the correct .env path
sudo sed -i 's|lendyr_code_engine/.env|/etc/lendyr/.env|g' /opt/lendyr/scripts/cron_credit_history_increment.sh
```

#### Step 4: Configure Cron

```bash
# Edit crontab
sudo crontab -e

# Add this line to run on the 1st of every month at midnight
0 0 1 * * /opt/lendyr/scripts/cron_credit_history_increment.sh >> /var/log/lendyr/credit_history_increment.log 2>&1

# Create log directory
sudo mkdir -p /var/log/lendyr
sudo chmod 755 /var/log/lendyr
```

#### Step 5: Test the Cron Job

```bash
# Run manually to test
sudo /opt/lendyr/scripts/cron_credit_history_increment.sh

# Check the log
tail -f /var/log/lendyr/credit_history_increment.log
```

## Monitoring and Maintenance

### Check Job Status (Code Engine)

```bash
# List recent job runs
ibmcloud ce jobrun list

# Get details of a specific run
ibmcloud ce jobrun get --name <jobrun-name>

# View logs
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

### Check Cron Status (Traditional Server)

```bash
# View cron logs
tail -f /var/log/lendyr/credit_history_increment.log

# Check if cron job is scheduled
sudo crontab -l

# View system cron logs
grep CRON /var/log/syslog
```

### Verify Database Updates

After the job runs, verify the dates were incremented:

```sql
-- Connect to DB2
db2 connect to <database> user <username>

-- Check the date range
SELECT 
    MIN(score_date) as earliest_date,
    MAX(score_date) as latest_date,
    COUNT(*) as total_records
FROM "LENDYR-DEMO".CREDIT_SCORE_HISTORY;

-- View sample records
SELECT customer_id, score_date, credit_score
FROM "LENDYR-DEMO".CREDIT_SCORE_HISTORY
ORDER BY customer_id, score_date DESC
FETCH FIRST 20 ROWS ONLY;
```

## Troubleshooting

### Issue: Job Fails with Connection Error

**Solution**: Verify DB2 credentials and network connectivity

```bash
# Test DB2 connection
python3 -c "
import ibm_db
import os
conn_str = f'DATABASE={os.getenv(\"DB2_DATABASE\")};HOSTNAME={os.getenv(\"DB2_HOST\")};PORT={os.getenv(\"DB2_PORT\")};PROTOCOL=TCPIP;UID={os.getenv(\"DB2_USERNAME\")};PWD={os.getenv(\"DB2_PASSWORD\")};'
conn = ibm_db.connect(conn_str, '', '')
print('Connection successful!')
ibm_db.close(conn)
"
```

### Issue: Job Runs But No Records Updated

**Solution**: Check SQL syntax and table permissions

```bash
# Run the script with verbose logging
python3 scripts/increment_credit_history_dates.py
```

### Issue: Cron Job Not Running

**Solution**: Check cron service and permissions

```bash
# Check if cron is running
sudo systemctl status cron

# Verify crontab syntax
sudo crontab -l

# Check cron logs
grep CRON /var/log/syslog | tail -20
```

## Rollback Procedure

If you need to roll back the date increment:

```sql
-- Decrement all dates by one month
UPDATE "LENDYR-DEMO".CREDIT_SCORE_HISTORY
SET score_date = ADD_MONTHS(score_date, -1);

COMMIT;
```

## Security Considerations

1. **Credentials**: Store DB2 credentials in IBM Cloud Secrets Manager or environment variables, never in code
2. **Access Control**: Limit database user permissions to only UPDATE on CREDIT_SCORE_HISTORY table
3. **Logging**: Ensure logs don't contain sensitive information
4. **Monitoring**: Set up alerts for job failures

## Support

For issues or questions:
- Check logs first: `/var/log/lendyr/credit_history_increment.log` or Code Engine logs
- Verify database connectivity and credentials
- Review the Python script for error messages
- Contact the Lendyr development team

## Schedule Reference

The cron schedule `0 0 1 * *` means:
- Minute: 0 (at the top of the hour)
- Hour: 0 (midnight)
- Day of Month: 1 (first day)
- Month: * (every month)
- Day of Week: * (any day)

**Result**: Runs at midnight on the 1st of every month