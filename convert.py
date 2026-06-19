import json

with open("data/synthetic_sessions.jsonl", "r", encoding="utf-8") as f:
    first_session = json.loads(f.readline())

with open("data/sample_session.json", "w", encoding="utf-8") as f:
    json.dump(first_session, f, indent=2)

print("Created data/sample_session.json")