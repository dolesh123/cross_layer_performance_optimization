// frontend/src/components/BottleneckReport.jsx
import React from 'react';
import { AlertOctagon, AlertTriangle, CheckCircle, Lightbulb, ShieldCheck, ArrowRight } from 'lucide-react';

export default function BottleneckReport({ analysis }) {
  if (!analysis) return null;

  const { primaryBottleneck, secondaryBottleneck, detectedIssues = [], recommendations = [], optimizationGainIndex = 0 } = analysis;

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'CRITICAL': return <span className="badge badge-rose">CRITICAL</span>;
      case 'HIGH': return <span className="badge badge-amber">HIGH PRIORITY</span>;
      case 'MEDIUM': return <span className="badge badge-purple">MEDIUM</span>;
      case 'OPTIMAL': return <span className="badge badge-emerald">OPTIMAL</span>;
      default: return <span className="badge badge-cyan">{severity}</span>;
    }
  };

  return (
    <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
      {/* Title */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertOctagon size={20} color="var(--accent-amber)" />
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Automated Bottleneck Diagnostics & Recommendations</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Cross-layer heuristic analysis detecting latency anti-patterns
            </p>
          </div>
        </div>
        
        {primaryBottleneck && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Primary Bottleneck:</span>
            <span className="badge badge-amber" style={{ fontSize: '0.82rem', padding: '5px 12px' }}>
              {primaryBottleneck.layer} ({primaryBottleneck.percentage}% of latency)
            </span>
          </div>
        )}
      </div>

      {/* Grid of Issues and Recommendations */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        {/* Detected Issues */}
        <div>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>IDENTIFIED LAYER DEFICIENCIES ({detectedIssues.length})</span>
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {detectedIssues.map((issue, idx) => (
              <div
                key={idx}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '12px 14px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontSize: '0.88rem', fontWeight: 600, color: '#ffffff' }}>
                    {issue.title}
                  </span>
                  {getSeverityBadge(issue.severity)}
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                  {issue.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Actionable Recommendations */}
        <div>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-emerald)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Lightbulb size={16} />
            <span>ACTIONABLE OPTIMIZATION DIRECTIVES</span>
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {recommendations.map((rec, idx) => (
              <div
                key={idx}
                style={{
                  background: 'rgba(16, 185, 129, 0.03)',
                  border: '1px solid rgba(16, 185, 129, 0.2)',
                  borderRadius: '10px',
                  padding: '12px 14px',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px'
                }}
              >
                <ArrowRight size={16} color="#34d399" style={{ flexShrink: 0, marginTop: '2px' }} />
                <p style={{ fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: '1.4' }}>
                  {rec}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
