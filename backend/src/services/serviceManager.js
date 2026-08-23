// backend/src/services/serviceManager.js
// Cross-Layer Request Orchestrator & Execution Pipeline

const dbEngine = require('../database/dbEngine');
const connectionPool = require('../database/connectionPool');
const l1Cache = require('../cache/l1Cache');
const l2Cache = require('../cache/l2Cache');
const tracer = require('../telemetry/tracer');
const bottleneckClassifier = require('../telemetry/bottleneckClassifier');

class ServiceManager {
  async executeQuery(options = {}) {
    const {
      clientTraceId = null,
      queryType = 'products', // 'products' | 'orders' | 'heavy'
      category = 'Electronics',
      minPrice = 0,
      maxPrice = 1500,
      inStockOnly = false,
      limit = 50,
      
      // Layer Toggles
      enableDbIndex = false,
      enableDbPool = false,
      enableDbJoin = false,
      enableL1Cache = false,
      enableL2Cache = false,
      enableAsyncExec = false,
      enableDtoProjection = false,
      enableCompression = false,
      enableCdnEdge = false,
      enableVirtualization = false,
      
      // Client telemetry simulation
      simulatedNetworkRttMs = null,
      simulatedClientRenderMs = null
    } = options;

    const trace = tracer.createTrace(clientTraceId);
    const cacheKey = `${queryType}_${category}_${minPrice}_${maxPrice}_${inStockOnly}_${limit}_${enableDtoProjection}`;

    // --- LAYER 2: Network & Transport Simulation ---
    let networkRtt = simulatedNetworkRttMs !== null 
      ? simulatedNetworkRttMs 
      : (enableCdnEdge ? 3 : 85 + Math.floor(Math.random() * 30));

    // --- LAYER 3: Backend Gateway & Caching ---
    const gwStart = process.hrtime.bigint();
    
    // Check L1 In-Memory Cache
    if (enableL1Cache) {
      const l1Result = l1Cache.get(cacheKey);
      if (l1Result) {
        const gwEnd = process.hrtime.bigint();
        trace.addSpan('Backend', 'L1 In-Memory Cache Hit (Caffeine-style)', Number(gwEnd - gwStart) / 1e6, {
          cacheLevel: 'L1_MEMORY',
          status: 'HIT'
        });

        const clientRenderMs = simulatedClientRenderMs || (enableVirtualization ? 4 : 45);
        const traceRecord = trace.finalize(clientRenderMs, networkRtt);
        tracer.recordTrace(traceRecord);
        const analysis = bottleneckClassifier.analyze(traceRecord, options);

        return {
          source: 'L1_CACHE',
          data: l1Result,
          trace: traceRecord,
          analysis,
          payloadMeta: {
            itemCount: l1Result.length,
            compressed: enableCompression,
            dtoProjected: enableDtoProjection
          }
        };
      }
    }

    // Check L2 Distributed Cache (Redis)
    if (enableL2Cache) {
      const l2Start = process.hrtime.bigint();
      const l2Result = await l2Cache.get(cacheKey);
      const l2End = process.hrtime.bigint();
      const l2DurationMs = Number(l2End - l2Start) / 1e6;

      if (l2Result) {
        trace.addSpan('Backend', 'L2 Distributed Cache Hit (Redis-style)', l2DurationMs, {
          cacheLevel: 'L2_REDIS',
          status: 'HIT'
        });

        // Populate L1 if enabled
        if (enableL1Cache) l1Cache.set(cacheKey, l2Result);

        const clientRenderMs = simulatedClientRenderMs || (enableVirtualization ? 4 : 45);
        const traceRecord = trace.finalize(clientRenderMs, networkRtt);
        tracer.recordTrace(traceRecord);
        const analysis = bottleneckClassifier.analyze(traceRecord, options);

        return {
          source: 'L2_CACHE',
          data: l2Result,
          trace: traceRecord,
          analysis,
          payloadMeta: {
            itemCount: l2Result.length,
            compressed: enableCompression,
            dtoProjected: enableDtoProjection
          }
        };
      } else {
        trace.addSpan('Backend', 'L2 Cache Miss (Redis-style)', l2DurationMs, { status: 'MISS' });
      }
    }

    // --- LAYER 3: Backend Processing (Async Worker vs Sync) ---
    const backendProcStart = process.hrtime.bigint();
    if (!enableAsyncExec) {
      // Synchronous thread blocking computation simulation
      let sum = 0;
      for (let i = 0; i < 250000; i++) {
        sum += (i * 3.1415) % 7;
      }
    } else {
      // Non-blocking async tick
      await new Promise(resolve => setImmediate(resolve));
    }
    const backendProcEnd = process.hrtime.bigint();
    trace.addSpan('Backend', enableAsyncExec ? 'Async Worker Thread Dispatch' : 'Sync Request Thread Processing', 
      Number(backendProcEnd - backendProcStart) / 1e6, {
        asyncExecution: enableAsyncExec
      });

    // --- LAYER 4: Database Connection Acquisition ---
    let dbConn = null;
    if (enableDbPool) {
      dbConn = await connectionPool.acquirePooledConnection();
      trace.addSpan('Database', 'HikariCP Pooled Connection Lease', dbConn.acquiredInMs, {
        pool: dbConn.poolStatus
      });
    } else {
      dbConn = await connectionPool.acquireUnpooledConnection();
      trace.addSpan('Database', 'Unpooled Raw TCP/TLS Handshake', dbConn.acquiredInMs, {
        overhead: 'Unpooled connection creation delay'
      });
    }

    // --- LAYER 4: Database Query Execution ---
    let dbResult = null;
    if (queryType === 'orders') {
      dbResult = dbEngine.queryOrdersWithProducts('CUST-00042', enableDbJoin);
      trace.addSpan('Database', enableDbJoin ? 'Batched Indexed JOIN Query' : 'N+1 Sequential Relational Queries', 
        dbResult.meta.executionTimeMs, dbResult.meta);
    } else {
      // Products query: Indexed vs Full Table Scan
      if (enableDbIndex) {
        dbResult = dbEngine.queryIndexed({ category, minPrice, maxPrice, inStockOnly, limit });
        trace.addSpan('Database', 'B-Tree Index Range Scan', dbResult.meta.executionTimeMs, dbResult.meta);
      } else {
        dbResult = dbEngine.queryUnindexed({ category, minPrice, maxPrice, inStockOnly, limit });
        trace.addSpan('Database', 'Full Table Scan (100,000 Records)', dbResult.meta.executionTimeMs, dbResult.meta);
      }
    }

    // Release database connection
    if (dbConn && dbConn.release) dbConn.release();

    // --- LAYER 3: DTO Projection / Serialization ---
    const serStart = process.hrtime.bigint();
    let finalPayload = dbResult.data;

    if (enableDtoProjection && queryType !== 'orders') {
      // Lean DTO projection: Only required UI columns
      finalPayload = dbResult.data.map(p => ({
        id: p.id,
        name: p.name,
        category: p.category,
        price: p.price,
        inStock: p.inStock,
        rating: p.rating
      }));
    }
    const serEnd = process.hrtime.bigint();
    trace.addSpan('Backend', enableDtoProjection ? 'Lean DTO Projection' : 'Heavy Entity Graph Serialization', 
      Number(serEnd - serStart) / 1e6, {
        dtoProjection: enableDtoProjection,
        rawEntities: !enableDtoProjection
      });

    // Populate Caches if enabled
    if (enableL1Cache) l1Cache.set(cacheKey, finalPayload);
    if (enableL2Cache) await l2Cache.set(cacheKey, finalPayload, 60);

    // --- LAYER 1: Frontend Render Simulation ---
    const clientRenderMs = simulatedClientRenderMs || (enableVirtualization ? 3 : 55);

    // Finalize Distributed Trace
    const traceRecord = trace.finalize(clientRenderMs, networkRtt);
    tracer.recordTrace(traceRecord);

    // Run Bottleneck Classification Analysis
    const analysis = bottleneckClassifier.analyze(traceRecord, options);

    return {
      source: 'DATABASE',
      data: finalPayload,
      queryMeta: dbResult.meta,
      trace: traceRecord,
      analysis,
      payloadMeta: {
        itemCount: finalPayload.length,
        compressed: enableCompression,
        dtoProjected: enableDtoProjection,
        rawByteSizeApprox: JSON.stringify(finalPayload).length
      }
    };
  }

