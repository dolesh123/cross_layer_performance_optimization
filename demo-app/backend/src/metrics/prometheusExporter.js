// demo-app/backend/src/metrics/prometheusExporter.js
// Prometheus Metrics Exporter & Automatic Platform Ingest Reporter

const client = require('prom-client');

// Initialize Prometheus Registry
const register = new client.Registry();
client.collectDefaultMetrics({ register, prefix: 'impof_demo_' });

// Custom Prometheus Metrics
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests processed',
  labelNames: ['method', 'route', 'status_code', 'service_id'],
  registers: [register]
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code', 'service_id'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [register]
});

const dbQueryDuration = new client.Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query execution duration in seconds',
  labelNames: ['query_type', 'table', 'status'],
  buckets: [0.001, 0.005, 0.02, 0.05, 0.1, 0.2, 0.5, 1],
  registers: [register]
});

const cacheHits = new client.Counter({
  name: 'cache_hits_total',
  help: 'Total Redis cache hits',
  labelNames: ['cache_name'],
  registers: [register]
});

const cacheMisses = new client.Counter({
  name: 'cache_misses_total',
  help: 'Total Redis cache misses',
  labelNames: ['cache_name'],
  registers: [register]
});

// Telemetry state aggregator
const state = {
  recentLatencies: [],
  recentDbLatencies: [],
  totalHits: 45,
  totalMisses: 15,
  errorCount: 0
};

function recordRequest(method, route, statusCode, durationSec) {
  httpRequestsTotal.inc({ method, route, status_code: statusCode, service_id: 'APP-001' });
  httpRequestDuration.observe({ method, route, status_code: statusCode, service_id: 'APP-001' }, durationSec);

  const durationMs = durationSec * 1000;
  state.recentLatencies.push(durationMs);
  if (state.recentLatencies.length > 50) state.recentLatencies.shift();
  if (statusCode >= 400) state.errorCount++;
}

function recordDbQuery(queryType, durationMs) {
  const durationSec = durationMs / 1000;
  dbQueryDuration.observe({ query_type: queryType, table: 'movies', status: 'SUCCESS' }, durationSec);
  state.recentDbLatencies.push(durationMs);
  if (state.recentDbLatencies.length > 50) state.recentDbLatencies.shift();
}

function recordCache(hit) {
  if (hit) {
    cacheHits.inc({ cache_name: 'redis_movies' });
    state.totalHits++;
  } else {
    cacheMisses.inc({ cache_name: 'redis_movies' });
    state.totalMisses++;
  }
}

// Background auto-reporter: Periodically pushes multi-layer metrics snapshot to Platform Backend (:5000)
function startPeriodicIngestReporter(appId = 'APP-001', intervalMs = 5000) {
  setInterval(async () => {
    try {
      const avgLatency = state.recentLatencies.length > 0 
        ? Math.round((state.recentLatencies.reduce((a, b) => a + b, 0) / state.recentLatencies.length) * 10) / 10 
        : 85;

      const avgDbLatency = state.recentDbLatencies.length > 0 
        ? Math.round((state.recentDbLatencies.reduce((a, b) => a + b, 0) / state.recentDbLatencies.length) * 10) / 10 
        : 25;

      const cacheTotal = state.totalHits + state.totalMisses;
      const hitRatio = cacheTotal > 0 ? Math.round((state.totalHits / cacheTotal) * 10000) / 100 : 70;

      const mem = process.memoryUsage();
      const cpuUsage = Math.min(95, Math.round((15 + (avgLatency > 200 ? 55 : 10) + Math.random() * 8) * 10) / 10);

      const snapshotPayload = {
        appId,
        backend: {
          requestCount: state.recentLatencies.length + 10,
          avgLatencyMs: avgLatency,
          p95LatencyMs: Math.round(avgLatency * 1.6 * 10) / 10,
          p99LatencyMs: Math.round(avgLatency * 2.2 * 10) / 10,
          errorRatePercent: state.errorCount > 0 ? 1.5 : 0.2
        },
        database: {
          engine: 'PostgreSQL 16',
          avgQueryLatencyMs: avgDbLatency,
          activeConnections: 12,
          slowQueriesCount: avgDbLatency > 100 ? 8 : 0,
          rowsScanned: avgDbLatency > 100 ? 50000 : 20
        },
        cache: {
          engine: 'Redis 7.2',
          hits: state.totalHits,
          misses: state.totalMisses,
          hitRatioPercent: hitRatio,
          memoryMb: 48
        },
        infrastructure: {
          cpuPercent: cpuUsage,
          memoryMb: Math.round(mem.heapUsed / 1024 / 1024),
          containerStatus: 'RUNNING',
          restarts: 0
        },
        frontend: {
          pageLoadTimeMs: Math.round((350 + avgLatency * 1.2) * 10) / 10,
          lcpSec: Math.round((0.5 + avgLatency / 500) * 100) / 100,
          fidMs: 16,
          cls: 0.02
        }
      };

      await fetch('http://localhost:5000/api/metrics/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(snapshotPayload)
      });
    } catch (err) {
      // Backend may be starting
    }
  }, intervalMs);
}

module.exports = {
  register,
  recordRequest,
  recordDbQuery,
  recordCache,
  startPeriodicIngestReporter
};
