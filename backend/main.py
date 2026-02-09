"""
Cyber-Suraksha FastAPI Backend
Main application with REST endpoints
"""

import os
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Import workflow and data
from graph import run_fraud_workflow
from data.nodal_officers import get_all_nodal_officers, get_nodal_officer_by_bank, get_all_banks
from data.scam_types import get_scam_types, get_scam_by_id, check_suspect


def get_api_key(x_api_key: Optional[str] = None) -> Optional[str]:
    """Get API key from header or environment"""
    if x_api_key:
        return x_api_key
    return os.getenv("GOOGLE_API_KEY")


# Initialize FastAPI app
app = FastAPI(
    title="Cyber-Suraksha API",
    description="AI-powered First Responder for Financial Fraud Recovery",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Pydantic Models ============

class FraudReportRequest(BaseModel):
    """Request model for fraud report submission"""
    complaint: str = Field(..., min_length=10, description="Description of the fraud")
    utr: Optional[str] = Field(None, description="Transaction reference number")
    bank_name: Optional[str] = Field(None, description="Bank involved")
    amount: Optional[float] = Field(None, ge=0, description="Amount lost in rupees")
    suspect_phone: Optional[str] = Field(None, description="Suspect's phone number")
    suspect_url: Optional[str] = Field(None, description="Fraudulent URL or app name")
    incident_date: Optional[str] = Field(None, description="Date of incident (YYYY-MM-DD)")
    victim_name: Optional[str] = Field(None, description="Victim's name")
    victim_phone: Optional[str] = Field(None, description="Victim's contact number")


class TriageRequest(BaseModel):
    """Request model for triage analysis only"""
    complaint: str = Field(..., min_length=10, description="Description of the fraud")


class SuspectCheckRequest(BaseModel):
    """Request model for suspect verification"""
    suspect_type: str = Field(..., description="Type: phone, url, or upi")
    value: str = Field(..., description="Value to check")


class NodalLookupRequest(BaseModel):
    """Request model for nodal officer lookup"""
    bank_name: str = Field(..., description="Bank name to lookup")


# ============ API Endpoints ============

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Cyber-Suraksha API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check(x_api_key: Optional[str] = Header(None)):
    """Detailed health check with optional API key validation"""
    api_key = get_api_key(x_api_key)
    api_key_configured = bool(api_key)
    
    return {
        "status": "healthy" if api_key_configured else "degraded",
        "llm_configured": api_key_configured,
        "api_key_source": "header" if x_api_key else ("env" if os.getenv("GOOGLE_API_KEY") else "none"),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/test-key")
async def test_api_key(x_api_key: Optional[str] = Header(None)):
    """Test if API key is valid by making a simple LLM call"""
    api_key = get_api_key(x_api_key)
    
    if not api_key:
        return {"valid": False, "error": "No API key provided"}
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Quick test
        response = await llm.ainvoke("Reply with 'OK'")
        
        return {
            "valid": True,
            "message": "API key is valid"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@app.post("/api/analyze")
async def analyze_fraud(request: FraudReportRequest, x_api_key: Optional[str] = Header(None)):
    """
    Run the complete 4-node fraud analysis workflow
    
    This executes:
    1. Triage Auditor - Classify scam type
    2. Evidence Collector - Validate evidence
    3. Nodal Router - Find bank contacts
    4. Portal Reporter - Generate report
    """
    # Set API key from header if provided
    api_key = get_api_key(x_api_key)
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    try:
        input_data = {
            "complaint": request.complaint,
            "utr": request.utr,
            "bank_name": request.bank_name,
            "amount": request.amount,
            "suspect_phone": request.suspect_phone,
            "suspect_url": request.suspect_url,
            "incident_date": request.incident_date or datetime.now().strftime("%Y-%m-%d"),
            "victim_name": request.victim_name,
            "victim_phone": request.victim_phone
        }
        
        result = await run_fraud_workflow(input_data)
        
        return {
            "success": True,
            "workflow_complete": result.get("workflow_complete", False),
            "data": {
                "triage": {
                    "scam_type": result.get("scam_type"),
                    "confidence": result.get("scam_confidence"),
                    "urgency": result.get("urgency"),
                    "reasoning": result.get("scam_reasoning"),
                    "indicators": result.get("key_indicators", [])
                },
                "evidence": result.get("evidence", {}),
                "routing": result.get("routing", {}),
                "report": result.get("report", {})
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow error: {str(e)}")


@app.post("/api/triage")
async def triage_only(request: TriageRequest, x_api_key: Optional[str] = Header(None)):
    """Quick triage analysis without full workflow"""
    # Set API key from header if provided
    api_key = get_api_key(x_api_key)
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    try:
        from nodes.triage import triage_auditor
        
        state = {"complaint": request.complaint}
        result = await triage_auditor(state)
        
        return {
            "success": True,
            "scam_type": result.get("scam_type"),
            "confidence": result.get("scam_confidence"),
            "urgency": result.get("urgency"),
            "reasoning": result.get("scam_reasoning"),
            "indicators": result.get("key_indicators", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage error: {str(e)}")


@app.post("/api/lookup-nodal")
async def lookup_nodal_officer(request: NodalLookupRequest):
    """Look up nodal officers for a specific bank"""
    officers = get_nodal_officer_by_bank(request.bank_name)
    
    return {
        "success": len(officers) > 0,
        "bank_name": request.bank_name,
        "officers": officers,
        "count": len(officers)
    }


@app.post("/api/check-suspect")
async def check_suspect_endpoint(request: SuspectCheckRequest):
    """Check if a phone/URL/UPI is flagged in I4C repository"""
    if request.suspect_type not in ["phone", "url", "upi"]:
        raise HTTPException(status_code=400, detail="Invalid suspect type. Use: phone, url, or upi")
    
    result = check_suspect(request.suspect_type, request.value)
    
    return {
        "success": True,
        "suspect_type": request.suspect_type,
        "value": request.value,
        "result": result
    }


@app.get("/api/scam-types")
async def get_all_scam_types():
    """Get list of all scam categories"""
    return {
        "success": True,
        "scam_types": get_scam_types()
    }


@app.get("/api/scam-types/{scam_id}")
async def get_scam_type_details(scam_id: str):
    """Get details of a specific scam type"""
    scam = get_scam_by_id(scam_id)
    
    if not scam:
        raise HTTPException(status_code=404, detail=f"Scam type '{scam_id}' not found")
    
    return {
        "success": True,
        "scam": scam
    }


@app.get("/api/banks")
async def get_banks():
    """Get list of all banks with nodal officers"""
    return {
        "success": True,
        "banks": get_all_banks()
    }


@app.get("/api/nodal-officers")
async def get_all_officers():
    """Get complete nodal officer directory"""
    return {
        "success": True,
        "officers": get_all_nodal_officers()
    }


# ============ Run Server ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
