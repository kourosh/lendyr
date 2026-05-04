#!/bin/bash

# Deploy Lendyr Assets to TechZone Environment
# This script sets up the TechZone environment and imports all assets

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Lendyr TechZone Deployment Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print info messages
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if orchestrate CLI is available
if ! command -v orchestrate &> /dev/null; then
    print_error "orchestrate CLI not found. Please install the IBM watsonx Orchestrate ADK."
    exit 1
fi

print_success "orchestrate CLI found"

# ========================================
# STEP 1: Environment Setup
# ========================================
print_section "Step 1: Setting up TechZone Environment"

# Check if techzone environment already exists
if orchestrate env list | grep -q "techzone"; then
    print_info "TechZone environment already exists"
else
    print_info "Adding TechZone environment..."
    
    # Prompt for environment details
    echo ""
    echo -e "${YELLOW}Please provide TechZone environment details:${NC}"
    echo ""
    
    read -p "Enter TechZone instance URL: " TECHZONE_URL
    read -p "Enter environment type (ibm_iam/mcsp/cpd) [default: ibm_iam]: " ENV_TYPE
    ENV_TYPE=${ENV_TYPE:-ibm_iam}
    
    # Add the environment
    if orchestrate env add -n techzone -u "$TECHZONE_URL" -t "$ENV_TYPE"; then
        print_success "TechZone environment added successfully"
    else
        print_error "Failed to add TechZone environment"
        exit 1
    fi
fi

# ========================================
# STEP 2: Activate TechZone Environment
# ========================================
print_section "Step 2: Activating TechZone Environment"

echo ""
echo -e "${YELLOW}Authenticating to TechZone environment...${NC}"
echo -e "${YELLOW}You will be prompted for your API key.${NC}"
echo ""

if orchestrate env activate techzone; then
    print_success "TechZone environment activated"
else
    print_error "Failed to activate TechZone environment"
    exit 1
fi

# Verify active environment
ACTIVE_ENV=$(orchestrate env list | grep "(active)" | awk '{print $1}')
if [ "$ACTIVE_ENV" != "techzone" ]; then
    print_error "TechZone environment is not active. Current: $ACTIVE_ENV"
    exit 1
fi

print_success "Confirmed TechZone environment is active"

# ========================================
# STEP 3: Import Tools
# ========================================
print_section "Step 3: Importing Tools"

TOOLS_DIR="$PROJECT_ROOT/tools"
TOOL_COUNT=0
TOOL_SUCCESS=0
TOOL_FAILED=0

