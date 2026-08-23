// backend/src/services/loadTestEngine.js
// Concurrent Load Generator & Stress Testing Benchmark Engine

const serviceManager = require('./serviceManager');

class LoadTestEngine {
  constructor() {
    this.isRunning = false;
  }

  async runStressTest({
    virtualUsers = 50,
    totalRequests = 200,
    options = {}
  }) {
    if (this.isRunning) {
      throw new Error('A stress test is already actively executing.');
    }

    this.isRunning = true;
    const startTime = Date.now();
    const latencies = [];
    let completedRequests = 0;
    let failedRequests = 0;

    const categories = ['Electronics', 'Computing', 'Mobile', 'Audio', 'Gaming'];

    // Worker pool for concurrency simulation
    const runWorker = async () => {
      while (completedRequests + failedRequests < totalRequests) {
        const reqIdx = ++completedRequests;
        if (reqIdx > totalRequests) break;

        const category = categories[reqIdx % categories.length];
        const t0 = Date.now();

        try {
          await serviceManager.executeQuery({
            ...options,
            category,
            limit: 20
          });
          const dur = Date.now() - t0;
          latencies.push(dur);
        } catch (err) {
          failedRequests++;
        }
      }
    };

    const workers = [];
    const concurrency = Math.min(virtualUsers, totalRequests);
    for (let i = 0; i < concurrency; i++) {
      workers.push(runWorker());
    }

    await Promise.all(workers);
    this.isRunning = false;

    const totalTimeSec = (Date.now() - startTime) / 1000;
    latencies.sort((a, b) => a - b);

    const sum = latencies.reduce((acc, v) => acc + v, 0);
    const meanLatencyMs = latencies.length > 0 ? Math.round((sum / latencies.length) * 10) / 10 : 0;
    const throughputRps = totalTimeSec > 0 ? Math.round((latencies.length / totalTimeSec) * 10) / 10 : 0;

    const p50 = latencies[Math.floor(latencies.length * 0.50)] || 0;
    const p90 = latencies[Math.floor(latencies.length * 0.90)] || 0;
    const p95 = latencies[Math.floor(latencies.length * 0.95)] || 0;
    const p99 = latencies[Math.floor(latencies.length * 0.99)] || 0;

    return {
      virtualUsers,
      totalRequests,
      completedRequests: latencies.length,
      failedRequests,
      totalDurationSec: Math.round(totalTimeSec * 100) / 100,
      throughputRps,
      latencyMetrics: {
        meanMs: meanLatencyMs,
        p50Ms: p50,
        p90Ms: p90,
        p95Ms: p95,
        p99Ms: p99,
        minMs: latencies[0] || 0,
        maxMs: latencies[latencies.length - 1] || 0
      }
    };
  }
}

module.exports = new LoadTestEngine();
