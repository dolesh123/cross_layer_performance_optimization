// frontend/src/components/AnomaliesView.jsx
import React from 'react';
import { Sparkles, AlertTriangle, ShieldCheck, Activity, Clock, BarChart2 } from 'lucide-react';

export default function AnomaliesView({ anomalies }) {
  return (
    <div>
      {/* ML Model Status Callout */}
      <div className="glass-card" style={{
        padding: '24px',
        marginBottom: '24px',
        border: '1px solid var(--border-glow)',
        background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 20px rgba(6, 182, 212, 0.4)'
            }}>
              <Sparkles size={22} color="#ffffff" />
            </div>
            <div>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>Machine Learning Anomaly Detection</h2>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Powered by <strong>Scikit-Learn Isolation Forest</strong> analyzing multivariate feature vectors: [CPU, Memory, API Latency, DB Latency, Error Rate, Cache Hit Ratio].
              </p>
            </div>
          </div>

          <span className="badge badge-cyan" style={{ padding: '6px 14px', fontSize: '0.8rem' }}>
            ML Model: Active & Fitted
          </span>
        </div>
      </div>

      {/* Anomalies Table / List */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
            Detected Multivariate Anomalies ({anomalies.length})
          </h3>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Evaluated on Python FastAPI Microservice (:8000)
          </span>
        </div>

        {anomalies.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
            <ShieldCheck size={40} style={{ margin: '0 auto 12px auto', color: '#34d399', opacity: 0.8 }} />
            <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>No Active Statistical Anomalies Detected</div>
            <p style={{ fontSize: '0.82rem', marginTop: '4px' }}>
              The multi-layer metric vectors currently reside within the Isolation Forest 95% confidence baseline envelope.
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {anomalies.map((anom, idx) => (
              <div
                key={idx}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '12px',
                  padding: '16px 20px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '16px'
                }}
              >
                <div style={{ flex: '1 1 320px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                    <span className="badge badge-rose">{anom.severity || 'HIGH'}</span>
                    <span className="font-mono" style={{ fontSize: '0.9rem', fontWeight: 700, color: '#ffffff' }}>
                      {anom.metric}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      • {new Date(anom.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                    {anom.description}
                  </p>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '20px', fontSize: '0.82rem' }}>
                  <div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>OBSERVED VALUE</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fb7185' }} className="font-mono">
                      {anom.observedValue}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>EXPECTED BASELINE</div>
                    <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)' }} className="font-mono">
                      {anom.expectedRange}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>ANOMALY SCORE</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-cyan)' }} className="font-mono">
                      {anom.anomalyScore}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
