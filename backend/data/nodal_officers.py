"""
Nodal Officer Database for Major Banks in India
RBI-mandated contacts for cyber fraud reporting
"""

NODAL_OFFICERS = [
    {
        "id": 1,
        "bank_name": "Bank of Maharashtra",
        "region": "Head Office (Recovery)",
        "officer_name": "CGM Recovery",
        "email": "cgmrecovery@bankofmaharashtra.bank.in",
        "phone": "020-25614252",
        "priority": "high"
    },
    {
        "id": 2,
        "bank_name": "Bank of Maharashtra",
        "region": "Mumbai City Zone",
        "officer_name": "DZM Mumbai",
        "email": "dzmmcz@bankofmaharashtra.bank.in",
        "phone": "022-22671568",
        "priority": "high"
    },
    {
        "id": 3,
        "bank_name": "State Bank of India",
        "region": "Nodal Officer (Cyber)",
        "officer_name": "AGM Nodal Cyber",
        "email": "agm.nodcyb@sbi.co.in",
        "phone": "1800-111-109",
        "priority": "high"
    },
    {
        "id": 4,
        "bank_name": "HDFC Bank",
        "region": "Pension/Nodal Dept",
        "officer_name": "Ajay Prabhakar",
        "email": "ajay.prabhakar@hdfcbank.com",
        "phone": "022-61606161",
        "priority": "high"
    },
    {
        "id": 5,
        "bank_name": "ICICI Bank",
        "region": "Corporate Head Office",
        "officer_name": "Vinayak More",
        "email": "vinayak.more@icicibank.com",
        "phone": "022-26536536",
        "priority": "high"
    },
    {
        "id": 6,
        "bank_name": "Axis Bank",
        "region": "Nodal Officer Cyber",
        "officer_name": "Nodal Officer",
        "email": "nodal.officer@axisbank.com",
        "phone": "1800-419-5555",
        "priority": "medium"
    },
    {
        "id": 7,
        "bank_name": "Punjab National Bank",
        "region": "Cyber Cell",
        "officer_name": "Chief Manager Cyber",
        "email": "cybercell@pnb.co.in",
        "phone": "1800-180-2222",
        "priority": "medium"
    },
    {
        "id": 8,
        "bank_name": "Kotak Mahindra Bank",
        "region": "Nodal Officer",
        "officer_name": "Nodal Officer",
        "email": "nodal.officer@kotak.com",
        "phone": "1800-266-2666",
        "priority": "medium"
    },
    {
        "id": 9,
        "bank_name": "Canara Bank",
        "region": "Cyber Security",
        "officer_name": "AGM Cyber Security",
        "email": "agmcyber@canarabank.com",
        "phone": "1800-425-0018",
        "priority": "medium"
    },
    {
        "id": 10,
        "bank_name": "Union Bank of India",
        "region": "Nodal Officer",
        "officer_name": "Nodal Officer Cyber",
        "email": "nodalofficer@unionbankofindia.bank",
        "phone": "1800-222-244",
        "priority": "medium"
    },
    {
        "id": 11,
        "bank_name": "Paytm Payments Bank",
        "region": "Fraud Prevention",
        "officer_name": "Nodal Officer",
        "email": "nodalofficer@paytm.com",
        "phone": "0120-4456456",
        "priority": "high"
    },
    {
        "id": 12,
        "bank_name": "PhonePe",
        "region": "Trust & Safety",
        "officer_name": "Grievance Officer",
        "email": "grievance@phonepe.com",
        "phone": "080-68727374",
        "priority": "high"
    },
    {
        "id": 13,
        "bank_name": "Google Pay (GPay)",
        "region": "User Safety",
        "officer_name": "Grievance Officer India",
        "email": "support-in@google.com",
        "phone": "1800-419-0157",
        "priority": "high"
    }
]


def get_nodal_officer_by_bank(bank_name: str) -> list:
    """Find nodal officers for a specific bank"""
    bank_name_lower = bank_name.lower()
    results = []
    for officer in NODAL_OFFICERS:
        if bank_name_lower in officer["bank_name"].lower():
            results.append(officer)
    return results


def get_all_banks() -> list:
    """Get unique list of all banks"""
    banks = list(set([officer["bank_name"] for officer in NODAL_OFFICERS]))
    return sorted(banks)


def get_all_nodal_officers() -> list:
    """Get all nodal officers"""
    return NODAL_OFFICERS
