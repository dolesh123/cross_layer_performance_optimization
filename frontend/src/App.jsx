// frontend/src/App.jsx
// Main IMPOF Observability Platform & Research Dashboard

import React, { useState, useEffect } from 'react';
import AppHeader from './components/AppHeader';
import OverviewView from './components/OverviewView';
import AppDetailsView from './components/AppDetailsView';
import BottlenecksView from './components/BottlenecksView';
import AnomaliesView from './components/AnomaliesView';
import ExperimentsView from './components/ExperimentsView';
import LoadTestView from './components/LoadTestView';
import RegisterAppModal from './components/RegisterAppModal';
import ProjectReportModal from './components/ProjectReportModal';

export default function App() {
  const [activeView, setActiveView] = useState('details');
  const [applications, setApplications] = useState([
    {
      id: 'APP-001',
      name: 'Movie Recommendation System',
      environment: 'production',
      url: 'http://localhost:4000',
      technology: 'Node.js / Express + PostgreSQL + Redis',
      description: 'Distributed content-based movie discovery and streaming API with 50,000 titles.'
    },
    {
      id: 'APP-002',
      name: 'E-Commerce Checkout & Payment Gateway',
      environment: 'staging',
      url: 'http://localhost:4002',
      technology: 'Spring Boot + MySQL + Kafka',
      description: 'High-throughput transactional billing microservice.'
    }
  ]);
  const [selectedAppId, setSelectedAppId] = useState('APP-001');
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [bottlenecks, setBottlenecks] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  useEffect(() => {
    fetchApplications();
  }, []);

  useEffect(() => {
    fetchAppTelemetry(selectedAppId);
    const interval = setInterval(() => {
      fetchAppTelemetry(selectedAppId);
    }, 4000);
    return () => clearInterval(interval);
  }, [selectedAppId]);

  const fetchApplications = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/applications');
      if (res.ok) {
        const data = await res.json();
        if (data.length > 0) setApplications(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchAppTelemetry = async (appId) => {
    try {
      // 1. Fetch Metrics History
      const mRes = await fetch(`http://localhost:5000/api/applications/${appId}/metrics`);
      if (mRes.ok) {
        const mData = await mRes.json();
        setMetricsHistory(mData);
      }

      // 2. Fetch Bottlenecks
      const bRes = await fetch(`http://localhost:5000/api/applications/${appId}/bottlenecks`);
      if (bRes.ok) {
        const bData = await bRes.json();
        setBottlenecks(bData);
      }

      // 3. Fetch Recommendations
      const rRes = await fetch(`http://localhost:5000/api/applications/${appId}/recommendations`);
      if (rRes.ok) {
        const rData = await rRes.json();
        setRecommendations(rData);
      }

      // 4. Fetch ML Anomalies
      const aRes = await fetch(`http://localhost:5000/api/applications/${appId}/anomalies`);
      if (aRes.ok) {
        const aData = await aRes.json();
        setAnomalies(aData);
      }
    } catch (e) {
      console.error('Telemetry fetch error:', e);
    }
  };

  const selectedApp = applications.find(a => a.id === selectedAppId) || applications[0];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Platform Header */}
      <AppHeader
        activeView={activeView}
        setActiveView={setActiveView}
        applications={applications}
        selectedAppId={selectedAppId}
        setSelectedAppId={setSelectedAppId}
        onOpenRegisterModal={() => setIsRegisterModalOpen(true)}
        onOpenReportModal={() => setIsReportModalOpen(true)}
        onRefresh={() => fetchAppTelemetry(selectedAppId)}
      />

      {/* Main Content Area */}
      <main style={{ maxWidth: '1540px', margin: '0 auto', padding: '28px', width: '100%', flex: 1 }}>
        {activeView === 'overview' && (
          <OverviewView
            applications={applications}
            onSelectApp={(id) => {
              setSelectedAppId(id);
              setActiveView('details');
            }}
          />
        )}

        {activeView === 'details' && (
          <AppDetailsView
            app={selectedApp}
            metricsHistory={metricsHistory}
            onRefresh={() => fetchAppTelemetry(selectedAppId)}
          />
        )}

        {activeView === 'bottlenecks' && (
          <BottlenecksView
            bottlenecks={bottlenecks}
            recommendations={recommendations}
          />
        )}

        {activeView === 'anomalies' && (
          <AnomaliesView
            anomalies={anomalies}
          />
        )}

        {activeView === 'experiments' && (
          <ExperimentsView
            app={selectedApp}
            onRefresh={() => fetchAppTelemetry(selectedAppId)}
          />
        )}

        {activeView === 'loadtest' && (
          <LoadTestView
            app={selectedApp}
          />
        )}
      </main>

      {/* Register App Modal */}
      <RegisterAppModal
        isOpen={isRegisterModalOpen}
        onClose={() => setIsRegisterModalOpen(false)}
        onAppCreated={(newApp) => {
          setApplications(prev => [...prev, newApp]);
          setSelectedAppId(newApp.id);
          setActiveView('details');
        }}
      />

      {/* Academic Project Report Modal */}
      <ProjectReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        currentResult={{ trace: { totalDurationMs: metricsHistory[0]?.backend?.avgLatencyMs || 120 } }}
        systemStats={{ database: { totalProducts: 50000 } }}
      />

      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        padding: '20px',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: '0.8rem',
        color: 'var(--text-muted)'
      }}>
        IMPOF • Integrated Multi-Layer Performance Monitoring, Bottleneck Detection & Optimization Framework
      </footer>
    </div>
  );
}
