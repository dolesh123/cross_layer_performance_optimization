# analysis-engine/app/analyzers/health_scorer.py
"""
Explainable Application Health Score Engine (0-100 Scale)
Computes weighted composite health scores across all 5 operational pillars.
"""

from typing import Dict, Any

class HealthScorer:
    def calculate_score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        backend = metrics.get('backend', {})
        database = metrics.get('database', {})
        cache = metrics.get('cache', {})
        infra = metrics.get('infrastructure', {})

        api_latency = float(backend.get('avgLatencyMs', 100))
        error_rate = float(backend.get('errorRatePercent', 0.1))
        db_latency = float(database.get('avgQueryLatencyMs', 25))
        cache_hit_ratio = float(cache.get('hitRatioPercent', 75.0))
        cpu_percent = float(infra.get('cpuPercent', 30.0))

        # 1. Latency Score (Weight: 30%)
        # Latency < 100ms -> 100 pts, Latency > 500ms -> 0 pts
        lat_score = max(0.0, min(100.0, 100.0 - ((api_latency - 50.0) / 450.0) * 100.0)) if api_latency > 50 else 100.0

        # 2. Availability & Error Rate Score (Weight: 20%)
        # Error Rate 0% -> 100 pts, Error Rate > 5% -> 0 pts
        err_score = max(0.0, min(100.0, 100.0 - (error_rate / 5.0) * 100.0))

        # 3. Database Health Score (Weight: 20%)
        # DB Latency < 20ms -> 100 pts, DB Latency > 150ms -> 0 pts
        db_score = max(0.0, min(100.0, 100.0 - ((db_latency - 10.0) / 140.0) * 100.0)) if db_latency > 10 else 100.0

        # 4. Cache Efficiency Score (Weight: 15%)
        # Hit ratio > 80% -> 100 pts, < 20% -> 20 pts
        cache_score = max(20.0, min(100.0, cache_hit_ratio * 1.25))

        # 5. Infrastructure Headroom Score (Weight: 15%)
        # CPU < 50% -> 100 pts, CPU > 90% -> 20 pts
        infra_score = max(20.0, min(100.0, 100.0 - max(0.0, cpu_percent - 50.0) * 2.0))

        # Weighted Total
        overall_health = (
            (lat_score * 0.30) +
            (err_score * 0.20) +
            (db_score * 0.20) +
            (cache_score * 0.15) +
            (infra_score * 0.15)
        )

        overall_health = round(overall_health, 1)

        status = "HEALTHY" if overall_health >= 80 else "DEGRADED" if overall_health >= 55 else "CRITICAL"

        return {
            'overallHealthScore': overall_health,
            'status': status,
            'breakdown': {
                'latencyHealth': round(lat_score, 1),
                'availabilityHealth': round(err_score, 1),
                'databaseHealth': round(db_score, 1),
                'cacheHealth': round(cache_score, 1),
                'infrastructureHealth': round(infra_score, 1)
            }
        }
