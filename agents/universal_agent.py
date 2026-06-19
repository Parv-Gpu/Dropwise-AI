from typing import Dict, Any


def generate_signals(
    preprocessing_output: Dict[str, Any],
    behavior_output: Dict[str, Any]
) -> Dict[str, Any]:

    metrics = behavior_output.get("behavior_metrics", {})

    price_sensitive = (
        metrics.get("price_checks", 0) >= 1
        or metrics.get("coupon_searches", 0) >= 1
    )

    trust_seeking = (
        metrics.get("review_checks", 0) >= 1
        or metrics.get("return_policy_checks", 0) >= 1
    )

    product_fit_concern = (
        metrics.get("size_chart_opens", 0) >= 1
        or (
            metrics.get("image_zooms", 0) >= 2
            and metrics.get("return_policy_checks", 0) >= 1
        )
    )

    checkout_friction = (
        metrics.get("checkout_attempts", 0) >= 1
        and metrics.get("login_or_account_hits", 0) >= 1
    )

    delivery_concern = (
        metrics.get("delivery_checks", 0) >= 2
    )

    comparison_behavior = (
        metrics.get("comparison_actions", 0) >= 1
        or metrics.get("product_page_visits", 0) >= 3
    )

    product_information_gap = (
        metrics.get("product_detail_checks", 0) >= 2
        or metrics.get("faq_checks", 0) >= 1
        or metrics.get("material_checks", 0) >= 1
    )

    has_strong_signal = any([
        price_sensitive,
        trust_seeking,
        product_fit_concern,
        checkout_friction,
        delivery_concern,
        comparison_behavior,
        product_information_gap
    ])

    low_purchase_intent = (
        not has_strong_signal
        and metrics.get("cart_additions", 0) == 0
        and metrics.get("checkout_attempts", 0) == 0
        and metrics.get("cta_clicks", 0) == 0
        and metrics.get("engagement_score", 0) <= 2
    )

    if metrics.get("checkout_attempts", 0) > 0:
        purchase_intent = "high"
    elif (
        metrics.get("cart_additions", 0) > 0
        or metrics.get("cta_clicks", 0) > 0
        or metrics.get("engagement_score", 0) >= 3
        or has_strong_signal
    ):
        purchase_intent = "medium"
    else:
        purchase_intent = "low"

    signals = {
        "price_sensitive": price_sensitive,
        "trust_seeking": trust_seeking,
        "product_fit_concern": product_fit_concern,
        "checkout_friction": checkout_friction,
        "delivery_concern": delivery_concern,
        "comparison_behavior": comparison_behavior,
        "product_information_gap": product_information_gap,
        "low_purchase_intent": low_purchase_intent,
        "purchase_intent": purchase_intent
    }

    return {
        "session_id": preprocessing_output.get("session_id"),
        "signals": signals
    }