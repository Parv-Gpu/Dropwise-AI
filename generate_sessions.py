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
    temperature=0.6,
    api_key=os.getenv("GROQ_API_KEY")
)


SCENARIOS = [
    {
        "persona": "price_sensitive_shopper",
        "drop_off_reason": "price_concern",
        "stage": "cart",
        "behavior": "checks price, coupon, discount, cart summary, total cost, then exits",
        "required_events": [
            "price",
            "coupon",
            "discount",
            "cart",
            "summary",
            "total"
        ]
    },
    {
        "persona": "trust_seeker",
        "drop_off_reason": "trust_concern",
        "stage": "product",
        "behavior": "checks reviews, ratings, verified purchases, about us, return policy, then exits",
        "required_events": [
            "review",
            "rating",
            "verified",
            "about",
            "return"
        ]
    },
    {
        "persona": "comparison_shopper",
        "drop_off_reason": "comparison_shopping",
        "stage": "product",
        "behavior": "visits multiple product pages, compares specs, prices, features, then exits",
        "required_events": [
            "compare",
            "specs",
            "product-1",
            "product-2",
            "product-3"
        ]
    },
    {
        "persona": "checkout_frustrated",
        "drop_off_reason": "checkout_friction",
        "stage": "checkout",
        "behavior": "adds to cart, goes to checkout, faces login/account creation, retries, exits",
        "required_events": [
            "add_to_cart",
            "checkout",
            "login",
            "account",
            "create_account"
        ]
    },
    {
        "persona": "low_intent_browser",
        "drop_off_reason": "low_purchase_intent",
        "stage": "home",
        "behavior": "briefly browses homepage and one product, no cart, no checkout, exits quickly",
        "required_events": [
            "homepage",
            "browse",
            "exit"
        ]
    },
    {
        "persona": "size_uncertain_user",
        "drop_off_reason": "product_fit_concern",
        "stage": "product",
        "behavior": "opens size chart, checks fit, zooms product images, checks return policy, exits",
        "required_events": [
            "size_chart",
            "fit",
            "zoom",
            "image",
            "return"
        ]
    },
    {
        "persona": "delivery_worried_user",
        "drop_off_reason": "delivery_concern",
        "stage": "cart",
        "behavior": "checks delivery date, shipping charges, pincode availability, delivery policy, then exits",
        "required_events": [
            "delivery",
            "shipping",
            "pincode",
            "charges",
            "date"
        ]
    },
    {
        "persona": "information_seeker",
        "drop_off_reason": "product_information_gap",
        "stage": "product",
        "behavior": "opens product details, description, material, FAQ, images, but exits due to missing info",
        "required_events": [
            "details",
            "description",
            "material",
            "faq",
            "information"
        ]
    }
]


PROMPT_TEMPLATE = """
Generate ONE realistic ecommerce session as VALID JSON only.

Scenario:
Persona: {persona}
Drop-off reason: {drop_off_reason}
Exit stage: {stage}
Behavior: {behavior}

IMPORTANT:
The session MUST clearly contain these required keywords in page paths or element names:
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
    }},
    {{
      "type": "click",
      "timestamp": 1718000010,
      "page": "/products/sample-product",
      "element": "price",
      "depth_percent": null
    }},
    {{
      "type": "scroll",
      "timestamp": 1718000020,
      "page": "/products/sample-product",
      "element": null,
      "depth_percent": 70
    }}
  ],
  "pages_visited": ["/", "/products/sample-product", "EXIT"]
}}

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- Include 15 to 35 events.
- Timestamps must increase by 5-20 seconds each event.
- type must be one of: page_view, click, scroll, search, input, exit, zoom.
- depth_percent must be a number only for scroll events, otherwise null.
- page and element names must contain the required keywords.
"""


def clean_llm_response(response: str) -> str:
    clean = response.strip()

    if clean.startswith("```json"):
        clean = clean.replace("```json", "").replace("```", "").strip()
    elif clean.startswith("```"):
        clean = clean.replace("```", "").strip()

    return clean


def generate_session(scenario: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(**scenario)

    response = llm.invoke(prompt).content
    clean_response = clean_llm_response(response)

    session = json.loads(clean_response)

    session["session_id"] = f"sess_{uuid.uuid4().hex[:6]}"
    session["user_id"] = f"anon_{random.randint(1000, 9999)}"

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