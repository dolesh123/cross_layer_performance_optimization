// backend/src/cache/l2Cache.js
// L2 Distributed Key-Value Store (Redis-Style with TTL and serialization)

class L2Cache {
  constructor() {
    this.store = new Map();
    this.hits = 0;
    this.misses = 0;
  }

  async get(key) {
    // Simulate brief Redis network/serialization hop (~0.5ms)
    await new Promise(r => setTimeout(r, 1));

    if (!this.store.has(key)) {
      this.misses++;
      return null;
    }

    const item = this.store.get(key);
    if (Date.now() > item.expiresAt) {
      this.store.delete(key);
      this.misses++;
      return null;
    }

    this.hits++;
    return JSON.parse(item.serializedValue);
  }

  async set(key, value, ttlSeconds = 60) {
    await new Promise(r => setTimeout(r, 1));
    const item = {
      serializedValue: JSON.stringify(value),
      expiresAt: Date.now() + (ttlSeconds * 1000)
    };
    this.store.set(key, item);
  }

  clear() {
    this.store.clear();
    this.hits = 0;
    this.misses = 0;
  }

  getStats() {
    const total = this.hits + this.misses;
    return {
      name: 'L2 Distributed Cache (Redis-Style)',
      size: this.store.size,
      hits: this.hits,
      misses: this.misses,
      hitRatePercent: total > 0 ? Math.round((this.hits / total) * 10000) / 100 : 0
    };
  }
}

module.exports = new L2Cache();
