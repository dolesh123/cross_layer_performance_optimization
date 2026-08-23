// frontend/src/components/AppDetailsView.jsx
import React, { useState, useEffect } from 'react';
import { Activity, Gauge, Server, Database, Zap, Cpu, Monitor, Clock, Sliders, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function AppDetailsView({ app, metricsHistory, onRefresh }) {
  const [timeRange, setTimeRange] = useState('1h');
  const [flawSwitches, setFlawSwitches] = useState({
    slowDbQuery: true,
    cpuLoad: false,
    disableIndex: true,
    disableCache: false,
    artificialDelay: false
  });
  const [isUpdatingFlaw, setIsUpdatingFlaw] = useState(false);

  // Fetch current flaw switch status from demo-app if APP-001
  useEffect(() => {
    if (app?.id === 'APP-001') {
      fetch('http://localhost:4000/api/control/status')
        .then(r => r.json())
        .then(d => {
          if (d.flaws) setFlawSwitches(d.flaws);
        })
        .catch(() => {});
    }
  }, [app]);

  const handleToggleFlaw = async (flawName) => {
    const newValue = !flawSwitches[flawName];
    setIsUpdatingFlaw(true);
    try {
      const res = await fetch('http://localhost:4000/api/control/toggle-flaw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ flawName, enabled: newValue })
      });
      const data = await res.json();
      if (data.flaws) setFlawSwitches(data.flaws);
      onRefresh();
    } catch (e) {
      console.error(e);
    } finally {
      setIsUpdatingFlaw(false);
    }
  };

  const current = metricsHistory && metricsHistory.length > 0 ? metricsHistory[0] : {
    backend: { avgLatencyMs: 140, p95LatencyMs: 280, p99LatencyMs: 420, errorRatePercent: 0.2 },
    database: { avgQueryLatencyMs: 35, slowQueriesCount: 0, rowsScanned: 20, activeConnections: 12 },
    cache: { hitRatioPercent: 72, hits: 140, misses: 30, memoryMb: 48 },
    infrastructure: { cpuPercent: 32, memoryMb: 140, containerStatus: 'RUNNING' },
    frontend: { pageLoadTimeMs: 480, lcpSec: 0.8, fidMs: 14, cls: 0.01 }
  };

  const healthScore = Math.round(Math.max(10, Math.min(98, 100 - (current.backend.avgLatencyMs / 10) - (current.database.avgQueryLatencyMs / 5))));

  return (
    <div>
      {/* App Header & Time Range Filter */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px',
        marginBottom: '24px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h2 style={{ fontSize: '1.35rem', fontWeight: 800 }}>{app?.name}</h2>
            <span className="badge badge-emerald font-mono">{app?.id}</span>
            <span className="badge badge-purple">{app?.environment}</span>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
            Live URL: <span className="font-mono" style={{ color: 'var(--accent-cyan)' }}>{app?.url}</span> • Stack: {app?.technology}
          </p>
        </div>

        {/* Time Range Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(255, 255, 255, 0.03)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          {['15m', '1h', '6h', '24h', '7d'].map(range => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`btn-preset ${timeRange === range ? 'active' : ''}`}
              style={{ padding: '6px 12px', fontSize: '0.78rem' }}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Health Score & Multi-Layer Overview */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px',
        marginBottom: '24px'
      }}>
        {/* Health Score Dial */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>APPLICATION HEALTH SCORE</span>
            <Gauge size={20} color="var(--accent-emerald)" />
          </div>

          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', margin: '14px 0' }}>
            <span style={{ fontSize: '3rem', fontWeight: 800, color: healthScore > 75 ? '#34d399' : healthScore > 50 ? '#fbbf24' : '#fb7185', letterSpacing: '-0.03em' }}>
              {healthScore}
            </span>
            <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>/ 100</span>
          </div>

          {/* Subscore breakdowns */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.75rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '10px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>API Latency Health:</span>
              <strong style={{ color: current.backend.avgLatencyMs < 200 ? '#34d399' : '#fbbf24' }}>{current.backend.avgLatencyMs < 200 ? '95%' : '58%'}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Database Query Health:</span>
              <strong style={{ color: current.database.avgQueryLatencyMs < 50 ? '#34d399' : '#fb7185' }}>{current.database.avgQueryLatencyMs < 50 ? '98%' : '32%'}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Cache Hit Efficiency:</span>
              <strong>{current.cache.hitRatioPercent}%</strong>
            </div>
          </div>
        </div>

        {/* Layer 2: Backend API */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--layer-backend)', fontWeight: 700 }}>LAYER 2: BACKEND / API</span>
            <Server size={18} color="var(--layer-backend)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            {current.backend.avgLatencyMs} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>ms</span>
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            P95: <strong>{current.backend.p95LatencyMs}ms</strong> • P99: <strong>{current.backend.p99LatencyMs}ms</strong>
          </div>
          <div style={{ fontSize: '0.74rem', color: '#34d399', marginTop: '8px' }}>
            Error Rate: {current.backend.errorRatePercent}%
          </div>
        </div>

        {/* Layer 3: Database */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--layer-database)', fontWeight: 700 }}>LAYER 3: DATABASE</span>
            <Database size={18} color="var(--layer-database)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: current.database.avgQueryLatencyMs > 60 ? '#fb7185' : '#ffffff' }}>
            {current.database.avgQueryLatencyMs} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>ms</span>
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Rows Scanned: <strong>{current.database.rowsScanned.toLocaleString()}</strong>
          </div>
          <div style={{ fontSize: '0.74rem', color: current.database.slowQueriesCount > 0 ? '#fb7185' : '#34d399', marginTop: '8px' }}>
            Slow Queries: {current.database.slowQueriesCount} detected
          </div>
        </div>

        {/* Layer 4: Redis Cache */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>LAYER 4: REDIS CACHE</span>
            <Zap size={18} color="var(--accent-cyan)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: current.cache.hitRatioPercent > 60 ? '#34d399' : '#fbbf24' }}>
            {current.cache.hitRatioPercent}%
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Hits: <strong>{current.cache.hits}</strong> • Misses: <strong>{current.cache.misses}</strong>
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '8px' }}>
            Memory: {current.cache.memoryMb} MB
          </div>
        </div>
      </div>

      {/* Controllable Demo Flaw Switches (For Live Evaluator Testing) */}
      {app?.id === 'APP-001' && (
        <div className="glass-card" style={{ padding: '24px', marginBottom: '24px', border: '1px solid var(--border-glow)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Sliders size={20} color="var(--accent-emerald)" />
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 800 }}>Controllable Demo Flaw Injections</h3>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                  Toggle live architectural defects on the monitored movie application to verify automated detection & experiments.
                </p>
              </div>
            </div>
            <span className="badge badge-emerald">Live Control Plane</span>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '14px'
          }}>
            {/* 1. Slow DB Query */}
            <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '0.84rem', fontWeight: 700 }}>Slow DB Full Table Scan</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Forces 50k row linear scan</div>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={flawSwitches.slowDbQuery}
                  onChange={() => handleToggleFlaw('slowDbQuery')}
                />
                <span className="slider"></span>
              </label>
            </div>

            {/* 2. CPU Heavy Load */}
            <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '0.84rem', fontWeight: 700 }}>High CPU Compute Load</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Heavy synchronous math loops</div>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={flawSwitches.cpuLoad}
                  onChange={() => handleToggleFlaw('cpuLoad')}
                />
                <span className="slider"></span>
              </label>
            </div>

            {/* 3. Disable Index */}
            <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '0.84rem', fontWeight: 700 }}>Missing B-Tree Indexes</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Bypasses index on genre/year</div>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={flawSwitches.disableIndex}
                  onChange={() => handleToggleFlaw('disableIndex')}
                />
                <span className="slider"></span>
              </label>
            </div>

            {/* 4. Disable Cache */}
            <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '0.84rem', fontWeight: 700 }}>Disable Redis Caching</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Forces 100% cache miss</div>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={flawSwitches.disableCache}
                  onChange={() => handleToggleFlaw('disableCache')}
                />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
