import json

from agents.preprocessing_agent import preprocess_session
from agents.behavior_extraction_agent import extract_behavior
from agents.universal_agent import generate_signals
from agents.reason_detection_agent import detect_reason
from agents.evidence_agent import generate_evidence
from agents.recommendation_agent import generate_recommendation


def load_sessions(file_path: str):
    sessions = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                sessions.append(json.loads(line))

    return sessions


if __name__ == "__main__":
    sessions = load_sessions("data/synthetic_sessions.jsonl")

    first_session = sessions[0]

    preprocessing_output = preprocess_session(first_session)
    behavior_output = extract_behavior(first_session)
    signal_output = generate_signals(preprocessing_output, behavior_output)
    reason_output = detect_reason(signal_output, behavior_output)
    evidence_output = generate_evidence(
        preprocessing_output,
        behavior_output,
        reason_output
    )
    recommendation_output = generate_recommendation(reason_output)

    print("\n===== FINAL DROPWISE AI OUTPUT =====")
    final_output = {
        "session_id": first_session.get("session_id"),
        "predicted_reason": reason_output.get("primary_reason"),
        "secondary_reason": reason_output.get("secondary_reason"),
        "confidence_score": reason_output.get("confidence_score"),
        "signals": signal_output.get("signals"),
        "evidence": evidence_output.get("evidence"),
        "recommended_actions": recommendation_output.get("recommended_actions"),
        "ground_truth": first_session.get("ground_truth")
    }

    print(json.dumps(final_output, indent=2))