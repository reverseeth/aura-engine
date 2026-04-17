-- Creative DNA Registry — schema SQLite
-- Criar com: sqlite3 registry.db < schema.sql

CREATE TABLE IF NOT EXISTS creatives (
  id              TEXT PRIMARY KEY,
  product_slug    TEXT NOT NULL,
  concept_id      TEXT,
  source_file     TEXT,
  features_json   TEXT NOT NULL,
  produced_at     TEXT NOT NULL,
  created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance (
  creative_id     TEXT PRIMARY KEY,
  cpa             REAL,
  ctr             REAL,
  thumbstop_3s    REAL,
  hold_15s        REAL,
  roas            REAL,
  spend           REAL,
  impressions     INTEGER,
  clicks          INTEGER,
  purchases       INTEGER,
  days_active     INTEGER,
  decile_rank     INTEGER,
  outcome         TEXT CHECK(outcome IN ('winner', 'loser', 'neutral', 'pending')),
  measured_at     TEXT NOT NULL,
  FOREIGN KEY (creative_id) REFERENCES creatives(id)
);

CREATE TABLE IF NOT EXISTS dna_snapshots (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  product_slug    TEXT NOT NULL,
  creative_count  INTEGER NOT NULL,
  winner_count    INTEGER NOT NULL,
  dna_json        TEXT NOT NULL,
  generated_at    TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_creatives_product ON creatives(product_slug);
CREATE INDEX IF NOT EXISTS idx_performance_outcome ON performance(outcome);
CREATE INDEX IF NOT EXISTS idx_snapshots_product ON dna_snapshots(product_slug, generated_at DESC);
