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

    all_text = elements + pages

    def count_keywords(keywords):
        count = 0
        for item in all_text:
            if any(keyword in item for keyword in keywords):
                count += 1
        return count

    product_pages = [
        page for page in pages
        if "/product" in page or "/products" in page
    ]

    behavior = {
        "price_checks": count_keywords(["price", "subtotal", "total", "cost"]),
        "coupon_searches": count_keywords(["coupon", "discount", "offer"]),

        "review_checks": count_keywords(["review", "rating", "verified"]),
        "return_policy_checks": count_keywords(["return", "refund", "exchange"]),

        "size_chart_opens": count_keywords(["size_chart", "size-chart", "size", "fit"]),
        "image_zooms": count_keywords(["zoom", "image"]),

        "cart_additions": count_keywords(["add_to_cart", "add_to_cart_button"]),
        "checkout_attempts": count_keywords(["checkout"]),
        "login_or_account_hits": count_keywords(["login", "account", "create-account", "signup"]),

        "delivery_checks": count_keywords(["delivery", "shipping", "pincode", "shipping_cost"]),

        "comparison_actions": count_keywords(["compare", "comparison", "specs", "specification"]),

        "product_detail_checks": count_keywords(["details", "description", "product_details", "product_description"]),
        "faq_checks": count_keywords(["faq", "faqs"]),
        "material_checks": count_keywords(["material", "fabric", "quality"]),
        "spec_checks": count_keywords(["spec", "specs", "specification"]),

        "back_clicks": count_keywords(["back", "back_button"]),
        "exit_clicks": count_keywords(["exit", "close", "cancel"]),

        "product_page_visits": len(product_pages),

        "cta_clicks": count_keywords(["add_to_cart", "buy_now", "checkout"])
    }

    return {
        "session_id": session.get("session_id"),
        "behavior_metrics": behavior
    }