#!/bin/bash
# Revert Orchestrate Configuration
# This script cleans up the orchestrate cache to fix issues caused by the -d flag

set -e

echo "🔄 Reverting Orchestrate Configuration"
echo "======================================"
echo ""

# Stop any running containers
echo "🛑 Stopping orchestrate containers..."
if [ -f ~/.cache/orchestrate/docker-compose.yml ]; then
    docker-compose -f ~/.cache/orchestrate/docker-compose.yml down 2>/dev/null || true
fi

# Backup current cache (just in case)
echo "💾 Creating backup of current cache..."
BACKUP_DIR=~/.cache/orchestrate_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
cp -r ~/.cache/orchestrate/* "$BACKUP_DIR/" 2>/dev/null || true
echo "   Backup saved to: $BACKUP_DIR"

# Remove the corrupted cache
echo "🗑️  Removing corrupted orchestrate cache..."
rm -rf ~/.cache/orchestrate/docker-compose.yml
rm -rf ~/.cache/orchestrate/merged.env

echo "✅ Cache cleaned!"
echo ""
echo "Next steps:"
echo "1. Restart orchestrate WITHOUT the -d flag:"
echo "   orchestrate server start -e ~/.env"
echo ""
echo "   OR for testing:"
echo "   orchestrate test"
echo ""
echo "2. The orchestrate command will regenerate the configuration correctly"
echo ""
echo "Note: Your backup is saved at: $BACKUP_DIR"

# Made with Bob
