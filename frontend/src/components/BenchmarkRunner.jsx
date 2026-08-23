// frontend/src/components/BenchmarkRunner.jsx
import React, { useState } from 'react';
import { BarChart3, Play, Sparkles, TrendingUp, Layers, CheckCircle2, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function BenchmarkRunner() {
  const [report, setReport] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const runBenchmark = async () => {
    setIsRunning(true);
    try {
      const response = await fetch('http://localhost:5000/api/benchmark/comparative', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setReport(data);

      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.6 }
      });
    } catch (err) {
      console.error('Benchmark failed:', err);
    } finally {
      setIsRunning(false);
    }
  };

  const getScenarioColor = (idx) => {
    switch (idx) {
      case 0: return '#fb7185'; // Rose (Unoptimized)
      case 1: return '#fbbf24'; // Amber (DB only)
      case 2: return '#38bdf8'; // Cyan (Backend + DB)
      case 3: return '#34d399'; // Emerald (Full IMPOF)
      default: return '#10b981';
    }
  };

  return (
    <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <BarChart3 size={24} color="#10b981" />
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>Multi-Tier Comparative Benchmark Suite</h2>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Empirical validation comparing Baseline against isolated layer enhancements and full cross-layer integration.
          </p>
        </div>

        <button
          onClick={runBenchmark}
          disabled={isRunning}
          className="btn-primary"
          style={{ padding: '12px 24px', fontSize: '0.95rem' }}
        >
          <Play size={18} fill="#ffffff" />
          <span>{isRunning ? 'Running 4-Tier Benchmark...' : 'Run Comparative Suite'}</span>
        </button>
      </div>

      {report && (
        <div>
          {/* Top KPI Callout */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)',
            border: '1px solid var(--border-glow)',
            borderRadius: '16px',
            padding: '20px 24px',
            marginBottom: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '16px'
          }}>
            <div>
              <div style={{ fontSize: '0.85rem', color: 'var(--accent-emerald)', fontWeight: 700 }}>
                CUMULATIVE SYSTEM PERFORMANCE GAIN
              </div>
              <div style={{ fontSize: '2.4rem', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.02em' }}>
                +{report.overallGainIndexPercent.toFixed(1)}% <span style={{ fontSize: '1.1rem', fontWeight: 500, color: 'var(--text-secondary)' }}>Optimization Gain Index (OGI)</span>
              </div>
            </div>

            <div style={{ textAlign: 'right' }}>
              <span className="badge badge-emerald" style={{ fontSize: '0.82rem', padding: '6px 14px' }}>
                <CheckCircle2 size={14} /> Full Cross-Layer Superiority
              </span>
            </div>
          </div>

          {/* Scenario Comparison Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '16px',
            marginBottom: '28px'
          }}>
            {report.scenarios.map((sc, idx) => {
              const color = getScenarioColor(idx);
              const maxDuration = Math.max(...report.scenarios.map(s => s.totalDurationMs));
              const heightPct = Math.max(10, Math.round((sc.totalDurationMs / maxDuration) * 100));

              return (
                <div
                  key={idx}
                  style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    border: `1px solid ${idx === 3 ? 'var(--border-glow)' : 'var(--border-subtle)'}`,
                    borderRadius: '14px',
                    padding: '18px',
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                >
                  <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '8px' }}>
                    {sc.name}
                  </div>

                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px', marginBottom: '12px' }}>
                    <span style={{ fontSize: '2rem', fontWeight: 800, color }}>
                      {sc.totalDurationMs.toFixed(1)}
                    </span>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>ms</span>
                  </div>

                  {/* Relative bar */}
                  <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '3px', marginBottom: '14px' }}>
                    <div style={{ width: `${heightPct}%`, height: '100%', background: color, borderRadius: '3px' }} />
                  </div>

                  {/* Layer Breakdown Table */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.78rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Frontend:</span>
                      <span className="font-mono">{sc.layers.frontendMs.toFixed(1)}ms</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Network:</span>
                      <span className="font-mono">{sc.layers.networkMs.toFixed(1)}ms</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Backend:</span>
                      <span className="font-mono">{sc.layers.backendMs.toFixed(1)}ms</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Database:</span>
                      <span className="font-mono">{sc.layers.databaseMs.toFixed(1)}ms</span>
                    </div>
                  </div>

                  {sc.gainVsBaseline !== undefined && idx > 0 && (
                    <div style={{ marginTop: '14px', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)', fontSize: '0.8rem', color: '#34d399', fontWeight: 700 }}>
                      ⚡ {sc.gainVsBaseline}% faster than baseline
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {!report && !isRunning && (
        <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
          <Sparkles size={36} style={{ margin: '0 auto 12px auto', opacity: 0.5 }} />
          <p>Click "Run Comparative Suite" above to execute all 4 optimization configurations and view side-by-side performance benchmarks.</p>
        </div>
      )}
    </div>
  );
}
