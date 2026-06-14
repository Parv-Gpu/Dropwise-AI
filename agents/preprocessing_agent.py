from typing import Dict, Any


def preprocess_session(session: Dict[str, Any]) -> Dict[str, Any]:
    events = session.get("events", [])

    if not events:
        return {
            "session_id": session.get("session_id"),
            "session_duration": 0,
            "total_events": 0,
            "page_views": 0,
            "clicks": 0,
            "scrolls": 0,
            "unique_pages": 0,
            "exit_page": None,
            "device": session.get("device")
        }

    timestamps = [event["timestamp"] for event in events if "timestamp" in event]

    page_views = sum(1 for e in events if e.get("type") == "page_view")
    clicks = sum(1 for e in events if e.get("type") == "click")
    scrolls = sum(1 for e in events if e.get("type") == "scroll")

    pages = [
        e.get("page")
        for e in events
        if e.get("page") is not None
    ]

    return {
        "session_id": session.get("session_id"),
        "user_id": session.get("user_id"),
        "device": session.get("device"),
        "session_duration": max(timestamps) - min(timestamps) if timestamps else 0,
        "total_events": len(events),
        "page_views": page_views,
        "clicks": clicks,
        "scrolls": scrolls,
        "unique_pages": len(set(pages)),
        "pages_visited": session.get("pages_visited", []),
        "exit_page": session.get("pages_visited", [None])[-1],
        "ground_truth": session.get("ground_truth")
    }