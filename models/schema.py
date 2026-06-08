
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class ClaimResponse(BaseModel):
    # Core response fields
    product: str = Field(..., description="Insurance product name")
    intent: str = Field(..., description="Detected user intent")
    summary: str = Field(..., description="Short summary of user request")
    
    # Claim processing details
    eligibility: str = Field(..., description="Eligibility status or rules")
    required_documents: List[str] = Field(default_factory=list)
    
    # Risk & fraud
    fraud_risk: str = Field(..., description="Low / Medium / High")
    
    # Actions
    next_steps: List[str] = Field(default_factory=list)
    
    # Confidence score (0 to 1)
    confidence: float = Field(..., ge=0.0, le=1.0)

    # fields (for evaluation / debugging)
    reasoning: Optional[str] = Field(
        default=None,
        description="Internal reasoning (hidden in UI, used for debugging)"
    )
    
    guardrail_flags: Optional[List[str]] = Field(
        default_factory=list,
        description="List of triggered guardrails (PII, injection, etc.)"
    )

    # Validation Rules
    @field_validator("fraud_risk")
    def validate_fraud_risk(cls, value):
        allowed = ["Low", "Medium", "High"]
        if value not in allowed:
            raise ValueError(f"fraud_risk must be one of {allowed}")
        return value

    @field_validator("intent")
    def validate_intent(cls, value):
        allowed_intents = [
            "claim_intake",
            "claim_status",
            "policy_validation",
            "fraud_check",
            "general_query",
            "unknown"
        ]
        if value not in allowed_intents:
            raise ValueError(f"Invalid intent: {value}")
        return value

    @field_validator("product")
    def validate_product(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Product cannot be empty")
        return value