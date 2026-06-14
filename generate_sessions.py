# generate_sessions.py

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
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
    }},
    {{
      "type": "click",
      "timestamp": 1718000010,
      "page": "/products/sample-product",
      "element": "product_image",
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

    session["ground_truth"] = {
        "primary_reason": scenario["drop_off_reason"],
        "drop_off_stage": scenario["stage"],
        "persona": scenario["persona"]
    }

    return session


def generate_dataset(sessions_per_scenario: int = 2) -> list:
    dataset = []

    for scenario in SCENARIOS:
        print(f"\nGenerating {sessions_per_scenario} sessions for: {scenario['drop_off_reason']}")

        for i in range(sessions_per_scenario):
            try:
                session = generate_session(scenario)
                dataset.append(session)
                print(f"  ✓ Generated session {i + 1}")
            except Exception as e:
                print(f"  ✗ Failed session {i + 1}: {e}")

    return dataset


if __name__ == "__main__":
    dataset = generate_dataset(sessions_per_scenario=2)

    os.makedirs("data", exist_ok=True)

    with open("data/synthetic_sessions.jsonl", "w", encoding="utf-8") as f:
        for session in dataset:
            f.write(json.dumps(session) + "\n")

    print(f"\n✅ Generated {len(dataset)} sessions")
    print("Saved to data/synthetic_sessions.jsonl")