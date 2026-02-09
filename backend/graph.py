"""
LangGraph Workflow Definition
Multi-step agent workflow for cyber fraud reporting
"""

from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import StateGraph, END

# Import nodes
from nodes.triage import triage_auditor
from nodes.evidence import evidence_collector
from nodes.router import nodal_router
from nodes.reporter import portal_reporter


class FraudReportState(TypedDict, total=False):
    """State schema for the fraud reporting workflow"""
    # Input fields
    complaint: str
    utr: Optional[str]
    bank_name: Optional[str]
    amount: Optional[float]
    suspect_phone: Optional[str]
    suspect_url: Optional[str]
    incident_date: Optional[str]
    victim_name: Optional[str]
    victim_phone: Optional[str]
    
    # Node 1: Triage outputs
    scam_type: Optional[str]
    scam_confidence: Optional[float]
    scam_reasoning: Optional[str]
    urgency: Optional[str]
    key_indicators: Optional[List[str]]
    triage_complete: Optional[bool]
    
    # Node 2: Evidence outputs
    evidence: Optional[dict]
    evidence_complete: Optional[bool]
    
    # Node 3: Router outputs
    routing: Optional[dict]
    routing_complete: Optional[bool]
    
    # Node 4: Reporter outputs
    report: Optional[dict]
    report_complete: Optional[bool]
    
    # Workflow state
    current_node: Optional[str]
    workflow_complete: Optional[bool]
    error: Optional[str]


def create_fraud_workflow():
    """Create and compile the LangGraph workflow"""
    
    # Initialize the graph with state schema
    workflow = StateGraph(FraudReportState)
    
    # Add nodes
    workflow.add_node("triage", triage_auditor)
    workflow.add_node("evidence", evidence_collector)
    workflow.add_node("router", nodal_router)
    workflow.add_node("reporter", portal_reporter)
    
    # Set entry point
    workflow.set_entry_point("triage")
    
    # Define edges (sequential flow)
    workflow.add_edge("triage", "evidence")
    workflow.add_edge("evidence", "router")
    workflow.add_edge("router", "reporter")
    workflow.add_edge("reporter", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


# Create the workflow instance
fraud_workflow = create_fraud_workflow()


async def run_fraud_workflow(input_data: dict) -> dict:
    """
    Execute the complete fraud reporting workflow
    
    Args:
        input_data: Dictionary containing complaint and evidence details
        
    Returns:
        Final state with all node outputs
    """
    
    # Initialize state with input data
    initial_state = {
        "complaint": input_data.get("complaint", ""),
        "utr": input_data.get("utr"),
        "bank_name": input_data.get("bank_name"),
        "amount": input_data.get("amount"),
        "suspect_phone": input_data.get("suspect_phone"),
        "suspect_url": input_data.get("suspect_url"),
        "incident_date": input_data.get("incident_date"),
        "victim_name": input_data.get("victim_name"),
        "victim_phone": input_data.get("victim_phone"),
        
        # Initialize completion flags
        "triage_complete": False,
        "evidence_complete": False,
        "routing_complete": False,
        "report_complete": False,
        "workflow_complete": False
    }
    
    # Run the workflow
    final_state = await fraud_workflow.ainvoke(initial_state)
    
    return final_state
