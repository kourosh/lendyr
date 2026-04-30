#!/bin/bash
# Re-import all current Lendyr tools and agents into the local watsonx Orchestrate environment.
# Run from the project root: bash scripts/import_local.sh

set -uo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

ORCHESTRATE_BIN="${ORCHESTRATE_BIN:-}"
if [[ -z "$ORCHESTRATE_BIN" ]]; then
    if command -v orchestrate >/dev/null 2>&1; then
        ORCHESTRATE_BIN="$(command -v orchestrate)"
    elif [[ -x "/Users/kk76/.venv/bin/orchestrate" ]]; then
        ORCHESTRATE_BIN="/Users/kk76/.venv/bin/orchestrate"
    else
        echo "Error: orchestrate CLI not found. Install it or set ORCHESTRATE_BIN."
        exit 1
    fi
fi

PASS=0
FAIL=0
FAILURES=()

green='\033[0;32m'
red='\033[0;31m'
yellow='\033[1;33m'
blue='\033[0;34m'
reset='\033[0m'

header() { echo; echo -e "${blue}━━━ $1 ━━━${reset}"; }

run() {
    local label="$1"; shift
    echo -e "${yellow}  importing: $label${reset}"
    if "$ORCHESTRATE_BIN" "$@" 2>&1; then
        echo -e "${green}  ✓ $label${reset}"
        PASS=$((PASS + 1))
    else
        echo -e "${red}  ✗ $label${reset}"
        FAIL=$((FAIL + 1))
        FAILURES+=("$label")
    fi
}

run_if_exists() {
    local label="$1"
    local path="$2"
    shift 2

    if [[ -e "$path" ]]; then
        run "$label" "$@"
    else
        echo -e "${yellow}  skipping: $label (${path} not found)${reset}"
    fi
}

# ── OpenAPI tools ──────────────────────────────────────────────────────────────
header "OpenAPI Tools"

run_if_exists "Customer auth" \
    "tools/customer_auth_tool/customer_auth_openapi.json" \
    tools import -k openapi -f tools/customer_auth_tool/customer_auth_openapi.json

run_if_exists "Get customer by ID" \
    "tools/get_customer_by_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_customer_by_id/lendyr_openapi.json

run_if_exists "Get accounts by customer ID" \
    "tools/get_accounts_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_accounts_by_customer_id/lendyr_openapi.json

run_if_exists "Get account by type and customer ID" \
    "tools/get_account_by_type_and_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_account_by_type_and_customer_id/lendyr_openapi.json

run_if_exists "Get cards by customer ID" \
    "tools/get_cards_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_cards_by_customer_id/lendyr_openapi.json

run_if_exists "Get transactions by customer ID" \
    "tools/get_transactions_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_transactions_by_customer_id/lendyr_openapi.json

run_if_exists "Get disputes by customer ID" \
    "tools/get_disputes_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_disputes_by_customer_id/lendyr_openapi.json

run_if_exists "Get transfers by customer ID" \
    "tools/get_transfers_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/get_transfers_by_customer_id/lendyr_openapi.json

run_if_exists "Transfer money by customer ID" \
    "tools/transfer_money_by_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/transfer_money_by_customer_id/lendyr_openapi.json

run_if_exists "Update card limit" \
    "tools/update_card_limit_cards_card_id_limit_patch/lendyr_openapi.json" \
    tools import -k openapi -f tools/update_card_limit_cards_card_id_limit_patch/lendyr_openapi.json

run_if_exists "Update card status" \
    "tools/update_card_status_cards_card_id_status_patch/lendyr_openapi.json" \
    tools import -k openapi -f tools/update_card_status_cards_card_id_status_patch/lendyr_openapi.json

run_if_exists "Create bill payment" \
    "tools/create_bill_payment/lendyr_openapi.json" \
    tools import -k openapi -f tools/create_bill_payment/lendyr_openapi.json

run_if_exists "Nested get account by type and customer ID copy" \
    "tools/tools/get_account_by_type_and_customer_id/lendyr_openapi.json" \
    tools import -k openapi -f tools/tools/get_account_by_type_and_customer_id/lendyr_openapi.json

# ── Python tools ───────────────────────────────────────────────────────────────
header "Python Tools"

run_if_exists "Calculate deferral terms" \
    "tools/calculate_deferral_terms/calculate_deferral_terms.py" \
    tools import -k python \
        -f tools/calculate_deferral_terms/calculate_deferral_terms.py \
        -r tools/calculate_deferral_terms/requirements.txt

