// backend/src/database/dbEngine.js
// High-Performance In-Memory Relational Engine with Indexing & Full-Scan Profiling

class DatabaseEngine {
  constructor() {
    this.products = [];
    this.orders = [];
    this.categories = ['Electronics', 'Computing', 'Mobile', 'Audio', 'Gaming', 'Home Appliances', 'Wearables', 'Networking'];
    this.brands = ['AcroTech', 'HyperGear', 'NovaByte', 'Zenith', 'OmniCore', 'PulseAudio', 'Vortex', 'NexusPro'];
    
    // B-Tree / Hash Indexes
    this.productIndexById = new Map();
    this.productIndexByCategory = new Map();
    this.productIndexByComposite = new Map(); // category + inStock
    this.orderIndexByCustomerId = new Map();

    this.isInitialized = false;
    this.totalRecords = 100000;
  }

  seedData(count = 100000) {
    this.totalRecords = count;
    this.products = new Array(count);
    this.productIndexById.clear();
    this.productIndexByCategory.clear();
    this.productIndexByComposite.clear();

    const startTime = Date.now();

    for (let i = 0; i < count; i++) {
      const id = i + 1;
      const category = this.categories[i % this.categories.length];
      const brand = this.brands[i % this.brands.length];
      const price = Math.round((20 + (i % 1500) + Math.random() * 50) * 100) / 100;
      const inStock = (i % 7 !== 0);
      const rating = Math.round((3.0 + (i % 20) * 0.1) * 10) / 10;
      const stockQuantity = (i % 500) + 1;

      const product = {
        id,
        sku: `SKU-${category.substring(0, 3).toUpperCase()}-${id.toString().padStart(6, '0')}`,
        name: `${brand} ${category} Model X-${(i % 999) + 100}`,
        category,
        brand,
        price,
        inStock,
        rating,
        stockQuantity,
        description: `High performance ${brand} ${category} engineered for durability and efficiency. Includes advanced multi-core processing, real-time power modulation, and 2-year enterprise warranty. Item #${id}`,
        specifications: {
          weightGrams: 200 + (i % 1800),
          powerWatts: 15 + (i % 250),
          firmwareVersion: `v${(i % 5) + 1}.${(i % 9)}.${(i % 20)}`,
          dimensions: `${10 + (i % 20)}x${5 + (i % 15)}x${1 + (i % 5)} cm`,
          manufacturingBatch: `BATCH-2026-Q${(i % 4) + 1}`
        },
        reviewsSummary: {
          totalReviews: (i % 450) + 12,
          positiveRatio: Math.round((0.75 + (i % 25) * 0.01) * 100) / 100
        },
        createdAt: new Date(Date.now() - (i * 3600000)).toISOString()
      };

      this.products[i] = product;

      // Build B-Tree / Map Indexes
      this.productIndexById.set(id, product);

      if (!this.productIndexByCategory.has(category)) {
        this.productIndexByCategory.set(category, []);
      }
      this.productIndexByCategory.get(category).push(product);

      const compKey = `${category}_${inStock}`;
      if (!this.productIndexByComposite.has(compKey)) {
        this.productIndexByComposite.set(compKey, []);
      }
      this.productIndexByComposite.get(compKey).push(product);
    }

    // Seed 10,000 synthetic relational Orders
    this.orders = [];
    this.orderIndexByCustomerId.clear();
    for (let o = 1; o <= 10000; o++) {
      const customerId = (o % 1000) + 1;
      const orderItemCount = (o % 4) + 1;
      const productIds = [];
      for (let p = 0; p < orderItemCount; p++) {
        productIds.push(((o * 7 + p * 13) % count) + 1);
      }
      
      const order = {
        orderId: `ORD-${o.toString().padStart(6, '0')}`,
        customerId: `CUST-${customerId.toString().padStart(5, '0')}`,
        productIds,
        totalAmount: (o % 800) + 50,
        status: o % 3 === 0 ? 'DELIVERED' : o % 3 === 1 ? 'SHIPPED' : 'PROCESSING',
        orderDate: new Date(Date.now() - (o * 86400000)).toISOString()
      };
      this.orders.push(order);

      if (!this.orderIndexByCustomerId.has(order.customerId)) {
        this.orderIndexByCustomerId.set(order.customerId, []);
      }
      this.orderIndexByCustomerId.get(order.customerId).push(order);
    }

    this.isInitialized = true;
    const elapsed = Date.now() - startTime;
    return {
      totalProducts: this.products.length,
      totalOrders: this.orders.length,
      seedingTimeMs: elapsed
    };
  }

