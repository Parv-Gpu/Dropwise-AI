from typing import List, Optional, Literal
from pydantic import BaseModel


class Event(BaseModel):
    type: Literal[
        "page_view",
        "click",
        "scroll",
        "search",
        "input",
        "exit",
        "zoom"
    ]

    timestamp: int
    page: str

    element: Optional[str] = None
    depth_percent: Optional[float] = None


class GroundTruth(BaseModel):
    primary_reason: str
    drop_off_stage: str
    persona: str


class SessionData(BaseModel):
    session_id: str
    user_id: str
    device: str

    start_time: int

    events: List[Event]

    pages_visited: List[str]

    ground_truth: Optional[GroundTruth] = None