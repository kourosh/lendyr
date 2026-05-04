#!/bin/bash
#
# Cron Job Wrapper for Credit Score History Date Increment
# This script loads environment variables and runs the Python script
#
# Usage in crontab:
#   0 0 1 * * /path/to/cron_credit_history_increment.sh >> /var/log/credit_history_increment.log 2>&1
#

# Set the working directory to the project root
cd "$(dirname "$0")/.." || exit 1

# Load environment variables from .env file if it exists
if [ -f "lendyr_code_engine/.env" ]; then
    export $(grep -v '^#' lendyr_code_engine/.env | xargs)
fi

# Run the Python script
python3 scripts/increment_credit_history_dates.py

# Capture exit code
EXIT_CODE=$?

# Log completion
if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Credit history date increment completed successfully"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Credit history date increment failed with exit code $EXIT_CODE" >&2
fi

exit $EXIT_CODE

# Made with Bob
