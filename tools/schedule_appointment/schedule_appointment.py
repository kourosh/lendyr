"""
Lendyr Bank - Appointment Scheduling Tool
Generates available appointment slots for in-branch KYC verification.
"""

from datetime import datetime, timedelta
import random
from typing import Dict, Any, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def schedule_appointment(
    branch_name: str,
    customer_name: str,
    action: str = "show_availability",
    selected_date: Optional[str] = None,
    selected_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Schedule appointment for account opening at Lendyr Bank branch.
    
    Args:
        branch_name: Name of the branch
        customer_name: Customer's full name
        action: One of: show_availability, confirm_appointment, finalize_appointment
        selected_date: Date in YYYY-MM-DD format
        selected_time: Time slot (e.g., "9:00 AM - 10:00 AM")
    
    Returns:
        Dictionary with appointment information
    """
    
    if action == "show_availability":
        # Generate 7 days of slots starting tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        slots_text = [f"\n**Available Appointment Slots at {branch_name}**\n"]
        
        days_shown = 0
        current = tomorrow
        
        while days_shown < 7:
            if current.weekday() != 6:  # Skip Sundays
                date_str = current.strftime("%A, %B %d, %Y")
                slots_text.append(f"\n**{date_str}**")
                
                times = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM",
                        "12:00 PM - 1:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM"]
                
                for time_slot in times:
                    available = random.choice([True, False])
                    marker = "✓" if available else "✗"
                    status = "" if available else " (Unavailable)"
                    slots_text.append(f"  {marker} {time_slot}{status}")
                
                days_shown += 1
            current += timedelta(days=1)
        
        return {
            "success": True,
            "branch_name": branch_name,
            "calendar": "\n".join(slots_text),
            "instructions": "Please select your preferred date and time from the available slots (marked with ✓)."
        }
    
    elif action == "confirm_appointment":
        if not selected_date or not selected_time:
            return {"success": False, "error": "Please provide both date and time."}
        
        try:
            date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
            display_date = date_obj.strftime("%A, %B %d, %Y")
        except ValueError:
            return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD."}
        
        return {
            "success": True,
            "message": f"Appointment selected: {display_date} at {selected_time}",
            "details": {
                "customer": customer_name,
                "branch": branch_name,
                "date": display_date,
                "time": selected_time
            },
            "next_step": "Please confirm to finalize, or request to see availability again."
        }
    
    elif action == "finalize_appointment":
        if not selected_date or not selected_time:
            return {"success": False, "error": "Please provide both date and time."}
        
        confirmation = f"LB{random.randint(100000, 999999)}"
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        display_date = date_obj.strftime("%A, %B %d, %Y")
        
        return {
            "success": True,
            "confirmation_number": confirmation,
            "message": f"""
✓ Appointment Confirmed!

Confirmation #: {confirmation}
Customer: {customer_name}
Branch: {branch_name}
Date: {display_date}
Time: {selected_time}

Please bring valid government-issued ID and your Social Security card to your appointment.
You will receive a confirmation email shortly.
""",
            "next_steps": "Visit the branch at your scheduled time to complete your account opening."
        }
    
    return {"success": False, "error": f"Invalid action: {action}"}


# Tool metadata for watsonx Orchestrate
__tool_name__ = "schedule_appointment"
__tool_description__ = "Schedules appointments for in-branch KYC verification at Lendyr Bank branches."

# Made with Bob
