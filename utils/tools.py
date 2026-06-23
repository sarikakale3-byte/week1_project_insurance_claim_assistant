from langchain_core.tools import tool
from pydantic import BaseModel, Field

class IntentResult(BaseModel):
    intent: str = Field(description="Type of insurance request")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    product: str = Field(description="Insurance product (Motor, Health, Life, Travel)")
    routing: str = Field(description="Service to route (claims_api, policy_system, etc.)")

@tool
def classify_intent(customer_message: str) -> IntentResult:
    """
    Classify customer intent for insurance queries.
    Extract intent, product, confidence, and routing.
    return in the JSON format 
    class IntentResult(BaseModel):
    intent: str = Field(description="Type of insurance request")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    product: str = Field(description="Insurance product (Motor, Health, Life, Travel)")
    routing: str = Field(description="Service to route (claims_api, policy_system, etc.)")
    """

class ComplaintResult(BaseModel):
    is_complaint: bool = Field(description="Whether message is a complaint")
    complaint_type: str = Field(description="Type (delay, denial, service, pricing)")
    severity: str = Field(description="low, medium, high")
    confidence: float = Field(ge=0, le=1)

@tool
def detect_complaint(customer_message: str) -> ComplaintResult:
    """
    Detect if the message contains a complaint and classify it.
    return in the JSON format 
    class ComplaintResult(BaseModel):
    is_complaint: bool = Field(description="Whether message is a complaint")
    complaint_type: str = Field(description="Type (delay, denial, service, pricing)")
    severity: str = Field(description="low, medium, high")
    confidence: float = Field(ge=0, le=1)
    """

class SentimentResult(BaseModel):
    sentiment: str = Field(description="positive, neutral, negative")
    score: float = Field(description="Range -1 (negative) to +1 (positive)")
    emotion: str = Field(description="happy, angry, frustrated, confused")

@tool
def analyze_sentiment(customer_message: str) -> SentimentResult:
    """
    Analyze sentiment and emotional tone of the message.
    return in the JSON format 
class SentimentResult(BaseModel):
    sentiment: str = Field(description="positive, neutral, negative")
    score: float = Field(description="Range -1 (negative) to +1 (positive)")
    emotion: str = Field(description="happy, angry, frustrated, confused")
    """

class EscalationResult(BaseModel):
    escalate: bool = Field(description="Whether escalation is needed")
    level: str = Field(description="L1, L2, Manager, Fraud Team")
    reason: str = Field(description="Reason for escalation")
    priority: str = Field(description="low, medium, high, critical")

@tool
def decide_escalation(customer_message: str) -> EscalationResult:
    """
    Decide if escalation is required based on message severity.
    Escalate for:
    - high complaint severity
    - negative sentiment
    - fraud/legal signals
    return in json format
    class EscalationResult(BaseModel):
        escalate: bool = Field(description="Whether escalation is needed")
        level: str = Field(description="L1, L2, Manager, Fraud Team")
        reason: str = Field(description="Reason for escalation")
        priority: str = Field(description="low, medium, high, critical")
    """


#print(classify_intent.name)
#print(classify_intent.description)
#print(classify_intent.invoke({"customer_message": "my medical expense claim is not processed"}))
    
