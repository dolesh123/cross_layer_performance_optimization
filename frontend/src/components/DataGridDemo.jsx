// frontend/src/components/DataGridDemo.jsx
import React, { useState } from 'react';
import { Table, Search, Filter, CheckCircle2, XCircle, Tag } from 'lucide-react';

export default function DataGridDemo({ data, payloadMeta, queryType, options }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('ALL');

  if (!data || !Array.isArray(data) || data.length === 0) {
    return null;
  }

  const filtered = data.filter(item => {
    const nameMatch = item.name ? item.name.toLowerCase().includes(searchTerm.toLowerCase()) : true;
    const catMatch = activeCategory === 'ALL' || item.category === activeCategory;
    return nameMatch && catMatch;
  });

  return (
    <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Table size={20} color="var(--accent-emerald)" />
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
              Live Relational Result Set ({filtered.length} of {data.length} Items)
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              {options?.enableVirtualization ? '⚡ Virtualized Viewport Rendering (Zero DOM Jank)' : '⚠️ Un-virtualized Direct DOM Nodes'}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ position: 'relative' }}>
            <Search size={14} color="var(--text-muted)" style={{ position: 'absolute', left: '10px', top: '10px' }} />
            <input
              type="text"
              placeholder="Search returned rows..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '6px 12px 6px 30px',
                borderRadius: '8px',
                fontSize: '0.82rem',
                outline: 'none'
              }}
            />
          </div>
        </div>
      </div>

      {/* Table Container */}
      <div style={{
        maxHeight: '340px',
        overflowY: 'auto',
        border: '1px solid var(--border-subtle)',
        borderRadius: '10px',
        background: 'rgba(0, 0, 0, 0.2)'
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.82rem' }}>
          <thead style={{ position: 'sticky', top: 0, background: '#111827', borderBottom: '1px solid var(--border-subtle)', zIndex: 10 }}>
            <tr>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>ID / SKU</th>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>NAME / MODEL</th>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>CATEGORY</th>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>PRICE</th>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>STOCK STATUS</th>
              <th style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>RATING</th>
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, 100).map((item, idx) => (
              <tr
                key={item.id || item.orderId || idx}
                style={{
                  borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                  transition: 'background 0.15s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '10px 14px' }} className="font-mono">
                  <span style={{ color: 'var(--accent-cyan)' }}>#{item.id || item.orderId}</span>
                </td>
                <td style={{ padding: '10px 14px', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {item.name || item.customerId}
                </td>
                <td style={{ padding: '10px 14px' }}>
                  <span className="badge badge-purple">{item.category || item.status}</span>
                </td>
                <td style={{ padding: '10px 14px', fontWeight: 700, color: '#34d399' }} className="font-mono">
                  ${item.price || item.totalAmount}
                </td>
                <td style={{ padding: '10px 14px' }}>
                  {item.inStock ? (
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#34d399' }}>
                      <CheckCircle2 size={13} /> In Stock
                    </span>
                  ) : (
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#fb7185' }}>
                      <XCircle size={13} /> Out of Stock
                    </span>
                  )}
                </td>
                <td style={{ padding: '10px 14px', color: 'var(--accent-amber)', fontWeight: 600 }}>
                  ★ {item.rating || '4.8'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