if [ -d "$TOOLS_DIR" ]; then
    # Import Python tools (files with .py extension in subdirectories)
    print_info "Scanning for Python tools..."
    while IFS= read -r -d '' tool_dir; do
        tool_name=$(basename "$tool_dir")
        
        # Skip archived tools
        if [[ "$tool_dir" == *"archived"* ]]; then
            continue
        fi
        
        # Look for Python files in the tool directory
        if [ -f "$tool_dir/${tool_name}.py" ]; then
            TOOL_COUNT=$((TOOL_COUNT + 1))
            print_info "Importing Python tool: $tool_name"
            
            # Check if requirements.txt exists
            if [ -f "$tool_dir/requirements.txt" ]; then
                if orchestrate tools import -k python -f "$tool_dir/${tool_name}.py" -r "$tool_dir/requirements.txt"; then
                    print_success "Imported Python tool: $tool_name (with requirements)"
                    TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
                else
                    print_error "Failed to import Python tool: $tool_name"
                    TOOL_FAILED=$((TOOL_FAILED + 1))
                fi
            else
                if orchestrate tools import -k python -f "$tool_dir/${tool_name}.py"; then
                    print_success "Imported Python tool: $tool_name"
                    TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
                else
                    print_error "Failed to import Python tool: $tool_name"
                    TOOL_FAILED=$((TOOL_FAILED + 1))
                fi
            fi
        fi
    done < <(find "$TOOLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0)
    
    # Import OpenAPI tools (JSON files in subdirectories)
    print_info "Scanning for OpenAPI tools..."
    while IFS= read -r -d '' openapi_file; do
        tool_dir=$(dirname "$openapi_file")
        tool_name=$(basename "$tool_dir")
        
        # Skip archived tools
        if [[ "$tool_dir" == *"archived"* ]]; then
            continue
        fi
        
        TOOL_COUNT=$((TOOL_COUNT + 1))
        print_info "Importing OpenAPI tool: $tool_name"
        
        if orchestrate tools import -k openapi -f "$openapi_file"; then
            print_success "Imported OpenAPI tool: $tool_name"
            TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
        else
            print_error "Failed to import OpenAPI tool: $tool_name"
            TOOL_FAILED=$((TOOL_FAILED + 1))
        fi
    done < <(find "$TOOLS_DIR" -mindepth 2 -maxdepth 2 -name "*.json" -print0)
    
    # Import Flow tools (JSON files with "flow" in the name at root level)
    print_info "Scanning for Flow tools..."
    while IFS= read -r -d '' flow_file; do
        flow_name=$(basename "$flow_file" .json)
        
        TOOL_COUNT=$((TOOL_COUNT + 1))
        print_info "Importing Flow tool: $flow_name"
        
        if orchestrate tools import -k flow -f "$flow_file"; then
            print_success "Imported Flow tool: $flow_name"
            TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
        else
            print_error "Failed to import Flow tool: $flow_name"
            TOOL_FAILED=$((TOOL_FAILED + 1))
        fi
    done < <(find "$TOOLS_DIR" -maxdepth 1 -name "*flow*.json" -print0)
    
    print_info "Tools imported: $TOOL_SUCCESS/$TOOL_COUNT successful, $TOOL_FAILED failed"
else
    print_warning "Tools directory not found: $TOOLS_DIR"
fi

# ========================================
# STEP 4: Import Knowledge Bases
# ========================================
print_section "Step 4: Importing Knowledge Bases"

KB_DIR="$PROJECT_ROOT/knowledge_bases"
KB_COUNT=0
KB_SUCCESS=0
KB_FAILED=0

if [ -d "$KB_DIR" ]; then
    print_info "Scanning for knowledge base files..."
    
    while IFS= read -r -d '' kb_file; do
        kb_name=$(basename "$kb_file")
        KB_COUNT=$((KB_COUNT + 1))
        
        print_info "Importing knowledge base: $kb_name"
        
        if orchestrate knowledge-bases import -f "$kb_file"; then
            print_success "Imported knowledge base: $kb_name"
            KB_SUCCESS=$((KB_SUCCESS + 1))
        else
            print_error "Failed to import knowledge base: $kb_name"
            KB_FAILED=$((KB_FAILED + 1))
        fi
    done < <(find "$KB_DIR" -maxdepth 1 -name "*.yaml" -o -name "*.yml" -print0)
    
    print_info "Knowledge bases imported: $KB_SUCCESS/$KB_COUNT successful, $KB_FAILED failed"
else
    print_warning "Knowledge bases directory not found: $KB_DIR"
fi

# ========================================
# STEP 5: Import Connections
# ========================================
print_section "Step 5: Importing Connections"

CONN_DIR="$PROJECT_ROOT/connections"
CONN_COUNT=0
CONN_SUCCESS=0
CONN_FAILED=0

if [ -d "$CONN_DIR" ]; then
    print_info "Scanning for connection files..."
    
    while IFS= read -r -d '' conn_file; do
        conn_name=$(basename "$conn_file")
        CONN_COUNT=$((CONN_COUNT + 1))
        
        print_info "Importing connection: $conn_name"
        
        if orchestrate connections import -f "$conn_file"; then
            print_success "Imported connection: $conn_name"
            CONN_SUCCESS=$((CONN_SUCCESS + 1))
        else
            print_error "Failed to import connection: $conn_name"
            CONN_FAILED=$((CONN_FAILED + 1))
        fi
    done < <(find "$CONN_DIR" -maxdepth 1 -name "*.yaml" -o -name "*.yml" -print0)
    
    if [ $CONN_COUNT -eq 0 ]; then
        print_warning "No connection files found in: $CONN_DIR"
    else
        print_info "Connections imported: $CONN_SUCCESS/$CONN_COUNT successful, $CONN_FAILED failed"
    fi
else
    print_warning "Connections directory not found: $CONN_DIR"
fi

# ========================================
# STEP 6: Import Agents (with dependency handling)
# ========================================
print_section "Step 6: Importing Agents"

AGENTS_DIR="$PROJECT_ROOT/agents"
AGENT_COUNT=0
AGENT_SUCCESS=0
AGENT_FAILED=0

if [ -d "$AGENTS_DIR" ]; then
    print_info "Importing agents in multiple passes to handle dependencies..."
    
    # Create temporary directory for tracking
    TEMP_DIR="/tmp/agent_import_techzone_$$"
    mkdir -p "$TEMP_DIR"
    
    # Create list of all agent files
    find "$AGENTS_DIR" -maxdepth 1 \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.py" \) > "$TEMP_DIR/all_agents.txt"
    AGENT_COUNT=$(wc -l < "$TEMP_DIR/all_agents.txt")
    
    # Copy to pending list
    cp "$TEMP_DIR/all_agents.txt" "$TEMP_DIR/pending_agents.txt"
    
    # Maximum number of passes to prevent infinite loops
    MAX_PASSES=5
    pass=1
    
    while [ $pass -le $MAX_PASSES ] && [ -s "$TEMP_DIR/pending_agents.txt" ]; do
        if [ $pass -gt 1 ]; then
            print_info "Pass $pass: Retrying failed agents..."
        fi
        
        # Clear the retry list
        > "$TEMP_DIR/retry_agents.txt"
        
        # Track if we made progress this pass
        progress_made=0
        
        while IFS= read -r agent_file; do
            agent_name=$(basename "$agent_file")
            
            # Skip if already imported
            if grep -q "^${agent_file}$" "$TEMP_DIR/imported_agents.txt" 2>/dev/null; then
                continue
            fi
            
            print_info "Importing agent: $agent_name"
            
            # Capture output and check for errors
            if orchestrate agents import -f "$agent_file" > "$TEMP_DIR/import_output.log" 2>&1; then
                print_success "Imported agent: $agent_name"
                AGENT_SUCCESS=$((AGENT_SUCCESS + 1))
                echo "$agent_file" >> "$TEMP_DIR/imported_agents.txt"
                progress_made=1
            else
                # Check if it's a dependency error
                if grep -q "Failed to find collaborator" "$TEMP_DIR/import_output.log"; then
                    print_warning "Agent $agent_name has unmet dependencies, will retry"
                    echo "$agent_file" >> "$TEMP_DIR/retry_agents.txt"
                else
                    print_error "Failed to import agent: $agent_name"
                    # Show the actual error message
                    echo -e "${RED}Error details:${NC}"
                    cat "$TEMP_DIR/import_output.log" | grep -E "\[ERROR\]|\[WARNING\]|Error|Failed" | head -5
                    AGENT_FAILED=$((AGENT_FAILED + 1))
                    echo "$agent_file" >> "$TEMP_DIR/failed_agents.txt"
                fi
            fi
        done < "$TEMP_DIR/pending_agents.txt"
        
        # If no progress was made, break to avoid infinite loop
        if [ $progress_made -eq 0 ] && [ -s "$TEMP_DIR/retry_agents.txt" ]; then
            print_warning "No progress made in pass $pass, stopping retries"
            while IFS= read -r agent_file; do
                agent_name=$(basename "$agent_file")
                print_error "Failed to import agent: $agent_name (unresolved dependencies)"
                AGENT_FAILED=$((AGENT_FAILED + 1))
            done < "$TEMP_DIR/retry_agents.txt"
            break
        fi
        
        # Update pending list with retry list
        mv "$TEMP_DIR/retry_agents.txt" "$TEMP_DIR/pending_agents.txt"
        pass=$((pass + 1))
    done
    
    # Clean up temp directory
    rm -rf "$TEMP_DIR"
    
    print_info "Agents imported: $AGENT_SUCCESS/$AGENT_COUNT successful, $AGENT_FAILED failed"
else
    print_warning "Agents directory not found: $AGENTS_DIR"
fi

# ========================================
# Summary
# ========================================
print_section "TechZone Deployment Summary"

TOTAL_COUNT=$((TOOL_COUNT + KB_COUNT + CONN_COUNT + AGENT_COUNT))
TOTAL_SUCCESS=$((TOOL_SUCCESS + KB_SUCCESS + CONN_SUCCESS + AGENT_SUCCESS))
TOTAL_FAILED=$((TOOL_FAILED + KB_FAILED + CONN_FAILED + AGENT_FAILED))

echo ""
echo -e "${BLUE}Environment:${NC}     techzone"
echo -e "${BLUE}Tools:${NC}           $TOOL_SUCCESS/$TOOL_COUNT successful"
echo -e "${BLUE}Knowledge Bases:${NC} $KB_SUCCESS/$KB_COUNT successful"
echo -e "${BLUE}Connections:${NC}     $CONN_SUCCESS/$CONN_COUNT successful"
echo -e "${BLUE}Agents:${NC}          $AGENT_SUCCESS/$AGENT_COUNT successful"
echo ""
echo -e "${BLUE}Total:${NC}           $TOTAL_SUCCESS/$TOTAL_COUNT successful, $TOTAL_FAILED failed"
echo ""

# ========================================
# Post-Deployment Instructions
# ========================================
if [ $TOTAL_SUCCESS -gt 0 ]; then
    print_section "Post-Deployment Steps"
    echo ""
    
    if [ $CONN_SUCCESS -gt 0 ]; then
        print_info "Configure connection credentials:"
        echo "  orchestrate connections configure -a <app_id> --env draft --kind <auth_type> --type team"
        echo "  orchestrate connections set-credentials -a <app_id> --env draft -u <username> -p <password>"
        echo ""
    fi
    
    print_info "Verify imports:"
    echo "  orchestrate tools list"
    echo "  orchestrate knowledge-bases list"
    echo "  orchestrate connections list"
    echo "  orchestrate agents list"
    echo ""
    
    print_info "Test agents in draft environment:"
    echo "  orchestrate agents test -n <agent_name>"
    echo ""
    
    print_info "Deploy agents to live environment:"
    echo "  orchestrate agents deploy -n <agent_name>"
    echo ""
fi

if [ $TOTAL_FAILED -eq 0 ]; then
    print_success "All assets deployed successfully to TechZone!"
    exit 0
else
    print_warning "Some assets failed to deploy. Please review the errors above."
    exit 1
fi

# Made with Bob