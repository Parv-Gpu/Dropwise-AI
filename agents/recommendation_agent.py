from typing import Dict, Any


def generate_recommendation(reason_output: Dict[str, Any]) -> Dict[str, Any]:

    primary_reason = reason_output.get("primary_reason")

    recommendations = {

        "price_concern": [
            "Show shipping charges earlier before the cart page.",
            "Offer limited-time coupons or first-order discounts.",
            "Highlight value-for-money benefits and savings clearly."
        ],

        "trust_concern": [
            "Add more verified customer reviews and ratings.",
            "Display trust badges, secure payment icons, and return policies prominently.",
            "Show customer photos, testimonials, and social proof."
        ],

        "product_fit_concern": [
            "Improve size chart visibility and clarity.",
            "Provide AI-powered size recommendations.",
            "Display customer fit reviews such as 'true to size' feedback."
        ],

        "checkout_friction": [
            "Enable guest checkout without mandatory account creation.",
            "Reduce checkout form fields and steps.",
            "Simplify login and signup experience."
        ],

        "delivery_concern": [
            "Show delivery estimates directly on the product page.",
            "Display shipping charges before checkout.",
            "Add pincode availability checks near the CTA."
        ],

        "comparison_shopping": [
            "Provide product comparison tables.",
            "Highlight unique selling points clearly.",
            "Show feature and value comparisons against alternatives."
        ],

        "product_information_gap": [
            "Add richer product descriptions and FAQs.",
            "Improve product images, videos, and material details.",
            "Provide an AI assistant for product-related questions."
        ],

        "low_purchase_intent": [
            "Improve product discovery and homepage engagement.",
            "Use personalized recommendations based on browsing behavior.",
            "Retarget users with relevant offers and reminders."
        ]
    }

    return {
        "session_id": reason_output.get("session_id"),
        "recommended_actions": recommendations.get(
            primary_reason,
            ["Review the session manually for additional insights."]
        )
    }