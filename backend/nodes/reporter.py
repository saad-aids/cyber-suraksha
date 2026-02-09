"""
Node 4: Portal Reporter
Uses LLM to generate formatted report for Maha-Cyber Portal
"""

import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )


REPORT_PROMPT = """You are an expert complaint writer for Maharashtra Cyber Police.
Generate a formal cyber fraud complaint report based on the following details.

The report MUST be at least 200 characters (mandatory for NCRP portal).

CASE DETAILS:
- Scam Type: {scam_type}
- Description: {complaint}
- Amount Lost: Rs.{amount}
- Transaction Reference (UTR): {utr}
- Bank Involved: {bank_name}
- Suspect Phone: {suspect_phone}
- Suspect URL/App: {suspect_url}
- Date of Incident: {incident_date}

Evidence Quality Score: {evidence_score}/100

Generate the report in valid JSON format (no markdown, no code blocks):
{{"report_title": "Brief title for the complaint", "report_body": "Detailed complaint text (minimum 200 characters). Include all relevant details, timeline, and transaction information. Write formally.", "key_evidence": ["list", "of", "key", "evidence", "points"], "recommended_actions": ["action1", "action2"], "priority_level": "critical/high/medium/low"}}
"""

EMAIL_TEMPLATE = """Subject: URGENT: Cyber Fraud Report - {scam_type} - Rs.{amount}

Dear Nodal Officer,

I am reporting a cyber fraud incident that occurred on {incident_date}.

{report_body}

Transaction Details:
- UTR/Reference: {utr}
- Amount: Rs.{amount}
- Bank: {bank_name}

Suspect Information:
- Phone: {suspect_phone}
- Website/App: {suspect_url}

Request for immediate action as this falls within the Cyber Golden Hour.

Regards,
{victim_name}
Contact: {victim_phone}
"""


async def portal_reporter(state: dict) -> dict:
    """
    Node 4: Generate formatted report for Maha-Cyber Portal
    Input: all collected data from previous nodes
    Output: formatted report ready for submission
    """
    
    # Extract data from state
    complaint = state.get("complaint", "")
    scam_type = state.get("scam_type", "other")
    amount = state.get("amount", 0)
    utr = state.get("utr", "N/A")
    bank_name = state.get("bank_name", "Unknown")
    suspect_phone = state.get("suspect_phone", "N/A")
    suspect_url = state.get("suspect_url", "N/A")
    incident_date = state.get("incident_date", datetime.now().strftime("%Y-%m-%d"))
    evidence = state.get("evidence", {})
    victim_name = state.get("victim_name", "Complainant")
    victim_phone = state.get("victim_phone", "N/A")
    
    evidence_score = evidence.get("evidence_score", 50) if isinstance(evidence, dict) else 50
    
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)
        parser = JsonOutputParser()
        
        chain = prompt | llm | parser
        
        result = await chain.ainvoke({
            "scam_type": scam_type,
            "complaint": complaint,
            "amount": amount,
            "utr": utr,
            "bank_name": bank_name,
            "suspect_phone": suspect_phone,
            "suspect_url": suspect_url,
            "incident_date": incident_date,
            "evidence_score": evidence_score
        })
        
        report_body = result.get("report_body", complaint)
        
        # Generate email draft
        email_draft = EMAIL_TEMPLATE.format(
            scam_type=scam_type.replace("_", " ").title(),
            amount=amount,
            incident_date=incident_date,
            report_body=report_body,
            utr=utr,
            bank_name=bank_name,
            suspect_phone=suspect_phone,
            suspect_url=suspect_url,
            victim_name=victim_name,
            victim_phone=victim_phone
        )
        
        return {
            **state,
            "report": {
                "title": result.get("report_title", f"Cyber Fraud Report - {scam_type}"),
                "body": report_body,
                "body_length": len(report_body),
                "meets_minimum": len(report_body) >= 200,
                "key_evidence": result.get("key_evidence", []),
                "recommended_actions": result.get("recommended_actions", []),
                "priority_level": result.get("priority_level", "medium"),
                "email_draft": email_draft,
                "generated_at": datetime.now().isoformat()
            },
            "current_node": "reporter",
            "report_complete": True,
            "workflow_complete": True
        }
        
    except Exception as e:
        print(f"Reporter error: {e}")
        # Fallback: Generate basic report without LLM
        basic_report = f"""
Cyber Fraud Complaint Report

Type: {scam_type.replace("_", " ").title()}
Date: {incident_date}
Amount Lost: Rs.{amount}

Incident Description:
{complaint}

Transaction Details:
- UTR/Reference Number: {utr}
- Bank: {bank_name}

Suspect Information:
- Phone Number: {suspect_phone}
- Website/App: {suspect_url}

This complaint is being filed for immediate action under the Cyber Golden Hour protocol.
        """.strip()
        
        return {
            **state,
            "report": {
                "title": f"Cyber Fraud Report - {scam_type}",
                "body": basic_report,
                "body_length": len(basic_report),
                "meets_minimum": len(basic_report) >= 200,
                "key_evidence": [utr, suspect_phone, suspect_url],
                "recommended_actions": ["File FIR", "Contact bank nodal officer", "Report on NCRP"],
                "priority_level": "medium",
                "email_draft": basic_report,
                "generated_at": datetime.now().isoformat(),
                "llm_error": str(e)
            },
            "current_node": "reporter",
            "report_complete": True,
            "workflow_complete": True
        }
