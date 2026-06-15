from typing import Dict, Any


def preprocess_session(session: Dict[str, Any]) -> Dict[str, Any]:
    events = session.get("events", [])

    if not events:
        return {
            "session_id": session.get("session_id"),
            "user_id": session.get("user_id"),
            "device": session.get("device"),
            "session_duration": 0,
            "total_events": 0,
            "page_views": 0,
            "clicks": 0,
            "scrolls": 0,
            "max_scroll_depth": 0,
            "avg_scroll_depth": 0,
            "unique_pages": 0,
            "pages_visited": session.get("pages_visited", []),
            "entry_page": None,
            "actual_exit_page": None,
            "ground_truth": session.get("ground_truth")
        }

    timestamps = [
        event.get("timestamp")
        for event in events
        if event.get("timestamp") is not None
    ]

    page_views = sum(1 for event in events if event.get("type") == "page_view")
    clicks = sum(1 for event in events if event.get("type") == "click")
    scrolls = sum(1 for event in events if event.get("type") == "scroll")

    pages = [
        event.get("page")
        for event in events
        if event.get("page") is not None
    ]

    scroll_depths = []

    for event in events:
      if (
        event.get("type") == "scroll"
        and event.get("depth_percent") is not None
     ):
        try:
            scroll_depths.append(float(event.get("depth_percent")))
        except:
            pass

    max_scroll_depth = max(scroll_depths) if scroll_depths else 0
    avg_scroll_depth = round(sum(scroll_depths) / len(scroll_depths), 2) if scroll_depths else 0

    entry_page = pages[0] if pages else None
    actual_exit_page = pages[-1] if pages else None

    return {
        "session_id": session.get("session_id"),
        "user_id": session.get("user_id"),
        "device": session.get("device"),
        "session_duration": max(timestamps) - min(timestamps) if timestamps else 0,
        "total_events": len(events),
        "page_views": page_views,
        "clicks": clicks,
        "scrolls": scrolls,
        "max_scroll_depth": max_scroll_depth,
        "avg_scroll_depth": avg_scroll_depth,
        "unique_pages": len(set(pages)),
        "pages_visited": session.get("pages_visited", []),
        "entry_page": entry_page,
        "actual_exit_page": actual_exit_page,
        "ground_truth": session.get("ground_truth")
    }