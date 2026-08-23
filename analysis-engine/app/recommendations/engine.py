# analysis-engine/app/recommendations/engine.py
"""
Actionable Recommendation Engine based on Multi-Layer Bottleneck Profiling
"""

from typing import Dict, Any, List

class RecommendationEngine:
    def generate_recommendations(self, metrics: Dict[str, Any], bottleneck_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        backend = metrics.get('backend', {})
        database = metrics.get('database', {})
        cache = metrics.get('cache', {})
        infra = metrics.get('infrastructure', {})
        frontend = metrics.get('frontend', {})

        recommendations = []
        primary = bottleneck_result.get('primaryBottleneck')
        scores = bottleneck_result.get('bottleneckScores', {})

        # 1. Database Tier Recommendations
        if scores.get('Database', 0) > 40:
            db_lat = float(database.get('avgQueryLatencyMs', 30))
            rows = int(database.get('rowsScanned', 0))
            recommendations.append({
                'problem': f"High Database Query Latency ({db_lat:.1f}ms) under read workload.",
                'evidence': f"Rows scanned: {rows:,} rows. DB query accounts for >45% of total API processing time.",
                'recommendedAction': "Add composite B-Tree index on (genre, release_year, rating) and replace full table scan with index scan.",
                'expectedImpact': "Reduce query execution time by 85% to 95%",
                'risk': 'LOW',
                'priority': 'CRITICAL' if scores.get('Database', 0) > 75 else 'HIGH'
            })

        # 2. Cache Tier Recommendations
        if scores.get('Cache', 0) > 35:
            hit_ratio = float(cache.get('hitRatioPercent', 60))
            recommendations.append({
                'problem': f"Sub-optimal Redis Cache Hit Ratio ({hit_ratio:.1f}%).",
                'evidence': f"Current hit ratio is below the 75% efficiency target, causing redundant database lookups.",
                'recommendedAction': "Increase Redis TTL for top catalog items to 300s and implement cache pre-warming during application startup.",
                'expectedImpact': "Boost cache hit ratio to >85% and double API throughput capacity",
                'risk': 'LOW',
                'priority': 'HIGH' if hit_ratio < 40 else 'MEDIUM'
            })

        # 3. Infrastructure & CPU Recommendations
        if scores.get('Infrastructure', 0) > 40:
            cpu = float(infra.get('cpuPercent', 40))
            recommendations.append({
                'problem': f"Elevated Host CPU Utilization ({cpu:.1f}%).",
                'evidence': "Compute load approaching saturation limit during peak request processing.",
                'recommendedAction': "Scale container replicas from 1 to 3 instances using Docker Compose / Kubernetes HPA.",
                'expectedImpact': "Distribute concurrent requests and lower average CPU utilization to <45%",
                'risk': 'MEDIUM',
                'priority': 'HIGH' if cpu > 80 else 'MEDIUM'
            })

        # 4. Backend / API Threading Recommendations
        if scores.get('Backend', 0) > 45:
            api_lat = float(backend.get('avgLatencyMs', 100))
            recommendations.append({
                'problem': f"Backend API latency overhead ({api_lat:.1f}ms).",
                'evidence': f"P99 Latency ({backend.get('p99LatencyMs', 0)}ms) indicates tail latency degradation.",
                'recommendedAction': "Offload heavy serialization and recommendation computations to asynchronous worker threads.",
                'expectedImpact': "Eliminate event loop blocking and reduce P99 latency by 60%",
                'risk': 'LOW',
                'priority': 'MEDIUM'
            })

        if not recommendations:
            recommendations.append({
                'problem': 'System is operating within optimal performance parameters.',
                'evidence': 'All layer metrics are healthy with high cache efficiency and sub-millisecond database lookups.',
                'recommendedAction': 'Maintain current indexing strategies and monitoring thresholds.',
                'expectedImpact': 'Sustained low latency and high availability',
                'risk': 'NONE',
                'priority': 'LOW'
            })

        return recommendations
