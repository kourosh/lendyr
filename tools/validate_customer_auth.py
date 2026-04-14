#!/usr/bin/env python3
"""
Tool to validate customer authentication (ID and PIN)
"""

import ibm_db
import os
from pydantic import BaseModel, Field
from typing import Optional


class AuthRequest(BaseModel):
    """Customer authentication request"""
    customer_id: int = Field(description="The customer's ID number (e.g., 846301)")
    pin: str = Field(description="The customer's 5-digit PIN")


class AuthResponse(BaseModel):
    """Authentication response"""
    authenticated: bool = Field(description="Whether authentication was successful")
    customer_email: Optional[str] = Field(default=None, description="Customer's email if authenticated")
    customer_name: Optional[str] = Field(default=None, description="Customer's full name if authenticated")
    error_message: Optional[str] = Field(default=None, description="Error message if authentication failed")


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


def validate_customer_auth(auth_request: AuthRequest) -> AuthResponse:
    """
    Validate customer authentication by checking customer ID and PIN.
    
    Args:
        auth_request: Authentication request with customer_id and pin
        
    Returns:
        AuthResponse with authentication result
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
        ibm_db.bind_param(stmt, 1, auth_request.customer_id)
        ibm_db.bind_param(stmt, 2, auth_request.pin)
        ibm_db.execute(stmt)
        
        row = ibm_db.fetch_assoc(stmt)
        
        if row:
            # Authentication successful
            customer_name = f"{row['FIRST_NAME']} {row['LAST_NAME']}"
            customer_email = row['EMAIL']
            
            ibm_db.close(conn)
            
            return AuthResponse(
                authenticated=True,
                customer_email=customer_email,
                customer_name=customer_name
            )
        else:
            # Authentication failed
            ibm_db.close(conn)
            
            return AuthResponse(
                authenticated=False,
                error_message="Invalid customer ID or PIN. Please try again."
            )
            
    except Exception as e:
        return AuthResponse(
            authenticated=False,
            error_message=f"Authentication error: {str(e)}"
        )


if __name__ == "__main__":
    # Test the function
    from dotenv import load_dotenv
    import sys
    sys.path.insert(0, '..')
    load_dotenv('../lendyr_code_engine/.env')
    
    # Test with valid credentials
    print("Testing with valid credentials (Alice Martinez):")
    result = validate_customer_auth(AuthRequest(customer_id=846301, pin="93810"))
    print(f"Authenticated: {result.authenticated}")
    print(f"Name: {result.customer_name}")
    print(f"Email: {result.customer_email}")
    print()
    
    # Test with invalid credentials
    print("Testing with invalid credentials:")
    result = validate_customer_auth(AuthRequest(customer_id=846301, pin="00000"))
    print(f"Authenticated: {result.authenticated}")
    print(f"Error: {result.error_message}")

# Made with Bob
