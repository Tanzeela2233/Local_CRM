INTAKE_PROMPT = """
Extract lead information from the customer inquiry below.

Return ONLY a JSON object with exactly these fields:
{{
  "name": "",
  "company": "",
  "email": "",
  "phone": "",
  "service": "",
  "budget": "",
  "deadline": "",
  "intent": "",
  "urgency": "",
  "missing_fields": []
}}

Use empty strings when information is not provided.
Do not invent information.

Customer inquiry:
{inquiry}
"""

RESPONSE_PROMPT = """
Draft a professional customer reply.

Customer inquiry:
{inquiry}

Extracted lead:
{lead}

Approved company knowledge:
{knowledge}

Rules:
1. Use the approved company knowledge when answering company-specific questions.
2. Do not invent prices, discounts, guarantees, policies, services, or timelines.
3. If the knowledge base does not contain an answer, clearly say that the team
   can confirm the detail rather than making it up.
4. Keep the response concise and professional.
5. Address the customer's actual request.
6. Ask only useful follow-up questions when required.
"""
