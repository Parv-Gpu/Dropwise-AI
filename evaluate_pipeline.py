import json
import os
from collections import Counter

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
    reason_output = detect_reason(signal_output, behavior_output)

    evidence_output = generate_evidence(
        preprocessing_output,
        behavior_output,
        reason_output
    )

    recommendation_output = generate_recommendation(reason_output)

    ground_truth_reason = session.get("ground_truth", {}).get("primary_reason")
    predicted_reason = reason_output.get("primary_reason")

    return {
        "session_id": session.get("session_id"),
        "user_id": session.get("user_id"),
        "device": session.get("device"),

        "predicted_reason": predicted_reason,
        "secondary_reason": reason_output.get("secondary_reason"),
        "ground_truth_reason": ground_truth_reason,
        "is_correct": predicted_reason == ground_truth_reason,

        "confidence_score": reason_output.get("confidence_score"),
        "confidence_level": reason_output.get("confidence_level"),
        "reason_scores": reason_output.get("reason_scores"),

        "preprocessing": preprocessing_output,
        "behavior_metrics": behavior_output.get("behavior_metrics"),
        "signals": signal_output.get("signals"),
        "evidence": evidence_output.get("evidence"),
        "recommended_actions": recommendation_output.get("recommended_actions")
    }


def calculate_category_accuracy(results):
    category_stats = {}

    for result in results:
        category = result.get("ground_truth_reason")

        if category not in category_stats:
            category_stats[category] = {
                "total": 0,
                "correct": 0
            }

        category_stats[category]["total"] += 1

        if result.get("is_correct"):
            category_stats[category]["correct"] += 1

    category_accuracy = {}

    for category, stats in category_stats.items():
        category_accuracy[category] = {
            "total": stats["total"],
            "correct": stats["correct"],
            "wrong": stats["total"] - stats["correct"],
            "accuracy": round(
                (stats["correct"] / stats["total"]) * 100,
                2
            ) if stats["total"] > 0 else 0
        }

    return category_accuracy


if __name__ == "__main__":
    input_file = "data/synthetic_sessions.jsonl"
    output_results_file = "data/evaluation_results.json"
    output_summary_file = "data/evaluation_summary.json"

    os.makedirs("data", exist_ok=True)

    sessions = load_sessions(input_file)

    results = []
    correct = 0

    for session in sessions:
        result = run_pipeline(session)
        results.append(result)

        if result["is_correct"]:
            correct += 1

    total = len(results)
    wrong_results = [result for result in results if not result["is_correct"]]
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0

    predicted_counter = Counter(result["predicted_reason"] for result in results)
    ground_truth_counter = Counter(result["ground_truth_reason"] for result in results)

    category_accuracy = calculate_category_accuracy(results)

    summary = {
        "total_sessions": total,
        "correct_predictions": correct,
        "wrong_predictions": len(wrong_results),
        "accuracy": accuracy,
        "predicted_reason_distribution": dict(predicted_counter),
        "ground_truth_reason_distribution": dict(ground_truth_counter),
        "category_accuracy": category_accuracy,
        "wrong_prediction_details": wrong_results
    }

    print("\n===== DROPWISE AI PIPELINE EVALUATION =====")
    print(f"Total Sessions: {total}")
    print(f"Correct Predictions: {correct}")
    print(f"Wrong Predictions: {len(wrong_results)}")
    print(f"Accuracy: {accuracy}%")

    print("\n===== CATEGORY-WISE ACCURACY =====")
    for category, stats in category_accuracy.items():
        print(
            f"{category} | "
            f"Correct: {stats['correct']}/{stats['total']} | "
            f"Wrong: {stats['wrong']} | "
            f"Accuracy: {stats['accuracy']}%"
        )

    print("\n===== SESSION-WISE RESULTS =====")
    for index, result in enumerate(results, start=1):
        status = "✅" if result["is_correct"] else "❌"

        print(
            f"{status} Session {index} | "
            f"Predicted: {result['predicted_reason']} | "
            f"Secondary: {result['secondary_reason']} | "
            f"Ground Truth: {result['ground_truth_reason']} | "
            f"Confidence: {result['confidence_score']} "
            f"({result['confidence_level']})"
        )

    print("\n===== WRONG PREDICTIONS =====")
    if not wrong_results:
        print("No wrong predictions. All sessions matched ground truth.")
    else:
        for result in wrong_results:
            print(
                f"Session ID: {result['session_id']} | "
                f"Predicted: {result['predicted_reason']} | "
                f"Ground Truth: {result['ground_truth_reason']}"
            )

    with open(output_results_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    with open(output_summary_file, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"\nSaved detailed results to {output_results_file}")
    print(f"Saved summary to {output_summary_file}")