from typing import Dict, Any


def detect_reason(
    signal_output: Dict[str, Any],
    behavior_output: Dict[str, Any]
) -> Dict[str, Any]:

    signals = signal_output.get("signals", {})
    metrics = behavior_output.get("behavior_metrics", {})

    reason_scores = {
        "price_concern": 0,
        "trust_concern": 0,
        "product_fit_concern": 0,
        "checkout_friction": 0,
        "delivery_concern": 0,
        "comparison_shopping": 0,
        "product_information_gap": 0,
        "low_purchase_intent": 0
    }

    purchase_intent = signals.get("purchase_intent")
    cart_additions = metrics.get("cart_additions", 0)
    checkout_attempts = metrics.get("checkout_attempts", 0)

    # Metric-based scoring
    reason_scores["price_concern"] += metrics.get("price_checks", 0) * 1.5
    reason_scores["price_concern"] += metrics.get("coupon_searches", 0) * 2.0

    reason_scores["trust_concern"] += metrics.get("review_checks", 0) * 0.9
    reason_scores["trust_concern"] += metrics.get("return_policy_checks", 0) * 0.6

    reason_scores["product_fit_concern"] += metrics.get("size_chart_opens", 0) * 1.5
    reason_scores["product_fit_concern"] += metrics.get("image_zooms", 0) * 0.4
    reason_scores["product_fit_concern"] += metrics.get("return_policy_checks", 0) * 0.3

    reason_scores["checkout_friction"] += checkout_attempts * 1.2
    reason_scores["checkout_friction"] += metrics.get("login_or_account_hits", 0) * 1.2

    reason_scores["delivery_concern"] += metrics.get("delivery_checks", 0) * 1.3

    reason_scores["comparison_shopping"] += metrics.get("comparison_actions", 0) * 1.2
    reason_scores["comparison_shopping"] += metrics.get("product_page_visits", 0) * 0.25

    reason_scores["product_information_gap"] += metrics.get("product_detail_checks", 0) * 1.2
    reason_scores["product_information_gap"] += metrics.get("faq_checks", 0) * 1.2
    reason_scores["product_information_gap"] += metrics.get("material_checks", 0) * 1.2

    # Signal-based boosts
    if signals.get("price_sensitive"):
        reason_scores["price_concern"] += 1.0

    if signals.get("trust_seeking"):
        reason_scores["trust_concern"] += 1.0

    if signals.get("product_fit_concern"):
        reason_scores["product_fit_concern"] += 1.0

    if signals.get("checkout_friction"):
        reason_scores["checkout_friction"] += 1.0

    if signals.get("delivery_concern"):
        reason_scores["delivery_concern"] += 1.0

    if signals.get("comparison_behavior"):
        reason_scores["comparison_shopping"] += 1.0

    if signals.get("product_information_gap"):
        reason_scores["product_information_gap"] += 1.0

    # Low intent should only win when no meaningful behavior exists
    non_low_max_score = max(
        score
        for reason, score in reason_scores.items()
        if reason != "low_purchase_intent"
    )

    if (
        signals.get("low_purchase_intent")
        and purchase_intent == "low"
        and cart_additions == 0
        and checkout_attempts == 0
        and non_low_max_score < 1.0
    ):
        reason_scores["low_purchase_intent"] += 2.0

    sorted_reasons = sorted(
        reason_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_reason = sorted_reasons[0][0]
    secondary_reason = None

    if sorted_reasons[1][1] >= 1.5:
        secondary_reason = sorted_reasons[1][0]

    total_score = sum(reason_scores.values())

    if total_score == 0:
        confidence_score = 0.3
    else:
        confidence_score = round(sorted_reasons[0][1] / total_score, 2)

    if confidence_score >= 0.75:
        confidence_level = "high"
    elif confidence_score >= 0.5:
        confidence_level = "medium"
    else:
        confidence_level = "low"

    return {
        "session_id": signal_output.get("session_id"),
        "primary_reason": primary_reason,
        "secondary_reason": secondary_reason,
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "reason_scores": reason_scores
    }