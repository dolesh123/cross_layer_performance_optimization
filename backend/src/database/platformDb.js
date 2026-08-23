// backend/src/database/platformDb.js
// Production-grade Multi-Tenant Observability & Application Registry Store

const bcrypt = require('bcryptjs');
const crypto = require('crypto');

class PlatformDatabase {
  constructor() {
    this.users = new Map();
    this.applications = new Map();
    this.metricsStore = new Map(); // appId -> array of time-series metric snapshots
    this.bottlenecksStore = new Map(); // appId -> array of detected bottlenecks
    this.recommendationsStore = new Map(); // appId -> array of recommendations
    this.anomaliesStore = new Map(); // appId -> array of anomaly events
    this.experimentsStore = new Map(); // experimentId -> experiment object
    this.loadTestsStore = new Map(); // loadTestId -> load test result object
    this.auditLogs = [];

    this.initDefaults();
  }

  initDefaults() {
    // 1. Seed Default Users
    const salt = bcrypt.genSaltSync(10);
    const adminHash = bcrypt.hashSync('admin123', salt);
    const devHash = bcrypt.hashSync('dev123', salt);

    this.users.set('USR-001', {
      id: 'USR-001',
      name: 'Dr. Ravi (Lead DevOps)',
      email: 'admin@impof.io',
      passwordHash: adminHash,
      role: 'ADMIN',
      createdAt: new Date().toISOString()
    });

    this.users.set('USR-002', {
      id: 'USR-002',
      name: 'Engineering Team',
      email: 'developer@impof.io',
      passwordHash: devHash,
      role: 'DEVELOPER',
      createdAt: new Date().toISOString()
    });

    // 2. Seed Default Registered Applications
    this.registerApplication({
      appId: 'APP-001',
      name: 'Movie Recommendation System',
      environment: 'production',
      url: 'http://localhost:4000',
      technology: 'Node.js / Express + PostgreSQL + Redis',
      status: 'ACTIVE',
      description: 'Distributed content-based movie discovery and streaming API with 50,000 titles.'
    });

    this.registerApplication({
      appId: 'APP-002',
      name: 'E-Commerce Checkout & Payment Gateway',
      environment: 'staging',
      url: 'http://localhost:4002',
      technology: 'Spring Boot + MySQL + Kafka',
      status: 'ACTIVE',
      description: 'High-throughput transactional billing microservice.'
    });

    this.logAudit('USR-001', 'SYSTEM_INITIALIZATION', 'Default multi-tenant applications and security roles seeded.');
  }

  // --- User Management & Auth ---
  findUserByEmail(email) {
    for (const user of this.users.values()) {
      if (user.email.toLowerCase() === email.toLowerCase()) return user;
    }
    return null;
  }

  findUserById(id) {
    return this.users.get(id) || null;
  }

  createUser({ name, email, password, role = 'DEVELOPER' }) {
    if (this.findUserByEmail(email)) {
      throw new Error('A user with this email address already exists.');
    }
    const id = `USR-${crypto.randomBytes(3).toString('hex').toUpperCase()}`;
    const salt = bcrypt.genSaltSync(10);
    const passwordHash = bcrypt.hashSync(password, salt);

    const user = {
      id,
      name,
      email,
      passwordHash,
      role,
      createdAt: new Date().toISOString()
    };
    this.users.set(id, user);
    this.logAudit(id, 'USER_REGISTERED', `User ${email} created with role ${role}`);
    return { id, name, email, role, createdAt: user.createdAt };
  }

  // --- Application Registry ---
  registerApplication({ appId, name, environment = 'production', url, technology, description }) {
    const id = appId || `APP-${(this.applications.size + 1).toString().padStart(3, '0')}`;
    if (this.applications.has(id)) {
      // update
      const existing = this.applications.get(id);
      const updated = { ...existing, name, environment, url, technology, description, updatedAt: new Date().toISOString() };
      this.applications.set(id, updated);
      return updated;
    }

    const newApp = {
      id,
      name,
      environment,
      url,
      technology,
      status: 'ACTIVE',
      apiKey: `impof_live_${crypto.randomBytes(12).toString('hex')}`,
      description: description || '',
      createdAt: new Date().toISOString()
    };
    this.applications.set(id, newApp);
    this.metricsStore.set(id, []);
    this.bottlenecksStore.set(id, []);
    this.recommendationsStore.set(id, []);
    this.anomaliesStore.set(id, []);

    this.logAudit('SYSTEM', 'APP_REGISTERED', `Application ${name} (${id}) registered under ${environment} environment.`);
    return newApp;
  }

  getAllApplications() {
    return Array.from(this.applications.values());
  }

  getApplicationById(id) {
    return this.applications.get(id) || null;
  }

  deleteApplication(id) {
    if (this.applications.has(id)) {
      this.applications.delete(id);
      this.metricsStore.delete(id);
      this.bottlenecksStore.delete(id);
      this.recommendationsStore.delete(id);
      this.anomaliesStore.delete(id);
      return true;
    }
    return false;
  }

