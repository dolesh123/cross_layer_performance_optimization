// backend/src/telemetry/bottleneckClassifier.js
// Automated Bottleneck Identification & Optimization Gain Analysis Engine

class BottleneckClassifier {
  analyze(traceRecord, activeOptions = {}) {
    const { layers, totalDurationMs, spans } = traceRecord;
    const { frontendMs, networkMs, backendMs, databaseMs } = layers;

    const layerBreakdown = [
      { layer: 'Database', durationMs: databaseMs, ratio: databaseMs / totalDurationMs },
      { layer: 'Backend', durationMs: backendMs, ratio: backendMs / totalDurationMs },
      { layer: 'Network', durationMs: networkMs, ratio: networkMs / totalDurationMs },
      { layer: 'Frontend', durationMs: frontendMs, ratio: frontendMs / totalDurationMs }
    ].sort((a, b) => b.durationMs - a.durationMs);

    const primary = layerBreakdown[0];
    const secondary = layerBreakdown[1];

    const detectedIssues = [];
    const recommendations = [];

    // 1. Database Layer Analysis
    if (primary.layer === 'Database' || primary.ratio > 0.35) {
      if (!activeOptions.enableDbIndex) {
        detectedIssues.push({
          layer: 'Database',
          severity: 'CRITICAL',
          title: 'Full Table Scan on 100k Records',
          description: `Linear search O(N) took ${databaseMs.toFixed(1)}ms (${(primary.ratio * 100).toFixed(0)}% of total request time) due to missing B-Tree indexes.`
        });
        recommendations.push('Create B-Tree Composite Index on (category, inStock, price) to reduce scan cost from O(N) to O(log N).');
      }

      if (!activeOptions.enableDbPool) {
        detectedIssues.push({
          layer: 'Database',
          severity: 'HIGH',
          title: 'Unpooled Database Connection Overhead',
          description: 'Each request creates and tears down a raw database connection, adding 15-30ms TCP/TLS handshake latency.'
        });
        recommendations.push('Enable HikariCP high-performance connection pool with pre-warmed connections.');
      }

      if (activeOptions.queryType === 'orders' && !activeOptions.enableDbJoin) {
        detectedIssues.push({
          layer: 'Database',
          severity: 'CRITICAL',
          title: 'N+1 Query Relational Anti-Pattern',
          description: 'Executing sequential queries for parent and each child record causes severe I/O contention.'
        });
        recommendations.push('Refactor relational queries into a single batched indexed JOIN.');
      }
    }

    // 2. Backend / Application Layer Analysis
    if (primary.layer === 'Backend' || primary.ratio > 0.30) {
      if (!activeOptions.enableL1Cache && !activeOptions.enableL2Cache) {
        detectedIssues.push({
          layer: 'Backend',
          severity: 'HIGH',
          title: 'Repeated Computation & Cache Misses',
          description: `Backend execution took ${backendMs.toFixed(1)}ms computing results that could be served from an in-memory cache.`
        });
        recommendations.push('Implement two-tier caching: L1 In-Memory (Caffeine-style LRU) + L2 Distributed (Redis-style TTL).');
      }

      if (!activeOptions.enableAsyncExec) {
        detectedIssues.push({
          layer: 'Backend',
          severity: 'MEDIUM',
          title: 'Synchronous Blocking Thread Contention',
          description: 'Blocking main thread during heavy data serialization degrades throughput under concurrent load.'
        });
        recommendations.push('Delegate compute-heavy logic to asynchronous worker threads / non-blocking executors.');
      }
    }

    // 3. Network & Transport Layer Analysis
    if (primary.layer === 'Network' || networkMs > 100) {
      if (!activeOptions.enableCompression) {
        detectedIssues.push({
          layer: 'Network',
          severity: 'HIGH',
          title: 'Uncompressed High-Volume Payloads',
          description: 'Sending raw uncompressed JSON increases byte payload and network transmission time.'
        });
        recommendations.push('Apply Brotli / Gzip response compression (saving up to 85% bandwidth).');
      }

      if (!activeOptions.enableCdnEdge) {
        detectedIssues.push({
          layer: 'Network',
          severity: 'MEDIUM',
          title: 'Direct Origin Round-Trip Latency',
          description: `All requests traverse full internet route (${networkMs.toFixed(1)}ms) without edge CDN caching.`
        });
        recommendations.push('Serve cacheable static and read-only API responses from Edge CDN nodes.');
      }
    }

    // 4. Frontend Layer Analysis
    if (primary.layer === 'Frontend' || frontendMs > 50) {
      if (!activeOptions.enableVirtualization) {
        detectedIssues.push({
          layer: 'Frontend',
          severity: 'HIGH',
          title: 'Un-virtualized Massive DOM Insertion',
          description: `Rendering thousands of raw DOM nodes caused ${frontendMs.toFixed(1)}ms main thread jank and frame drops.`
        });
        recommendations.push('Adopt DOM Virtualization (react-window) to render only elements currently visible in viewport.');
      }
    }

    // Optimization Gain Index (OGI) comparison against estimated unoptimized baseline (~350ms)
    const baselineEstimateMs = 380;
    const ogiPercent = Math.max(0, Math.round(((baselineEstimateMs - totalDurationMs) / baselineEstimateMs) * 10000) / 100);

    return {
      totalLatencyMs: totalDurationMs,
      primaryBottleneck: {
        layer: primary.layer,
        percentage: Math.round(primary.ratio * 100),
        durationMs: primary.durationMs
      },
      secondaryBottleneck: {
        layer: secondary.layer,
        percentage: Math.round(secondary.ratio * 100),
        durationMs: secondary.durationMs
      },
      detectedIssues: detectedIssues.length > 0 ? detectedIssues : [
        {
          layer: 'System',
          severity: 'OPTIMAL',
          title: 'Fully Optimized Cross-Layer Pipeline',
          description: 'All layers are operating with active index scanning, pooled connections, multi-tier caching, compression, and virtualized rendering.'
        }
      ],
      recommendations: recommendations.length > 0 ? recommendations : ['System is operating at peak efficiency across all 4 architectural layers.'],
      optimizationGainIndex: ogiPercent
    };
  }
}

module.exports = new BottleneckClassifier();
