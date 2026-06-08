import json
import re
from datetime import datetime
from llm_engine import run_llm
from utils.data_loader import PRODUCTS
from models.schema import ClaimResponse
import os

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

LOG_FILE = os.path.join(REPORT_DIR, "evaluation_logs.json")


product_names = PRODUCTS.keys()

SYSTEM_PROMPT = f"""
You are an Insurance Claims Assistant from SK Insurance Company.

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

### Available Products:
{PRODUCTS}

### Out-of-Scope Handling:
If the question is outside scope, respond EXACTLY with:
"Please ask questions about SK Insurance products only."

### Instructions:
- Think step-by-step internally before answering (do NOT show reasoning)
- First provide a natural, human-readable response
- Then generate structured JSON for internal processing
- Ensure the JSON is complete and valid

### Output Instructions:
- First provide a clear and friendly human-readable answer
- Then provide structured JSON for internal processing
- The JSON must be valid and complete
- Do NOT include extra explanations outside this format

"""

# ✅ Save JSON internally
def log_data(query, parsed_json):
 
    entry = {
        "query": query,
        "response": parsed_json,
        "timestamp": datetime.now().isoformat()   # ✅ ADDED
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def askllm(query, system_prompt):

    stream = run_llm(query, system_prompt)

    full_response = ""

    # ✅ Step 1: Collect stream → string
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        full_response += content

    parsed_json = None

    # ✅ Step 2: Extract JSON
    try:
        match = re.search(r"JSON:\s*(\{.*\})", full_response, re.DOTALL)

        if match:
            json_str = match.group(1)

            # ✅ Step 3: Convert JSON string → dict
            parsed = json.loads(json_str)

            # ✅ ✅ Step 4: Validate using Pydantic ✅ ✅
            validated = ClaimResponse(**parsed)

            parsed_json = validated.dict()

            # ✅ Step 5: Store JSON internally
            log_data(query, parsed_json)

        else:
            parsed_json = {"error": "JSON not found"}

    except Exception as e:
        parsed_json = {"error": f"Validation failed: {str(e)}"}

    # ✅ Step 6: Return ONLY text (no JSON)
    return full_response