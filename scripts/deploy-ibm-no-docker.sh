#!/bin/bash
# Script to deploy lendyr_code_engine to IBM Cloud Code Engine WITHOUT Docker
# Uses Code Engine's built-in build service instead of local Docker

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Lendyr Code Engine - Docker-Free Deployment ===${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found in current directory${NC}"
    exit 1
fi

# Load environment variables from .env file
echo -e "${BLUE}Loading environment variables from .env...${NC}"
set -a  # automatically export all variables
source .env
set +a  # stop automatically exporting

# Check for IBM Cloud API Key
if [ -z "${IBM_CLOUD_API_KEY}" ]; then
    echo -e "${RED}Error: IBM_CLOUD_API_KEY not found in .env file${NC}"
    echo "Please add your IBM Cloud API key to the .env file:"
    echo "IBM_CLOUD_API_KEY=your_api_key_here"
    exit 1
fi

# Configuration variables
PROJECT_NAME="gartner-demo"
APP_NAME="lendyr-db2-api"
REGION="${IBM_REGION:-us-south}"
RESOURCE_GROUP="gartner_demo"
SECRET_NAME="${IBM_SECRET_NAME:-${APP_NAME}-env}"

echo -e "${BLUE}Deployment Configuration:${NC}"
echo "  Project: ${PROJECT_NAME}"
echo "  App Name: ${APP_NAME}"
echo "  Region: ${REGION}"
echo "  Resource Group: ${RESOURCE_GROUP}"
echo "  Build Method: Code Engine Build Service (no Docker required)"
echo ""

# Check if IBM Cloud CLI is installed
if ! command -v ibmcloud &> /dev/null; then
    echo -e "${RED}Error: IBM Cloud CLI is not installed${NC}"
    echo "Install from: https://cloud.ibm.com/docs/cli"
    exit 1
fi

# Check if Code Engine plugin is installed
if ! ibmcloud plugin list | grep -q "code-engine"; then
    echo -e "${YELLOW}Code Engine plugin not found. Installing...${NC}"
    ibmcloud plugin install code-engine
fi

# Login to IBM Cloud using API key
echo -e "${BLUE}Logging in to IBM Cloud with API key...${NC}"
ibmcloud login --apikey "${IBM_CLOUD_API_KEY}" -r ${REGION} -g ${RESOURCE_GROUP}

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to login to IBM Cloud${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Successfully logged in to IBM Cloud${NC}"

# Target the resource group explicitly
echo -e "${BLUE}Targeting resource group...${NC}"
ibmcloud target -g ${RESOURCE_GROUP}

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to target resource group${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Resource group targeted successfully${NC}"

# Select Code Engine project
echo -e "${BLUE}Selecting Code Engine project...${NC}"
if ibmcloud ce project get --name ${PROJECT_NAME} &> /dev/null; then
    ibmcloud ce project select --name ${PROJECT_NAME}
    echo -e "${GREEN}✓ Project selected${NC}"
else
    echo -e "${RED}✗ Project ${PROJECT_NAME} not found${NC}"
    exit 1
fi

# Create or update Code Engine secret for application environment
echo -e "${BLUE}Creating or updating Code Engine secret...${NC}"
SECRET_TMP_FILE=$(mktemp)
cat > "${SECRET_TMP_FILE}" <<EOF
DRIVER=${DRIVER}
DATABASE=${DATABASE}
DSN_HOSTNAME=${DSN_HOSTNAME}
DSN_PORT=${DSN_PORT}
PROTOCOL=${PROTOCOL}
USERNAME=${USERNAME}
PASSWORD=${PASSWORD}
SECURITY=${SECURITY}
EOF

if ibmcloud ce secret get --name ${SECRET_NAME} &> /dev/null; then
    ibmcloud ce secret delete --name ${SECRET_NAME} --force
fi

ibmcloud ce secret create --name ${SECRET_NAME} --from-env-file "${SECRET_TMP_FILE}"
rm -f "${SECRET_TMP_FILE}"
echo -e "${GREEN}✓ Secret created${NC}"

# Update application using Code Engine's build service
echo -e "${BLUE}Updating application with Code Engine build service...${NC}"
echo -e "${YELLOW}This will build from source code (no Docker needed)${NC}"

if ibmcloud ce app get --name ${APP_NAME} &> /dev/null; then
    echo "Updating existing application..."
    ibmcloud ce app update --name ${APP_NAME} \
        --build-source . \
        --env-from-secret ${SECRET_NAME} \
        --port 8080 \
        --min-scale 1 \
        --max-scale 3 \
        --cpu 0.5 \
        --memory 1G \
        --wait \
        --wait-timeout 600
else
    echo -e "${RED}✗ Application ${APP_NAME} not found${NC}"
    echo "Use the original deploy-ibm.sh script to create the app initially"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Application deployed successfully${NC}"
    echo ""
    echo -e "${BLUE}Getting application URL...${NC}"
    APP_URL=$(ibmcloud ce app get --name ${APP_NAME} --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)
    
    if [ -n "$APP_URL" ]; then
        echo -e "${GREEN}Application URL: ${APP_URL}${NC}"
        echo -e "${GREEN}Health check: ${APP_URL}/health${NC}"
        echo -e "${GREEN}API docs: ${APP_URL}/docs${NC}"
        echo ""
        echo -e "${BLUE}Testing new customer_id endpoint...${NC}"
        curl -s "${APP_URL}/customers/by-id/846302" | head -20
    fi
    
    echo ""
    echo -e "${BLUE}Useful commands:${NC}"
    echo "  View logs: ibmcloud ce app logs --name ${APP_NAME}"
    echo "  Get app details: ibmcloud ce app get --name ${APP_NAME}"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi

# Made with Bob
