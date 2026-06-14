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


def run_pipeline(session):
    preprocessing_output = preprocess_session(session)
    behavior_output = extract_behavior(session)
    signal_output = generate_signals(preprocessing_output, behavior_output)
    reason_output = detect_reason(signal_output)
    evidence_output = generate_evidence(
        preprocessing_output,
        behavior_output,
        reason_output
    )
    recommendation_output = generate_recommendation(reason_output)

    return {
        "session_id": session.get("session_id"),
        "predicted_reason": reason_output.get("primary_reason"),
        "ground_truth_reason": session.get("ground_truth", {}).get("primary_reason"),
        "is_correct": reason_output.get("primary_reason") == session.get("ground_truth", {}).get("primary_reason"),
        "confidence_score": reason_output.get("confidence_score"),
        "signals": signal_output.get("signals"),
        "evidence": evidence_output.get("evidence"),
        "recommended_actions": recommendation_output.get("recommended_actions")
    }


if __name__ == "__main__":
    sessions = load_sessions("data/synthetic_sessions.jsonl")

    results = []
    correct = 0

    for session in sessions:
        result = run_pipeline(session)
        results.append(result)

        if result["is_correct"]:
            correct += 1

    total = len(results)
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0

    print("\n===== DROPWISE AI PIPELINE EVALUATION =====")
    print(f"Total Sessions: {total}")
    print(f"Correct Predictions: {correct}")
    print(f"Accuracy: {accuracy}%")

    print("\n===== SESSION-WISE RESULTS =====")
    for i, result in enumerate(results, start=1):
        status = "✅" if result["is_correct"] else "❌"

        print(
            f"{status} Session {i} | "
            f"Predicted: {result['predicted_reason']} | "
            f"Ground Truth: {result['ground_truth_reason']} | "
            f"Confidence: {result['confidence_score']}"
        )

    print("\n===== WRONG PREDICTIONS =====")
    wrong_results = [r for r in results if not r["is_correct"]]

    if not wrong_results:
        print("No wrong predictions. All sessions matched ground truth.")
    else:
        for result in wrong_results:
            print(json.dumps(result, indent=2))

    with open("data/evaluation_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print("\nSaved detailed results to data/evaluation_results.json")