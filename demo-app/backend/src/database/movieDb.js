// demo-app/backend/src/database/movieDb.js
// Monitored Relational Movie Database with Controllable Query Execution Paths

class MovieDatabase {
  constructor() {
    this.movies = [];
    this.indexByGenre = new Map();
    this.indexById = new Map();
    this.genres = ['Action', 'Sci-Fi', 'Drama', 'Thriller', 'Comedy', 'Horror', 'Adventure', 'Animation'];
    this.directors = ['Christopher Nolan', 'Denis Villeneuve', 'Steven Spielberg', 'Quentin Tarantino', 'Martin Scorsese', 'Greta Gerwig', 'James Cameron', 'Ridley Scott'];
    
    this.seedMovies(50000);
  }

  seedMovies(count = 50000) {
    this.movies = new Array(count);
    this.indexByGenre.clear();
    this.indexById.clear();

    for (let i = 0; i < count; i++) {
      const id = i + 1;
      const genre = this.genres[i % this.genres.length];
      const director = this.directors[i % this.directors.length];
      const releaseYear = 1980 + (i % 46);
      const rating = Math.round((6.0 + (i % 38) * 0.1) * 10) / 10;
      const votes = (i % 25000) + 500;

      const movie = {
        id,
        title: `${genre} Odyssey Episode ${id}`,
        genre,
        director,
        releaseYear,
        rating,
        votes,
        synopsis: `An epic ${genre.toLowerCase()} journey directed by ${director}. Explores complex multidimensional dynamics, existential dilemmas, and visual spectacle. Movie #${id}`,
        runtimeMinutes: 90 + (i % 90),
        boxOfficeMillions: Math.round(((i % 800) + 15) * 10) / 10,
        createdAt: new Date(Date.now() - (i * 1800000)).toISOString()
      };

      this.movies[i] = movie;
      this.indexById.set(id, movie);

      if (!this.indexByGenre.has(genre)) {
        this.indexByGenre.set(genre, []);
      }
      this.indexByGenre.get(genre).push(movie);
    }
  }

  // Fast B-Tree Indexed Search
  findMoviesIndexed({ genre, minRating = 0, limit = 20 }) {
    const t0 = process.hrtime.bigint();
    const pool = genre && this.indexByGenre.has(genre) ? this.indexByGenre.get(genre) : this.movies;
    const results = [];
    let rowsScanned = 0;

    for (let i = 0; i < pool.length; i++) {
      rowsScanned++;
      const m = pool[i];
      if (m.rating < minRating) continue;
      results.push(m);
      if (results.length >= limit) break;
    }

    const t1 = process.hrtime.bigint();
    const durationMs = Number(t1 - t0) / 1e6;

    return {
      results,
      meta: {
        strategy: 'INDEX_SCAN (B-Tree on genre)',
        rowsScanned,
        durationMs: Math.max(0.1, Math.round(durationMs * 100) / 100)
      }
    };
  }

  // Intentionally Slow Full Table Scan across 50,000 records
  findMoviesSlowScan({ genre, minRating = 0, limit = 20 }) {
    const t0 = process.hrtime.bigint();
    const results = [];
    let rowsScanned = 0;

    // Linear full scan with simulated disk I/O / row locks
    for (let i = 0; i < this.movies.length; i++) {
      rowsScanned++;
      const m = this.movies[i];
      if (genre && m.genre !== genre) continue;
      if (m.rating < minRating) continue;

      results.push(m);
      if (results.length >= limit) break;
    }

    // Add deliberate query execution latency representing unindexed heavy disk scan
    const delayMs = 120 + Math.floor(Math.random() * 40);
    const start = Date.now();
    while (Date.now() - start < delayMs) {
      // Busy wait simulation
    }

    const t1 = process.hrtime.bigint();
    const durationMs = Number(t1 - t0) / 1e6;

    return {
      results,
      meta: {
        strategy: 'FULL_TABLE_SCAN (Missing Index on genre, rating)',
        rowsScanned,
        durationMs: Math.round(durationMs * 100) / 100
      }
    };
  }

  getMovieById(id) {
    return this.indexById.get(Number(id)) || null;
  }
}

module.exports = new MovieDatabase();
