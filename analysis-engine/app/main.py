# analysis-engine/app/main.py
"""
FastAPI Performance Analysis, Bottleneck Detection & ML Anomaly Service
Runs on port 8000.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from app.analyzers.bottleneck_scorer import BottleneckScorer
from app.analyzers.health_scorer import HealthScorer
from app.anomaly_detection.isolation_forest import AnomalyDetector
from app.recommendations.engine import RecommendationEngine

app = FastAPI(
    title="IMPOF Analysis & AI Anomaly Engine",
    description="Multi-Layer Performance Scoring, Bottleneck Detection and Machine Learning Service",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
bottleneck_scorer = BottleneckScorer()
health_scorer = HealthScorer()
anomaly_detector = AnomalyDetector()
recommendation_engine = RecommendationEngine()

class MetricsPayload(BaseModel):
    appId: str
    metrics: Dict[str, Any]

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "IMPOF Python FastAPI Analysis Engine",
        "mlModel": "Scikit-Learn IsolationForest (Trained)",
        "version": "2.0.0"
    }

@app.post("/analyze")
def analyze_metrics(payload: MetricsPayload):
    try:
        metrics = payload.metrics
        bottlenecks = bottleneck_scorer.evaluate(metrics)
        health = health_scorer.calculate_score(metrics)
        anomalies = anomaly_detector.detect(metrics)
        recommendations = recommendation_engine.generate_recommendations(metrics, bottlenecks)

        return {
            "appId": payload.appId,
            "health": health,
            "bottlenecks": bottlenecks,
            "anomalies": anomalies,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anomalies")
def detect_anomalies(payload: MetricsPayload):
    try:
        anomalies = anomaly_detector.detect(payload.metrics)
        return {"appId": payload.appId, "anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/health-score")
def compute_health_score(payload: MetricsPayload):
    try:
        health = health_scorer.calculate_score(payload.metrics)
        return {"appId": payload.appId, "healthScore": health}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
