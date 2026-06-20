from pydantic import BaseModel


class BehaviorMetrics(BaseModel):
    price_checks: int = 0
    coupon_searches: int = 0
    review_checks: int = 0
    return_policy_checks: int = 0
    size_chart_opens: int = 0
    image_zooms: int = 0
    cart_additions: int = 0
    checkout_attempts: int = 0
    login_or_account_hits: int = 0
    delivery_checks: int = 0
    comparison_actions: int = 0
    product_detail_checks: int = 0
    faq_checks: int = 0
    material_checks: int = 0
    spec_checks: int = 0
    back_clicks: int = 0
    exit_clicks: int = 0
    product_page_visits: int = 0
    cta_clicks: int = 0


class BehaviorOutput(BaseModel):
    session_id: str
    behavior_metrics: BehaviorMetrics