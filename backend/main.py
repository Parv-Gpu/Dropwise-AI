from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
import json

from evaluate_pipeline import run_pipeline


app = FastAPI(
    title="DropWise AI API",
    description="AI-powered customer drop-off analysis system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format_response(result: dict):
    return {
        "session_id": result.get("session_id"),
        "user_id": result.get("user_id"),
        "device": result.get("device"),
        "predicted_reason": result.get("predicted_reason"),
        "secondary_reason": result.get("secondary_reason"),
        "ground_truth_reason": result.get("ground_truth_reason"),
        "is_correct": result.get("is_correct"),
        "confidence_score": result.get("confidence_score"),
        "confidence_level": result.get("confidence_level"),
        "evidence": result.get("evidence"),
        "recommended_actions": result.get("recommended_actions"),
        "signals": result.get("signals"),
        "behavior_metrics": result.get("behavior_metrics")
    }


@app.get("/")
def home():
    return {
        "message": "DropWise AI Backend is running",
        "status": "active",
        "docs": "/docs"
    }


@app.post("/analyze-session")
def analyze_session(session: dict):
    try:
        result = run_pipeline(session)
        return format_response(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-session")
async def upload_session(file: UploadFile = File(...)):
    try:
        content = await file.read()
        session = json.loads(content.decode("utf-8"))

        result = run_pipeline(session)
        return format_response(result)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8")

        sessions = []

        for line in text.splitlines():
            if line.strip():
                sessions.append(json.loads(line))

        results = []
        correct = 0

        for session in sessions:
            result = run_pipeline(session)
            results.append(result)

            if result.get("is_correct"):
                correct += 1

        total = len(results)
        wrong_predictions = total - correct

        accuracy = round((correct / total) * 100, 2) if total > 0 else 0

        reason_distribution = Counter(
            result.get("predicted_reason") for result in results
        )

        confidence_distribution = Counter(
            result.get("confidence_level") for result in results
        )

        device_distribution = Counter(
            result.get("device") for result in results
        )

        secondary_reason_distribution = Counter(
            result.get("secondary_reason")
            for result in results
            if result.get("secondary_reason")
        )

        category_accuracy = {}

        ground_truth_reasons = set(
            result.get("ground_truth_reason") for result in results
        )

        for reason in ground_truth_reasons:
            reason_sessions = [
                result for result in results
                if result.get("ground_truth_reason") == reason
            ]

            if reason_sessions:
                correct_reason = sum(
                    1 for result in reason_sessions
                    if result.get("is_correct")
                )

                category_accuracy[reason] = round(
                    (correct_reason / len(reason_sessions)) * 100,
                    2
                )

        avg_confidence_by_reason = {}

        for reason in reason_distribution.keys():
            reason_sessions = [
                result for result in results
                if result.get("predicted_reason") == reason
            ]

            if reason_sessions:
                avg_confidence_by_reason[reason] = round(
                    sum(
                        result.get("confidence_score", 0)
                        for result in reason_sessions
                    ) / len(reason_sessions),
                    2
                )

        review_count_by_reason = {}

        for reason in reason_distribution.keys():
            review_count_by_reason[reason] = sum(
                1
                for result in results
                if result.get("predicted_reason") == reason
                and not result.get("is_correct")
            )

        avg_confidence = round(
            sum(result.get("confidence_score", 0) for result in results) / total,
            2
        ) if total > 0 else 0

        return {
            "total_sessions": total,
            "correct_predictions": correct,
            "wrong_predictions": wrong_predictions,
            "accuracy": accuracy,
            "avg_confidence": avg_confidence,
            "unique_reasons": len(reason_distribution),

            "reason_distribution": dict(reason_distribution),
            "confidence_distribution": dict(confidence_distribution),
            "device_distribution": dict(device_distribution),
            "secondary_reason_distribution": dict(secondary_reason_distribution),

            "category_accuracy": category_accuracy,
            "avg_confidence_by_reason": avg_confidence_by_reason,
            "review_count_by_reason": review_count_by_reason,

            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))