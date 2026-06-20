from langchain_groq import ChatGroq
from dotenv import load_dotenv
from schemas.session_schema import SessionData

import json
import os
import time
import uuid
import random


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
)


SCENARIOS = [
    {
        "persona": "price_sensitive_shopper",
        "drop_off_reason": "price_concern",
        "stage": "cart",
        "behavior": "checks price, coupon, discount, cart summary, total cost, then exits",
        "required_events": ["price", "coupon", "discount", "summary", "total"]
    },
    {
        "persona": "trust_seeker",
        "drop_off_reason": "trust_concern",
        "stage": "product",
        "behavior": "checks reviews, ratings, verified purchases, return policy, then exits",
        "required_events": ["review", "rating", "verified", "return"]
    },
    {
        "persona": "comparison_shopper",
        "drop_off_reason": "comparison_shopping",
        "stage": "product",
        "behavior": "visits multiple product pages, compares specs, prices, features, then exits",
        "required_events": ["compare", "specs", "product-1", "product-2", "product-3"]
    },
    {
        "persona": "checkout_frustrated",
        "drop_off_reason": "checkout_friction",
        "stage": "checkout",
        "behavior": "adds to cart, goes to checkout, faces login/account creation, retries, exits",
        "required_events": ["add_to_cart", "checkout", "login", "account", "create_account"]
    },
    {
        "persona": "low_intent_browser",
        "drop_off_reason": "low_purchase_intent",
        "stage": "home",
        "behavior": "briefly browses homepage and one product, no cart, no checkout, exits quickly",
        "required_events": ["homepage", "browse", "exit"]
    },
    {
        "persona": "size_uncertain_user",
        "drop_off_reason": "product_fit_concern",
        "stage": "product",
        "behavior": "opens size chart, checks fit, zooms product images, checks return policy, exits",
        "required_events": ["size_chart", "fit", "zoom", "image", "return"]
    },
    {
        "persona": "delivery_worried_user",
        "drop_off_reason": "delivery_concern",
        "stage": "cart",
        "behavior": "checks delivery date, shipping charges, pincode availability, delivery policy, then exits",
        "required_events": ["delivery", "shipping", "pincode", "charges"]
    },
    {
        "persona": "information_seeker",
        "drop_off_reason": "product_information_gap",
        "stage": "product",
        "behavior": "opens product details, description, material, FAQ, images, but exits due to missing info",
        "required_events": ["details", "description", "material", "faq", "information"]
    }
]


PROMPT_TEMPLATE = """
Generate ONE realistic ecommerce session as VALID JSON only.

Scenario:
Persona: {persona}
Drop-off reason: {drop_off_reason}
Exit stage: {stage}
Behavior: {behavior}

The session should contain these keywords in page paths or element names:
{required_events}

Return JSON with this exact structure:

{{
  "session_id": "sess_random6chars",
  "user_id": "anon_random4digits",
  "device": "desktop",
  "start_time": 1718000000,
  "events": [
    {{
      "type": "page_view",
      "timestamp": 1718000000,
      "page": "/",
      "element": null,
      "depth_percent": null
    }}
  ],
  "pages_visited": ["/", "/products/sample-product", "EXIT"]
}}

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- Include 15 to 30 events.
- Timestamps must increase.
- type must be one of: page_view, click, scroll, search, input, exit, zoom.
- depth_percent must be a number only for scroll events, otherwise null.
"""


def clean_llm_response(response: str) -> str:
    clean = response.strip()

    if clean.startswith("```json"):
        clean = clean.replace("```json", "").replace("```", "").strip()
    elif clean.startswith("```"):
        clean = clean.replace("```", "").strip()

    return clean


def get_last_timestamp(session: dict) -> int:
    events = session.get("events", [])

    timestamps = [
        event.get("timestamp", 1718000000)
        for event in events
        if isinstance(event.get("timestamp", 1718000000), int)
    ]

    return max(timestamps) if timestamps else 1718000000