  // --- Metrics Ingestion & History ---
  ingestMetrics(appId, metricsPayload) {
    if (!this.applications.has(appId)) {
      throw new Error(`Application ${appId} is not registered.`);
    }

    const snapshot = {
      id: `SNAP-${crypto.randomBytes(4).toString('hex')}`,
      appId,
      timestamp: new Date().toISOString(),
      ...metricsPayload
    };

    const history = this.metricsStore.get(appId) || [];
    history.unshift(snapshot);
    if (history.length > 200) history.pop();
    this.metricsStore.set(appId, history);
    return snapshot;
  }

  getMetricsHistory(appId, limit = 50) {
    const list = this.metricsStore.get(appId) || [];
    return list.slice(0, limit);
  }

  // --- Bottlenecks & Anomalies ---
  saveBottleneckAnalysis(appId, bottleneckData) {
    this.bottlenecksStore.set(appId, bottleneckData);
  }

  getBottlenecks(appId) {
    return this.bottlenecksStore.get(appId) || null;
  }

  saveAnomalies(appId, anomaliesList) {
    const existing = this.anomaliesStore.get(appId) || [];
    const merged = [...anomaliesList, ...existing].slice(0, 50);
    this.anomaliesStore.set(appId, merged);
  }

  getAnomalies(appId) {
    return this.anomaliesStore.get(appId) || [];
  }

  saveRecommendations(appId, recommendationsList) {
    this.recommendationsStore.set(appId, recommendationsList);
  }

  getRecommendations(appId) {
    return this.recommendationsStore.get(appId) || [];
  }

  // --- Optimization Experiments ---
  createExperiment({ appId, name, targetLayer, description, baselineMetrics }) {
    const id = `EXP-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
    const experiment = {
      id,
      appId,
      name,
      targetLayer,
      description,
      status: 'IN_PROGRESS', // 'IN_PROGRESS' | 'COMPLETED'
      baselineMetrics,
      optimizedMetrics: null,
      improvementGains: null,
      createdAt: new Date().toISOString()
    };
    this.experimentsStore.set(id, experiment);
    this.logAudit('USER', 'EXPERIMENT_CREATED', `Optimization experiment ${name} (${id}) started for ${appId}`);
    return experiment;
  }

  finalizeExperiment(id, optimizedMetrics) {
    const exp = this.experimentsStore.get(id);
    if (!exp) throw new Error('Experiment not found');

    const base = exp.baselineMetrics;
    const opt = optimizedMetrics;

    const latencyGain = base.apiLatencyMs > 0 
      ? Math.round(((base.apiLatencyMs - opt.apiLatencyMs) / base.apiLatencyMs) * 10000) / 100 
      : 0;

    const dbLatencyGain = base.dbLatencyMs > 0 
      ? Math.round(((base.dbLatencyMs - opt.dbLatencyMs) / base.dbLatencyMs) * 10000) / 100 
      : 0;

    const throughputGain = base.throughputRps > 0 
      ? Math.round(((opt.throughputRps - base.throughputRps) / base.throughputRps) * 10000) / 100 
      : 0;

    const cpuGain = base.cpuPercent > 0 
      ? Math.round(((base.cpuPercent - opt.cpuPercent) / base.cpuPercent) * 10000) / 100 
      : 0;

    exp.optimizedMetrics = opt;
    exp.status = 'COMPLETED';
    exp.completedAt = new Date().toISOString();
    exp.improvementGains = {
      overallLatencyReductionPercent: latencyGain,
      databaseLatencyReductionPercent: dbLatencyGain,
      throughputImprovementPercent: throughputGain,
      cpuUtilizationReductionPercent: cpuGain
    };

    this.experimentsStore.set(id, exp);
    this.logAudit('USER', 'EXPERIMENT_FINALIZED', `Experiment ${exp.name} completed with ${latencyGain}% latency gain.`);
    return exp;
  }

  getExperiments(appId = null) {
    const list = Array.from(this.experimentsStore.values());
    if (appId) return list.filter(e => e.appId === appId);
    return list;
  }

  // --- Load Tests ---
  saveLoadTestResult(result) {
    const id = `LT-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
    const entry = { id, timestamp: new Date().toISOString(), ...result };
    this.loadTestsStore.set(id, entry);
    return entry;
  }

  getLoadTests(appId = null) {
    const list = Array.from(this.loadTestsStore.values());
    if (appId) return list.filter(l => l.appId === appId);
    return list;
  }

  // --- Audit Logs ---
  logAudit(userId, action, details) {
    this.auditLogs.unshift({
      id: `AUD-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      userId,
      action,
      details,
      timestamp: new Date().toISOString()
    });
    if (this.auditLogs.length > 200) this.auditLogs.pop();
  }

  getAuditLogs(limit = 50) {
    return this.auditLogs.slice(0, limit);
  }
}

module.exports = new PlatformDatabase();
