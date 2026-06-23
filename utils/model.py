from pydantic import BaseModel, Field
from enum import Enum

class IntentResult(BaseModel):
    intent: str = Field(description="Type of insurance request")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    product: str = Field(description="Insurance product (Motor, Health, Life, Travel)")
    routing: str = Field(description="Service to route (claims_api, policy_system, etc.)")

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer insurance message"
    )
    session_id: str = Field(
        default="default",
        description="session identifier"
    )

class ChatResponse(BaseModel):
    response: str
    session_id: str
    cached: bool = False