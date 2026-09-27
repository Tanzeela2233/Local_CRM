def qualify_lead(lead: dict):
    """
    Transparent lightweight qualification:
    service +25
    budget +25
    deadline +20
    name/company +15
    email/phone +15
    """
    score = 0
    reasons = []

    if lead.get("service"):
        score += 25
        reasons.append("Service requirement identified.")

    if lead.get("budget"):
        score += 25
        reasons.append("Budget information provided.")

    if lead.get("deadline"):
        score += 20
        reasons.append("Timeline/deadline provided.")

    if lead.get("name") or lead.get("company"):
        score += 15
        reasons.append("Name or company information provided.")

    if lead.get("email") or lead.get("phone"):
        score += 15
        reasons.append("Contact details provided.")

    if score >= 70:
        status = "qualified"
    elif score >= 40:
        status = "nurture"
    else:
        status = "low_priority"

    return {
        "score": score,
        "status": status,
        "reasons": reasons,
    }
