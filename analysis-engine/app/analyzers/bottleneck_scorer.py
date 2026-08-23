# analysis-engine/app/analyzers/bottleneck_scorer.py
"""
Rule-based Transparent Bottleneck Scoring Engine (0-100 Scale)
Computes exact layer contribution scores with evidence and likely root causes.
"""

from typing import Dict, Any, List

class BottleneckScorer:
    def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        backend = metrics.get('backend', {})
        database = metrics.get('database', {})
        cache = metrics.get('cache', {})
        infra = metrics.get('infrastructure', {})
        frontend = metrics.get('frontend', {})

        api_latency = float(backend.get('avgLatencyMs', 120))
        error_rate = float(backend.get('errorRatePercent', 0.5))
        db_latency = float(database.get('avgQueryLatencyMs', 30))
        slow_queries = int(database.get('slowQueriesCount', 0))
        rows_scanned = int(database.get('rowsScanned', 100))
        cache_hit_ratio = float(cache.get('hitRatioPercent', 65.0))
        cpu_percent = float(infra.get('cpuPercent', 35.0))
        mem_mb = float(infra.get('memoryMb', 120.0))
        page_load_ms = float(frontend.get('pageLoadTimeMs', 450))

        # 1. Compute Database Bottleneck Score (0-100)
        # Factor A: Absolute Query Latency (>50ms is warning, >150ms is critical)
        db_factor_lat = min(50.0, (db_latency / 180.0) * 50.0)
        # Factor B: Latency Contribution Ratio (db_latency / api_latency)
        db_ratio = db_latency / max(1.0, api_latency)
        db_factor_ratio = min(30.0, db_ratio * 30.0)
        # Factor C: Slow Queries & Rows Scanned
        db_factor_scan = 20.0 if (slow_queries > 0 or rows_scanned > 1000) else 0.0
        db_score = round(min(100.0, db_factor_lat + db_factor_ratio + db_factor_scan), 1)

        # 2. Compute Backend / Application Bottleneck Score (0-100)
        be_factor_lat = min(50.0, (api_latency / 300.0) * 50.0)
        be_factor_err = min(30.0, (error_rate / 5.0) * 30.0)
        be_factor_p99 = min(20.0, (float(backend.get('p99LatencyMs', api_latency * 2)) / 600.0) * 20.0)
        backend_score = round(min(100.0, be_factor_lat + be_factor_err + be_factor_p99), 1)

        # 3. Compute Infrastructure Bottleneck Score (0-100)
        infra_factor_cpu = min(60.0, (cpu_percent / 90.0) * 60.0) if cpu_percent > 40 else 10.0
        infra_factor_mem = min(40.0, (mem_mb / 512.0) * 40.0) if mem_mb > 200 else 10.0
        infra_score = round(min(100.0, infra_factor_cpu + infra_factor_mem), 1)

        # 4. Compute Cache Bottleneck Score (0-100)
        # Low hit ratio (<50%) indicates cache inefficiency
        if cache_hit_ratio < 40.0:
            cache_score = round(80.0 - (cache_hit_ratio * 0.8), 1)
        elif cache_hit_ratio < 70.0:
            cache_score = round(50.0 - (cache_hit_ratio * 0.3), 1)
        else:
            cache_score = 12.0

        # 5. Compute Frontend Bottleneck Score (0-100)
        fe_score = round(min(100.0, (page_load_ms / 3000.0) * 100.0), 1)

        scores = {
            'Database': db_score,
            'Backend': backend_score,
            'Infrastructure': infra_score,
            'Cache': cache_score,
            'Frontend': fe_score
        }

        # Sort layers by bottleneck score
        sorted_layers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_layer, primary_score = sorted_layers[0]
        secondary_layer, secondary_score = sorted_layers[1]

        severity = "CRITICAL" if primary_score >= 75 else "HIGH" if primary_score >= 50 else "MEDIUM" if primary_score >= 30 else "OPTIMAL"

        # Formulate Explainable Evidence and Causes
        evidence_items = []
        likely_cause = "System is operating within established operational SLO thresholds."

        if primary_layer == 'Database':
            evidence_items.append(f"Database Query Latency = {db_latency:.1f}ms (Accounts for {db_ratio*100:.1f}% of total API Latency)")
            if rows_scanned > 1000:
                evidence_items.append(f"Excessive rows scanned ({rows_scanned:,} rows) without index utilization")
            likely_cause = "Unindexed database query / Full table scan causing high I/O wait times."

        elif primary_layer == 'Backend':
            evidence_items.append(f"API Latency = {api_latency:.1f}ms with Error Rate = {error_rate:.2f}%")
            likely_cause = "Synchronous thread contention / un-cached CPU operations."

        elif primary_layer == 'Infrastructure':
            evidence_items.append(f"Host CPU Utilization = {cpu_percent:.1f}%, Memory = {mem_mb:.1f}MB")
            likely_cause = "Host compute resource saturation. Additional container replicas or CPU scaling recommended."

        elif primary_layer == 'Cache':
            evidence_items.append(f"Cache Hit Ratio = {cache_hit_ratio:.1f}% (Threshold: >70%)")
            likely_cause = "Cache miss storm or insufficient TTL causing excessive downstream database calls."

        elif primary_layer == 'Frontend':
            evidence_items.append(f"Page Load Time = {page_load_ms:.1f}ms")
            likely_cause = "Heavy un-virtualized DOM rendering or large JavaScript asset payload."

        return {
            'primaryBottleneck': primary_layer,
            'primaryScore': primary_score,
            'secondaryBottleneck': secondary_layer,
            'secondaryScore': secondary_score,
            'severity': severity,
            'bottleneckScores': scores,
            'evidence': " • ".join(evidence_items) if evidence_items else "All layers nominal.",
            'likelyCause': likely_cause
        }
