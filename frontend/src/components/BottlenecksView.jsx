// frontend/src/components/BottlenecksView.jsx
import React from 'react';
import { AlertOctagon, Lightbulb, ShieldAlert, ArrowRight, CheckCircle2, TrendingDown } from 'lucide-react';

export default function BottlenecksView({ bottlenecks, recommendations }) {
  const primary = bottlenecks?.primaryBottleneck || 'Database';
  const scores = bottlenecks?.bottleneckScores || { Database: 88, Backend: 45, Infrastructure: 35, Cache: 60, Frontend: 25 };
  const evidence = bottlenecks?.evidence || 'Database latency accounts for >70% of total API response time.';
  const likelyCause = bottlenecks?.likelyCause || 'Missing composite B-Tree indexes on frequently filtered columns.';

  const getLayerColor = (layer) => {
    switch (layer) {
      case 'Database': return 'var(--layer-database)';
      case 'Backend': return 'var(--layer-backend)';
      case 'Infrastructure': return 'var(--accent-purple)';
      case 'Cache': return 'var(--accent-cyan)';
      case 'Frontend': return 'var(--layer-frontend)';
      default: return 'var(--accent-emerald)';
    }
  };

  return (
    <div>
      {/* Top Bottleneck Banner */}
      <div className="glass-card" style={{
        padding: '28px',
        marginBottom: '24px',
        border: '1px solid var(--border-glow)',
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(245, 158, 11, 0.05) 100%)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              background: 'rgba(244, 63, 94, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid rgba(244, 63, 94, 0.3)'
            }}>
              <AlertOctagon size={22} color="#fb7185" />
            </div>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>IDENTIFIED PRIMARY BOTTLENECK LAYER</span>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#ffffff' }}>
                {primary} Layer <span className="badge badge-rose" style={{ fontSize: '0.8rem', marginLeft: '8px' }}>CRITICAL</span>
              </h2>
            </div>
          </div>

          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Bottleneck Score:</span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fb7185' }}>
              {bottlenecks?.primaryScore || scores[primary] || 88} <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/ 100</span>
            </div>
          </div>
        </div>

        {/* Evidence & Root Cause Box */}
        <div style={{ background: 'rgba(0, 0, 0, 0.25)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '16px' }}>
          <div style={{ fontSize: '0.85rem', color: '#ffffff', marginBottom: '6px' }}>
            <strong>Observed Evidence:</strong> <span style={{ color: 'var(--text-secondary)' }}>{evidence}</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: '#ffffff' }}>
            <strong>Likely Root Cause:</strong> <span style={{ color: '#fbbf24' }}>{likelyCause}</span>
          </div>
        </div>
      </div>

      {/* Layer-by-Layer Bottleneck Scores (0-100) */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '16px' }}>
          Cross-Layer Transparent Bottleneck Scores (0–100 Scale)
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {Object.entries(scores).map(([layer, score]) => {
            const color = getLayerColor(layer);
            return (
              <div key={layer}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{layer} Layer</span>
                  <span className="font-mono" style={{ fontWeight: 700, color }}>{score} / 100</span>
                </div>
                <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${score}%`,
                    height: '100%',
                    background: color,
                    borderRadius: '4px',
                    boxShadow: `0 0 10px ${color}`
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actionable Recommendations Table */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '18px' }}>
          <Lightbulb size={20} color="var(--accent-emerald)" />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Prioritized Optimization Directives</h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {recommendations.map((rec, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '12px',
                padding: '16px 20px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className={`badge ${rec.priority === 'CRITICAL' ? 'badge-rose' : rec.priority === 'HIGH' ? 'badge-amber' : 'badge-cyan'}`}>
                    {rec.priority} PRIORITY
                  </span>
                  <span className="badge badge-purple">RISK: {rec.risk}</span>
                </div>
                <span style={{ fontSize: '0.78rem', color: '#34d399', fontWeight: 600 }}>
                  Expected Impact: {rec.expectedImpact}
                </span>
              </div>

              <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#ffffff', marginBottom: '6px' }}>
                {rec.problem}
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '10px' }}>
                <strong>Evidence:</strong> {rec.evidence}
              </div>
              <div style={{
                background: 'rgba(16, 185, 129, 0.05)',
                borderLeft: '3px solid #10b981',
                padding: '10px 14px',
                borderRadius: '0 8px 8px 0',
                fontSize: '0.84rem',
                color: 'var(--text-primary)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <ArrowRight size={15} color="#34d399" />
                <span><strong>Recommended Action:</strong> {rec.recommendedAction}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
