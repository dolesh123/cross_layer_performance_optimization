// frontend/src/components/Navbar.jsx
import React from 'react';
import { Layers, Activity, Cpu, Database, RefreshCw, FileText, Zap, BarChart3, Gauge } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onClearCache, onExportReport, systemStats }) {
  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(10, 14, 23, 0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '12px 24px'
    }}>
      <div style={{
        maxWidth: '1440px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        {/* Brand & Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(16, 185, 129, 0.4)'
          }}>
            <Layers size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#ffffff' }}>
                IMPOF
              </h1>
              <span className="badge badge-emerald">v1.0 RESEARCH SUITE</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
              Integrated Multi-Layer Performance Optimization Framework
            </p>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav style={{
          display: 'flex',
          background: 'rgba(255, 255, 255, 0.03)',
          padding: '4px',
          borderRadius: '12px',
          border: '1px solid var(--border-subtle)',
          gap: '4px'
        }}>
          <button
            onClick={() => setActiveTab('playground')}
            className={`btn-preset ${activeTab === 'playground' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px' }}
          >
            <Zap size={16} />
            <span>Interactive Lab</span>
          </button>

          <button
            onClick={() => setActiveTab('benchmark')}
            className={`btn-preset ${activeTab === 'benchmark' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px' }}
          >
            <BarChart3 size={16} />
            <span>Comparative Benchmark</span>
          </button>

          <button
            onClick={() => setActiveTab('stresstest')}
            className={`btn-preset ${activeTab === 'stresstest' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px' }}
          >
            <Gauge size={16} />
            <span>Stress Test (Virtual Users)</span>
          </button>
        </nav>

        {/* Quick System Telemetry & Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: 'rgba(255, 255, 255, 0.02)',
            padding: '6px 14px',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)',
            fontSize: '0.78rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Database size={14} color="#10b981" />
              <span>100,000 Records</span>
            </div>
            <div style={{ width: '1px', height: '12px', background: 'var(--border-subtle)' }} />
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }} />
              <span>Engine Active</span>
            </div>
          </div>

          <button
            onClick={onClearCache}
            title="Clear L1/L2 Caches"
            className="btn-secondary"
            style={{ padding: '8px 12px', fontSize: '0.8rem' }}
          >
            <RefreshCw size={14} />
            <span>Flush Caches</span>
          </button>

          <button
            onClick={onExportReport}
            className="btn-primary"
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <FileText size={15} />
            <span>Export Report</span>
          </button>
        </div>
      </div>
    </header>
  );
}
