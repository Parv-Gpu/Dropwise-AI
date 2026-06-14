from typing import Dict, Any


def generate_recommendation(reason_output: Dict[str, Any]) -> Dict[str, Any]:
    primary_reason = reason_output.get("primary_reason")

    recommendations = {
        "price_concern": [
            "Show shipping charges earlier before the cart page.",
            "Offer limited-time coupons or first-order discounts.",
            "Highlight savings, offers, and value-for-money benefits clearly."
        ],

        "trust_concern": [
            "Add more verified customer reviews and ratings.",
            "Show trust badges, secure payment icons, and return policy clearly.",
            "Add customer photos or testimonials on product pages."
        ],

        "product_fit_concern": [
            "Improve size chart visibility and clarity.",
            "Add AI-based size recommendation or fit guide.",
            "Show customer fit reviews such as 'true to size' feedback."
        ],

        "checkout_friction": [
            "Allow guest checkout without forced account creation.",
            "Reduce checkout steps and form fields.",
            "Show login/signup as optional instead of mandatory."
        ],

        "delivery_concern": [
            "Show estimated delivery date on the product page itself.",
            "Display delivery charges before cart.",
            "Add pincode availability check near the product CTA."
        ],

        "comparison_shopping": [
            "Add product comparison table.",
            "Highlight unique selling points clearly.",
            "Show competitor-price/value comparison if possible."
        ],

        "low_purchase_intent": [
            "Use personalized product recommendations.",
            "Improve homepage hero section and product discovery.",
            "Retarget user later with relevant offers."
        ],

        "product_information_gap": [
            "Add richer product descriptions and FAQs.",
            "Improve product images, videos, and material details.",
            "Add 'Ask AI about this product' assistant."
        ]
    }

    return {
        "session_id": reason_output.get("session_id"),
        "recommended_actions": recommendations.get(
            primary_reason,
            ["Review the session manually for unclear user behavior."]
        )
    }