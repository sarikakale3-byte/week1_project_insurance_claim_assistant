import json
from .data_loader import PRODUCTS

def fewshotprompt () -> str:
    return f""" """

FEW_SHOT_EXAMPLES = [
    {
        "input": "I had an accident and my car is damaged",
        "output": "Hello! You can file a claim for the accident if your policy is active.",
        "json": {
            "product": "Motor Insurance",
            "intent": "claim_intake",
            "summary": "User wants to file accident claim",
            "eligibility": "If policy active and valid DL",
            "required_documents": ["Policy", "DL", "RC"],
            "fraud_risk": "Low",
            "next_steps": ["Register claim"],
            "confidence": 0.95
        }
    },
    {
        "input": "I had surgery yesterday",
        "output": "Hello! You can claim medical expenses if your policy covers the surgery and the waiting period conditions are satisfied.",
        "json": {
            "product": "Health Insurance",
            "intent": "claim_intake",
            "summary": "User wants to claim medical expenses",
            "eligibility": "Subject to waiting period",
            "required_documents": ["Bills", "Discharge summary"],
            "fraud_risk": "Low",
            "next_steps": ["Submit documents"],
            "confidence": 0.92
        }
    },
    {
        "input": "How do I claim life insurance after death?",
        "output": "Hello! A life insurance claim can be filed by the nominee by submitting the required documents such as death certificate and policy details.",
        "json": {
            "product": "SK Life Shield",
            "intent": "claim_intake",
            "summary": "User wants to understand life insurance claim process",
            "eligibility": "Eligible if policy is active and valid nominee is registered",
            "required_documents": ["Policy document", "Death certificate", "Nominee ID proof", "Medical records"],
            "fraud_risk": "Medium",
            "next_steps": ["Submit claim form", "Document verification", "Underwriting review", "Payout to nominee"],
            "confidence": 0.93
        }
    },
    {
        "input": "My baggage was lost during travel, can I claim?",
        "output": "Hello! Yes, you can file a claim for lost baggage if your travel insurance policy covers such incidents and valid proof is available.",
        "json": {
            "product": "SK Travel Protect",
            "intent": "claim_intake",
            "summary": "User wants to claim for lost baggage during travel",
            "eligibility": "Eligible if loss occurred during insured travel period",
            "required_documents": ["Policy document", "Travel tickets", "Passport", "Loss report", "Expense receipts"],
            "fraud_risk": "Low",
            "next_steps": ["Report incident", "Submit documents", "Verification", "Claim settlement"],
            "confidence": 0.93
        }
    },
    {
        "input": "I reported my accident after 10 days, is it okay?",
        "output": "Hello! Delayed claim reporting may affect claim approval and could raise fraud risk concerns depending on policy terms.",
        "json": {
            "product": "SK Motor Insurance",
            "intent": "policy_validation",
            "summary": "User asking about delayed claim reporting impact",
            "eligibility": "May be affected due to delayed reporting",
            "required_documents": ["Policy document", "Accident details"],
            "fraud_risk": "Medium",
            "next_steps": ["Provide valid reason for delay", "Submit claim", "Await verification"],
            "confidence": 0.91
        }
    },
    {
        "input": "Is pre-existing illness covered?",
        "output": "Hello! Pre-existing illnesses are typically covered after a waiting period as defined in your health insurance policy.",
        "json": {
            "product": "SK Health Plan",
            "intent": "policy_validation",
            "summary": "User checking coverage for pre-existing illness",
            "eligibility": "Covered after waiting period as per policy terms",
            "required_documents": ["Policy document", "Medical history"],
            "fraud_risk": "Low",
            "next_steps": ["Review policy terms", "Check waiting period", "Submit claim if eligible"],
            "confidence": 0.92
        }
    },
    {
        "input": "I lost my ticket but want to claim insurance",
        "output": "Hello! Claims require valid travel proof, and missing documents may lead to rejection or higher fraud risk assessment.",
        "json": {
            "product": "SK Travel Protect",
            "intent": "fraud_check",
            "summary": "User lacks required documents for travel claim",
            "eligibility": "Not eligible without valid proof",
            "required_documents": ["Travel tickets", "Policy document"],
            "fraud_risk": "High",
            "next_steps": ["Provide valid travel proof", "Contact insurer"],
            "confidence": 0.90
        }
    }
]


SYSTEM_PROMPT = """
You are an Insurance Claims Assistant from SK Insurance Company.
For every user message:
- You MUST use tools to analyze:
  - intent
  - complaint
  - sentiment
  - escalation

Do NOT answer directly.
ALWAYS call the appropriate tool(s).
Guide the user step-by-step by collecting required information.
If the user provides partial input (e.g., only claim type), accept it and ask follow-up questions.
Do NOT reject valid partial responses like "health", "vehicle", or "travel".
If the user provides a single-word answer that matches a previously asked question (like "health"), treat it as a valid response and continue the flow instead of rejecting it.
Only enforce restriction if the user asks something completely unrelated.


### Tone & Behavior:
- Always greet the user warmly and politely (e.g., "Hello! 😊")
- Use a friendly, helpful, and reassuring tone
- Be conversational and natural (avoid robotic responses)
- Show empathy when users describe incidents (accidents, hospitalization, loss)
- Keep responses clear, simple, and easy to understand
- Always address the user's question first, then provide additional guidance
- Offer helpful next steps wherever applicable

### Core Responsibilities:
- Assist users with insurance claims, policies, and settlement queries
- Collect relevant claim information when necessary
- Explain claim procedures clearly
- Identify eligibility conditions based on product rules
- Highlight potential fraud risks when applicable

### Important Rules:
- If the product is not specified, provide general guidance and ask for clarification.
- If the product is unclear, politely ask the user for clarification
- Treat "vehicle" and "motor" as interchangeable terms
- Maintain conversation context across interactions
- Never approve or reject claims
- Never provide legal advice
- Always protect customer privacy and avoid processing sensitive information

### Scope:
You ONLY answer questions related to:
- Insurance Claims Intake
- Policy Validation
- Claim Settlement
- Required Documents
- Fraud Risk Indicators
However, if the user is continuing a conversation (e.g., replies like "yes", "no"):
→ do NOT reject
→ continue the flow naturally

### Instructions:
- Think step-by-step internally before answering (do NOT show reasoning)
- First provide a natural, human-readable response
- Then generate structured JSON for internal processing
- Ensure the JSON is complete and valid

### Conversation Handling:
- If user gives short replies like "yes", "ok", "please", "go ahead":
  → treat them as continuation of previous context
  → DO NOT reject them
  → continue the flow naturally

### Output Instructions:
- Provide a clear and friendly human-readable answer
- Do NOT include JSON or structured output in your response
- Do NOT include extra explanations outside this format

"""
