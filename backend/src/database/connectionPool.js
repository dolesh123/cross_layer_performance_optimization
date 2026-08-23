// backend/src/database/connectionPool.js
// HikariCP-Style Connection Pool Simulator with Real Latency Profiling

class ConnectionPool {
  constructor(maxSize = 10) {
    this.maxSize = maxSize;
    this.activeConnections = 0;
    this.idleConnections = maxSize;
    this.queueWaiters = [];
    this.totalAcquisitions = 0;
    this.totalWaitTimeMs = 0;
  }

  // Optimized: Lease from warm connection pool
  async acquirePooledConnection() {
    const t0 = process.hrtime.bigint();
    this.totalAcquisitions++;

    if (this.idleConnections > 0) {
      this.idleConnections--;
      this.activeConnections++;
      const t1 = process.hrtime.bigint();
      const waitMs = Number(t1 - t0) / 1e6;
      return {
        connectionId: `CONN-POOL-${this.activeConnections}`,
        acquiredInMs: Math.round(waitMs * 100) / 100,
        poolStatus: {
          active: this.activeConnections,
          idle: this.idleConnections,
          max: this.maxSize
        },
        release: () => {
          this.activeConnections = Math.max(0, this.activeConnections - 1);
          this.idleConnections = Math.min(this.maxSize, this.idleConnections + 1);
        }
      };
    }

    // Pool saturated - wait in queue (max 50ms)
    await new Promise(resolve => setTimeout(resolve, 5));
    this.activeConnections++;
    const t1 = process.hrtime.bigint();
    const waitMs = Number(t1 - t0) / 1e6;
    return {
      connectionId: `CONN-POOL-QUEUED`,
      acquiredInMs: Math.round(waitMs * 100) / 100,
      poolStatus: {
        active: this.activeConnections,
        idle: 0,
        max: this.maxSize
      },
      release: () => {
        this.activeConnections = Math.max(0, this.activeConnections - 1);
        this.idleConnections = Math.min(this.maxSize, this.idleConnections + 1);
      }
    };
  }

  // Unoptimized: Fresh connection overhead (simulates TCP Handshake + TLS + Auth = 15-30ms)
  async acquireUnpooledConnection() {
    const t0 = process.hrtime.bigint();
    const handshakeDelay = 15 + Math.floor(Math.random() * 15);
    await new Promise(resolve => setTimeout(resolve, handshakeDelay));
    
    const t1 = process.hrtime.bigint();
    const waitMs = Number(t1 - t0) / 1e6;

    return {
      connectionId: `CONN-RAW-${Math.floor(Math.random() * 99999)}`,
      acquiredInMs: Math.round(waitMs * 100) / 100,
      poolStatus: {
        strategy: 'UNPOOLED_RAW_HANDSHAKE',
        overhead: '15-30ms per request (TCP/TLS/Auth)'
      },
      release: () => {
        // Destroy connection immediately
      }
    };
  }

  getPoolStats() {
    return {
      maxSize: this.maxSize,
      activeConnections: this.activeConnections,
      idleConnections: this.idleConnections,
      totalAcquisitions: this.totalAcquisitions
    };
  }
}

module.exports = new ConnectionPool(20);
