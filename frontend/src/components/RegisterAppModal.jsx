// frontend/src/components/RegisterAppModal.jsx
import React, { useState } from 'react';
import { X, Plus, Layers, Check } from 'lucide-react';

export default function RegisterAppModal({ isOpen, onClose, onAppCreated }) {
  const [name, setName] = useState('');
  const [environment, setEnvironment] = useState('production');
  const [url, setUrl] = useState('http://localhost:4000');
  const [technology, setTechnology] = useState('Node.js / Express + PostgreSQL');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const res = await fetch('http://localhost:5000/api/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, environment, url, technology, description })
      });
      const newApp = await res.json();
      onAppCreated(newApp);
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)',
      zIndex: 100,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '540px',
        background: '#0e1524',
        border: '1px solid var(--border-glow)',
        borderRadius: '18px',
        padding: '28px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={20} color="var(--accent-emerald)" />
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>Register New Monitored Application</h3>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
              APPLICATION NAME
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Payment Billing Service"
              value={name}
              onChange={(e) => setName(e.target.value)}
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

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
                ENVIRONMENT
              </label>
              <select
                value={environment}
                onChange={(e) => setEnvironment(e.target.value)}
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
                <option value="production">Production</option>
                <option value="staging">Staging</option>
                <option value="development">Development</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
                TECHNOLOGY STACK
              </label>
              <input
                type="text"
                placeholder="e.g. Node.js / PostgreSQL"
                value={technology}
                onChange={(e) => setTechnology(e.target.value)}
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
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
              TARGET BASE URL / HEALTH ENDPOINT
            </label>
            <input
              type="text"
              required
              placeholder="http://localhost:4000"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
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

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
              DESCRIPTION
            </label>
            <textarea
              rows={2}
              placeholder="Brief summary of service responsibilities..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                fontSize: '0.85rem',
                resize: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
            <button type="button" onClick={onClose} className="btn-secondary" style={{ padding: '8px 16px' }}>
              Cancel
            </button>
            <button type="submit" disabled={isSubmitting} className="btn-primary" style={{ padding: '8px 20px' }}>
              {isSubmitting ? 'Registering...' : 'Register Application'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
