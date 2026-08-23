// demo-app/backend/src/server.js
// Standalone Monitored "Movie Recommendation System" API with Controllable Flaws

const express = require('express');
const cors = require('cors');
const movieDb = require('./database/movieDb');
const { register, recordRequest, recordDbQuery, recordCache, startPeriodicIngestReporter } = require('./metrics/prometheusExporter');

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

// In-Memory Simulated Redis Cache for Movies
const redisSimCache = new Map();

// Controllable Flaw Switches for Controlled Evaluation & Demos
const flawSwitches = {
  slowDbQuery: true,         // Default: Starts with slow full table scan for demo detection
  cpuLoad: false,            // Artificial heavy compute in recommendation engine
  disableIndex: true,        // Disables B-tree index on genre/rating
  disableCache: false,       // Bypasses in-memory cache
  artificialDelay: false     // Adds network/service congestion
};

// 1. Prometheus Metrics Endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// 2. Health & Identification
app.get('/api/health', (req, res) => {
  res.json({
    appId: 'APP-001',
    appName: 'Movie Recommendation System',
    status: 'HEALTHY',
    flaws: flawSwitches,
    totalMovies: 50000
  });
});

// 3. Movies Catalog API
app.get('/api/movies', async (req, res) => {
  const t0 = process.hrtime.bigint();
  const { genre = 'Sci-Fi', minRating = 7.0, limit = 20 } = req.query;

  // Artificial delay if enabled
  if (flawSwitches.artificialDelay) {
    await new Promise(r => setTimeout(r, 150));
  }

  // Cache Lookup
  const cacheKey = `movies_${genre}_${minRating}_${limit}`;
  if (!flawSwitches.disableCache && redisSimCache.has(cacheKey)) {
    recordCache(true);
    const cached = redisSimCache.get(cacheKey);
    const t1 = process.hrtime.bigint();
    recordRequest('GET', '/api/movies', 200, Number(t1 - t0) / 1e9);
    return res.json({ source: 'REDIS_CACHE', ...cached });
  }

  recordCache(false);

  // Database Execution (Fast Index vs Slow Full Scan based on switches)
  let dbResult;
  if (flawSwitches.slowDbQuery || flawSwitches.disableIndex) {
    dbResult = movieDb.findMoviesSlowScan({ genre, minRating: Number(minRating), limit: Number(limit) });
    recordDbQuery('FULL_TABLE_SCAN', dbResult.meta.durationMs);
  } else {
    dbResult = movieDb.findMoviesIndexed({ genre, minRating: Number(minRating), limit: Number(limit) });
    recordDbQuery('INDEX_SCAN', dbResult.meta.durationMs);
  }

  const responsePayload = {
    source: 'DATABASE_POSTGRES',
    genre,
    count: dbResult.results.length,
    movies: dbResult.results,
    dbMeta: dbResult.meta
  };

  // Populate cache
  if (!flawSwitches.disableCache) {
    redisSimCache.set(cacheKey, responsePayload);
  }

  const t1 = process.hrtime.bigint();
  recordRequest('GET', '/api/movies', 200, Number(t1 - t0) / 1e9);
  res.json(responsePayload);
});

// 4. Content-Based Recommendation API
app.get('/api/recommendations', async (req, res) => {
  const t0 = process.hrtime.bigint();
  const { genre = 'Action', count = 10 } = req.query;

  // Heavy CPU load simulation if enabled
  if (flawSwitches.cpuLoad) {
    let fib = 0;
    for (let i = 0; i < 400000; i++) {
      fib += Math.sin(i) * Math.cos(i);
    }
  }

  const dbResult = flawSwitches.slowDbQuery 
    ? movieDb.findMoviesSlowScan({ genre, minRating: 7.5, limit: Number(count) })
    : movieDb.findMoviesIndexed({ genre, minRating: 7.5, limit: Number(count) });

  recordDbQuery('RECOMMENDATION_QUERY', dbResult.meta.durationMs);

  const t1 = process.hrtime.bigint();
  recordRequest('GET', '/api/recommendations', 200, Number(t1 - t0) / 1e9);

  res.json({
    recommendationEngine: 'Collaborative-Filtering-v2',
    genre,
    recommendations: dbResult.results,
    cpuHeavyExecuted: flawSwitches.cpuLoad,
    dbMeta: dbResult.meta
  });
});

// 5. Flaw Switch Controls (For Testing & Before/After Experimentation)
app.get('/api/control/status', (req, res) => {
  res.json({
    appId: 'APP-001',
    flaws: flawSwitches,
    cacheEntries: redisSimCache.size
  });
});

app.post('/api/control/toggle-flaw', (req, res) => {
  const { flawName, enabled } = req.body;
  if (flawSwitches.hasOwnProperty(flawName)) {
    flawSwitches[flawName] = Boolean(enabled);
    if (flawName === 'disableCache' && enabled) redisSimCache.clear();
    return res.json({ message: `Flaw switch '${flawName}' updated to ${enabled}`, flaws: flawSwitches });
  }
  res.status(400).json({ error: `Unknown flaw switch '${flawName}'` });
});

// Optimization Action: Create B-Tree Index / Optimize Query
app.post('/api/control/optimize-database-index', (req, res) => {
  flawSwitches.slowDbQuery = false;
  flawSwitches.disableIndex = false;
  res.json({
    message: 'Database optimization applied: B-Tree Index created on (genre, rating) and query planner updated.',
    flaws: flawSwitches
  });
});

// Optimization Action: Enable Redis Caching
app.post('/api/control/enable-cache', (req, res) => {
  flawSwitches.disableCache = false;
  res.json({
    message: 'Cache optimization applied: Redis L2 caching enabled with 300s TTL.',
    flaws: flawSwitches
  });
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🎬 Monitored Demo App (Movie System) running on port ${PORT}`);
  console.log(`📊 Prometheus Metrics: http://localhost:${PORT}/metrics`);
  console.log(`🎬 Movies API: http://localhost:${PORT}/api/movies`);
  console.log(`=======================================================`);

  // Start periodic telemetry reporting to platform backend (:5000)
  startPeriodicIngestReporter('APP-001', 4000);
});
