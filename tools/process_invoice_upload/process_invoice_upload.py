"""
Invoice Upload and Processing Tool

Accepts invoice file uploads (PDF or images), extracts payment information,
and returns a formatted table for customer confirmation.
"""

import re
from typing import List
from ibm_watsonx_orchestrate.agent_builder.tools import tool, WXOFile, MultiFileConstraints


@tool()
def process_invoice_upload(
    invoice_files: List[WXOFile] = MultiFileConstraints(
        min_files=1,
        max_files=1,
        accepted_file_extensions=[".pdf", ".png", ".jpg", ".jpeg"],
        text="Upload your invoice (PDF or image)"
    )
) -> str:
    """
    Process an uploaded invoice file and extract payment information.
    
    Accepts PDF or image files, extracts key payment details, and returns
    a formatted table for customer review and confirmation.
    
    Args:
        invoice_files: The invoice file to process (PDF or image format)
        
    Returns:
        A formatted markdown table with extracted payment information
    """
    if not invoice_files or len(invoice_files) == 0:
        return "No invoice file was uploaded. Please upload an invoice to process."
    
    # Get the first (and only) file
    invoice_file = invoice_files[0]
    
    # Get file content as text
    # Note: In production, you would use OCR for images and PDF parsing for PDFs
    # For now, we'll extract text content directly
    try:
        file_content = invoice_file.get_content()
        invoice_text = file_content.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error reading invoice file: {str(e)}. Please ensure the file is a valid PDF or image."
    
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
    table = f"""I've extracted the following payment information from your invoice:

| Item | Details |
|------|---------|
| Payee Name | {payee_name} |
| Mailing Address | {address} |
| Amount Due | ${amount} |
| Invoice Number | {invoice_number} |
| Due Date | {due_date} |

Does this information look correct? If yes, which account would you like to pay from - checking or savings?"""
    
    return table

# Made with Bob
