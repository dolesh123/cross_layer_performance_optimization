// backend/src/routes/apiRoutes.js
// Complete REST API Specification for Observability Platform

const express = require('express');
const router = express.Router();

const platformController = require('../controllers/platformController');
const { verifyToken, requireRole } = require('../middleware/auth');

// Existing cross-layer simulation services
const dbEngine = require('../database/dbEngine');
const connectionPool = require('../database/connectionPool');
const l1Cache = require('../cache/l1Cache');
const l2Cache = require('../cache/l2Cache');
const tracer = require('../telemetry/tracer');
const serviceManager = require('../services/serviceManager');
const loadTestEngine = require('../services/loadTestEngine');

// 1. Authentication Endpoints
router.post('/auth/register', platformController.register);
router.post('/auth/login', platformController.login);
router.get('/auth/me', verifyToken, platformController.getCurrentUser);

// 2. Application Registration & Management
router.get('/applications', verifyToken, platformController.listApplications);
router.post('/applications', verifyToken, requireRole(['ADMIN', 'DEVELOPER']), platformController.createApplication);
router.get('/applications/:id', verifyToken, platformController.getApplication);
router.delete('/applications/:id', verifyToken, requireRole('ADMIN'), platformController.deleteApplication);

// 3. Multi-Layer Metrics & Ingestion
router.post('/metrics/ingest', platformController.ingestMetrics);
router.get('/applications/:id/metrics', verifyToken, platformController.getApplicationMetrics);
router.get('/applications/:id/performance', verifyToken, platformController.getApplicationMetrics);

// 4. Bottleneck Detection, Anomalies & Recommendations
router.get('/applications/:id/bottlenecks', verifyToken, platformController.getApplicationBottlenecks);
router.get('/applications/:id/recommendations', verifyToken, platformController.getApplicationRecommendations);
router.get('/applications/:id/anomalies', verifyToken, platformController.getApplicationAnomalies);

// 5. Optimization Experiments (Before vs After)
router.post('/applications/:id/experiments', verifyToken, platformController.createExperiment);
router.get('/applications/:id/experiments', verifyToken, platformController.listExperiments);
router.post('/experiments/:id/finalize', verifyToken, platformController.finalizeExperiment);

// 6. Controlled Load Testing
router.post('/load-tests', verifyToken, platformController.executeLoadTest);

// 7. Academic & Performance Reports
router.get('/reports/:applicationId', verifyToken, platformController.getApplicationReport);

// 8. Health and Framework Status
router.get('/health', (req, res) => {
  res.json({
    status: 'UP',
    framework: 'Integrated Multi-Layer Performance Monitoring, Bottleneck Detection and Optimization Framework',
    version: '2.0.0',
    timestamp: new Date().toISOString()
  });
});

// --- Backwards-Compatible Research Lab Endpoints ---
router.post('/query', async (req, res) => {
  try {
    const result = await serviceManager.executeQuery(req.body);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/benchmark/comparative', async (req, res) => {
  try {
    const report = await serviceManager.runComparativeBenchmark();
    res.json(report);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/benchmark/stress-test', async (req, res) => {
  try {
    const { virtualUsers = 50, totalRequests = 200, options = {} } = req.body;
    const result = await loadTestEngine.runStressTest({ virtualUsers, totalRequests, options });
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/traces/recent', (req, res) => {
  res.json(tracer.getRecentTraces(req.query.limit || 20));
});

router.get('/system/stats', (req, res) => {
  res.json({
    database: dbEngine.getStats(),
    connectionPool: connectionPool.getPoolStats(),
    l1Cache: l1Cache.getStats(),
    l2Cache: l2Cache.getStats(),
    memoryUsage: process.memoryUsage()
  });
});

router.post('/system/clear-cache', (req, res) => {
  l1Cache.clear();
  l2Cache.clear();
  res.json({ message: 'L1 and L2 caches cleared successfully.' });
});

module.exports = router;
