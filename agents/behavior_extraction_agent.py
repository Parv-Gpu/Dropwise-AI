from typing import Dict, Any


def extract_behavior(session: Dict[str, Any]) -> Dict[str, Any]:
    events = session.get("events", [])

    elements = [
        str(event.get("element", "")).lower()
        for event in events
        if event.get("element") is not None
    ]

    pages = [
        str(event.get("page", "")).lower()
        for event in events
        if event.get("page") is not None
    ]

    def count_keywords(keywords):
        count = 0
        for item in elements + pages:
            if any(keyword in item for keyword in keywords):
                count += 1
        return count

    behavior = {
        "price_checks": count_keywords(["price", "subtotal", "total", "cost"]),
        "coupon_searches": count_keywords(["coupon", "discount", "offer"]),
        "review_checks": count_keywords(["review", "rating", "verified"]),
        "return_policy_checks": count_keywords(["return", "refund", "exchange"]),
        "size_chart_opens": count_keywords(["size", "fit"]),
        "image_zooms": count_keywords(["zoom", "image"]),
        "cart_additions": count_keywords(["add_to_cart", "add_to_cart_button"]),
        "checkout_attempts": count_keywords(["checkout"]),
        "login_or_account_hits": count_keywords(["login", "account", "create-account", "signup"]),
        "delivery_checks": count_keywords(["delivery", "shipping", "pincode", "shipping_cost"]),
        "comparison_actions": count_keywords(["compare", "specs", "product_456", "product_123"]),
        "cta_clicks": count_keywords(["add_to_cart", "buy_now", "checkout"]),
    }

    return {
        "session_id": session.get("session_id"),
        "behavior_metrics": behavior
    }