"""
Node 1: Triage Auditor
Uses LLM to classify scam type from user description
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize Gemini LLM
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )

TRIAGE_PROMPT = """You are an expert cyber crime analyst for Maharashtra Cyber Police.
Analyze the following fraud complaint and classify it into one of these categories:

SCAM CATEGORIES:
1. digital_arrest - Impersonation of police/CBI/customs, fake arrest threats
2. investment_scam - Fake trading apps, crypto schemes, guaranteed returns
3. upi_fraud - Fake payment requests, QR code scams, UPI PIN theft  
4. loan_app_fraud - Illegal loan apps, harassment, blackmail
5. otp_fraud - Social engineering for OTP/bank credentials
6. job_fraud - Fake job offers, work-from-home task scams
7. sextortion - Blackmail with intimate content, romance scams
8. tech_support - Fake tech support, remote access scams
9. courier_scam - Fake courier/customs holding package
10. other - Other cyber fraud

USER COMPLAINT:
{complaint}

Respond ONLY with valid JSON (no markdown, no code blocks) with these fields:
{{"scam_type": "category_id from above", "confidence": 0.0-1.0, "reasoning": "brief explanation", "urgency": "critical/high/medium/low", "key_indicators": ["indicator1", "indicator2"]}}
"""


async def triage_auditor(state: dict) -> dict:
    """
    Node 1: Analyze complaint and classify scam type
    Input: complaint text
    Output: scam classification with confidence
    """
    complaint = state.get("complaint", "")
    
    if not complaint:
        return {
            **state,
            "error": "No complaint provided",
            "current_node": "triage"
        }
    
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_template(TRIAGE_PROMPT)
        parser = JsonOutputParser()
        
        chain = prompt | llm | parser
        
        result = await chain.ainvoke({"complaint": complaint})
        
        return {
            **state,
            "scam_type": result.get("scam_type", "other"),
            "scam_confidence": result.get("confidence", 0.5),
            "scam_reasoning": result.get("reasoning", ""),
            "urgency": result.get("urgency", "medium"),
            "key_indicators": result.get("key_indicators", []),
            "current_node": "triage",
            "triage_complete": True
        }
        
    except Exception as e:
        print(f"Triage error: {e}")
        return {
            **state,
            "scam_type": "other",
            "scam_confidence": 0.3,
            "urgency": "medium",
            "error": f"Triage error: {str(e)}",
            "current_node": "triage",
            "triage_complete": True
        }
