// backend/src/telemetry/tracer.js
// Distributed Tracing Engine (Trace ID & Span Hierarchy)

const crypto = require('crypto');

class DistributedTracer {
  constructor() {
    this.tracesHistory = [];
    this.maxHistory = 100;
  }

  createTrace(clientTraceId = null) {
    const traceId = clientTraceId || `TR-${crypto.randomBytes(6).toString('hex').toUpperCase()}`;
    const spans = [];
    const startTimeNs = process.hrtime.bigint();
    const startIso = new Date().toISOString();

    return {
      traceId,
      startIso,
      startTimeNs,
      spans,

      addSpan(layer, spanName, durationMs, metadata = {}) {
        spans.push({
          spanId: `SP-${crypto.randomBytes(4).toString('hex')}`,
          layer, // 'Frontend' | 'Network' | 'Backend' | 'Database'
          name: spanName,
          durationMs: Math.max(0.01, Math.round(durationMs * 100) / 100),
          timestamp: new Date().toISOString(),
          metadata
        });
      },

      finalize(clientRenderDurationMs = 0, networkRttMs = 0) {
        const endTimeNs = process.hrtime.bigint();
        const serverDurationMs = Number(endTimeNs - startTimeNs) / 1e6;

        // Add client and network spans if reported by telemetry
        if (networkRttMs > 0) {
          spans.unshift({
            spanId: `SP-${crypto.randomBytes(4).toString('hex')}`,
            layer: 'Network',
            name: 'Network Transport & Edge Routing',
            durationMs: Math.round(networkRttMs * 100) / 100,
            metadata: { description: 'Round trip time and packet transport' }
          });
        }

        if (clientRenderDurationMs > 0) {
          spans.push({
            spanId: `SP-${crypto.randomBytes(4).toString('hex')}`,
            layer: 'Frontend',
            name: 'DOM Parsing & Script Execution',
            durationMs: Math.round(clientRenderDurationMs * 100) / 100,
            metadata: { description: 'Client rendering and layout calculation' }
          });
        }

        // Calculate layer sums
        let dbTotalMs = 0;
        let backendTotalMs = 0;
        let networkTotalMs = networkRttMs;
        let frontendTotalMs = clientRenderDurationMs;

        spans.forEach(s => {
          if (s.layer === 'Database') dbTotalMs += s.durationMs;
          else if (s.layer === 'Backend') backendTotalMs += s.durationMs;
        });

        // Backend exclusive time (excluding DB wait)
        const backendExclusiveMs = Math.max(0.1, serverDurationMs - dbTotalMs);
        const totalDurationMs = Math.round((frontendTotalMs + networkTotalMs + serverDurationMs) * 100) / 100;

        const traceRecord = {
          traceId,
          timestamp: startIso,
          totalDurationMs,
          layers: {
            frontendMs: Math.round(frontendTotalMs * 100) / 100,
            networkMs: Math.round(networkTotalMs * 100) / 100,
            backendMs: Math.round(backendExclusiveMs * 100) / 100,
            databaseMs: Math.round(dbTotalMs * 100) / 100
          },
          spans
        };

        return traceRecord;
      }
    };
  }

  recordTrace(traceRecord) {
    this.tracesHistory.unshift(traceRecord);
    if (this.tracesHistory.length > this.maxHistory) {
      this.tracesHistory.pop();
    }
  }

  getRecentTraces(limit = 20) {
    return this.tracesHistory.slice(0, limit);
  }
}

module.exports = new DistributedTracer();
