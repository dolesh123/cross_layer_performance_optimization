// frontend/src/components/OverviewView.jsx
import React from 'react';
import { Layers, Activity, CheckCircle, AlertTriangle, XCircle, ArrowUpRight, Cpu, Database, Server, Zap } from 'lucide-react';

export default function OverviewView({ applications, onSelectApp }) {
  return (
    <div>
      {/* Top Global Health KPIs */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '16px',
        marginBottom: '28px'
      }}>
        {/* Total Apps */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>REGISTERED APPLICATIONS</span>
            <Layers size={20} color="var(--accent-emerald)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            {applications.length}
          </div>
          <div style={{ fontSize: '0.76rem', color: '#34d399', marginTop: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <CheckCircle size={13} /> {applications.length} Active Services Monitored
          </div>
        </div>

        {/* Healthy vs Warnings */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>HEALTH STATUS</span>
            <Activity size={20} color="var(--accent-cyan)" />
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px' }}>
            <span style={{ fontSize: '2rem', fontWeight: 800, color: '#34d399' }}>1</span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Healthy</span>
            <span style={{ fontSize: '2rem', fontWeight: 800, color: '#fbbf24', marginLeft: '12px' }}>1</span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Warning</span>
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            Multi-Layer Analysis Active
          </div>
        </div>

        {/* Global Latency */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>GLOBAL MEAN LATENCY</span>
            <Zap size={20} color="var(--accent-amber)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            142.4 <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>ms</span>
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            Across all monitored endpoints
          </div>
        </div>

        {/* Global Error Rate */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>GLOBAL ERROR RATE</span>
            <Server size={20} color="var(--accent-purple)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            0.24%
          </div>
          <div style={{ fontSize: '0.76rem', color: '#34d399', marginTop: '6px' }}>
            Within SLO target (&lt;1.0%)
          </div>
        </div>
      </div>

      {/* Monitored Applications Directory */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Monitored Application Registry</h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
              Select an application to view real-time multi-layer telemetry, bottleneck diagnosis, and optimization experiments.
            </p>
          </div>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
          gap: '20px'
        }}>
          {applications.map(app => (
            <div
              key={app.id}
              onClick={() => onSelectApp(app.id)}
              style={{
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '16px',
                padding: '22px',
                cursor: 'pointer',
                transition: 'all 0.25s ease',
                position: 'relative'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent-emerald)';
                e.currentTarget.style.background = 'rgba(16, 185, 129, 0.04)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-subtle)';
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.02)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <span className="badge badge-emerald font-mono">{app.id}</span>
                <span className={`badge ${app.environment === 'production' ? 'badge-purple' : 'badge-cyan'}`}>
                  {app.environment}
                </span>
              </div>

              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginBottom: '6px' }}>
                {app.name}
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: '1.4', marginBottom: '16px' }}>
                {app.description}
              </p>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                paddingTop: '14px',
                borderTop: '1px solid var(--border-subtle)',
                fontSize: '0.78rem'
              }}>
                <span style={{ color: 'var(--text-muted)' }}>Tech: <strong style={{ color: 'var(--text-primary)' }}>{app.technology}</strong></span>
                <span style={{ color: 'var(--accent-emerald)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                  Inspect Telemetry <ArrowUpRight size={14} />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
