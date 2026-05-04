#!/bin/bash
#
# Cron Job Wrapper for Transaction Date Increment
# This script loads environment variables and runs the Python script
#
# Usage in crontab:
#   59 23 * * * /path/to/cron_transaction_increment.sh >> /var/log/transaction_increment.log 2>&1
#
# This runs at 11:59 PM every day to ensure the most recent transaction is dated today

# Set the working directory to the project root
cd "$(dirname "$0")/.." || exit 1

# Load environment variables from .env file if it exists
if [ -f "lendyr_code_engine/.env" ]; then
    export $(grep -v '^#' lendyr_code_engine/.env | xargs)
fi

# Run the Python script
python3 scripts/increment_transaction_dates.py

# Capture exit code
EXIT_CODE=$?

# Log completion
if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transaction date increment completed successfully"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transaction date increment failed with exit code $EXIT_CODE" >&2
fi

exit $EXIT_CODE

# Made with Bob