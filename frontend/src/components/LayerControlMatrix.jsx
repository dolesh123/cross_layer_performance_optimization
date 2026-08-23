// frontend/src/components/LayerControlMatrix.jsx
import React from 'react';
import { Layers, Database, Cpu, Globe, Monitor, CheckCircle, Sliders, Play } from 'lucide-react';

export default function LayerControlMatrix({ options, setOptions, onExecuteQuery, isLoading }) {
  const handleToggle = (key) => {
    setOptions(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const applyPreset = (presetType) => {
    if (presetType === 'baseline') {
      setOptions({
        enableDbIndex: false,
        enableDbPool: false,
        enableDbJoin: false,
        enableL1Cache: false,
        enableL2Cache: false,
        enableAsyncExec: false,
        enableDtoProjection: false,
        enableCompression: false,
        enableCdnEdge: false,
        enableVirtualization: false,
        queryType: 'products',
        category: 'Electronics',
        limit: 50
      });
    } else if (presetType === 'db_only') {
      setOptions(prev => ({
        ...prev,
        enableDbIndex: true,
        enableDbPool: true,
        enableDbJoin: true,
        enableL1Cache: false,
        enableL2Cache: false,
        enableAsyncExec: false,
        enableDtoProjection: false,
        enableCompression: false,
        enableCdnEdge: false,
        enableVirtualization: false
      }));
    } else if (presetType === 'backend_db') {
      setOptions(prev => ({
        ...prev,
        enableDbIndex: true,
        enableDbPool: true,
        enableDbJoin: true,
        enableL1Cache: true,
        enableL2Cache: true,
        enableAsyncExec: true,
        enableDtoProjection: true,
        enableCompression: false,
        enableCdnEdge: false,
        enableVirtualization: false
      }));
    } else if (presetType === 'full_impof') {
      setOptions({
        enableDbIndex: true,
        enableDbPool: true,
        enableDbJoin: true,
        enableL1Cache: true,
        enableL2Cache: true,
        enableAsyncExec: true,
        enableDtoProjection: true,
        enableCompression: true,
        enableCdnEdge: true,
        enableVirtualization: true,
        queryType: 'products',
        category: 'Electronics',
        limit: 50
      });
    }
  };

  return (
    <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
      {/* Header & Presets */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px',
        borderBottom: '1px solid var(--border-subtle)',
        paddingBottom: '16px',
        marginBottom: '20px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={18} color="#10b981" />
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Cross-Layer Optimization Control Matrix</h2>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            Selectively activate individual layer optimizations to observe isolated and cumulative performance gains.
          </p>
        </div>

        {/* Quick Presets */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>PRESETS:</span>
          <button onClick={() => applyPreset('baseline')} className="btn-preset">
            1. Baseline (Unoptimized)
          </button>
          <button onClick={() => applyPreset('db_only')} className="btn-preset">
            2. Database Only
          </button>
          <button onClick={() => applyPreset('backend_db')} className="btn-preset">
            3. Backend + Database
          </button>
          <button onClick={() => applyPreset('full_impof')} className="btn-preset active" style={{ fontWeight: 700 }}>
            🚀 4. Full IMPOF (All 4 Layers)
          </button>
        </div>
      </div>

      {/* 4 Architectural Layers Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px',
        marginBottom: '24px'
      }}>
        {/* 1. FRONTEND LAYER */}
        <div style={{
          background: 'rgba(6, 182, 212, 0.03)',
          border: '1px solid rgba(6, 182, 212, 0.2)',
          borderRadius: '12px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Monitor size={18} color="var(--layer-frontend)" />
            <h3 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--layer-frontend)' }}>
              1. Frontend Layer
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>DOM Virtualization (Windowing)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableVirtualization}
                  onChange={() => handleToggle('enableVirtualization')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Async State & Non-blocking Render</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableVirtualization}
                  onChange={() => handleToggle('enableVirtualization')}
                />
                <span className="slider"></span>
              </label>
            </label>
          </div>
        </div>

        {/* 2. NETWORK LAYER */}
        <div style={{
          background: 'rgba(139, 92, 246, 0.03)',
          border: '1px solid rgba(139, 92, 246, 0.2)',
          borderRadius: '12px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Globe size={18} color="var(--layer-network)" />
            <h3 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--layer-network)' }}>
              2. Network & Transport Layer
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Brotli / Gzip Payload Compression</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableCompression}
                  onChange={() => handleToggle('enableCompression')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Edge CDN Caching (0ms RTT)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableCdnEdge}
                  onChange={() => handleToggle('enableCdnEdge')}
                />
                <span className="slider"></span>
              </label>
            </label>
          </div>
        </div>

        {/* 3. BACKEND LAYER */}
        <div style={{
          background: 'rgba(245, 158, 11, 0.03)',
          border: '1px solid rgba(245, 158, 11, 0.2)',
          borderRadius: '12px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Cpu size={18} color="var(--layer-backend)" />
            <h3 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--layer-backend)' }}>
              3. Backend Layer (Spring Boot)
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>L1 In-Memory Cache (Caffeine LRU)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableL1Cache}
                  onChange={() => handleToggle('enableL1Cache')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>L2 Distributed Cache (Redis TTL)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableL2Cache}
                  onChange={() => handleToggle('enableL2Cache')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Async Worker Thread Execution</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableAsyncExec}
                  onChange={() => handleToggle('enableAsyncExec')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Lean DTO Projection Serialization</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableDtoProjection}
                  onChange={() => handleToggle('enableDtoProjection')}
                />
                <span className="slider"></span>
              </label>
            </label>
          </div>
        </div>

        {/* 4. DATABASE LAYER */}
        <div style={{
          background: 'rgba(16, 185, 129, 0.03)',
          border: '1px solid rgba(16, 185, 129, 0.2)',
          borderRadius: '12px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Database size={18} color="var(--layer-database)" />
            <h3 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--layer-database)' }}>
              4. Database Layer (MySQL)
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>B-Tree Composite Indexes (O(log N))</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableDbIndex}
                  onChange={() => handleToggle('enableDbIndex')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>HikariCP Connection Pool (Warm Leases)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableDbPool}
                  onChange={() => handleToggle('enableDbPool')}
                />
                <span className="slider"></span>
              </label>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', cursor: 'pointer' }}>
              <span>Batched Indexed JOIN (Eliminate N+1)</span>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={options.enableDbJoin}
                  onChange={() => handleToggle('enableDbJoin')}
                />
                <span className="slider"></span>
              </label>
            </label>
          </div>
        </div>
      </div>

      {/* Query Parameters & Trigger Button */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px',
        background: 'rgba(255, 255, 255, 0.02)',
        padding: '16px 20px',
        borderRadius: '12px',
        border: '1px solid var(--border-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '4px', fontWeight: 600 }}>
              QUERY WORKLOAD TYPE
            </label>
            <select
              value={options.queryType}
              onChange={(e) => setOptions(prev => ({ ...prev, queryType: e.target.value }))}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                fontSize: '0.85rem'
              }}
            >
              <option value="products">Product Catalog Search (100k Records)</option>
              <option value="orders">Relational Customer Orders (N+1 Test)</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '4px', fontWeight: 600 }}>
              CATEGORY FILTER
            </label>
            <select
              value={options.category}
              onChange={(e) => setOptions(prev => ({ ...prev, category: e.target.value }))}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                fontSize: '0.85rem'
              }}
            >
              <option value="Electronics">Electronics</option>
              <option value="Computing">Computing</option>
              <option value="Mobile">Mobile</option>
              <option value="Audio">Audio</option>
              <option value="Gaming">Gaming</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '4px', fontWeight: 600 }}>
              RESULT BATCH LIMIT
            </label>
            <input
              type="number"
              min="10"
              max="500"
              value={options.limit}
              onChange={(e) => setOptions(prev => ({ ...prev, limit: Number(e.target.value) }))}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                fontSize: '0.85rem',
                width: '90px'
              }}
            />
          </div>
        </div>

        <button
          onClick={onExecuteQuery}
          disabled={isLoading}
          className="btn-primary"
          style={{ padding: '12px 28px', fontSize: '1rem' }}
        >
          <Play size={18} fill="#ffffff" />
          <span>{isLoading ? 'Executing Request Lifecycle...' : 'Dispatch Request & Trace'}</span>
        </button>
      </div>
    </div>
  );
}
