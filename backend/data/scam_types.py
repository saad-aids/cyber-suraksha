"""
Scam Classification Types for Maharashtra Cyber Crime
Based on common fraud patterns reported to 1930 helpline
"""

SCAM_TYPES = [
    {
        "id": "digital_arrest",
        "name": "Digital Arrest Scam",
        "description": "Fraudster impersonates police/CBI/customs officer, claims victim is involved in crime",
        "keywords": ["arrest", "police", "cbi", "customs", "parcel", "drugs", "money laundering", "warrant"],
        "urgency": "critical",
        "typical_loss": "₹1-50 lakhs"
    },
    {
        "id": "investment_scam",
        "name": "Investment/Trading Scam",
        "description": "Fake investment apps, crypto schemes, stock trading with guaranteed returns",
        "keywords": ["investment", "trading", "crypto", "bitcoin", "returns", "profit", "stock", "mutual fund"],
        "urgency": "high",
        "typical_loss": "₹5-100 lakhs"
    },
    {
        "id": "upi_fraud",
        "name": "UPI/Payment Fraud",
        "description": "Fake payment requests, QR code scams, UPI PIN theft",
        "keywords": ["upi", "gpay", "phonepe", "paytm", "qr code", "payment", "request", "pin"],
        "urgency": "critical",
        "typical_loss": "₹5,000-2 lakhs"
    },
    {
        "id": "loan_app_fraud",
        "name": "Loan App Fraud",
        "description": "Illegal loan apps with excessive interest, harassment, morphed photos blackmail",
        "keywords": ["loan", "app", "interest", "emi", "harassment", "photos", "contact list", "blackmail"],
        "urgency": "high",
        "typical_loss": "₹10,000-5 lakhs"
    },
    {
        "id": "otp_fraud",
        "name": "OTP/Vishing Fraud",
        "description": "Social engineering to steal OTP, bank credentials via phone calls",
        "keywords": ["otp", "call", "bank", "kyc", "update", "card blocked", "account", "verify"],
        "urgency": "critical",
        "typical_loss": "₹10,000-10 lakhs"
    },
    {
        "id": "job_fraud",
        "name": "Job/Task Fraud",
        "description": "Fake job offers requiring upfront payment, work-from-home task scams",
        "keywords": ["job", "work from home", "task", "rating", "review", "commission", "hiring", "salary"],
        "urgency": "medium",
        "typical_loss": "₹20,000-5 lakhs"
    },
    {
        "id": "sextortion",
        "name": "Sextortion/Romance Scam",
        "description": "Blackmail using intimate content, fake relationships for money",
        "keywords": ["video call", "nude", "intimate", "relationship", "marriage", "blackmail", "viral"],
        "urgency": "high",
        "typical_loss": "₹50,000-10 lakhs"
    },
    {
        "id": "tech_support",
        "name": "Tech Support Scam",
        "description": "Fake tech support calls, remote access software installation",
        "keywords": ["tech support", "anydesk", "teamviewer", "remote", "virus", "microsoft", "refund"],
        "urgency": "medium",
        "typical_loss": "₹10,000-5 lakhs"
    },
    {
        "id": "courier_scam",
        "name": "Courier/Customs Scam",
        "description": "Fake courier companies claiming package held, demanding fees",
        "keywords": ["courier", "fedex", "dhl", "customs", "package", "held", "fee", "clearance"],
        "urgency": "medium",
        "typical_loss": "₹5,000-1 lakh"
    },
    {
        "id": "other",
        "name": "Other Cyber Fraud",
        "description": "Other types of cyber fraud not categorized above",
        "keywords": [],
        "urgency": "medium",
        "typical_loss": "Variable"
    }
]


# I4C Flagged Database (Simulation)
FLAGGED_SUSPECTS = [
    {"type": "phone", "value": "9876543210", "reports": 45, "status": "confirmed_fraud"},
    {"type": "phone", "value": "8765432109", "reports": 23, "status": "suspected"},
    {"type": "phone", "value": "7654321098", "reports": 67, "status": "confirmed_fraud"},
    {"type": "url", "value": "fake-trading-app.com", "reports": 120, "status": "confirmed_fraud"},
    {"type": "url", "value": "quick-loan-india.in", "reports": 89, "status": "confirmed_fraud"},
    {"type": "upi", "value": "scammer@ybl", "reports": 34, "status": "suspected"},
]


def get_scam_types() -> list:
    """Get all scam types"""
    return SCAM_TYPES


def get_scam_by_id(scam_id: str) -> dict:
    """Get scam details by ID"""
    for scam in SCAM_TYPES:
        if scam["id"] == scam_id:
            return scam
    return None


def check_suspect(suspect_type: str, value: str) -> dict:
    """Check if a phone/URL/UPI is flagged in I4C repository"""
    value_lower = value.lower().strip()
    for suspect in FLAGGED_SUSPECTS:
        if suspect["type"] == suspect_type and suspect["value"].lower() == value_lower:
            return {
                "found": True,
                "reports": suspect["reports"],
                "status": suspect["status"]
            }
    return {"found": False, "reports": 0, "status": "not_found"}
