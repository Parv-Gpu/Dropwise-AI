from typing import Dict, Any


def detect_reason(signal_output: Dict[str, Any],
                  behavior_output: Dict[str, Any] = None) -> Dict[str, Any]:

    signals = signal_output.get("signals", {})
    metrics = behavior_output.get("behavior_metrics", {}) if behavior_output else {}

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

    # Price concern
    reason_scores["price_concern"] += metrics.get("price_checks", 0) * 0.8
    reason_scores["price_concern"] += metrics.get("coupon_searches", 0) * 1.0

    # Trust concern
    reason_scores["trust_concern"] += metrics.get("review_checks", 0) * 0.8
    reason_scores["trust_concern"] += metrics.get("return_policy_checks", 0) * 0.7

    # Product fit concern
    reason_scores["product_fit_concern"] += metrics.get("size_chart_opens", 0) * 1.2
    reason_scores["product_fit_concern"] += metrics.get("image_zooms", 0) * 0.4
    reason_scores["product_fit_concern"] += metrics.get("return_policy_checks", 0) * 0.4

    # Checkout friction
    reason_scores["checkout_friction"] += metrics.get("checkout_attempts", 0) * 1.0
    reason_scores["checkout_friction"] += metrics.get("login_or_account_hits", 0) * 1.2

    # Delivery concern
    reason_scores["delivery_concern"] += metrics.get("delivery_checks", 0) * 1.0

    # Comparison shopping
    reason_scores["comparison_shopping"] += metrics.get("comparison_actions", 0) * 1.0

    # Product information gap
    reason_scores["product_information_gap"] += metrics.get("image_zooms", 0) * 0.5
    reason_scores["product_information_gap"] += metrics.get("product_detail_checks", 0) * 1.0
    reason_scores["product_information_gap"] += metrics.get("faq_checks", 0) * 1.0
    reason_scores["product_information_gap"] += metrics.get("material_checks", 0) * 1.0

    # Low purchase intent
    if signals.get("purchase_intent") == "low":
        reason_scores["low_purchase_intent"] += 2

    if signals.get("low_purchase_intent"):
        reason_scores["low_purchase_intent"] += 3

    sorted_reasons = sorted(
        reason_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_reason = sorted_reasons[0][0]
    primary_score = sorted_reasons[0][1]

    secondary_reason = None
    secondary_score = sorted_reasons[1][1]

    if secondary_score >= 1.5:
        secondary_reason = sorted_reasons[1][0]

    total_score = sum(reason_scores.values())

    if total_score == 0:
        confidence_score = 0.3
    else:
        confidence_score = round(primary_score / total_score, 2)

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