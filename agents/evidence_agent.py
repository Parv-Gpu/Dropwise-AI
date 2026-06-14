from typing import Dict, Any, List


def generate_evidence(
    preprocessing_output: Dict[str, Any],
    behavior_output: Dict[str, Any],
    reason_output: Dict[str, Any]
) -> Dict[str, Any]:

    metrics = behavior_output.get("behavior_metrics", {})
    primary_reason = reason_output.get("primary_reason")

    evidence: List[str] = []

    if primary_reason == "price_concern":
        if metrics.get("price_checks", 0) > 0:
            evidence.append(f"User checked price-related elements {metrics.get('price_checks')} times.")
        if metrics.get("coupon_searches", 0) > 0:
            evidence.append(f"User searched or clicked coupon/discount elements {metrics.get('coupon_searches')} times.")
        if metrics.get("cart_additions", 0) > 0 and metrics.get("checkout_attempts", 0) == 0:
            evidence.append("User added product to cart but did not proceed to checkout.")

    elif primary_reason == "trust_concern":
        if metrics.get("review_checks", 0) > 0:
            evidence.append(f"User checked reviews/ratings/verified purchase details {metrics.get('review_checks')} times.")
        if metrics.get("return_policy_checks", 0) > 0:
            evidence.append(f"User checked return/refund/exchange policy {metrics.get('return_policy_checks')} times.")

    elif primary_reason == "product_fit_concern":
        if metrics.get("size_chart_opens", 0) > 0:
            evidence.append(f"User opened size/fit related elements {metrics.get('size_chart_opens')} times.")
        if metrics.get("image_zooms", 0) > 0:
            evidence.append(f"User zoomed or inspected product images {metrics.get('image_zooms')} times.")
        if metrics.get("return_policy_checks", 0) > 0:
            evidence.append("User checked return policy, indicating hesitation about fit or suitability.")

    elif primary_reason == "checkout_friction":
        if metrics.get("checkout_attempts", 0) > 0:
            evidence.append(f"User attempted checkout {metrics.get('checkout_attempts')} times.")
        if metrics.get("login_or_account_hits", 0) > 0:
            evidence.append(f"User encountered login/account creation related steps {metrics.get('login_or_account_hits')} times.")

    elif primary_reason == "delivery_concern":
        if metrics.get("delivery_checks", 0) > 0:
            evidence.append(f"User checked delivery/shipping/pincode related information {metrics.get('delivery_checks')} times.")

    elif primary_reason == "comparison_shopping":
        if metrics.get("comparison_actions", 0) > 0:
            evidence.append(f"User performed comparison/specification related actions {metrics.get('comparison_actions')} times.")
        evidence.append("User visited multiple product pages without moving to checkout.")

    elif primary_reason == "low_purchase_intent":
        evidence.append(f"Session duration was only {preprocessing_output.get('session_duration')} seconds.")
        evidence.append(f"CTA clicks were {metrics.get('cta_clicks', 0)}, indicating weak purchase intent.")

    if not evidence:
        evidence.append("User behavior showed insufficient strong signals; reason inferred from overall session pattern.")

    return {
        "session_id": reason_output.get("session_id"),
        "evidence": evidence
    }