// frontend/src/components/StressTestRunner.jsx
import React, { useState } from 'react';
import { Gauge, Users, Zap, Play, CheckCircle2, TrendingUp, AlertCircle } from 'lucide-react';

export default function StressTestRunner() {
  const [virtualUsers, setVirtualUsers] = useState(50);
  const [totalRequests, setTotalRequests] = useState(150);
  const [profile, setProfile] = useState('full_impof');
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunStressTest = async () => {
    setIsRunning(true);
    setResult(null);

    const isOptimized = profile === 'full_impof';
    const options = isOptimized ? {
      enableDbIndex: true,
      enableDbPool: true,
      enableDbJoin: true,
      enableL1Cache: true,
      enableL2Cache: true,
      enableAsyncExec: true,
      enableDtoProjection: true,
      enableCompression: true,
      enableCdnEdge: true,
      enableVirtualization: true
    } : {
      enableDbIndex: false,
      enableDbPool: false,
      enableDbJoin: false,
      enableL1Cache: false,
      enableL2Cache: false,
      enableAsyncExec: false,
      enableDtoProjection: false,
      enableCompression: false,
      enableCdnEdge: false,
      enableVirtualization: false
    };

    try {
      const response = await fetch('http://localhost:5000/api/benchmark/stress-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          virtualUsers,
          totalRequests,
          options
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Stress test failed:', err);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Gauge size={24} color="var(--accent-cyan)" />
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>Concurrent Virtual User Load & Stress Engine</h2>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Evaluate throughput capacity (RPS) and latency percentiles (P50/P90/P95/P99) under simulated concurrent traffic.
          </p>
        </div>
      </div>

      {/* Configuration Controls */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '16px',
        background: 'rgba(255, 255, 255, 0.02)',
        padding: '20px',
        borderRadius: '14px',
        border: '1px solid var(--border-subtle)',
        marginBottom: '24px'
      }}>
        {/* Virtual Users */}
        <div>
          <label style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
            <span>CONCURRENT VIRTUAL USERS</span>
            <span style={{ color: '#ffffff', fontWeight: 700 }}>{virtualUsers} Users</span>
          </label>
          <input
            type="range"
            min="10"
            max="200"
            step="10"
            value={virtualUsers}
            onChange={(e) => setVirtualUsers(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--accent-emerald)', cursor: 'pointer' }}
          />
        </div>

        {/* Total Requests */}
        <div>
          <label style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
            <span>TOTAL REQUEST LOAD</span>
            <span style={{ color: '#ffffff', fontWeight: 700 }}>{totalRequests} Requests</span>
          </label>
          <input
            type="range"
            min="50"
            max="500"
            step="50"
            value={totalRequests}
            onChange={(e) => setTotalRequests(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--accent-cyan)', cursor: 'pointer' }}
          />
        </div>

        {/* Optimization Mode */}
        <div>
          <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
            TARGET SYSTEM PROFILE
          </label>
          <select
            value={profile}
            onChange={(e) => setProfile(e.target.value)}
            style={{
              width: '100%',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-primary)',
              padding: '8px 12px',
              borderRadius: '8px',
              fontSize: '0.85rem'
            }}
          >
            <option value="full_impof">🚀 Fully Optimized (IMPOF Cross-Layer)</option>
            <option value="baseline">⚠️ Baseline (Unoptimized Multi-Tier)</option>
          </select>
        </div>

        {/* Trigger Button */}
        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <button
            onClick={handleRunStressTest}
            disabled={isRunning}
            className="btn-primary"
            style={{ width: '100%', padding: '10px 16px', justifyContent: 'center' }}
          >
            <Play size={16} fill="#ffffff" />
            <span>{isRunning ? 'Simulating Load...' : 'Start Stress Test'}</span>
          </button>
        </div>
      </div>

      {/* Stress Test Results */}
      {result && (
        <div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            marginBottom: '24px'
          }}>
            {/* RPS Throughput */}
            <div className="glass-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>SYSTEM THROUGHPUT</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-emerald)', marginTop: '4px' }}>
                {result.throughputRps} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>RPS</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                Requests Processed Per Second
              </div>
            </div>

            {/* Mean Latency */}
            <div className="glass-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>MEAN RESPONSE TIME</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                {result.latencyMetrics.meanMs} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>ms</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                Average request latency under concurrency
              </div>
            </div>

            {/* Total Duration */}
            <div className="glass-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>TOTAL TEST DURATION</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)', marginTop: '4px' }}>
                {result.totalDurationSec} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>sec</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                {result.completedRequests} requests completed
              </div>
            </div>
          </div>

          {/* Latency Percentiles Breakdown */}
          <div style={{
            background: 'rgba(255, 255, 255, 0.02)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '12px',
            padding: '20px'
          }}>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '16px' }}>
              LATENCY PERCENTILES DISTRIBUTION
            </h4>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '12px' }}>
              <div style={{ padding: '12px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>P50 (Median)</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', marginTop: '4px' }}>
                  {result.latencyMetrics.p50Ms} ms
                </div>
              </div>

              <div style={{ padding: '12px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>P90</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#38bdf8', marginTop: '4px' }}>
                  {result.latencyMetrics.p90Ms} ms
                </div>
              </div>

              <div style={{ padding: '12px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>P95</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fbbf24', marginTop: '4px' }}>
                  {result.latencyMetrics.p95Ms} ms
                </div>
              </div>

              <div style={{ padding: '12px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>P99 (Tail Latency)</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fb7185', marginTop: '4px' }}>
                  {result.latencyMetrics.p99Ms} ms
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
