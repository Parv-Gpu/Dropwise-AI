from typing import Optional, Dict, Literal
from pydantic import BaseModel


ReasonType = Literal[
    "price_concern",
    "trust_concern",
    "product_fit_concern",
    "checkout_friction",
    "delivery_concern",
    "comparison_shopping",
    "product_information_gap",
    "low_purchase_intent"
]


class ReasonOutput(BaseModel):
    session_id: str
    primary_reason: ReasonType
    secondary_reason: Optional[ReasonType] = None
    confidence_score: float
    confidence_level: Literal["low", "medium", "high"]
    reason_scores: Dict[str, float]