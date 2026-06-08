import json

def build_prompt(query, product_info):

    prompt = f"""
You are processing an insurance-related query.

### Instructions:
- First provide a natural, human-friendly answer to the user
- Then provide structured JSON output
- Use ONLY the provided product information
- Detect fraud risk appropriately
- Do NOT include explanations outside the defined format
- Think step-by-step internally before answering
- Do NOT include reasoning in output


### Product Information:
{json.dumps(product_info, indent=2)}

### Few-shot Examples:

Example 1:
User: I had an accident and my car is damaged
Answer:
Hello! You can file a claim for the accident if your policy is active.

JSON:
{{
  "product": "Motor Insurance",
  "intent": "claim_intake",
  "summary": "User wants to file accident claim",
  "eligibility": "If policy active and valid DL",
  "required_documents": ["Policy", "DL", "RC"],
  "fraud_risk": "Low",
  "next_steps": ["Register claim"],
  "confidence": 0.95
}}

Example 2:
User: I had surgery yesterday
Answer:
Hello! You can claim medical expenses if your policy covers the surgery and the waiting period conditions are satisfied.

JSON:
{{
  "product": "Health Insurance",
  "intent": "claim_intake",
  "summary": "User wants to claim medical expenses",
  "eligibility": "Subject to waiting period",
  "required_documents": ["Bills", "Discharge summary"],
  "fraud_risk": "Low",
  "next_steps": ["Submit documents"],
  "confidence": 0.92
}}


Example 3 (Life Insurance - Claim Process):
User: How do I claim life insurance after death?
Answer:
Hello! A life insurance claim can be filed by the nominee by submitting the required documents such as death certificate and policy details.
JSON:
{{
  "product": "SK Life Shield",
  "intent": "claim_intake",
  "summary": "User wants to understand life insurance claim process",
  "eligibility": "Eligible if policy is active and valid nominee is registered",
  "required_documents": ["Policy document", "Death certificate", "Nominee ID proof", "Medical records"],
  "fraud_risk": "Medium",
  "next_steps": ["Submit claim form", "Document verification", "Underwriting review", "Payout to nominee"],
  "confidence": 0.93
}}


Example 4 (Travel Insurance - Claim):
User: My baggage was lost during travel, can I claim?
Answer:
Hello! Yes, you can file a claim for lost baggage if your travel insurance policy covers such incidents and valid proof is available.
JSON:
{{
  "product": "SK Travel Protect",
  "intent": "claim_intake",
  "summary": "User wants to claim for lost baggage during travel",
  "eligibility": "Eligible if loss occurred during insured travel period",
  "required_documents": ["Policy document", "Travel tickets", "Passport", "Loss report", "Expense receipts"],
  "fraud_risk": "Low",
  "next_steps": ["Report incident", "Submit documents", "Verification", "Claim settlement"],
  "confidence": 0.93
}}


Example 5 (Motor Insurance - Fraud Scenario):
User: I reported my accident after 10 days, is it okay?
Answer:
Hello! Delayed claim reporting may affect claim approval and could raise fraud risk concerns depending on policy terms.
JSON:
{{
  "product": "SK Motor Insurance",
  "intent": "policy_validation",
  "summary": "User asking about delayed claim reporting impact",
  "eligibility": "May be affected due to delayed reporting",
  "required_documents": ["Policy document", "Accident details"],
  "fraud_risk": "Medium",
  "next_steps": ["Provide valid reason for delay", "Submit claim", "Await verification"],
  "confidence": 0.91
}}


Example 6 (Health Insurance – Policy Validation):
User: Is pre-existing illness covered?
Answer:
Hello! Pre-existing illnesses are typically covered after a waiting period as defined in your health insurance policy.
JSON:
{{
  "product": "SK Health Plan",
  "intent": "policy_validation",
  "summary": "User checking coverage for pre-existing illness",
  "eligibility": "Covered after waiting period as per policy terms",
  "required_documents": ["Policy document", "Medical history"],
  "fraud_risk": "Low",
  "next_steps": ["Review policy terms", "Check waiting period", "Submit claim if eligible"],
  "confidence": 0.92
}}


Example 7 (Travel Insurance – Fraud Risk):
User: I lost my ticket but want to claim insurance
Answer:
Hello! Claims require valid travel proof, and missing documents may lead to rejection or higher fraud risk assessment.
JSON:
{{
  "product": "SK Travel Protect",
  "intent": "fraud_check",
  "summary": "User lacks required documents for travel claim",
  "eligibility": "Not eligible without valid proof",
  "required_documents": ["Travel tickets", "Policy document"],
  "fraud_risk": "High",
  "next_steps": ["Provide valid travel proof", "Contact insurer"],
  "confidence": 0.90
}}


### User Query:
{query}

### Output Format:

Answer:
<write a clear, friendly response>

JSON:
{{
  "product": "",
  "intent": "",
  "summary": "",
  "eligibility": "",
  "required_documents": [],
  "fraud_risk": "",
  "next_steps": [],
  "confidence": 0.0
}}
"""

    return prompt