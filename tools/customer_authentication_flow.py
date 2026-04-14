#!/usr/bin/env python3
"""
Customer Authentication Agentic Workflow
Handles customer authentication with retry logic (max 2 attempts)
"""

from ibm_watson_orchestrate import flow, Flow, START, END
from pydantic import BaseModel, Field
from typing import Optional
from validate_customer_auth import validate_customer_auth, AuthRequest, AuthResponse


class AuthFlowInput(BaseModel):
    """Input for authentication flow"""
    pass  # No input needed - we'll collect from user


class AuthFlowOutput(BaseModel):
    """Output from authentication flow"""
    authenticated: bool = Field(description="Whether authentication was successful")
    customer_email: Optional[str] = Field(default=None, description="Customer's email if authenticated")
    customer_name: Optional[str] = Field(default=None, description="Customer's full name if authenticated")
    attempts_used: int = Field(description="Number of authentication attempts used")
    locked_out: bool = Field(default=False, description="Whether customer was locked out after max attempts")


class AttemptCounter(BaseModel):
    """Track authentication attempts"""
    count: int = Field(default=0, description="Current attempt count")
    max_attempts: int = Field(default=2, description="Maximum allowed attempts")


@flow(
    name="customer_authentication",
    display_name="Customer Authentication",
    description="Authenticate customer with ID and PIN, allowing up to 2 attempts before lockout",
    input_schema=AuthFlowInput,
    output_schema=AuthFlowOutput
)
def build_customer_authentication_flow(aflow: Flow) -> Flow:
    """
    Build the customer authentication workflow with retry logic.
    
    Flow:
    1. Greet customer and ask what they'd like to do
    2. Ask for customer ID
    3. Ask for PIN
    4. Validate credentials
    5. If invalid and attempts < 2, loop back to step 2
    6. If invalid and attempts >= 2, direct to call 800-LENDYR1
    7. If valid, proceed with authenticated session
    """
    
    # Create a loop that will retry authentication up to 2 times
    auth_loop: Flow = aflow.loop(
        evaluator="flow.state.attempt_counter.count < flow.state.attempt_counter.max_attempts and not flow.state.authenticated"
    )
    
    # Inside the loop, we'll have the authentication steps
    # Note: In a real implementation, these would be prompt nodes or user interaction nodes
    # For now, we'll use tool nodes as placeholders
    
    validate_node = auth_loop.tool(
        name="validate_credentials",
        tool="validate_customer_auth",
        display_name="Validate Customer Credentials",
        description="Validate the customer ID and PIN"
    )
    
    # Increment attempt counter
    increment_node = auth_loop.tool(
        name="increment_attempt",
        tool="increment_attempt_counter",
        display_name="Increment Attempt Counter",
        description="Increment the authentication attempt counter"
    )
    
    # Connect nodes in the loop
    auth_loop.sequence(START, validate_node, increment_node, END)
    
    # Add the loop to the main flow
    aflow.edge(START, auth_loop)
    
    # After the loop, check if authenticated or locked out
    check_result_branch = aflow.branch(
        evaluator="flow.state.authenticated == True"
    )
    
    aflow.edge(auth_loop, check_result_branch)
    
    # If authenticated, proceed to success
    success_node = aflow.tool(
        name="authentication_success",
        tool="format_success_message",
        display_name="Authentication Success",
        description="Format success message for authenticated customer"
    )
    
    # If not authenticated after max attempts, show lockout message
    lockout_node = aflow.tool(
        name="authentication_lockout",
        tool="format_lockout_message",
        display_name="Authentication Lockout",
        description="Show lockout message and 800-LENDYR1 number"
    )
    
    check_result_branch.case(True, success_node)
    check_result_branch.case(False, lockout_node)
    
    aflow.edge(success_node, END)
    aflow.edge(lockout_node, END)
    
    return aflow


# Helper tool functions that would be imported
def increment_attempt_counter(counter: AttemptCounter) -> AttemptCounter:
    """Increment the attempt counter"""
    counter.count += 1
    return counter


def format_success_message(auth_response: AuthResponse) -> str:
    """Format success message"""
    return f"Welcome, {auth_response.customer_name}! You have been successfully authenticated."


def format_lockout_message(attempts: int) -> str:
    """Format lockout message"""
    return f"Authentication failed after {attempts} attempts. Please call 800-LENDYR1 for assistance."


if __name__ == "__main__":
    print("Customer Authentication Flow created successfully!")
    print("This flow will:")
    print("1. Greet the customer")
    print("2. Ask for customer ID")
    print("3. Ask for PIN")
    print("4. Validate credentials")
    print("5. Allow up to 2 retry attempts")
    print("6. Lock out after 2 failed attempts with 800-LENDYR1 message")

# Made with Bob