run_if_exists "Get loan details" \
    "tools/get_loan_details/get_loan_details.py" \
    tools import -k python \
        -f tools/get_loan_details/get_loan_details.py \
        -r tools/get_loan_details/requirements.txt

run_if_exists "Extract invoice info" \
    "tools/extract_invoice_info/extract_invoice_info.py" \
    tools import -k python \
        -f tools/extract_invoice_info/extract_invoice_info.py

run_if_exists "Process invoice upload" \
    "tools/process_invoice_upload/process_invoice_upload.py" \
    tools import -k python \
        -f tools/process_invoice_upload/process_invoice_upload.py

# ── Flow tools ─────────────────────────────────────────────────────────────────
header "Flow Tools"

run_if_exists "Invoice extraction flow" \
    "tools/invoice_extraction_flow.py" \
    tools import -k flow -f tools/invoice_extraction_flow.py

run_if_exists "Wire transfer flow" \
    "tools/Wire_transfer_flow_6740Tg.json" \
    tools import -k flow -f tools/Wire_transfer_flow_6740Tg.json

# ── Knowledge bases ────────────────────────────────────────────────────────────
header "Knowledge Bases"

run_if_exists "Lendyr overlimit transfers knowledge base" \
    "knowledge_bases/lendyr_overlimit_transfers_knowledge_base.yaml" \
    knowledge-bases import -f knowledge_bases/lendyr_overlimit_transfers_knowledge_base.yaml

run_if_exists "Lendyr agent assist knowledge base" \
    "knowledge_bases/Lendyr_agent_assist_4368Rc.yaml" \
    knowledge-bases import -f knowledge_bases/Lendyr_agent_assist_4368Rc.yaml

# ── Connections ────────────────────────────────────────────────────────────────
header "Connections"

shopt -s nullglob
connection_files=(connections/*.yaml)
shopt -u nullglob

if [[ ${#connection_files[@]} -eq 0 ]]; then
    echo -e "${yellow}  no connection yaml files found${reset}"
else
    for conn_file in "${connection_files[@]}"; do
        conn_name="$(basename "$conn_file" .yaml)"
        run "Connection: $conn_name" connections import -f "$conn_file"
    done
fi

# ── Agents (specialists first, orchestrators last) ────────────────────────────
header "Agents — Specialists"

run_if_exists "Account agent" \
    "agents/account_agent.yaml" \
    agents import -f agents/account_agent.yaml

run_if_exists "Card agent" \
    "agents/card_agent.yaml" \
    agents import -f agents/card_agent.yaml

run_if_exists "Loan deferral agent" \
    "agents/loan_deferral_agent.yaml" \
    agents import -f agents/loan_deferral_agent.yaml

run_if_exists "Loan agent" \
    "agents/loan_agent.yaml" \
    agents import -f agents/loan_agent.yaml

run_if_exists "Disputes agent" \
    "agents/lendyr_disputes_agent.yaml" \
    agents import -f agents/lendyr_disputes_agent.yaml

run_if_exists "Transfer agent" \
    "agents/transfer_agent.yaml" \
    agents import -f agents/transfer_agent.yaml

run_if_exists "Wire transfer agent" \
    "agents/wire_transfer_agent.yaml" \
    agents import -f agents/wire_transfer_agent.yaml

run_if_exists "Bill payment agent" \
    "agents/bill_payment_agent.yaml" \
    agents import -f agents/bill_payment_agent.yaml

run_if_exists "Agent assist" \
    "agents/lendyr_agent_assist.yaml" \
    agents import -f agents/lendyr_agent_assist.yaml

run_if_exists "Gartner Banking Agent" \
    "agents/Gartner_Banking_Agent.yaml" \
    agents import -f agents/Gartner_Banking_Agent.yaml

run_if_exists "Gartner Realtime Agent" \
    "agents/Gartner_Realtime_Agent_58153S.yaml" \
    agents import -f agents/Gartner_Realtime_Agent_58153S.yaml

header "Agents — Orchestrators"

run_if_exists "Lena (lendyr_customer_care)" \
    "agents/lendyr_customer_care.yaml" \
    agents import -f agents/lendyr_customer_care.yaml

# ── Summary ────────────────────────────────────────────────────────────────────
header "Summary"
echo -e "${green}  Passed: $PASS${reset}"
if [[ $FAIL -gt 0 ]]; then
    echo -e "${red}  Failed: $FAIL${reset}"
    for f in "${FAILURES[@]}"; do
        echo -e "${red}    - $f${reset}"
    done
    exit 1
else
    echo -e "${green}  All imports succeeded.${reset}"
fi

# Made with Bob
