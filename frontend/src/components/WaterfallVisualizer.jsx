// frontend/src/components/WaterfallVisualizer.jsx
import React from 'react';
import { Activity, Clock, ShieldAlert, CheckCircle2, ChevronRight, Hash, Layers } from 'lucide-react';

export default function WaterfallVisualizer({ traceData }) {
  if (!traceData || !traceData.layers) {
    return (
      <div className="glass-card" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
        <Activity size={36} style={{ margin: '0 auto 12px auto', opacity: 0.4 }} />
        <p>No active trace data. Click "Dispatch Request & Trace" above to visualize the live cross-layer waterfall.</p>
      </div>
    );
  }

  const { traceId, totalDurationMs, layers, spans } = traceData;
  const { frontendMs = 0, networkMs = 0, backendMs = 0, databaseMs = 0 } = layers;

  const total = Math.max(0.1, totalDurationMs);
  const frontendPct = Math.round((frontendMs / total) * 100);
  const networkPct = Math.round((networkMs / total) * 100);
  const backendPct = Math.round((backendMs / total) * 100);
  const databasePct = Math.round((databaseMs / total) * 100);

  const getLayerColor = (layer) => {
    switch (layer) {
      case 'Frontend': return 'var(--layer-frontend)';
      case 'Network': return 'var(--layer-network)';
      case 'Backend': return 'var(--layer-backend)';
      case 'Database': return 'var(--layer-database)';
      default: return 'var(--accent-emerald)';
    }
  };

  return (
    <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
      {/* Title & Trace ID */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        marginBottom: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Clock size={20} color="#10b981" />
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>End-to-End Distributed Trace Timeline</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Total Request Lifecycle: <span style={{ color: '#ffffff', fontWeight: 700 }}>{totalDurationMs.toFixed(2)} ms</span>
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="font-mono" style={{
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '4px 10px',
            borderRadius: '8px',
            fontSize: '0.75rem',
            color: 'var(--accent-cyan)',
            border: '1px solid var(--border-subtle)'
          }}>
            Trace ID: {traceId}
          </span>
        </div>
      </div>

      {/* Cross-Layer Cumulative Progress Bar */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{
          display: 'flex',
          height: '24px',
          borderRadius: '8px',
          overflow: 'hidden',
          background: 'rgba(255, 255, 255, 0.05)',
          marginBottom: '10px',
          border: '1px solid var(--border-subtle)'
        }}>
          <div style={{ width: `${frontendPct}%`, background: 'var(--layer-frontend)', transition: 'width 0.5s ease' }} title={`Frontend: ${frontendMs}ms (${frontendPct}%)`} />
          <div style={{ width: `${networkPct}%`, background: 'var(--layer-network)', transition: 'width 0.5s ease' }} title={`Network: ${networkMs}ms (${networkPct}%)`} />
          <div style={{ width: `${backendPct}%`, background: 'var(--layer-backend)', transition: 'width 0.5s ease' }} title={`Backend: ${backendMs}ms (${backendPct}%)`} />
          <div style={{ width: `${databasePct}%`, background: 'var(--layer-database)', transition: 'width 0.5s ease' }} title={`Database: ${databaseMs}ms (${databasePct}%)`} />
        </div>

        {/* Legend */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '12px',
          fontSize: '0.8rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: 'var(--layer-frontend)' }} />
            <span>Frontend: <strong>{frontendMs.toFixed(1)} ms</strong> ({frontendPct}%)</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: 'var(--layer-network)' }} />
            <span>Network: <strong>{networkMs.toFixed(1)} ms</strong> ({networkPct}%)</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: 'var(--layer-backend)' }} />
            <span>Backend: <strong>{backendMs.toFixed(1)} ms</strong> ({backendPct}%)</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: 'var(--layer-database)' }} />
            <span>Database: <strong>{databaseMs.toFixed(1)} ms</strong> ({databasePct}%)</span>
          </div>
        </div>
      </div>

      {/* Detailed Waterfall Spans */}
      <div>
        <h4 style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '12px' }}>
          INDIVIDUAL EXECUTION SPANS
        </h4>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {spans && spans.map((span, idx) => {
            const spanWidthPct = Math.max(3, Math.min(100, Math.round((span.durationMs / total) * 100)));
            const color = getLayerColor(span.layer);

            return (
              <div
                key={span.spanId || idx}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '10px 14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '16px',
                  flexWrap: 'wrap'
                }}
              >
                {/* Span details */}
                <div style={{ flex: '1 1 300px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span className="badge" style={{ background: `rgba(${color === 'var(--layer-database)' ? '16, 185, 129' : '6, 182, 212'}, 0.15)`, color, borderColor: color }}>
                    {span.layer}
                  </span>
                  <div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                      {span.name}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }} className="font-mono">
                      {span.spanId} {span.metadata?.strategy ? `• ${span.metadata.strategy}` : ''}
                    </div>
                  </div>
                </div>

                {/* Duration bar & timing */}
                <div style={{ flex: '1 1 240px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{
                    flex: 1,
                    height: '8px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${spanWidthPct}%`,
                      height: '100%',
                      background: color,
                      borderRadius: '4px',
                      boxShadow: `0 0 8px ${color}`
                    }} />
                  </div>
                  <span className="font-mono" style={{ fontSize: '0.82rem', fontWeight: 700, minWidth: '70px', textAlign: 'right' }}>
                    {span.durationMs.toFixed(2)} ms
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