def force_required_events(session: dict, scenario: dict) -> dict:
    reason = scenario["drop_off_reason"]
    events = session.get("events", [])
    timestamp = get_last_timestamp(session)

    forced_events = []

    def add_event(event_type, page, element=None, depth_percent=None):
        nonlocal timestamp
        timestamp += random.randint(5, 15)

        forced_events.append({
            "type": event_type,
            "timestamp": timestamp,
            "page": page,
            "element": element,
            "depth_percent": depth_percent
        })

    if reason == "price_concern":
        add_event("click", "/products/sample-product", "price")
        add_event("click", "/cart/summary", "cart_total")
        add_event("search", "/cart/coupon", "coupon")
        add_event("click", "/cart/discount", "discount_offer")
        add_event("click", "/cart/summary", "total_cost")
        add_event("exit", "/cart/summary", "exit")

    elif reason == "trust_concern":
        add_event("click", "/products/sample-product/reviews", "review")
        add_event("click", "/products/sample-product/ratings", "rating")
        add_event("click", "/products/sample-product/verified-reviews", "verified")
        add_event("click", "/policies/return-policy", "return_policy")
        add_event("exit", "/products/sample-product", "exit")

    elif reason == "comparison_shopping":
        add_event("page_view", "/products/product-1", None)
        add_event("page_view", "/products/product-2", None)
        add_event("page_view", "/products/product-3", None)
        add_event("click", "/products/product-1/specs", "specs")
        add_event("click", "/products/compare", "compare")
        add_event("exit", "/products/compare", "exit")

    elif reason == "checkout_friction":
        add_event("click", "/products/sample-product", "add_to_cart")
        add_event("page_view", "/checkout", None)
        add_event("click", "/checkout/login", "login")
        add_event("click", "/checkout/account", "create_account")
        add_event("exit", "/checkout/account", "exit")

    elif reason == "low_purchase_intent":
        add_event("page_view", "/", None)
        add_event("scroll", "/", None, 30)
        add_event("page_view", "/products/sample-product", None)
        add_event("exit", "/products/sample-product", "exit")

    elif reason == "product_fit_concern":
        add_event("click", "/products/sample-product/size-chart", "size_chart")
        add_event("click", "/products/sample-product/fit-guide", "fit")
        add_event("zoom", "/products/sample-product/gallery", "zoom_image")
        add_event("zoom", "/products/sample-product/gallery", "product_image")
        add_event("click", "/policies/return-policy", "return_policy")
        add_event("exit", "/products/sample-product", "exit")

    elif reason == "delivery_concern":
        add_event("click", "/products/sample-product", "delivery")
        add_event("click", "/cart/shipping", "shipping")
        add_event("input", "/cart/pincode-check", "pincode")
        add_event("click", "/cart/delivery-charges", "charges")
        add_event("exit", "/cart/shipping", "exit")

    elif reason == "product_information_gap":
        add_event("click", "/products/sample-product/details", "details")
        add_event("click", "/products/sample-product/description", "description")
        add_event("click", "/products/sample-product/material", "material")
        add_event("click", "/products/sample-product/faq", "faq")
        add_event("click", "/products/sample-product/information", "information")
        add_event("exit", "/products/sample-product", "exit")

    session["events"] = events + forced_events

    pages = [
        event["page"]
        for event in session["events"]
        if event.get("page")
    ]

    session["pages_visited"] = pages + ["EXIT"]

    return session


def generate_session(scenario: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(**scenario)

    response = llm.invoke(prompt).content
    clean_response = clean_llm_response(response)

    session = json.loads(clean_response)

    session["session_id"] = f"sess_{uuid.uuid4().hex[:6]}"
    session["user_id"] = f"anon_{random.randint(1000, 9999)}"

    session = force_required_events(session, scenario)

    session["ground_truth"] = {
        "primary_reason": scenario["drop_off_reason"],
        "drop_off_stage": scenario["stage"],
        "persona": scenario["persona"]
    }

    validated = SessionData.model_validate(session)
    return validated.model_dump()


def generate_dataset(sessions_per_scenario: int = 10) -> list:
    dataset = []

    for scenario in SCENARIOS:
        print(f"\nGenerating {sessions_per_scenario} sessions for: {scenario['drop_off_reason']}")

        generated_count = 0
        attempts = 0
        max_attempts = sessions_per_scenario * 6

        while generated_count < sessions_per_scenario and attempts < max_attempts:
            attempts += 1

            try:
                session = generate_session(scenario)
                dataset.append(session)
                generated_count += 1
                print(f"  ✓ Generated session {generated_count}")
                time.sleep(1)

            except Exception as e:
                print(f"  ✗ Failed attempt {attempts}: {e}")

                if "429" in str(e) or "rate limit" in str(e).lower():
                    print("  Waiting 10 seconds due to rate limit...")
                    time.sleep(10)
                else:
                    time.sleep(2)

        if generated_count < sessions_per_scenario:
            print(f"  ⚠ Only generated {generated_count}/{sessions_per_scenario}")

    return dataset


if __name__ == "__main__":
    sessions_count = 10
    output_file = "data/synthetic_sessions.jsonl"

    os.makedirs("data", exist_ok=True)

    print(f"DEBUG sessions_per_scenario = {sessions_count}")
    print(f"DEBUG expected sessions = {len(SCENARIOS) * sessions_count}")

    dataset = generate_dataset(sessions_per_scenario=sessions_count)

    with open(output_file, "w", encoding="utf-8") as file:
        for session in dataset:
            file.write(json.dumps(session) + "\n")

    print(f"\n✅ Generated {len(dataset)} sessions")
    print(f"Saved to {output_file}")