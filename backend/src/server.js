// backend/src/server.js
// Main Application Server with Compression, CORS & Routing

const express = require('express');
const cors = require('cors');
const compression = require('compression');
const apiRoutes = require('./routes/apiRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// Enable Cross-Origin Resource Sharing
app.use(cors());

// Compression Middleware (Brotli/Gzip)
app.use(compression({
  filter: (req, res) => {
    // Only compress if client requests it or if enabled
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res);
  },
  threshold: 1024 // compress payloads larger than 1KB
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Trace context interceptor
app.use((req, res, next) => {
  res.setHeader('X-Framework', 'IMPOF-v1.0');
  res.setHeader('X-Powered-By', 'Integrated-Multi-Layer-Framework');
  next();
});

// Mount Routes
app.use('/api', apiRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({
    framework: 'Integrated Multi-Layer Performance Optimization Framework (IMPOF)',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      query: '/api/query',
      comparativeBenchmark: '/api/benchmark/comparative',
      stressTest: '/api/benchmark/stress-test',
      traces: '/api/traces/recent',
      systemStats: '/api/system/stats'
    }
  });
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 IMPOF Multi-Layer Backend Engine Running on port ${PORT}`);
  console.log(`🌐 Base URL: http://localhost:${PORT}`);
  console.log(`📊 Health Endpoint: http://localhost:${PORT}/api/health`);
  console.log(`=======================================================`);
});
