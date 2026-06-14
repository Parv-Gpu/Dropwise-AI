from typing import Dict, Any


def generate_signals(preprocessing_output: Dict[str, Any],
                     behavior_output: Dict[str, Any]) -> Dict[str, Any]:

    metrics = behavior_output.get("behavior_metrics", {})

    signals = {
        "price_sensitive": (
            metrics.get("price_checks", 0) >= 2
            or metrics.get("coupon_searches", 0) >= 1
        ),

        "trust_seeking": (
            metrics.get("review_checks", 0) >= 2
            or metrics.get("return_policy_checks", 0) >= 1
        ),

        "product_fit_concern": (
            metrics.get("size_chart_opens", 0) >= 1
            or metrics.get("image_zooms", 0) >= 2
        ),

        "checkout_friction": (
            metrics.get("checkout_attempts", 0) >= 1
            and metrics.get("login_or_account_hits", 0) >= 1
        ),

        "delivery_concern": (
            metrics.get("delivery_checks", 0) >= 2
        ),

        "comparison_behavior": (
            metrics.get("comparison_actions", 0) >= 2
        ),

        "low_purchase_intent": (
            preprocessing_output.get("session_duration", 0) < 80
            and metrics.get("cta_clicks", 0) == 0
        )
    }

    if metrics.get("checkout_attempts", 0) > 0:
        purchase_intent = "high"
    elif metrics.get("cart_additions", 0) > 0 or metrics.get("cta_clicks", 0) > 0:
        purchase_intent = "medium"
    else:
        purchase_intent = "low"

    signals["purchase_intent"] = purchase_intent

    return {
        "session_id": preprocessing_output.get("session_id"),
        "signals": signals
    }