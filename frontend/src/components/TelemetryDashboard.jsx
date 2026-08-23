// frontend/src/components/TelemetryDashboard.jsx
import React from 'react';
import { Gauge, Zap, TrendingUp, HardDrive, Database, ArrowDownRight, CheckCircle } from 'lucide-react';

export default function TelemetryDashboard({ result, systemStats }) {
  if (!result || !result.trace) {
    return null;
  }

  const { trace, analysis, payloadMeta, source, queryMeta } = result;
  const { totalDurationMs } = trace;
  const ogi = analysis?.optimizationGainIndex || 0;

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
      gap: '16px',
      marginBottom: '24px'
    }}>
      {/* 1. Total Latency */}
      <div className="glass-card" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
            TOTAL REQUEST LATENCY
          </span>
          <Gauge size={18} color="var(--accent-cyan)" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <span style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff' }}>
            {totalDurationMs.toFixed(1)}
          </span>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>ms</span>
        </div>
        <div style={{ fontSize: '0.75rem', color: totalDurationMs < 50 ? '#34d399' : '#fb7185', marginTop: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <span>{totalDurationMs < 50 ? '● High Speed (<50ms)' : '▲ Latency Overhead (>50ms)'}</span>
        </div>
      </div>

      {/* 2. Optimization Gain Index (OGI) */}
      <div className="glass-card" style={{ padding: '20px', borderColor: ogi > 50 ? 'var(--border-glow)' : 'var(--border-subtle)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
            OPTIMIZATION GAIN (OGI)
          </span>
          <TrendingUp size={18} color="var(--accent-emerald)" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <span style={{ fontSize: '1.8rem', fontWeight: 800, color: ogi > 70 ? 'var(--accent-emerald)' : '#ffffff' }}>
            +{ogi.toFixed(1)}%
          </span>
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
          Gain vs Baseline (380ms reference)
        </div>
      </div>

      {/* 3. Data Retrieval Tier */}
      <div className="glass-card" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
            DATA SOURCE TIER
          </span>
          <Zap size={18} color="var(--accent-amber)" />
        </div>
        <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', textTransform: 'uppercase' }}>
          {source === 'L1_CACHE' ? '⚡ L1 Memory Cache' : source === 'L2_CACHE' ? '🔄 L2 Redis Store' : '🗄️ MySQL Database'}
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '6px' }}>
          {source.includes('CACHE') ? 'Sub-millisecond retrieval' : queryMeta?.strategy || 'Disk / Memory Scan'}
        </div>
      </div>

      {/* 4. Database Scanning & Indexing */}
      <div className="glass-card" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
            DATABASE ROWS SCANNED
          </span>
          <Database size={18} color="var(--accent-purple)" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <span style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff' }}>
            {queryMeta?.rowsScanned ? queryMeta.rowsScanned.toLocaleString() : (payloadMeta?.itemCount || 0)}
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>rows</span>
        </div>
        <div style={{ fontSize: '0.75rem', color: queryMeta?.indexUsed ? '#34d399' : '#fbbf24', marginTop: '6px' }}>
          {queryMeta?.indexUsed ? `Index: ${queryMeta.indexUsed}` : (source.includes('CACHE') ? '0 DB rows (Served from Cache)' : 'Full Table Scan O(N)')}
        </div>
      </div>
    </div>
  );
}
