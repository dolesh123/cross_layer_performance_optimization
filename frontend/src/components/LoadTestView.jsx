// frontend/src/components/LoadTestView.jsx
import React, { useState } from 'react';
import { Gauge, Users, Play, Activity, Server, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function LoadTestView({ app }) {
  const [targetUrl, setTargetUrl] = useState(app?.url ? `${app.url}/api/movies` : 'http://localhost:4000/api/movies');
  const [virtualUsers, setVirtualUsers] = useState(25);
  const [totalRequests, setTotalRequests] = useState(100);
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunLoadTest = async () => {
    setIsRunning(true);
    setResult(null);

    try {
      const res = await fetch('http://localhost:5000/api/load-tests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          appId: app?.id || 'APP-001',
          targetUrl,
          virtualUsers,
          totalRequests
        })
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div>
      <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <Gauge size={22} color="var(--accent-cyan)" />
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>Controlled Application Load Testing Engine</h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Simulate concurrent virtual user traffic against registered service endpoints and measure throughput (RPS) and latency percentiles.
            </p>
          </div>
        </div>

        {/* Configuration Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '16px',
          background: 'rgba(255, 255, 255, 0.02)',
          padding: '20px',
          borderRadius: '14px',
          border: '1px solid var(--border-subtle)',
          marginBottom: '20px'
        }}>
          {/* Target URL */}
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              TARGET SERVICE ENDPOINT URL
            </label>
            <input
              type="text"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                fontSize: '0.85rem'
              }}
            />
          </div>

          {/* Virtual Users */}
          <div>
            <label style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              <span>CONCURRENT VIRTUAL USERS</span>
              <strong style={{ color: '#ffffff' }}>{virtualUsers} Users</strong>
            </label>
            <input
              type="range"
              min="5"
              max="150"
              step="5"
              value={virtualUsers}
              onChange={(e) => setVirtualUsers(Number(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-emerald)', cursor: 'pointer' }}
            />
          </div>

          {/* Total Requests */}
          <div>
            <label style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              <span>TOTAL REQUEST VOLUME</span>
              <strong style={{ color: '#ffffff' }}>{totalRequests} Requests</strong>
            </label>
            <input
              type="range"
              min="20"
              max="500"
              step="20"
              value={totalRequests}
              onChange={(e) => setTotalRequests(Number(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-cyan)', cursor: 'pointer' }}
            />
          </div>

          {/* Run Button */}
          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button
              onClick={handleRunLoadTest}
              disabled={isRunning}
              className="btn-primary"
              style={{ width: '100%', padding: '10px 16px', justifyContent: 'center' }}
            >
              <Play size={16} fill="#ffffff" />
              <span>{isRunning ? 'Executing Workload...' : 'Execute Load Test'}</span>
            </button>
          </div>
        </div>

        {/* Load Test Results */}
        {result && (
          <div style={{ marginTop: '20px' }}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '14px',
              marginBottom: '20px'
            }}>
              {/* Throughput */}
              <div className="glass-card" style={{ padding: '18px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>THROUGHPUT CAPACITY</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-emerald)', marginTop: '4px' }}>
                  {result.throughputRps} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>RPS</span>
                </div>
                <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Requests per second
                </div>
              </div>

              {/* Mean Latency */}
              <div className="glass-card" style={{ padding: '18px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>MEAN LATENCY</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                  {result.latencyMetrics.meanMs} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>ms</span>
                </div>
                <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Completed {result.completedRequests} requests
                </div>
              </div>

              {/* Duration */}
              <div className="glass-card" style={{ padding: '18px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>TEST DURATION</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)', marginTop: '4px' }}>
                  {result.durationSec} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>sec</span>
                </div>
                <div style={{ fontSize: '0.74rem', color: result.failedRequests === 0 ? '#34d399' : '#fb7185', marginTop: '4px' }}>
                  {result.failedRequests} failures
                </div>
              </div>
            </div>

            {/* Percentile Cards */}
            <div style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid var(--border-subtle)', borderRadius: '12px', padding: '18px' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, marginBottom: '12px' }}>
                RESPONSE TIME PERCENTILES
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '12px' }}>
                <div style={{ padding: '10px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>P50 (Median)</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff' }}>{result.latencyMetrics.p50Ms} ms</div>
                </div>
                <div style={{ padding: '10px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>P95</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fbbf24' }}>{result.latencyMetrics.p95Ms} ms</div>
                </div>
                <div style={{ padding: '10px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>P99 (Tail Latency)</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fb7185' }}>{result.latencyMetrics.p99Ms} ms</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