  // Side-by-side Multi-Layer Comparison Benchmark
  async runComparativeBenchmark() {
    // 1. Fully Unoptimized Baseline
    const baseline = await this.executeQuery({
      enableDbIndex: false,
      enableDbPool: false,
      enableDbJoin: false,
      enableL1Cache: false,
      enableL2Cache: false,
      enableAsyncExec: false,
      enableDtoProjection: false,
      enableCompression: false,
      enableCdnEdge: false,
      enableVirtualization: false,
      queryType: 'products',
      limit: 100
    });

    // 2. Database Layer Only Optimized
    const dbOnly = await this.executeQuery({
      enableDbIndex: true,
      enableDbPool: true,
      enableDbJoin: true,
      enableL1Cache: false,
      enableL2Cache: false,
      enableAsyncExec: false,
      enableDtoProjection: false,
      enableCompression: false,
      enableCdnEdge: false,
      enableVirtualization: false,
      queryType: 'products',
      limit: 100
    });

    // 3. Backend & DB Optimized
    const backendAndDb = await this.executeQuery({
      enableDbIndex: true,
      enableDbPool: true,
      enableDbJoin: true,
      enableL1Cache: true,
      enableL2Cache: true,
      enableAsyncExec: true,
      enableDtoProjection: true,
      enableCompression: false,
      enableCdnEdge: false,
      enableVirtualization: false,
      queryType: 'products',
      limit: 100
    });

    // 4. Fully Optimized (All 4 Layers)
    const fullyOptimized = await this.executeQuery({
      enableDbIndex: true,
      enableDbPool: true,
      enableDbJoin: true,
      enableL1Cache: true,
      enableL2Cache: true,
      enableAsyncExec: true,
      enableDtoProjection: true,
      enableCompression: true,
      enableCdnEdge: true,
      enableVirtualization: true,
      queryType: 'products',
      limit: 100
    });

    const baselineTotal = baseline.trace.totalDurationMs;
    const fullyOptimizedTotal = fullyOptimized.trace.totalDurationMs;
    const ogiGainPercent = Math.round(((baselineTotal - fullyOptimizedTotal) / baselineTotal) * 10000) / 100;

    return {
      timestamp: new Date().toISOString(),
      overallGainIndexPercent: ogiGainPercent,
      scenarios: [
        {
          name: '1. Baseline (Unoptimized)',
          layers: baseline.trace.layers,
          totalDurationMs: baselineTotal,
          source: baseline.source,
          analysis: baseline.analysis
        },
        {
          name: '2. Database Tier Optimized',
          layers: dbOnly.trace.layers,
          totalDurationMs: dbOnly.trace.totalDurationMs,
          source: dbOnly.source,
          gainVsBaseline: Math.round(((baselineTotal - dbOnly.trace.totalDurationMs) / baselineTotal) * 100)
        },
        {
          name: '3. Backend + Database Optimized',
          layers: backendAndDb.trace.layers,
          totalDurationMs: backendAndDb.trace.totalDurationMs,
          source: backendAndDb.source,
          gainVsBaseline: Math.round(((baselineTotal - backendAndDb.trace.totalDurationMs) / baselineTotal) * 100)
        },
        {
          name: '4. Fully Integrated Cross-Layer (IMPOF)',
          layers: fullyOptimized.trace.layers,
          totalDurationMs: fullyOptimizedTotal,
          source: fullyOptimized.source,
          gainVsBaseline: ogiGainPercent,
          analysis: fullyOptimized.analysis
        }
      ]
    };
  }
}

module.exports = new ServiceManager();
