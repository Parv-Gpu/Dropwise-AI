from typing import Literal
from pydantic import BaseModel


class Signals(BaseModel):
    price_sensitive: bool = False
    trust_seeking: bool = False
    product_fit_concern: bool = False
    checkout_friction: bool = False
    delivery_concern: bool = False
    comparison_behavior: bool = False
    low_purchase_intent: bool = False
    purchase_intent: Literal["low", "medium", "high"] = "low"


class SignalOutput(BaseModel):
    session_id: str
    signals: Signals