  // 1. Unindexed Query: Full Table Scan (Simulates O(N) traversal on 100k items)
  queryUnindexed({ category, minPrice = 0, maxPrice = 10000, inStockOnly = false, limit = 50 }) {
    const t0 = process.hrtime.bigint();
    const results = [];
    let rowsScanned = 0;

    for (let i = 0; i < this.products.length; i++) {
      rowsScanned++;
      const p = this.products[i];
      
      // Deliberate realistic linear filter simulation across 100,000 elements
      if (category && p.category !== category) continue;
      if (p.price < minPrice || p.price > maxPrice) continue;
      if (inStockOnly && !p.inStock) continue;

      results.push(p);
      if (results.length >= limit) break;
    }

    const t1 = process.hrtime.bigint();
    const durationMs = Number(t1 - t0) / 1e6;

    return {
      data: results,
      meta: {
        strategy: 'FULL_TABLE_SCAN (Unindexed)',
        indexUsed: null,
        rowsScanned,
        rowsReturned: results.length,
        executionTimeMs: Math.round(durationMs * 100) / 100,
        costScore: rowsScanned * 1.2
      }
    };
  }

  // 2. Indexed Query: B-Tree / Hash Lookup (Simulates O(log N) or O(1) indexed scan)
  queryIndexed({ category, minPrice = 0, maxPrice = 10000, inStockOnly = false, limit = 50 }) {
    const t0 = process.hrtime.bigint();
    let candidatePool = [];
    let indexUsed = 'PRIMARY_INDEX';
    let rowsScanned = 0;

    if (category && inStockOnly && this.productIndexByComposite.has(`${category}_true`)) {
      candidatePool = this.productIndexByComposite.get(`${category}_true`);
      indexUsed = 'IDX_CATEGORY_INSTOCK (Composite B-Tree)';
    } else if (category && this.productIndexByCategory.has(category)) {
      candidatePool = this.productIndexByCategory.get(category);
      indexUsed = 'IDX_CATEGORY (B-Tree Index)';
    } else {
      candidatePool = this.products;
      indexUsed = 'IDX_PRICE_RANGE (Range Scan)';
    }

    const results = [];
    for (let i = 0; i < candidatePool.length; i++) {
      rowsScanned++;
      const p = candidatePool[i];
      if (p.price < minPrice || p.price > maxPrice) continue;
      if (inStockOnly && !p.inStock) continue;

      results.push(p);
      if (results.length >= limit) break;
    }

    const t1 = process.hrtime.bigint();
    const durationMs = Number(t1 - t0) / 1e6;

    return {
      data: results,
      meta: {
        strategy: 'INDEX_RANGE_SCAN (Optimized)',
        indexUsed,
        rowsScanned,
        rowsReturned: results.length,
        executionTimeMs: Math.max(0.05, Math.round(durationMs * 100) / 100),
        costScore: rowsScanned * 0.05
      }
    };
  }

  // 3. Relational Query: N+1 Unoptimized vs. Batched JOIN Optimized
  queryOrdersWithProducts(customerId = 'CUST-00042', useJoin = false) {
    const t0 = process.hrtime.bigint();
    let queryCount = 0;
    let enrichedOrders = [];

    if (!useJoin) {
      // N+1 Problem Simulation: 1 query for orders + N queries for each product lookup
      const orders = this.orders.filter(o => o.customerId === customerId).slice(0, 10);
      queryCount = 1;

      enrichedOrders = orders.map(order => {
        const fullProducts = order.productIds.map(pid => {
          queryCount++;
          // Unindexed lookups
          return this.products.find(p => p.id === pid) || null;
        });
        return { ...order, items: fullProducts };
      });
    } else {
      // Optimized Batched JOIN: 1 indexed query for orders + 1 batched IN() query
      const orders = (this.orderIndexByCustomerId.get(customerId) || []).slice(0, 10);
      const allProductIds = new Set();
      orders.forEach(o => o.productIds.forEach(id => allProductIds.add(id)));

      // Single batched indexed fetch
      const productMap = new Map();
      allProductIds.forEach(id => {
        const prod = this.productIndexById.get(id);
        if (prod) productMap.set(id, prod);
      });

      enrichedOrders = orders.map(order => ({
        ...order,
        items: order.productIds.map(id => productMap.get(id) || null)
      }));
      queryCount = 2;
    }

    const t1 = process.hrtime.bigint();
    const durationMs = Number(t1 - t0) / 1e6;

    return {
      data: enrichedOrders,
      meta: {
        strategy: useJoin ? 'BATCHED_INDEX_JOIN (Optimized)' : 'N_PLUS_ONE_SEQUENTIAL (Unoptimized)',
        queriesExecuted: queryCount,
        executionTimeMs: Math.round(durationMs * 100) / 100,
        ordersCount: enrichedOrders.length
      }
    };
  }

  getStats() {
    return {
      totalProducts: this.products.length,
      totalOrders: this.orders.length,
      indexedCategories: Array.from(this.productIndexByCategory.keys()),
      isReady: this.isInitialized
    };
  }
}

const dbInstance = new DatabaseEngine();
dbInstance.seedData(100000);

module.exports = dbInstance;
