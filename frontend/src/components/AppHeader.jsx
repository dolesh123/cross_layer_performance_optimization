// frontend/src/components/AppHeader.jsx
import React from 'react';
import { Layers, Activity, Plus, Database, RefreshCw, FileText, LayoutDashboard, AlertOctagon, Sparkles, Sliders, Gauge } from 'lucide-react';

export default function AppHeader({
  activeView,
  setActiveView,
  applications,
  selectedAppId,
  setSelectedAppId,
  onOpenRegisterModal,
  onOpenReportModal,
  onRefresh
}) {
  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(10, 14, 23, 0.92)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '14px 28px'
    }}>
      <div style={{
        maxWidth: '1540px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        {/* Brand & App Identity */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 25px rgba(16, 185, 129, 0.45)'
          }}>
            <Layers size={26} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#ffffff' }}>
                IMPOF PLATFORM
              </h1>
              <span className="badge badge-emerald">DEV-OPS OBSERVABILITY</span>
            </div>
            <p style={{ fontSize: '0.76rem', color: 'var(--text-secondary)' }}>
              Integrated Multi-Layer Performance Monitoring, Bottlenecks & Optimization
            </p>
          </div>
        </div>

        {/* Global Application Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>MONITORED APP:</span>
          <select
            value={selectedAppId}
            onChange={(e) => setSelectedAppId(e.target.value)}
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-primary)',
              padding: '8px 14px',
              borderRadius: '10px',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            {applications.map(app => (
              <option key={app.id} value={app.id}>
                {app.id} — {app.name} ({app.environment})
              </option>
            ))}
          </select>

          <button
            onClick={onOpenRegisterModal}
            className="btn-secondary"
            style={{ padding: '8px 12px', fontSize: '0.8rem' }}
            title="Register New Application"
          >
            <Plus size={14} />
            <span>Register App</span>
          </button>
        </div>

        {/* Navigation Tabs */}
        <nav style={{
          display: 'flex',
          background: 'rgba(255, 255, 255, 0.03)',
          padding: '4px',
          borderRadius: '12px',
          border: '1px solid var(--border-subtle)',
          gap: '4px'
        }}>
          <button
            onClick={() => setActiveView('overview')}
            className={`btn-preset ${activeView === 'overview' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <LayoutDashboard size={15} />
            <span>Overview</span>
          </button>

          <button
            onClick={() => setActiveView('details')}
            className={`btn-preset ${activeView === 'details' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <Activity size={15} />
            <span>Multi-Layer Metrics</span>
          </button>

          <button
            onClick={() => setActiveView('bottlenecks')}
            className={`btn-preset ${activeView === 'bottlenecks' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <AlertOctagon size={15} />
            <span>Bottlenecks & Recs</span>
          </button>

          <button
            onClick={() => setActiveView('anomalies')}
            className={`btn-preset ${activeView === 'anomalies' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <Sparkles size={15} />
            <span>ML Anomalies</span>
          </button>

          <button
            onClick={() => setActiveView('experiments')}
            className={`btn-preset ${activeView === 'experiments' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <Sliders size={15} />
            <span>Before / After Experiments</span>
          </button>

          <button
            onClick={() => setActiveView('loadtest')}
            className={`btn-preset ${activeView === 'loadtest' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
          >
            <Gauge size={15} />
            <span>Load Testing</span>
          </button>
        </nav>

        {/* Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            onClick={onRefresh}
            className="btn-secondary"
            style={{ padding: '8px 12px', fontSize: '0.8rem' }}
            title="Refresh Platform Metrics"
          >
            <RefreshCw size={14} />
          </button>

          <button
            onClick={onOpenReportModal}
            className="btn-primary"
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <FileText size={15} />
            <span>Project Report</span>
          </button>
        </div>
      </div>
    </header>
  );
}
