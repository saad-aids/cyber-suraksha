"""
Node 2: Evidence Collector
Validates and enriches evidence data (UTR, bank info, suspect details)
"""

import re
from data.scam_types import check_suspect


def validate_utr(utr: str) -> dict:
    """Validate UTR number format (12 digits for NEFT/RTGS or 12-16 for UPI)"""
    utr_clean = utr.strip().replace(" ", "")
    
    # UTR patterns
    patterns = {
        "neft_rtgs": r"^[A-Z]{4}[0-9]{7,13}$",  # Bank code + numbers
        "upi": r"^[0-9]{12,16}$",  # UPI transaction ID
        "imps": r"^[0-9]{12}$"  # IMPS reference
    }
    
    for txn_type, pattern in patterns.items():
        if re.match(pattern, utr_clean, re.IGNORECASE):
            return {
                "valid": True,
                "type": txn_type,
                "formatted": utr_clean.upper()
            }
    
    # Check if it's at least numeric and reasonable length
    if re.match(r"^[A-Za-z0-9]{8,20}$", utr_clean):
        return {
            "valid": True,
            "type": "unknown",
            "formatted": utr_clean.upper(),
            "warning": "UTR format not standard but accepted"
        }
    
    return {
        "valid": False,
        "type": None,
        "error": "Invalid UTR format. Should be 12-16 alphanumeric characters."
    }


def extract_bank_from_utr(utr: str) -> str:
    """Attempt to identify bank from UTR prefix"""
    utr_upper = utr.upper().strip()
    
    bank_prefixes = {
        "SBIN": "State Bank of India",
        "HDFC": "HDFC Bank",
        "ICIC": "ICICI Bank",
        "AXIS": "Axis Bank",
        "PUNB": "Punjab National Bank",
        "BARB": "Bank of Baroda",
        "MAHB": "Bank of Maharashtra",
        "CNRB": "Canara Bank",
        "UBIN": "Union Bank of India",
        "KKBK": "Kotak Mahindra Bank"
    }
    
    for prefix, bank in bank_prefixes.items():
        if utr_upper.startswith(prefix):
            return bank
    
    return None


async def evidence_collector(state: dict) -> dict:
    """
    Node 2: Validate and enrich evidence data
    Input: utr, bank_name, suspect_phone, suspect_url
    Output: validated data with I4C check results
    """
    
    utr = state.get("utr", "")
    bank_name = state.get("bank_name", "")
    suspect_phone = state.get("suspect_phone", "")
    suspect_url = state.get("suspect_url", "")
    amount = state.get("amount", 0)
    
    evidence_result = {
        "utr_validated": False,
        "utr_info": {},
        "bank_identified": None,
        "suspect_checks": [],
        "evidence_score": 0
    }
    
    score = 0
    
    # Validate UTR
    if utr:
        utr_validation = validate_utr(utr)
        evidence_result["utr_info"] = utr_validation
        evidence_result["utr_validated"] = utr_validation["valid"]
        if utr_validation["valid"]:
            score += 30
            
            # Try to identify bank from UTR if not provided
            if not bank_name:
                extracted_bank = extract_bank_from_utr(utr)
                if extracted_bank:
                    bank_name = extracted_bank
                    evidence_result["bank_identified"] = extracted_bank
    
    # Validate bank
    if bank_name:
        evidence_result["bank_name"] = bank_name
        score += 20
    
    # Check suspect phone in I4C repository
    if suspect_phone:
        phone_clean = re.sub(r"[^\d]", "", suspect_phone)
        if len(phone_clean) == 10:
            phone_check = check_suspect("phone", phone_clean)
            evidence_result["suspect_checks"].append({
                "type": "phone",
                "value": phone_clean,
                "result": phone_check
            })
            if phone_check["found"]:
                score += 25
    
    # Check suspect URL in I4C repository
    if suspect_url:
        url_clean = suspect_url.lower().replace("http://", "").replace("https://", "").split("/")[0]
        url_check = check_suspect("url", url_clean)
        evidence_result["suspect_checks"].append({
            "type": "url",
            "value": url_clean,
            "result": url_check
        })
        if url_check["found"]:
            score += 25
    
    # Amount validation
    if amount and amount > 0:
        evidence_result["amount"] = amount
        evidence_result["amount_category"] = (
            "low" if amount < 10000 else
            "medium" if amount < 100000 else
            "high" if amount < 1000000 else
            "critical"
        )
        score += 10
    
    evidence_result["evidence_score"] = min(score, 100)
    
    return {
        **state,
        "bank_name": bank_name,
        "evidence": evidence_result,
        "current_node": "evidence",
        "evidence_complete": True
    }
