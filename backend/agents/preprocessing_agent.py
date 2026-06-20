from typing import Dict, Any


def get_value(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


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

    timestamps = []

    for event in events:
        timestamp = get_value(event, "timestamp")

        if timestamp is not None:
            try:
                timestamps.append(int(timestamp))
            except:
                pass

    page_views = sum(
        1 for event in events
        if get_value(event, "type") == "page_view"
    )

    clicks = sum(
        1 for event in events
        if get_value(event, "type") == "click"
    )

    scrolls = sum(
        1 for event in events
        if get_value(event, "type") == "scroll"
    )

    pages = []

    for event in events:
        page = get_value(event, "page")

        if page is not None:
            pages.append(str(page))

    if not pages:
        pages = session.get("pages_visited", [])

    scroll_depths = []

    for event in events:
        event_type = get_value(event, "type")
        depth = get_value(event, "depth_percent")

        if event_type == "scroll" and depth is not None:
            try:
                scroll_depths.append(float(depth))
            except:
                pass

    max_scroll_depth = max(scroll_depths) if scroll_depths else 0
    avg_scroll_depth = round(sum(scroll_depths) / len(scroll_depths), 2) if scroll_depths else 0

    entry_page = pages[0] if pages else None

    real_pages = [
    page for page in pages
    if str(page).lower() != "exit"
    ]

    actual_exit_page = real_pages[-1] if real_pages else None

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
        "pages_visited": pages,
        "entry_page": entry_page,
        "actual_exit_page": actual_exit_page,
        "ground_truth": session.get("ground_truth")
    }