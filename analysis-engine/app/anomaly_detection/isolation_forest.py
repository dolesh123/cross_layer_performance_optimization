# analysis-engine/app/anomaly_detection/isolation_forest.py
"""
Multivariate Statistical Anomaly Detector using Scikit-Learn Isolation Forest
Identifies abnormal operational behavior across multi-layer performance vectors.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List
from datetime import datetime

class AnomalyDetector:
    def __init__(self):
        # Feature names: [cpu, mem, api_latency, db_latency, error_rate, cache_hit_ratio]
        self.feature_names = ['cpuPercent', 'memoryMb', 'avgLatencyMs', 'avgQueryLatencyMs', 'errorRatePercent', 'hitRatioPercent']
        
        # Expected baseline ranges (mean, std)
        self.baselines = {
            'cpuPercent': (35.0, 10.0, '20% - 50%'),
            'memoryMb': (128.0, 30.0, '80MB - 180MB'),
            'avgLatencyMs': (80.0, 25.0, '50ms - 130ms'),
            'avgQueryLatencyMs': (20.0, 8.0, '10ms - 35ms'),
            'errorRatePercent': (0.2, 0.1, '0% - 0.5%'),
            'hitRatioPercent': (75.0, 10.0, '60% - 90%')
        }

        # Train Isolation Forest on synthetic nominal baseline distribution (1000 samples)
        np.random.seed(42)
        X_train = np.column_stack([
            np.random.normal(35.0, 8.0, 1000),    # cpu
            np.random.normal(128.0, 20.0, 1000),  # mem
            np.random.normal(80.0, 20.0, 1000),   # api_latency
            np.random.normal(20.0, 6.0, 1000),    # db_latency
            np.random.normal(0.2, 0.1, 1000),     # error_rate
            np.random.normal(75.0, 8.0, 1000)     # cache_hit
        ])

        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.model.fit(X_train)

    def extract_features(self, metrics: Dict[str, Any]) -> np.ndarray:
        backend = metrics.get('backend', {})
        database = metrics.get('database', {})
        cache = metrics.get('cache', {})
        infra = metrics.get('infrastructure', {})

        return np.array([[
            float(infra.get('cpuPercent', 35.0)),
            float(infra.get('memoryMb', 128.0)),
            float(backend.get('avgLatencyMs', 80.0)),
            float(database.get('avgQueryLatencyMs', 20.0)),
            float(backend.get('errorRatePercent', 0.2)),
            float(cache.get('hitRatioPercent', 75.0))
        ]])

    def detect(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        X = self.extract_features(metrics)
        prediction = self.model.predict(X)[0] # -1 for anomaly, 1 for normal
        decision_score = self.model.decision_function(X)[0]

        anomalies = []
        if prediction == -1 or decision_score < -0.05:
            # Determine which feature deviated most from baseline
            values = X[0]
            max_dev_feature = None
            max_z_score = 0.0

            for i, name in enumerate(self.feature_names):
                mean, std, expected_range = self.baselines[name]
                val = values[i]
                z_score = abs(val - mean) / max(0.01, std)

                if z_score > max_z_score:
                    max_z_score = z_score
                    max_dev_feature = (name, val, expected_range)

            if max_dev_feature and max_z_score > 2.0:
                feat_name, obs_val, exp_range = max_dev_feature
                anomalies.append({
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'metric': feat_name,
                    'observedValue': f"{obs_val:.1f}" if isinstance(obs_val, float) else str(obs_val),
                    'expectedRange': exp_range,
                    'anomalyScore': round(min(1.0, abs(decision_score) * 4.0), 3),
                    'zScore': round(max_z_score, 2),
                    'severity': 'HIGH' if max_z_score > 3.5 else 'MEDIUM',
                    'description': f"Statistical outlier detected by Isolation Forest. Observed {feat_name}={obs_val:.1f} deviates significantly from baseline."
                })

        return anomalies
