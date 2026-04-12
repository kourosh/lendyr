#!/bin/bash
# Script to deploy lendyr_code_engine to IBM Cloud Code Engine
# Uses environment variables from .env file

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Lendyr Code Engine - IBM Cloud Deployment ===${NC}"

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

# Configuration variables - modify these as needed
PROJECT_NAME="gartner-demo"
APP_NAME="lendyr-db2-api"
REGION="${IBM_REGION:-us-south}"
REGISTRY="${IBM_REGISTRY:-us.icr.io}"
NAMESPACE="${IBM_NAMESPACE:-lendyr}"
RESOURCE_GROUP="gartner_demo"
IMAGE_NAME="${REGISTRY}/${NAMESPACE}/${APP_NAME}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

SECRET_NAME="${IBM_SECRET_NAME:-${APP_NAME}-env}"
REGISTRY_SECRET_NAME="${APP_NAME}-registry-secret"

echo -e "${BLUE}Deployment Configuration:${NC}"
echo "  Project: ${PROJECT_NAME}"
echo "  App Name: ${APP_NAME}"
echo "  Region: ${REGION}"
echo "  Resource Group: ${RESOURCE_GROUP}"
echo "  Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "  Secret: ${SECRET_NAME}"
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

# Check if Container Registry plugin is installed
if ! ibmcloud plugin list | grep -q "container-registry"; then
    echo -e "${YELLOW}Container Registry plugin not found. Installing...${NC}"
    ibmcloud plugin install container-registry
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
    echo -e "${YELLOW}Available resource groups:${NC}"
    ibmcloud resource groups
    exit 1
fi
echo -e "${GREEN}✓ Resource group targeted successfully${NC}"

# Build and push Docker image to IBM Container Registry
echo -e "${BLUE}Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Docker build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker image built successfully${NC}"

# Log in to IBM Container Registry
echo -e "${BLUE}Logging in to IBM Container Registry...${NC}"
ibmcloud cr login

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to login to Container Registry${NC}"
    exit 1
fi

# Create namespace if it doesn't exist
echo -e "${BLUE}Ensuring Container Registry namespace exists...${NC}"
if ibmcloud cr namespace-list | grep -q "^${NAMESPACE}$"; then
    echo -e "${GREEN}✓ Namespace '${NAMESPACE}' already exists${NC}"
else
    echo "Creating namespace '${NAMESPACE}'..."
    ibmcloud cr namespace-add ${NAMESPACE} -g ${RESOURCE_GROUP}
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to create namespace${NC}"
        echo -e "${YELLOW}Available namespaces:${NC}"
        ibmcloud cr namespace-list
        exit 1
    fi
    echo -e "${GREEN}✓ Namespace created successfully${NC}"
fi

# Push image to registry
echo -e "${BLUE}Pushing image to IBM Container Registry...${NC}"
docker push ${IMAGE_NAME}:${IMAGE_TAG}

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to push image to registry${NC}"
    echo -e "${YELLOW}Checking namespace permissions...${NC}"
    ibmcloud cr namespace-list
    exit 1
fi
echo -e "${GREEN}✓ Image pushed successfully${NC}"

# Select or create Code Engine project
echo -e "${BLUE}Setting up Code Engine project...${NC}"
if ibmcloud ce project get --name ${PROJECT_NAME} &> /dev/null; then
    echo "Project ${PROJECT_NAME} exists, selecting it..."
    ibmcloud ce project select --name ${PROJECT_NAME}
else
    echo "Creating new project ${PROJECT_NAME}..."
    ibmcloud ce project create --name ${PROJECT_NAME}
    ibmcloud ce project select --name ${PROJECT_NAME}
fi

# Create or update registry access secret for Code Engine to pull images
echo -e "${BLUE}Creating or updating registry access secret...${NC}"
if ibmcloud ce registry get --name ${REGISTRY_SECRET_NAME} &> /dev/null; then
    echo "Registry secret exists, deleting to recreate..."
    ibmcloud ce registry delete --name ${REGISTRY_SECRET_NAME} --force
fi

echo "Creating registry access secret..."
ibmcloud ce registry create --name ${REGISTRY_SECRET_NAME} \
    --server ${REGISTRY} \
    --username iamapikey \
    --password "${IBM_CLOUD_API_KEY}"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to create registry access secret${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Registry access secret created successfully${NC}"

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

# Check if application exists
if ibmcloud ce app get --name ${APP_NAME} &> /dev/null; then
    echo -e "${BLUE}Updating existing application...${NC}"
    ibmcloud ce app update --name ${APP_NAME} \
        --image ${IMAGE_NAME}:${IMAGE_TAG} \
        --registry-secret ${REGISTRY_SECRET_NAME} \
        --env-from-secret ${SECRET_NAME} \
        --port 8080 \
        --min-scale 1 \
        --max-scale 3 \
        --cpu 0.5 \
        --memory 1G
else
    echo -e "${BLUE}Creating new application...${NC}"
    ibmcloud ce app create --name ${APP_NAME} \
        --image ${IMAGE_NAME}:${IMAGE_TAG} \
        --registry-secret ${REGISTRY_SECRET_NAME} \
        --env-from-secret ${SECRET_NAME} \
        --port 8080 \
        --min-scale 1 \
        --max-scale 3 \
        --cpu 0.5 \
        --memory 1G
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
    fi
    
    echo ""
    echo -e "${BLUE}Useful commands:${NC}"
    echo "  View logs: ibmcloud ce app logs --name ${APP_NAME}"
    echo "  Get app details: ibmcloud ce app get --name ${APP_NAME}"
    echo "  Delete app: ibmcloud ce app delete --name ${APP_NAME}"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi

# Made with Bob
