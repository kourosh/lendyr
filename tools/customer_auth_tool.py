#!/usr/bin/env python3
"""
Customer Authentication Tool for Lendyr Bank
Validates customer ID and PIN, returns customer email for API calls
"""

import ibm_db
import os
from pydantic import BaseModel, Field
from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


class CustomerAuthInput(BaseModel):
    """Input for customer authentication"""
    customer_id: int = Field(description="The customer's ID number (e.g., 846301)")
    pin: str = Field(description="The customer's 5-digit PIN")


class CustomerAuthOutput(BaseModel):
    """Output from customer authentication"""
    success: bool = Field(description="Whether authentication was successful")
    customer_email: Optional[str] = Field(default=None, description="Customer's email address for API calls")
    customer_name: Optional[str] = Field(default=None, description="Customer's full name")
    message: str = Field(description="Authentication result message")


def get_db_connection():
    """Get database connection using environment variables"""
    dsn = (
        f"DRIVER={os.getenv('DRIVER')};"
        f"DATABASE={os.getenv('DATABASE')};"
        f"HOSTNAME={os.getenv('DSN_HOSTNAME')};"
        f"PORT={os.getenv('DSN_PORT')};"
        f"PROTOCOL={os.getenv('PROTOCOL')};"
        f"UID={os.getenv('USERNAME')};"
        f"PWD={os.getenv('PASSWORD')};"
        f"SECURITY={os.getenv('SECURITY')};"
    )
    return ibm_db.connect(dsn, "", "")


@tool(
    name="authenticate_customer",
    display_name="Authenticate Customer",
    description="Validates customer ID and PIN, returns customer email for subsequent API calls if successful"
)
def authenticate_customer(input_data: CustomerAuthInput) -> CustomerAuthOutput:
    """
    Authenticate a customer using their ID and PIN.
    Returns customer email if successful for use in subsequent API calls.
    
    Args:
        input_data: CustomerAuthInput with customer_id and pin
        
    Returns:
        CustomerAuthOutput with authentication result and customer email
    """
    try:
        conn = get_db_connection()
        
        # Query to validate customer ID and PIN
        sql = '''
        SELECT customer_id, first_name, last_name, email, pin 
        FROM "LENDYR-DEMO".CUSTOMERS 
        WHERE customer_id = ? AND pin = ?
        '''
        
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, input_data.customer_id)
        ibm_db.bind_param(stmt, 2, input_data.pin)
        ibm_db.execute(stmt)
        
        row = ibm_db.fetch_assoc(stmt)
        
        if row:
            # Authentication successful
            customer_name = f"{row['FIRST_NAME']} {row['LAST_NAME']}"
            customer_email = row['EMAIL']
            
            ibm_db.close(conn)
            
            return CustomerAuthOutput(
                success=True,
                customer_email=customer_email,
                customer_name=customer_name,
                message=f"Welcome, {customer_name}! Authentication successful."
            )
        else:
            # Authentication failed
            ibm_db.close(conn)
            
            return CustomerAuthOutput(
                success=False,
                message="Invalid customer ID or PIN. Please try again."
            )
            
    except Exception as e:
        return CustomerAuthOutput(
            success=False,
            message=f"Authentication error: {str(e)}"
        )


if __name__ == "__main__":
    # Test the function
    from dotenv import load_dotenv
    load_dotenv('../lendyr_code_engine/.env')
    
    # Test with valid credentials
    print("Testing with valid credentials (Alice Martinez - 846301/93810):")
    result = authenticate_customer(CustomerAuthInput(customer_id=846301, pin="93810"))
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print(f"Email: {result.customer_email}")
    print()
    
    # Test with invalid credentials
    print("Testing with invalid credentials:")
    result = authenticate_customer(CustomerAuthInput(customer_id=846301, pin="00000"))
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")

# Made with Bob
