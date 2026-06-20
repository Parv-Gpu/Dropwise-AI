from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from schemas.reason_schema import ReasonType


class FinalOutput(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    device: Optional[str] = None

    predicted_reason: ReasonType
    secondary_reason: Optional[ReasonType] = None
    ground_truth_reason: Optional[str] = None
    is_correct: Optional[bool] = None

    confidence_score: float
    confidence_level: str
    reason_scores: Dict[str, float]

    preprocessing: Dict[str, Any]
    behavior_metrics: Dict[str, Any]
    signals: Dict[str, Any]
    evidence: List[str]
    recommended_actions: List[str]