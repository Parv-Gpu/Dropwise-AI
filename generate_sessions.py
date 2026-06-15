# generate_sessions.py

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os
import time
import uuid
import random

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.8,
    api_key=os.getenv("GROQ_API_KEY")
)

SCENARIOS = [
    {
        "persona": "price_sensitive_shopper",
        "drop_off_reason": "price_concern",
        "stage": "cart",
        "behavior": "checks price multiple times, searches for coupons, adds to cart, sees shipping cost or total price, then exits"
    },
    {
        "persona": "trust_seeker",
        "drop_off_reason": "trust_concern",
        "stage": "product",
        "behavior": "checks reviews, ratings, return policy, about us page, verified purchase information, then exits without buying"
    },
    {
        "persona": "comparison_shopper",
        "drop_off_reason": "comparison_shopping",
        "stage": "product",
        "behavior": "visits multiple product pages, compares specs and prices, opens same product repeatedly, never reaches checkout"
    },
    {
        "persona": "checkout_frustrated",
        "drop_off_reason": "checkout_friction",
        "stage": "checkout",
        "behavior": "adds product to cart, starts checkout, faces login or account creation friction, clicks back, retries, then exits"
    },
    {
        "persona": "low_intent_browser",
        "drop_off_reason": "low_purchase_intent",
        "stage": "home",
        "behavior": "lands on homepage, scrolls briefly, clicks one or two products, spends little time, exits quickly"
    },
    {
        "persona": "size_uncertain_user",
        "drop_off_reason": "product_fit_concern",
        "stage": "product",
        "behavior": "opens size chart multiple times, zooms product images, checks return policy, hesitates, exits without checkout"
    },
    {
        "persona": "delivery_worried_user",
        "drop_off_reason": "delivery_concern",
        "stage": "cart",
        "behavior": "adds to cart, checks delivery date, shipping policy, delivery charges, pincode availability, then exits"
    },
    {
        "persona": "information_seeker",
        "drop_off_reason": "product_information_gap",
        "stage": "product",
        "behavior": "opens product details, zooms images, checks material, description, FAQs, but cannot find enough information and exits"
    }
]

PROMPT_TEMPLATE = """
Generate ONE realistic e-commerce user session as valid JSON.

Scenario:
Persona: {persona}
Drop-off reason: {drop_off_reason}
Exit stage: {stage}
Behavior: {behavior}

Return JSON with this EXACT structure:

{{
  "session_id": "sess_random6chars",
  "user_id": "anon_random4digits",
  "device": "desktop or mobile",
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
- Do not use markdown.
- Do not add explanation.
- Include 15 to 40 events.
- Events must be chronologically ordered.
- Behavior must clearly reflect the drop-off reason.
- Use realistic e-commerce page paths.
- type must be only: "page_view", "click", or "scroll".
- element should be null for page_view and scroll unless needed.
- depth_percent should be null except for scroll events.
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

    # Force unique IDs because LLM often repeats same IDs
    session["session_id"] = f"sess_{uuid.uuid4().hex[:6]}"
    session["user_id"] = f"anon_{random.randint(1000, 9999)}"

    session["ground_truth"] = {
        "primary_reason": scenario["drop_off_reason"],
        "drop_off_stage": scenario["stage"],
        "persona": scenario["persona"]
    }

    return session


def generate_dataset(sessions_per_scenario: int = 5) -> list:
    dataset = []

    for scenario in SCENARIOS:
        print(f"\nGenerating {sessions_per_scenario} sessions for: {scenario['drop_off_reason']}")

        generated_count = 0
        attempts = 0
        max_attempts = sessions_per_scenario * 4

        while generated_count < sessions_per_scenario and attempts < max_attempts:
            attempts += 1

            try:
                session = generate_session(scenario)
                dataset.append(session)
                generated_count += 1
                print(f"  ✓ Generated session {generated_count}")

                time.sleep(0.5)

            except Exception as e:
                print(f"  ✗ Failed attempt {attempts}: {e}")
                time.sleep(1)

        if generated_count < sessions_per_scenario:
            print(f"  ⚠ Only generated {generated_count}/{sessions_per_scenario}")

    return dataset


if __name__ == "__main__":
    sessions_count = 10

    print(f"DEBUG sessions_per_scenario = {sessions_count}")
    print(f"DEBUG expected sessions = {len(SCENARIOS) * sessions_count}")

    dataset = generate_dataset(sessions_per_scenario=sessions_count)

    os.makedirs("data", exist_ok=True)

    with open("data/synthetic_sessions.jsonl", "w", encoding="utf-8") as f:
        for session in dataset:
            f.write(json.dumps(session) + "\n")

    print(f"\n✅ Generated {len(dataset)} sessions")
    print("Saved to data/synthetic_sessions.jsonl")