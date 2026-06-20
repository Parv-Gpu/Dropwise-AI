from typing import Dict, Any


def get_value(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def extract_behavior(session: Dict[str, Any]) -> Dict[str, Any]:
    events = session.get("events", [])

    elements = []
    pages = []
    event_types = []

    for event in events:
        element = get_value(event, "element")
        page = get_value(event, "page")
        event_type = get_value(event, "type")

        if element is not None:
            elements.append(str(element).lower())

        if page is not None:
            pages.append(str(page).lower())

        if event_type is not None:
            event_types.append(str(event_type).lower())

    pages_visited = [
        str(page).lower()
        for page in session.get("pages_visited", [])
        if page is not None
    ]

    pages = list(set(pages + pages_visited))
    all_text = elements + pages + event_types

    def count_keywords(keywords):
        return sum(
            1
            for item in all_text
            if any(keyword in item for keyword in keywords)
        )

    product_pages = [
        page for page in pages
        if "/product" in page or "/products" in page
    ]

    behavior = {
        "price_checks": count_keywords([
            "price", "subtotal", "total", "cost", "summary", "coupon"
        ]),

        "coupon_searches": count_keywords([
            "coupon", "discount", "offer", "promo"
        ]),

        "review_checks": count_keywords([
            "review", "rating", "verified", "testimonial", "customer-review"
        ]),

        "return_policy_checks": count_keywords([
            "return", "refund", "exchange", "return-policy", "return_policy"
        ]),

        "size_chart_opens": count_keywords([
            "size", "fit", "size_chart", "size-chart", "sizechart"
        ]),

        "image_zooms": count_keywords([
            "zoom", "image", "gallery", "photo"
        ]),

        "cart_additions": count_keywords([
            "add_to_cart", "add-to-cart", "addtocart"
        ]),

        "checkout_attempts": count_keywords([
            "checkout", "payment", "place-order", "place_order"
        ]),

        "login_or_account_hits": count_keywords([
            "login", "signup", "sign-up", "account",
            "create_account", "create-account"
        ]),

        "delivery_checks": count_keywords([
            "delivery", "shipping", "pincode", "charges",
            "delivery-policy", "delivery_charges"
        ]),

        "comparison_actions": count_keywords([
            "compare", "comparison", "spec", "specs", "specification"
        ]),

        "product_detail_checks": count_keywords([
            "details", "description", "information", "info",
            "product-detail", "product_details"
        ]),

        "faq_checks": count_keywords([
            "faq", "faqs", "help"
        ]),

        "material_checks": count_keywords([
            "material", "fabric", "quality", "materials_used"
        ]),

        "spec_checks": count_keywords([
            "spec", "specs", "specification"
        ]),

        "back_clicks": count_keywords([
            "back", "back_button"
        ]),

        "exit_clicks": count_keywords([
            "exit", "exits", "close", "cancel"
        ]),

        "product_page_visits": len(product_pages),

        "cta_clicks": count_keywords([
            "buy_now", "buy-now", "checkout",
            "add_to_cart", "add-to-cart", "addtocart"
        ])
    }

    behavior["engagement_score"] = (
        behavior["product_page_visits"]
        + behavior["cta_clicks"]
        + behavior["product_detail_checks"]
    )

    behavior["session_depth"] = len(set(pages))

    return {
        "session_id": session.get("session_id"),
        "behavior_metrics": behavior
    }