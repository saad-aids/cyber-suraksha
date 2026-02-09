"""
Node 3: Nodal Officer Router
Looks up appropriate nodal officer based on bank
"""

from data.nodal_officers import get_nodal_officer_by_bank, get_all_nodal_officers


async def nodal_router(state: dict) -> dict:
    """
    Node 3: Route to appropriate nodal officer
    Input: bank_name
    Output: nodal officer contact details
    """
    
    bank_name = state.get("bank_name", "")
    scam_type = state.get("scam_type", "other")
    urgency = state.get("urgency", "medium")
    
    routing_result = {
        "nodal_officers": [],
        "routing_success": False,
        "routing_message": ""
    }
    
    if bank_name:
        # Find nodal officers for the bank
        officers = get_nodal_officer_by_bank(bank_name)
        
        if officers:
            routing_result["nodal_officers"] = officers
            routing_result["routing_success"] = True
            routing_result["routing_message"] = f"Found {len(officers)} nodal officer(s) for {bank_name}"
            
            # Prioritize based on urgency
            if urgency in ["critical", "high"]:
                # Sort by priority if available
                routing_result["nodal_officers"] = sorted(
                    officers, 
                    key=lambda x: 0 if x.get("priority") == "high" else 1
                )
        else:
            # Bank not found - provide generic escalation contacts
            routing_result["routing_success"] = False
            routing_result["routing_message"] = f"No specific nodal officer found for {bank_name}. Use 1930 helpline."
            routing_result["fallback_contacts"] = [
                {
                    "name": "National Cyber Crime Helpline",
                    "phone": "1930",
                    "type": "helpline"
                },
                {
                    "name": "Cyber Crime Portal",
                    "url": "https://cybercrime.gov.in",
                    "type": "portal"
                },
                {
                    "name": "Maharashtra Cyber",
                    "url": "https://maharashtracyber.gov.in",
                    "type": "portal"
                }
            ]
    else:
        routing_result["routing_success"] = False
        routing_result["routing_message"] = "No bank identified. Cannot route to specific nodal officer."
        routing_result["fallback_contacts"] = [
            {
                "name": "National Cyber Crime Helpline",
                "phone": "1930",
                "type": "helpline"
            }
        ]
    
    # Add emergency contacts for critical cases
    if urgency == "critical":
        routing_result["emergency_action"] = {
            "action": "IMMEDIATE_CALL",
            "number": "1930",
            "message": "CRITICAL: Call 1930 immediately while we prepare your report"
        }
    
    return {
        **state,
        "routing": routing_result,
        "current_node": "router",
        "routing_complete": True
    }
