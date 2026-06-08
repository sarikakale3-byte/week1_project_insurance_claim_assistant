import os
import json
from openai import OpenAI
from utils.data_loader import PRODUCTS
from utils.prompt_builder import build_prompt
from models.schema import ClaimResponse
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_product(query):
    q = query.lower()

    product_map = {
        "motor_insurance": ["car", "vehicle", "accident", "theft", "bike"],
        "health_insurance": ["hospital", "surgery", "medical"],
        "life_insurance": ["death", "nominee"],
        "travel_insurance": ["travel", "baggage", "flight"]
    }

    for product, keywords in product_map.items():
        if any(k in q for k in keywords):
            return product

    # handle generic claim queries
    if "claim" in q:
        return "general"

    return "unknown"

def run_llm(query,system_prompt):
    #product_key = detect_product(query)
    #product_info = PRODUCTS.get(product_key, {})

    #prompt = build_prompt(query, product_info)
    #print(f"BUILT prompt = {prompt}")

   # Detect product
    product_key = detect_product(query)
    product_info = PRODUCTS.get(product_key, {})

    # fallback for generic claim queries, this i added because when i was giving prompt like "what are next steps to file claim" it was not able to identify product and failing back to consider it as offtopic qstn
    if product_key == "general":
        product_info = {
            "name": "General Insurance",
            "coverage": ["General claim assistance"],
            "eligibility": "Depends on policy",
            "required_documents": ["Policy document", "ID proof"],
            "claim_process": [
                "Register claim",
                "Submit documents",
                "Verification",
                "Claim settlement"
            ],
            "fraud_indicators": ["Delayed reporting", "Missing documents"]
        }

    # fallback for unknown
    if not product_info:
        product_info = {
            "name": "Unknown Product"
        }

    #Build prompt with ONLY relevant product
    prompt = build_prompt(query, product_info)

    #prompt=query
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    return response