"""
Invoice Extraction Agentic Workflow

Extracts payment information from uploaded invoice documents (PDF or images)
using the document field extractor node.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import (
    DocExtConfigField, 
    DocumentProcessingCommonInput
)


class InvoiceFields(BaseModel):
    """
    Configuration schema for invoice document extraction fields.
    
    Defines the fields to be extracted from invoice documents for bill payment processing.
    """
    payee_name: DocExtConfigField = Field(
        name="Payee Name",
        default=DocExtConfigField(
            name="Payee Name",
            field_name="payee_name",
            type="string",
            description="The name of the company or person to whom the payment should be made"
        )
    )
    
    payee_address: DocExtConfigField = Field(
        name="Payee Address",
        default=DocExtConfigField(
            name="Payee Address",
            field_name="payee_address",
            type="string",
            description="The complete mailing address where the check should be sent, including street, city, state, and ZIP code"
        )
    )
    
    amount_due: DocExtConfigField = Field(
        name="Amount Due",
        default=DocExtConfigField(
            name="Amount Due",
            field_name="amount_due",
            type="string",
            description="The total amount to be paid, typically shown as 'Amount Due' or 'Total'"
        )
    )
    
    invoice_number: DocExtConfigField = Field(
        name="Invoice Number",
        default=DocExtConfigField(
            name="Invoice Number",
            field_name="invoice_number",
            type="string",
            description="The unique identifier for this invoice, often labeled as 'Invoice No.' or 'Invoice #'"
        )
    )
    
    due_date: DocExtConfigField = Field(
        name="Due Date",
        default=DocExtConfigField(
            name="Due Date",
            field_name="due_date",
            type="date",
            description="The date by which the payment should be made"
        )
    )


@flow(
    name="invoice_extraction_flow",
    display_name="Extract Invoice Payment Information",
    description="Upload an invoice (PDF or image) to automatically extract payment details including payee name, address, amount, invoice number, and due date. The extracted information will be formatted for bill payment processing.",
    input_schema=DocumentProcessingCommonInput
)
def build_invoice_extraction_flow(aflow: Flow = None) -> Flow:
    """
    Build an agentic workflow that extracts invoice payment information from uploaded documents.
    
    This workflow uses the document field extractor node to automatically identify and extract
    key payment fields from invoice documents, making it easy for customers to pay bills by
    simply uploading their invoice.
    """
    
    # Create document extractor node with invoice fields
    doc_ext_node, ExtractedInvoiceValues = aflow.docext(
        name="invoice_extractor",
        display_name="Extract Invoice Payment Details",
        description="Extracts payee name, address, amount due, invoice number, and due date from the uploaded invoice",
        llm="groq/openai/gpt-oss-120b",
        fields=InvoiceFields(),
        enable_review=True,
        review_fields=["payee_name", "payee_address", "amount_due"],
        min_confidence=0.7
    )
    
    # Define the flow sequence
    aflow.sequence(START, doc_ext_node, END)
    
    return aflow

# Made with Bob
