"""
Invoice Information Extraction Tool

Extracts payment information from invoice text and formats it as a markdown table.
"""

import re
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool()
def extract_invoice_info(invoice_text: str) -> str:
    """
    Extract payment information from invoice text and format as markdown table.
    
    Args:
        invoice_text: The raw text content extracted from an invoice document
        
    Returns:
        A formatted markdown table with extracted payment information
    """
    # Initialize extracted data
    payee_name = ""
    address = ""
    amount = ""
    invoice_number = ""
    due_date = ""
    
    # Extract payee name (usually first line or after "Bill To")
    lines = invoice_text.split('\n')
    if lines:
        payee_name = lines[0].strip()
    
    # Extract invoice number
    invoice_match = re.search(r'Invoice\s+(?:No\.?|Number|#)\s*[:#]?\s*([A-Z0-9-]+)', invoice_text, re.IGNORECASE)
    if invoice_match:
        invoice_number = invoice_match.group(1)
    
    # Extract amount due
    amount_match = re.search(r'(?:AMOUNT\s+DUE|Total|Amount\s+Due)[:\s]*\$?([\d,]+\.?\d*)', invoice_text, re.IGNORECASE)
    if amount_match:
        amount = amount_match.group(1).replace(',', '')
    
    # Extract due date
    due_date_match = re.search(r'Due\s+Date[:\s]*([\w\s,]+\d{4})', invoice_text, re.IGNORECASE)
    if due_date_match:
        due_date = due_date_match.group(1).strip()
    
    # Extract address (look for street, city, state, zip pattern)
    address_match = re.search(r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way)[,\s]+[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5})', invoice_text, re.IGNORECASE)
    if address_match:
        address = address_match.group(1).strip()
    else:
        # Try simpler pattern
        address_match = re.search(r'(\d+\s+[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5})', invoice_text)
        if address_match:
            address = address_match.group(1).strip()
    
    # Format as markdown table
    table = f"""| Item | Details |
|------|---------|
| Payee Name | {payee_name} |
| Mailing Address | {address} |
| Amount Due | ${amount} |
| Invoice Number | {invoice_number} |
| Due Date | {due_date} |

Does this information look correct? If yes, which account would you like to pay from - checking or savings?"""
    
    return table

# Made with Bob
