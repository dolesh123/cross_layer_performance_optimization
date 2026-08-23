// backend/src/cache/l1Cache.js
// L1 In-Memory LRU Cache (Sub-millisecond local retrieval)

class L1Cache {
  constructor(capacity = 500) {
    this.capacity = capacity;
    this.cache = new Map();
    this.hits = 0;
    this.misses = 0;
  }

  get(key) {
    if (!this.cache.has(key)) {
      this.misses++;
      return null;
    }
    const val = this.cache.get(key);
    // Refresh LRU order
    this.cache.delete(key);
    this.cache.set(key, val);
    this.hits++;
    return val;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      // Evict oldest entry
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  clear() {
    this.cache.clear();
    this.hits = 0;
    this.misses = 0;
  }

  getStats() {
    const total = this.hits + this.misses;
    return {
      name: 'L1 In-Memory Cache (LRU)',
      size: this.cache.size,
      capacity: this.capacity,
      hits: this.hits,
      misses: this.misses,
      hitRatePercent: total > 0 ? Math.round((this.hits / total) * 10000) / 100 : 0
    };
  }
}

module.exports = new L1Cache(500);
